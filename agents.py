import os
from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

# Define the LLMs
gemini_llm = LLM(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-1.5-flash"
)

groq_llm = LLM(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.1-8b-instant"
)

class BrandingAgents:
    def personal_branding_strategist(self):
        return Agent(
            role='Personal Branding Strategist',
            goal="Create a tailored content plan to build a user's professional brand for their target career role.",
            backstory="You are an expert in career branding and content marketing. You analyze a user's background, skills, and career goals to devise a powerful, actionable content strategy.",
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def content_ideation_agent(self):
        return Agent(
            role='Creative Content Ideator',
            goal='Generate engaging content ideas based on a strategic plan.',
            backstory="You're a creative expert in social media content. You turn strategic plans into compelling post ideas with strong hooks and clear outlines for platforms like LinkedIn and Twitter.",
            llm=groq_llm,
            verbose=False,
            allow_delegation=False
        )
        
    def linkedin_ghostwriter_agent(self):
        return Agent(
            role='Professional LinkedIn Ghostwriter',
            goal='Draft a compelling, professional, and engaging LinkedIn post from a given content idea.',
            backstory="You are a master of words, specializing in writing for a sophisticated tech and business audience on LinkedIn. You can expand a simple idea into a full-fledged post that is clear, concise, and designed to spark conversation and establish thought leadership.",
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )

    def quality_assurance_agent(self):
        return Agent(
            role='Content Quality Assurance Analyst',
            goal='Review a drafted LinkedIn post for quality, clarity, tone, and strategic alignment, providing actionable feedback.',
            backstory="You are a meticulous editor with an eye for detail. Your job is to review a draft, compare it to the original goal, and provide specific, constructive criticism to elevate the post from good to great.",
            llm=gemini_llm,
            verbose=False,
            allow_delegation=False
        )
    
    # --- ADDED THIS MISSING AGENT ---
    def title_agent(self):
        return Agent(
            role='Chat Title Generator',
            goal='Create a concise, 3-5 word title for a branding strategy session.',
            backstory="You are an AI assistant skilled at summarizing conversations into short, descriptive titles for chat history.",
            llm=groq_llm,
            verbose=False,
            allow_delegation=False
        )