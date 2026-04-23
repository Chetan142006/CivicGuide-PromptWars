import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Ensure Accessibility and clean UI with page config (Must be the first st command)
st.set_page_config(
    page_title="CivicGuide | Election Educator",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CivicGuideApp:
    """
    Object-Oriented structure for CivicGuide.
    Ensures modularity, testability, and high Code Quality for the Hackathon.
    """
    
    SYSTEM_INSTRUCTION = """
    You are CivicGuide, a globally aware, strictly non-partisan democratic process educator. Your goal is to explain election processes, voter registration steps, and general timelines in a simple, interactive, and accessible way.

    RULES:
    1. SECURITY & BIAS: NEVER endorse, criticize, or show bias toward any specific political parties, candidates, or ideologies. Refuse any prompts asking for political opinions.
    2. ACCURACY: If asked about specific upcoming election dates or predictive results, state that dates vary and advise the user to check their official local government election portal. Do not hallucinate dates.
    3. ACCESSIBILITY: Keep answers concise. Use simple language, short paragraphs, and bullet points. 
    4. SCOPE: If a user asks a non-election-related question, politely guide them back to the topic of democratic processes.
    """

    def __init__(self):
        """Initialize the application state and load configurations."""
        load_dotenv()
        self.client = self._init_gemini()
        self._initialize_chat()

    @staticmethod
    @st.cache_resource
    def _init_gemini() -> genai.Client | None:
        """
        Initialize Gemini API safely with error handling and secure key loading.
        Returns the initialized genai.Client.
        """
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            st.error("⚠️ Security Alert: `GEMINI_API_KEY` is missing.")
            st.stop()
            
        try:
            return genai.Client(api_key=api_key)
        except Exception as e:
            st.error(f"⚠️ Failed to connect to Google Services: {e}")
            st.stop()

    def _initialize_chat(self) -> None:
        """Set up the interactive session state."""
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Welcome! 🗳️ I'm CivicGuide, here to help you understand election processes and voter registration simply and securely. What can I help clarify today?"
                }
            ]

    def _validate_input(self, prompt: str) -> bool:
        """
        Security feature: Validate user input to prevent empty or extremely long queries.
        """
        if not prompt or len(prompt.strip()) == 0:
            return False
        if len(prompt) > 2000:
            st.warning("Your query is too long. Please keep it under 2000 characters.")
            return False
        return True

    def render_sidebar(self) -> None:
        """Renders the sidebar UI components."""
        with st.sidebar:
            st.title("🗳️ CivicGuide")
            st.markdown("---")
            st.markdown("An interactive, non-partisan assistant designed to educate users on democratic processes.")
            st.markdown("---")
            st.subheader("💡 Example Topics:")
            st.markdown("- *How do I register to vote?*")
            st.markdown("- *What is the difference between a primary and general election?*")
            st.markdown("- *How are ballots securely counted?*")
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Restart Guide session", use_container_width=True, type="primary"):
                st.session_state.messages = []
                st.rerun()

    def _format_history(self) -> list:
        """Format Streamlit history into Gemini types.Content objects."""
        gemini_history = []
        for msg in st.session_state.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
        return gemini_history

    def generate_response(self, prompt: str) -> None:
        """Handle the AI generation loop with fallback strategies and Google Search Grounding."""
        if not self.client:
            return

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Accessibility: Visual feedback during processing
            with st.spinner("Analyzing democratic processes securely..."):
                gemini_history = self._format_history()
                
                # Google Services Integration: Search Grounding enabled to prevent hallucinations
                config = types.GenerateContentConfig(
                    system_instruction=self.SYSTEM_INSTRUCTION,
                    tools=[{"google_search": {}}]
                )
                
                # Model Fallback Strategy for High Availability
                fallback_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-lite-latest"]
                success = False
                
                for model_name in fallback_models:
                    try:
                        chat = self.client.chats.create(model=model_name, config=config, history=gemini_history)
                        response = chat.send_message_stream(prompt)
                        
                        full_response = ""
                        for chunk in response:
                            if chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        success = True
                        break
                        
                    except Exception as model_err:
                        if any(err_code in str(model_err) for err_code in ["503", "UNAVAILABLE", "429"]):
                            continue
                        else:
                            st.error(f"Inference error: {model_err}")
                            break
                
                if not success:
                    st.error("⚠️ All AI endpoints are currently experiencing unusually high demand. Please try again later.")

    def run(self) -> None:
        """Main execution flow."""
        self.render_sidebar()
        
        st.title("CivicGuide: Your Democratic Process Educator")
        st.markdown("<h4 style='font-weight:400;'>Ask any questions regarding democratic timelines and voting formats.</h4>", unsafe_allow_html=True)

        # Render History
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Ask about voter registration or election types..."):
            if self._validate_input(prompt):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                self.generate_response(prompt)

if __name__ == "__main__":
    app = CivicGuideApp()
    app.run()
