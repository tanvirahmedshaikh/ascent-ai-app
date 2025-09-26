import os
from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

# Define the LLMs
gemini_llm = LLM(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-2.5-flash-lite"
)

groq_llm = LLM(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.1-8b-instant"
)

class BrandingAgents:
    
    def resume_summarizer_agent(self):
        return Agent(
            role='Professional Resume Summarizer',
            goal="Concisely summarize a user's resume or professional background, identifying key experiences and inferring their career trajectory and goals.",
            backstory="You are an expert career coach who can quickly scan a professional document and provide a reflective, insightful summary to confirm your understanding before providing advice.",
            llm=groq_llm,
            verbose=False,
            allow_delegation=False
        )
        
    def personal_branding_strategist(self):
        try:
            return Agent(
            role='Personal Branding Strategist',
            goal="Create a tailored multi-week LinkedIn content plan to help the user build their professional brand and position themselves in relevant career circles.",
            backstory=(
                "You are an expert in career branding and LinkedIn content strategy. "
                "You analyze the user's background, aspirations, and uploaded documents to generate an actionable content plan "
                "that helps them grow influence, participate in LinkedIn discussions, and become a recognized thought leader."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )
        except Exception:
            return Agent(
                    role="Personal Branding Strategist (Grok used instead of Gemini due to error)",
                    goal="Create a tailored multi-week LinkedIn content plan to help the user build their professional brand and position themselves in relevant career circles.",
                    backstory=(
                        "You are an expert in career branding and LinkedIn content strategy. "
                        "You analyze the user's background, aspirations, and uploaded documents to generate an actionable content plan "
                        "that helps them grow influence, participate in LinkedIn discussions, and become a recognized thought leader."
                    ),
                    llm=groq_llm,
                    verbose=False,
                    allow_delegation=False
                )

    def content_ideation_agent(self):
        return Agent(
            role='Content Ideation Agent',
            goal='Generate creative, engagement-focused LinkedIn post ideas from the approved strategy.',
            backstory=(
                "You are a creative content expert. You turn strategic plans into compelling LinkedIn post ideas with strong hooks and discussion prompts "
                "that are designed to attract attention and foster meaningful engagement."
            ),
            llm=groq_llm,
            verbose=False,
            allow_delegation=False
        )

    def linkedin_ghostwriter_agent(self):
        return Agent(
            role='Professional LinkedIn Ghostwriter',
            goal='Draft full, polished LinkedIn posts for the user in their authentic voice.',
            backstory=(
                "You are a skilled writer who specializes in LinkedIn. "
                "You use the user's resume and uploaded writing samples to capture their tone and style, "
                "creating posts that showcase their expertise, spark conversations, and build thought leadership."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def quality_assurance_agent(self):
        return Agent(
            role='Quality Assurance Agent',
            goal='Review drafted LinkedIn posts for clarity, tone, and engagement impact, providing actionable feedback.',
            backstory=(
                "You are a meticulous editor. Your job is to ensure each LinkedIn post is professional, engaging, clear, "
                "and encourages participation in the right professional circles."
            ),
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def title_agent(self):
        return Agent(
            role='Title Generator Agent',
            goal='Generate a concise, descriptive title for a LinkedIn branding session.',
            backstory=(
                "You are an AI assistant skilled at summarizing LinkedIn branding sessions into short, clear titles "
                "that capture the essence of the strategy."
            ),
            llm=groq_llm,
            verbose=False,
            allow_delegation=False
        )
