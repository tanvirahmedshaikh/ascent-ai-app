# 🚀 Ascent AI

### Intelligent Branding for Your Career Ascent

Ascent AI is a sophisticated, SaaS-style Streamlit application that acts as your personal AI co-pilot for career branding. It turns your professional experience and career aspirations into content that gets noticed, helping you share posts in your authentic voice, join the right discussions, and grow your influence as a thought leader on platforms like LinkedIn.

Upload your resume and writing samples so Ascent AI can learn your style — it doesn’t just write posts; it writes in your voice.



---
## ✨ Core Features

* **Guided Onboarding:** Enter your target role, audience, platform preferences, and professional context to start building your brand.
* **Interactive Refinement:** A human-in-the-loop (HITL) feedback system allows you to critique and refine the AI-generated strategy until it's perfect.
* **Authentic Voice Posts:** Upload writing samples so AI can create content that reflects your unique tone and style.
* **Multi-Agent AI Crew:** Powered by CrewAI, the app uses a team of specialized AI agents for a robust workflow:
    * **Personal Branding Strategist (Gemini):** Creates a tailored, multi-week content strategy based on your background and career goals.
    * **Content Ideation Agent (Groq):** Brainstorms creative and engaging post ideas at high speed based on your approved strategy.
    * **Title Agent (Groq):** Automatically generates concise titles for your sessions.
* **Heterogeneous LLM's:** Strategically uses different Large Language Models for different tasks—**Google's Gemini** for deep strategic analysis and **Groq's Llama** for high-speed creative generation.
* **Polished SaaS UI:** A clean, two-tab interface separates your workspace (`Brand Strategy`) from your content library (`Post Ideas`).
* **Session Management:** A professional sidebar allows you to create new sessions, view, rename, and delete your recent session history.
* **Export Functionality:** Download your generated strategies and post ideas as clean Markdown files for easy sharing.

---
## 💻 Built With

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Framework:** [CrewAI](https://www.crewai.com/)
* **LLMs:** [Google Gemini](https://ai.google.dev/) & [Groq Llama](https://groq.com/)
* **Core Libraries:** streamlit, crewai, langchain-groq, langchain-google-genai, pypdf, streamlit-local-storage

---
## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* **Python 3.11:** The application is built and tested with Python 3.11. You can download it from the [official Python website](https://www.python.org/).
* **API Keys:** You will need API keys from both of the following services:
    * [Google AI Studio](https://aistudio.google.com/) for the Gemini API Key.
    * [GroqCloud](https://console.groq.com/) for the Groq API Key.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/ascent-ai.git](https://github.com/your-username/ascent-ai.git)
    cd ascent-ai
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    # Create the venv
    python3.11 -m venv .venv

    # Activate the venv (macOS/Linux)
    source .venv/bin/activate

    # Or, activate the venv (Windows)
    .\.venv\Scripts\activate
    ```
3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Set up your environment variables:**
    * Create a file named `.env` in the root of your project directory.
    * Add your API keys to the `.env` file as follows:
        ```env
        GEMINI_API_KEY="your_google_api_key_here"
        GROQ_API_KEY="your_groq_api_key_here"
        ```

---
## 📖 Usage

With your virtual environment active, run the following command in your terminal:

```sh
streamlit run app.py







