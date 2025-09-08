import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import BrandingAgents
from tasks import BrandingTasks
from utils import process_uploaded_files
import uuid

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Ascent AI", page_icon="🧑‍💼", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "editing_session_id" not in st.session_state:
    st.session_state.editing_session_id = None

# --- HELPER FUNCTIONS ---
def get_current_session():
    if st.session_state.current_session_id:
        return st.session_state.sessions.get(st.session_state.current_session_id)
    return None

def new_session():
    session_id = str(uuid.uuid4())
    st.session_state.current_session_id = session_id
    st.session_state.sessions[session_id] = {
        "title": "New Session", "context": {}, "strategy": "",
        "post_ideas": [], "selected_idea": "", "draft": "", "critique": ""
    }
    st.session_state.editing_session_id = None

# --- AGENT & TASK DEFINITIONS ---
agents = BrandingAgents()
tasks = BrandingTasks()

# --- SIDEBAR: Redesigned for Professional Look ---
with st.sidebar:
    st.title("🧑‍💼 Ascent AI")
    st.markdown("Your AI-Powered Career Branding Assistant.")
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_session()
        st.rerun()

    st.divider()

    st.subheader("Recent")
    # Show most recent sessions at the top
    for session_id, session_data in reversed(list(st.session_state.sessions.items())):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            if st.session_state.editing_session_id == session_id:
                new_title = st.text_input("New title", value=session_data["title"], key=f"edit_{session_id}")
                if new_title != session_data["title"]:
                    st.session_state.sessions[session_id]["title"] = new_title
                    st.session_state.editing_session_id = None
                    st.rerun()
            else:
                if st.button(session_data["title"], key=f"load_{session_id}", use_container_width=True):
                    st.session_state.current_session_id = session_id
                    st.session_state.editing_session_id = None
                    st.rerun()
        with col2:
            if st.button("✏️", key=f"start_edit_{session_id}", use_container_width=True):
                st.session_state.editing_session_id = session_id
                st.rerun()
        with col3:
            if st.button("🗑️", key=f"delete_{session_id}", use_container_width=True):
                del st.session_state.sessions[session_id]
                if st.session_state.current_session_id == session_id:
                    st.session_state.current_session_id = None
                st.rerun()

# --- MAIN CONTENT AREA ---
session = get_current_session()

# Robust check to ensure all necessary keys exist in any loaded session
if session:
    required_keys = ["context", "strategy", "post_ideas", "selected_idea", "draft", "critique"]
    for key in required_keys:
        if key not in session:
            session[key] = [] if key == "post_ideas" else ""

if not session:
    st.info("Start a new chat from the sidebar to begin.")
else:
    st.title(f"Session: {session['title']}")
    
    strategy_tab, posts_tab, writer_tab = st.tabs(["📝 Brand Strategy", "💡 Post Ideas", "✍️ Final Post"])

    with strategy_tab:
        if not session["strategy"]:
            st.info("Let's build your brand. Please provide your goals and context below to generate your strategy.")
            with st.expander("🎯 Step 1: Define Your Career Goals", expanded=True):
                session["context"]["target_role"] = st.text_input("Target Role", placeholder="e.g., AI Product Manager")
                session["context"]["target_audience"] = st.text_input("Target Audience", placeholder="e.g., Recruiters at FAANG companies")
                session["context"]["platform"] = st.selectbox("Primary Platform", ["LinkedIn", "Twitter", "Medium Blog"])
                session["context"]["duration"] = st.slider("Content Plan Duration (Weeks)", 2, 12, 4)

            with st.expander("📝 Step 2: Provide Your Professional Context", expanded=True):
                uploaded_files = st.file_uploader("Upload your resume, portfolio, etc.", type=['pdf', 'txt', 'md'], accept_multiple_files=True)
                user_info = st.text_area("Provide any extra details not on your resume...", height=150)
            
            if st.button("Generate My Strategy", use_container_width=True, type="primary"):
                if not session["context"].get("target_role"):
                    st.warning("Please define your target role first.")
                else:
                    file_text = process_uploaded_files(uploaded_files)
                    session["context"]["user_context"] = f"User's Summary:\n{user_info}\n\nDocuments Content:\n{file_text}"
                    
                    strategist_agent = agents.personal_branding_strategist()
                    strategy_task = tasks.strategy_task(strategist_agent, **session["context"])
                    crew = Crew(agents=[strategist_agent], tasks=[strategy_task], process=Process.sequential, verbose=False)
                    with st.spinner("🧑‍💼 The Strategist (Gemini) is crafting your brand strategy..."):
                        result = crew.kickoff().raw
                        session["strategy"] = result
                        
                        title_agent = agents.title_agent()
                        title_task = tasks.title_task(title_agent, result)
                        title_crew = Crew(agents=[title_agent], tasks=[title_task], process=Process.sequential, verbose=False)
                        session["title"] = title_crew.kickoff().raw
                        
                        # Add a toast notification to make the renaming obvious
                        st.toast(f"Session renamed to: {session['title']}")
                        st.rerun()
        
        if session["strategy"]:
            st.subheader("Your Generated Brand Strategy")
            with st.container(border=True):
                st.markdown(session["strategy"])
                st.download_button(label="📥 Download Strategy", data=str(session["strategy"]), file_name=f"{session['title'].replace(' ','_')}_strategy.md", mime="text/markdown")
            
            st.divider()
            st.subheader(" refine Your Strategy")
            with st.container(border=True):
                critique = st.text_area("Provide feedback here...", key=f"critique_{session['title']}")
                if st.button("🔄 Regenerate with Feedback"):
                    if critique:
                        strategist_agent = agents.personal_branding_strategist()
                        refine_task = tasks.refine_strategy_task(strategist_agent, session["strategy"], critique, **session["context"])
                        crew = Crew(agents=[strategist_agent], tasks=[refine_task], process=Process.sequential, verbose=False)
                        with st.spinner("🧑‍💼 Strategist (Gemini) is refining the work..."):
                            result = crew.kickoff().raw
                            session["strategy"] = result
                            st.success("Strategy has been updated!")
                            st.rerun()
                    else:
                        st.warning("Please provide feedback before regenerating.")

    with posts_tab:
        st.header("Your Content Ideas")
        if not session["strategy"]:
            st.info("Please generate a brand strategy first.")
        else:
            if st.button("💡 Generate Post Ideas from Strategy", use_container_width=True, type="primary"):
                ideator_agent = agents.content_ideation_agent()
                ideation_task = tasks.ideation_task(ideator_agent, session["strategy"])
                crew = Crew(agents=[ideator_agent], tasks=[ideation_task], process=Process.sequential, verbose=False)
                with st.spinner("💡 The Ideator (Groq) is brainstorming..."):
                    result = crew.kickoff().raw
                    session["post_ideas"] = result.split('\n\n')
                    st.rerun()
            
            if session["post_ideas"]:
                st.subheader("Generated Post Ideas")
                for i, idea in enumerate(session["post_ideas"]):
                    if idea.strip():
                        with st.container(border=True):
                            st.markdown(idea)
                            if st.button("✍️ Write This Post", key=f"write_{i}"):
                                session["selected_idea"] = idea
                                writer_agent = agents.linkedin_ghostwriter_agent()
                                qa_agent = agents.quality_assurance_agent()
                                write_task = tasks.writing_task(writer_agent, idea)
                                critique_task = tasks.qa_task(qa_agent, write_task)
                                writing_crew = Crew(agents=[writer_agent, qa_agent], tasks=[write_task, critique_task], process=Process.sequential)
                                with st.spinner("✍️ The Writer & QA Agents are working..."):
                                    post_result = writing_crew.kickoff()
                                    session["draft"] = post_result.raw 
                                    st.success("Draft generated! See the 'Final Post' tab.")

    with writer_tab:
        st.header("Your Final Post")
        if not session["draft"]:
            st.info("Select an idea from the 'Post Ideas' tab and click 'Write This Post' to generate a draft here.")
        else:
            st.subheader("Generated Draft & AI Critique")
            with st.container(border=True):
                st.markdown(session["draft"])
            
            st.divider()
            st.subheader(" refine Your Post")
            with st.container(border=True):
                 st.info("The refinement loop for the final post can be built here, similar to the strategy refinement.")
                 st.download_button(label="📥 Download Post", data=str(session["draft"]), file_name=f"{session['title'].replace(' ','_')}_post.md", mime="text/markdown")