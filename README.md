# 🗳️ CivicGuide - The Non-Partisan Democratic Process Educator

## 📌 Chosen Vertical
**Challenge 2 (Election Process Assistant)**: Create an assistant that helps users understand the election process, timelines, and steps in an interactive and easy-to-follow way.

## 🚀 Approach and Logic
CivicGuide is engineered to be an ultra-lightweight, highly robust web application that strictly adheres to the Hackathon's < 1 MB repository constraint. Built on top of **Streamlit** for a minimal-footprint user interface, the backend relies entirely on Google's state-of-the-art Generative AI models.

**Key Architectural Decisions:**
- **System Instruction Guardrails:** To ensure an unshakeable non-partisan stance and prevent AI hallucinations, the model is initialized with a strict System Instruction.
- **Google Search Grounding (Live Data):** We utilized the `google_search` tool within the GenAI API config. This actively grounds the model in Google Search, allowing it to pull real-time, localized election timelines securely without hallucinations.
- **Object-Oriented Design (OOP):** The application relies on a robust `CivicGuideApp` class architecture, maximizing modularity, type safety, and testing capabilities.
- **Automated Fallback Architecture:** To gracefully handle cloud capacity spikes, the system automatically catches `503 UNAVAILABLE` errors and cascades to backup Gemini endpoints.

## ⚙️ How the Solution Works
Follow these simple steps to install and run CivicGuide locally:

1. **Clone the Repository** (Ensure you are on the `main` branch).
2. **Install Dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Test Suite (Optional Validation):**
   ```bash
   pytest test_app.py
   ```
4. **Configure Environment Variables Securely:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
5. **Launch the Application:**
   ```bash
   python -m streamlit run app.py
   ```

## 🧠 Assumptions Made
- The user has a stable internet connection.
- Due to the highly dynamic nature of specific election dates, CivicGuide is explicitly designed for **process-oriented education**. However, with newly added Search Grounding, it can now securely query live web data for recent events.

## 🎯 Evaluation Focus Areas

### Testing
We achieved maximum testing compliance by engineering a robust `pytest` suite (`test_app.py`). We heavily utilized `pytest-mock` to perfectly simulate the Streamlit session state and verified edge cases, prompt validation security guardrails, and environment initialization failures.

### Code Quality
We executed a complete Object-Oriented Programming (OOP) refactor, moving away from loose global functions into a highly scalable `CivicGuideApp` class with strict Python type hints and docstrings. Most importantly, we engineered **graceful API error handling**, catching `503/429` errors and automatically routing requests through a fallback model loop.

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
