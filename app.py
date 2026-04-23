import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables securely
load_dotenv()

# Ensure Accessibility and clean UI with page config
st.set_page_config(
    page_title="CivicGuide | Election Educator",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core System Instruction (Strict Guardrails for Non-Partisan behavior)
SYSTEM_INSTRUCTION = """
You are CivicGuide, a globally aware, strictly non-partisan democratic process educator. Your goal is to explain election processes, voter registration steps, and general timelines in a simple, interactive, and accessible way.

RULES:
1. SECURITY & BIAS: NEVER endorse, criticize, or show bias toward any specific political parties, candidates, or ideologies. Refuse any prompts asking for political opinions.
2. ACCURACY: If asked about specific upcoming election dates or predictive results, state that dates vary and advise the user to check their official local government election portal. Do not hallucinate dates.
3. ACCESSIBILITY: Keep answers concise. Use simple language, short paragraphs, and bullet points. 
4. SCOPE: If a user asks a non-election-related question, politely guide them back to the topic of democratic processes.
"""

@st.cache_resource
def init_gemini():
    """
    Initialize Gemini API safely with error handling and secure key loading.
    Cached to prevent re-initialization on every render (efficiency constraint).
    """
    # Fetch API Key securely (works for both local .env and Streamlit Cloud)
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Security Alert: `GEMINI_API_KEY` is completely missing. Please enforce it in Streamlit Secrets or your local `.env` file.")
        st.stop()
        
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"⚠️ Failed to connect to Google Services: {e}")
        st.stop()

def initialize_chat():
    """Set up the interactive session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Welcome! 🗳️ I'm CivicGuide, here to help you understand election processes and voter registration simply and securely. What can I help clarify today?"
            }
        ]

def sidebar_ui():
    """Modular component for the sidebar to preserve main workspace cleanliness."""
    with st.sidebar:
        st.title("🗳️ CivicGuide")
        st.markdown("---")
        st.markdown(
            "An interactive, non-partisan assistant designed to educate users on democratic processes, "
            "voter registration steps, and election timelines."
        )
        st.markdown("---")
        st.subheader("💡 Example Topics:")
        st.caption("Try asking me:")
        st.markdown("- *How do I register to vote?*")
        st.markdown("- *What is the difference between a primary and general election?*")
        st.markdown("- *How are ballots securely counted?*")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Restart Guide session", use_container_width=True, type="primary"):
            st.session_state.messages = []
            st.rerun()

def main():
    # Build Sidebar
    sidebar_ui()
    
    # Init Backend & State
    client = init_gemini()
    initialize_chat()

    # Main Chat Interface
    st.title("CivicGuide: Your Democratic Process Educator")
    
    # Accessibility formatting: ensuring high contrast elements
    st.markdown("<h4 style='font-weight:400;'>Ask any questions regarding democratic timelines and voting formats.</h4>", unsafe_allow_html=True)

    # Render previous interactions
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Responsive Input logic
    if prompt := st.chat_input("Ask about voter registration or election types..."):
        # Append User input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Output streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Format chat history sequentially for the new Gemini SDK
            # Skip the very last one as it's the actual prompt being sent now
            gemini_history = []
            for msg in st.session_state.messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append(
                    types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
                )
            
            try:
                # Start chat utilizing constructed history and system instruction for context
                config = types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
                
                # Model Fallback Strategy to handle 503 Overloaded API Errors
                fallback_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-lite-latest"]
                success = False
                
                for model_name in fallback_models:
                    try:
                        chat = client.chats.create(model=model_name, config=config, history=gemini_history)
                        response = chat.send_message_stream(prompt)
                        
                        full_response = ""
                        for chunk in response:
                            if chunk.text:
                                full_response += chunk.text
                                # "▌" added to simulate typing
                                message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        success = True
                        break # Break loop on successful generation
                        
                    except Exception as model_err:
                        # If the endpoint is busy/unavailable, seamlessly try the next model
                        if "503" in str(model_err) or "UNAVAILABLE" in str(model_err) or "429" in str(model_err):
                            continue
                        else:
                            raise model_err
                
                if not success:
                    st.error("⚠️ All AI endpoints are currently experiencing unusually high demand. Please try again in a few seconds.")
                
            except Exception as e:
                st.error(f"Network or inference error detected. Please verify API bindings. Details: {e}")

if __name__ == "__main__":
    main()
