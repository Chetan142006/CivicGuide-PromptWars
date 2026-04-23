# 🗳️ CivicGuide - The Non-Partisan Democratic Process Educator

## 📌 Chosen Vertical
**Challenge 2 (Election Process Assistant)**: Create an assistant that helps users understand the election process, timelines, and steps in an interactive and easy-to-follow way.

## 🚀 Approach and Logic
CivicGuide is engineered to be an ultra-lightweight, highly robust web application that strictly adheres to the Hackathon's < 1 MB repository constraint. Built on top of **Streamlit** for a minimal-footprint user interface, the backend relies entirely on Google's state-of-the-art Generative AI models.

**Key Architectural Decisions:**
- **System Instruction Guardrails:** To ensure an unshakeable non-partisan stance and prevent AI hallucinations, the model is initialized with a strict System Instruction. It explicitly refuses political opinions, avoids predicting specific upcoming election dates, and maintains concise, accessible language.
- **Future-Proof Google Services:** We completely migrated to the newly released `google.genai` SDK to ensure long-term stability and modern schema typing.
- **Automated Fallback Architecture:** To ensure high availability and gracefully handle cloud capacity spikes, the system automatically catches `503 UNAVAILABLE` errors. It immediately cascades to backup Gemini endpoints (e.g., from `gemini-2.5-flash` down to `gemini-flash-lite-latest`) without breaking the user experience.

## ⚙️ How the Solution Works
Follow these simple steps to install and run CivicGuide locally:

1. **Clone the Repository** (Ensure you are on the `main` branch).
2. **Install Dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables Securely:**
   Create a `.env` file in the root directory and add your Google Gemini API key. This guarantees keys are never pushed to the public repo:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
4. **Launch the Application:**
   Run the Streamlit app using the following command:
   ```bash
   python -m streamlit run app.py
   ```

## 🧠 Assumptions Made
- The user has a stable internet connection to interface with Google's API services.
- Due to the highly dynamic and hyper-local nature of specific election dates, it is assumed that users will use CivicGuide for **process-oriented education**. The assistant is explicitly instructed to always direct users to official local government portals for exact election scheduling to avoid hallucinations.

## 🎯 Evaluation Focus Areas

### Code Quality
We adopted a clean, modular, single-file architecture (`app.py`). UI components are separated into distinct functions (e.g., `sidebar_ui()`). Most importantly, we engineered **graceful API error handling**, catching `503/429` errors and automatically routing requests through a fallback model loop so the application remains robust under heavy Hackathon evaluation load.

### Security
We maintain high security on two critical fronts: 
1. **Application Security:** The codebase never exposes API keys. It safely fetches them using `os.environ` via `python-dotenv` locally or through Streamlit Secrets in cloud production.
2. **Responsible AI Security:** The model operates under an unbreakable System Instruction wrapper that guarantees strictly non-partisan, unbiased responses and refuses to answer irrelevant prompts.

### Efficiency
The entire codebase and repository footprint is only a few kilobytes, easily mastering the strict < 1 MB constraint. For inference, we default to the `gemini-2.5-flash` model, providing the absolute best balance of blindingly fast reasoning and low latency necessary for a fluid chat experience.

### Accessibility
CivicGuide is designed for maximum inclusivity. The UI is clean, minimalistic, and relies on high-contrast Markdown formatting. The AI itself is explicitly instructed to communicate in simple language, short paragraphs, and bullet points to remain highly accessible to users of all civic literacy levels.

### Google Services
The application represents a deep, meaningful integration of Google's latest `google.genai` SDK ecosystem. We leverage Gemini's structured chat sessions, complex history arrays (`types.Content`), and real-time generation streaming to power the core educational capabilities of the assistant.
