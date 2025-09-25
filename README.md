
🚀 Ascent AI
Intelligent Branding for Your Career Ascent
Ascent AI is a sophisticated, SaaS-style Streamlit application that acts as your personal AI co-pilot for career branding. It turns your professional experience and career aspirations into content that gets noticed, helping you share posts in your authentic voice, join the right discussions, and grow your influence as a thought leader on platforms like LinkedIn.

Upload your resume and writing samples so Ascent AI can learn your style — it doesn’t just write posts; it writes in your voice.

✨ Core Features
Guided Onboarding: Enter your target role, audience, platform preferences, and professional context to start building your brand.

Interactive Refinement: A human-in-the-loop (HITL) feedback system allows you to critique and refine the AI-generated strategy until it's perfect.

Authentic Voice Posts: Upload writing samples so AI can create content that reflects your unique tone and style.

Multi-Agent AI Crew: Powered by CrewAI, the app uses a team of specialized AI agents for a robust workflow:

Personal Branding Strategist (Gemini): Creates a tailored, multi-week content strategy based on your background and career goals.

Content Ideation Agent (Groq): Brainstorms creative and engaging post ideas at high speed based on your approved strategy.

Title Agent (Groq): Automatically generates concise titles for your sessions.

Heterogeneous LLM's: Strategically uses different Large Language Models for different tasks—Google's Gemini for deep strategic analysis and Groq's Llama for high-speed creative generation.

Polished SaaS UI: A clean, two-tab interface separates your workspace (Brand Strategy) from your content library (Post Ideas).

Session Management: A professional sidebar allows you to create new sessions, view, rename, and delete your recent session history.

Export Functionality: Download your generated strategies and post ideas as clean Markdown files for easy sharing.

💻 Built With
Frontend: Streamlit

AI Framework: CrewAI

LLMs: Google Gemini & Groq Llama

Core Libraries: streamlit, crewai, langchain-groq, langchain-google-genai, pypdf, streamlit-local-storage

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Python 3.11: The application is built and tested with Python 3.11. You can download it from the official Python website.

API Keys: You will need API keys from both of the following services:

Google AI Studio for the Gemini API Key.

GroqCloud for the Groq API Key.

Installation
Clone the repository:

Bash

git clone [https://github.com/your-username/ascent-ai.git](https://github.com/your-username/ascent-ai.git)
cd ascent-ai
Create and activate a virtual environment:

Bash

# Create the venv
python3.11 -m venv .venv

# Activate the venv (macOS/Linux)
source .venv/bin/activate

# Or, activate the venv (Windows)
.\.venv\Scripts\activate
Install the required packages:

Bash

pip install -r requirements.txt
Set up your environment variables:

Create a file named .env in the root of your project directory.

Add your API keys to the .env file as follows:

Code snippet

GEMINI_API_KEY="your_google_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
📖 Usage
With your virtual environment active, run the following command in your terminal:

Bash

streamlit run app.py
Post Ideas Tab Logic and UI
Your Content Ideas
These ideas are based on your personal branding strategy. Use the options below to refine and select your favorites.

1. Future of PM in the Age of Generative AI

[ ] "As Generative AI reshapes our world, how will PMs adapt to leverage its power for transformative innovation?"
[➕3 More like this] [✍️ Write]

[ ] "Imagine PMs as AI strategists - what would be the most critical skillsets for success?"
[➕3 More like this] [✍️ Write]

[ ] "Will AI-generated insights revolutionize product decision-making - share your thoughts!"
[➕3 More like this] [✍️ Write]

Refine Ideas for This Theme



[Text input area: Provide feedback to refine existing ideas or generate new ones for the selected topics. Feedback will modify the current ideas; generating new ideas will replace all unselected ones with a fresh batch.]
[Refine Selected Topics] [🔄 Generate New Ideas for This Theme]

2. Quantifying Innovation's Impact at Genentech

[ ] "From zero to hero: how a simple data product transformed productivity at Genentech."
[➕3 More like this] [✍️ Write]

[ ] "26 FTEs freed to focus on strategy - what innovative solutions have you unlocked?"
[➕3 More like this] [✍️ Write]

[ ] "Unlocking the numbers: how data-driven innovation improved process efficiency."
[➕3 More like this] [✍️ Write]

Refine Ideas for This Theme



[Text input area: Provide feedback to refine existing ideas or generate new ones for the selected topics. Feedback will modify the current ideas; generating new ideas will replace all unselected ones with a fresh batch.]
[Refine Selected Topics] [🔄 Generate New Ideas for This Theme]

Overall Strategy Refinement
Actions that apply across all themes.



[Text input area: Provide feedback to refine selected topics or generate new ones for the unselected topics. Feedback will modify the selected ideas; generating new ideas will replace all unselected ones with a fresh batch.]
[Refine All Ideas with Feedback] [🔄 Generate New Ideas for All Unselected Topics]
