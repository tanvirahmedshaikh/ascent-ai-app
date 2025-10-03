# 🚀 Ascent AI

### Intelligent Branding for Your Career Ascent

Ascent AI is a sophisticated, SaaS-style Streamlit application that acts as your personal AI co-pilot for career branding. It turns your professional experience and career aspirations into content that gets noticed, helping you share posts in your authentic voice, join the right discussions, and grow your influence as a thought leader on platforms like LinkedIn.

Upload your resume and writing samples so Ascent AI can learn your style. It doesn’t just write posts; it writes in your voice.

---
## ✨ Core Features

* **Flexible Workflows:** Choose between two powerful modes from the sidebar:
    * **Strategic Branding:** A guided, multi-step process that builds a detailed, multi-week content strategy from your professional background and goals.
    * **Quick Ideas:** A quick-start option to instantly generate single post ideas or a 3-part series on a specific topic without a full strategy.

* **Human-in-the-Loop (HITL) Feedback:** An interactive system allows you to critique and refine AI-generated strategies and post drafts until they're perfect.

* **Authentic Voice Generation:** Upload writing samples so the AI can learn and replicate your unique tone and style, ensuring content truly reflects you.

* **Multi-Agent AI Crew:** Powered by CrewAI, the app uses a team of specialized AI agents for a robust workflow:
    * **Professional Resume Summarizer (Groq):** Concisely summarizes your professional background and career goals.
    * **Personal Branding Strategist (Gemini):** Creates a tailored, multi-week content strategy.
    * **Content Ideation Agent (Groq):** Brainstorms creative and engaging post ideas at high speed.
    * **LinkedIn Ghostwriter (Gemini):** Drafts polished, full-length posts in your authentic voice.
    * **Quality Assurance Agent (Gemini):** Reviews drafted posts for clarity, tone, and strategic impact.
    * **Title Generator (Groq):** Automatically creates concise titles for your sessions.

* **Heterogeneous LLMs:** Strategically uses different Large Language Models for different tasks—**Google's Gemini** for deep strategic analysis and polished writing, and **Groq's Llama** for high-speed creative generation and concise tasks.

* **Polished SaaS UI:** A clean, four-tab interface separates your workspace (`Brand Strategy`, `Post Ideas`, `Quick Ideas`, and `Final Post`) for a focused workflow.

* **Comprehensive Session Management:** A professional sidebar allows you to create, load, rename, and delete past sessions, providing a history of your branding efforts.

* **Export Functionality:** Easily download your generated strategies and finalized posts as clean text files.

---
## 💻 Built With

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Framework:** [CrewAI](https://www.crewai.com/)
* **LLMs:** [Google Gemini](https://ai.google.dev/) & [Groq Llama](https://groq.com/)
* **Core Libraries:** `streamlit`, `crewai`, `langchain-groq`, `langchain-google-genai`, `pypdf`, `streamlit-local-storage`

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
```

---
### Navigating the App

The application is structured into four main tabs, each designed for a specific part of the content creation workflow:

* **📝 Brand Strategy:**  
  A step-by-step process to define your professional brand.  
  You’ll answer questions about your background, career goals, and desired positioning.  
  The AI then generates a detailed, multi-week content strategy tailored to your needs — the starting point for building a long-term plan.

* **💡 Post Ideas:**  
  Your primary content creation hub. Once a strategy is approved, it populates with post ideas organized by theme.  
  You can refine existing ideas, generate more ideas for specific themes, or use the **Refine Selected Ideas** buttons to apply feedback across multiple themes.

* **✨ Quick Ideas:**  
  An on-demand, no-strategy-required workflow. You can generate single-post ideas or a 3-part series on any topic you choose.  
  This tab also allows you to save your favorite ideas to a history for later use.

* **✍️ Final Post:**  
  Your final workspace. Select any idea from the other tabs to have the AI write a full, polished draft. Here, you can:
  - Review a **Post Preview** styled like a real social media post.  
  - Get automated feedback from the **Quality Assurance Agent**.  
  - Provide your own feedback and refine the draft using the **Refine Draft** button.  
  - Save or download your final version.  

