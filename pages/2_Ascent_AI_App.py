import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import BrandingAgents
from tasks import BrandingTasks
from utils import process_uploaded_files
import uuid
import re

# Load environment variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Ascent AI", page_icon="🚀", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "editing_session_id" not in st.session_state:
    st.session_state.editing_session_id = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "📝 Brand Strategy"

# --- HELPER FUNCTIONS ---
def get_current_session():
    if st.session_state.current_session_id:
        return st.session_state.sessions.get(st.session_state.current_session_id)
    return None

def new_session():
    session_id = str(uuid.uuid4())
    st.session_state.current_session_id = session_id
    st.session_state.sessions[session_id] = {
        "title": "New Session",
        "messages": [{"role": "assistant", "content": "Hi, I’m Ascent AI, your personal branding co-pilot. Let’s shape your LinkedIn presence together. To start, would you like to share your resume?"}],
        "conversation_state": "awaiting_resume_choice",
        "context": {}, 
        "strategy": "", 
        "post_ideas": {},  # Changed to a dictionary
        "draft": "", 
        "selected_idea": None
    }
    st.session_state.editing_session_id = None
    st.session_state.active_tab = "📝 Brand Strategy"

def parse_ideas(text):
    """Parses the AI's text output into a dictionary of themes and ideas."""
    ideas_dict = {}
    current_theme = None
    for line in text.strip().split('\n'):
        line = line.strip()
        if line.upper().startswith("THEME:"):
            current_theme = line.split(':', 1)[1].strip()
            if current_theme not in ideas_dict:
                ideas_dict[current_theme] = []
        elif line.startswith('- ') and current_theme:
            idea = line[2:].strip()
            ideas_dict[current_theme].append({"text": idea, "checked": True})
    return ideas_dict

# --- AGENT & TASK DEFINITIONS ---
agents = BrandingAgents()
tasks = BrandingTasks()

# --- SIDEBAR: SESSION MANAGEMENT ---
with st.sidebar:
    st.title("🚀 Ascent AI")
    st.markdown("Intelligent Branding for Your Career Ascent")

    if st.button("➕ New Session", use_container_width=True, type="primary"):
        new_session()
        st.rerun()

    st.divider()
    if st.session_state.sessions:
        st.subheader("📜 Session History")
        for session_id, session_data in reversed(list(st.session_state.sessions.items())):
            is_active = (session_id == st.session_state.current_session_id)
            label = f"**▶ {session_data['title']}**" if is_active else session_data['title']
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                if st.button(label, key=f"load_{session_id}", use_container_width=True):
                    st.session_state.current_session_id = session_id
                    st.session_state.editing_session_id = None
                    st.session_state.active_tab = "📝 Brand Strategy"
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

            if st.session_state.editing_session_id == session_id:
                new_title = st.text_input("New title", value=session_data["title"], key=f"edit_{session_id}", label_visibility="collapsed")
                if new_title != session_data["title"]:
                    st.session_state.sessions[session_id]["title"] = new_title
                    st.session_state.editing_session_id = None
                    st.rerun()

# --- MAIN CONTENT AREA ---
session = get_current_session()

if not session:
    st.info("Start a new session from the sidebar to begin your branding journey.")
else:
    st.title(f"Session: {session['title']}")

    strategy_tab, posts_tab, writer_tab = st.tabs(["📝 Brand Strategy", "💡 Post Ideas", "✍️ Final Post"])

    with strategy_tab:
        # ... (This section remains unchanged, so it's omitted for brevity) ...
        st.header("Strategy Development")

        for message in session.get("messages", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        state = session.get("conversation_state", "start")

        if state == "awaiting_resume_choice":
            col1, col2, _ = st.columns([1, 2, 2])
            with col1:
                if st.button("📄 Upload Resume"):
                    session["messages"].append({"role": "user", "content": "I'll upload my resume."})
                    session["conversation_state"] = "awaiting_resume_upload"
                    st.rerun()
            with col2:
                if st.button("📝 Skip & Describe Yourself"):
                    session["messages"].append({"role": "user", "content": "I'll skip and describe myself."})
                    session["conversation_state"] = "awaiting_intro"
                    st.rerun()

        elif state == "awaiting_resume_upload":
            uploaded_file = st.file_uploader("Please upload your resume (PDF, TXT, MD)", type=['pdf', 'txt', 'md'])
            if uploaded_file:
                with st.spinner("Analyzing your document..."):
                    file_text = process_uploaded_files([uploaded_file])
                    session["context"]["user_context"] = file_text
                    summarizer_agent = agents.resume_summarizer_agent()
                    summary_task = tasks.summarize_resume_task(summarizer_agent, file_text)
                    crew = Crew(agents=[summarizer_agent], tasks=[summary_task], process=Process.sequential)
                    summary = crew.kickoff().raw
                    session["messages"].append({"role": "assistant", "content": summary})
                    session["conversation_state"] = "awaiting_confirmation"
                    st.rerun()

        elif state == "awaiting_intro":
            if prompt := st.chat_input("Please provide a brief summary of your professional background and goals."):
                session["messages"].append({"role": "user", "content": prompt})
                session["context"]["user_context"] = prompt
                session["messages"].append({"role": "assistant", "content": "Thank you. Now, what’s the target role you’re aiming for?"})
                session["conversation_state"] = "awaiting_target"
                st.rerun()

        elif state == "awaiting_confirmation":
            if prompt := st.chat_input("Did I get that right? Is there anything else to add?"):
                session["messages"].append({"role": "user", "content": prompt})
                session["context"]["user_context"] += f"\n\nAdditional User Notes:\n{prompt}"
                session["messages"].append({"role": "assistant", "content": "Excellent, thank you. What is the target role you're aiming for?"})
                session["conversation_state"] = "awaiting_target"
                st.rerun()

        elif state in ["awaiting_target", "awaiting_audience", "awaiting_positioning", "awaiting_samples", "awaiting_duration"]:
            prompt_map = {
                "awaiting_target": "What is your target role? (e.g., AI Product Manager)",
                "awaiting_audience": "Who is your target audience? (e.g., Recruiters, industry peers)",
                "awaiting_positioning": "How do you want to come across? (e.g., authoritative, approachable)",
                "awaiting_samples": "To learn your unique voice, please upload 1-3 writing samples (blog posts, articles, etc.). You can also skip this step.",
                "awaiting_duration": "How many weeks for the content plan? (e.g., '4 weeks')"
            }
            key_map = {
                "awaiting_target": "target_role",
                "awaiting_audience": "target_audience",
                "awaiting_positioning": "positioning",
                "awaiting_duration": "duration"
            }
            next_state_map = {
                "awaiting_target": "awaiting_audience",
                "awaiting_audience": "awaiting_positioning",
                "awaiting_positioning": "awaiting_samples",
                "awaiting_samples": "awaiting_duration",
                "awaiting_duration": "generating_strategy"
            }

            if state == "awaiting_samples":
                st.info(prompt_map[state])
                uploaded_files = st.file_uploader("Upload your writing samples (PDF, TXT, MD)", type=['pdf', 'txt', 'md'], accept_multiple_files=True)
                
                if st.button("Skip for now"):
                    session["context"]["writing_samples"] = "" # No samples provided
                    session["messages"].append({"role": "user", "content": "Skipped uploading writing samples."})
                    session["conversation_state"] = next_state_map[state]
                    session["messages"].append({"role": "assistant", "content": prompt_map[session["conversation_state"]]})
                    st.rerun()

                if uploaded_files:
                    with st.spinner("Analyzing writing style..."):
                        file_text = process_uploaded_files(uploaded_files)
                        session["context"]["writing_samples"] = file_text
                        session["messages"].append({"role": "user", "content": f"Uploaded {len(uploaded_files)} writing sample(s)."})
                        session["conversation_state"] = next_state_map[state]
                        session["messages"].append({"role": "assistant", "content": prompt_map[session["conversation_state"]]})
                        st.rerun()
            else:
                if prompt := st.chat_input(prompt_map.get(state)):
                    session["messages"].append({"role": "user", "content": prompt})
                    context_key = key_map.get(state)
                    if context_key:
                        session["context"][context_key] = prompt
                    session["conversation_state"] = next_state_map[state]
                    if session["conversation_state"] != "generating_strategy":
                        session["messages"].append({"role": "assistant", "content": prompt_map[session["conversation_state"]]})
                    st.rerun()

        elif state == "generating_strategy":
            with st.chat_message("assistant"):
                with st.spinner("Perfect, I have everything I need. The Strategist is now crafting your brand strategy..."):
                    if "platform" not in session["context"]:
                        session["context"]["platform"] = "LinkedIn"

                    strategist_agent = agents.personal_branding_strategist()
                    strategy_task = tasks.strategy_task(strategist_agent, **session["context"])
                    crew = Crew(agents=[strategist_agent], tasks=[strategy_task], process=Process.sequential)
                    strategy = crew.kickoff().raw
                    session["strategy"] = strategy

                    title_agent = agents.title_agent()
                    title_task = tasks.title_task(title_agent, strategy)
                    title_crew = Crew(agents=[title_agent], tasks=[title_task], process=Process.sequential)
                    session["title"] = title_crew.kickoff().raw
                    st.toast(f"Session renamed to: {session['title']}")

                    response = f"Here is the initial brand strategy I've developed for you:\n\n---\n\n{strategy}\n\n---\n\nDoes this feel like the right direction? Please provide feedback for refinement, or type 'looks good' to approve."
                    st.markdown(response)
                    session["messages"].append({"role": "assistant", "content": response})
                    session["conversation_state"] = "awaiting_refinement"
                    st.rerun()

        elif state == "awaiting_refinement":
            if prompt := st.chat_input("Provide feedback to refine the strategy, or type 'looks good' to approve..."):
                session["messages"].append({"role": "user", "content": prompt})
                if any(word in prompt.lower() for word in ["good", "approve", "perfect", "continue"]):
                    with st.spinner("Finalizing strategy and brainstorming post ideas..."):
                        ideator_agent = agents.content_ideation_agent()
                        ideation_task = tasks.ideation_task(ideator_agent, session["strategy"])
                        crew = Crew(agents=[ideator_agent], tasks=[ideation_task], process=Process.sequential)
                        ideas_text = crew.kickoff().raw
                        session["post_ideas"] = parse_ideas(ideas_text)
                        response = "Great! The strategy is finalized. I've also generated some initial post ideas for you. You can view them now in the **💡 Post Ideas** tab."
                        st.toast("Post ideas generated!")
                        session["conversation_state"] = "strategy_approved"
                else:
                    with st.spinner("Refining the strategy based on your feedback..."):
                        strategist_agent = agents.personal_branding_strategist()
                        refine_task = tasks.refine_strategy_task(strategist_agent, session["strategy"], prompt, **session["context"])
                        crew = Crew(agents=[strategist_agent], tasks=[refine_task], process=Process.sequential)
                        new_strategy = crew.kickoff().raw
                        session["strategy"] = new_strategy
                        response = f"I've updated the strategy based on your feedback:\n\n---\n\n{new_strategy}\n\n---\n\nHow does this new version look?"

                session["messages"].append({"role": "assistant", "content": response})
                st.rerun()

        elif state == "strategy_approved":
            st.success("Strategy approved! You can now generate post ideas or proceed to the other tabs.")


    with posts_tab:
        st.header("Your Content Ideas")
        if session.get("post_ideas"):
            post_ideas = session["post_ideas"]

            for theme, ideas in post_ideas.items():
                st.subheader(theme)
                for i, idea in enumerate(ideas):
                    col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
                    with col1:
                        idea["checked"] = st.checkbox("", value=idea["checked"], key=f"check_{theme}_{i}")
                    with col2:
                        st.markdown(f"- {idea['text']}")
                    with col3:
                        if st.button("✍️ Write", key=f"write_{theme}_{i}", use_container_width=True):
                            session["selected_idea"] = idea['text']
                            session["conversation_state"] = "drafting_post"
                            st.rerun()
                st.markdown("---")
            
            st.subheader("Refine & Regenerate")
            
            # Regenerate unchecked ideas
            if st.button("🔄 Generate New Ideas for Unselected"):
                themes_to_regenerate = []
                # Identify which themes have unchecked items
                for theme, ideas in post_ideas.items():
                    if any(not idea["checked"] for idea in ideas):
                        themes_to_regenerate.append(theme)
                
                if themes_to_regenerate:
                    with st.spinner("Generating new ideas for unselected items..."):
                        ideator_agent = agents.content_ideation_agent()
                        regenerate_task = tasks.regenerate_ideas_task(ideator_agent, session["strategy"], themes_to_regenerate)
                        crew = Crew(agents=[ideator_agent], tasks=[regenerate_task], process=Process.sequential)
                        new_ideas_text = crew.kickoff().raw
                        newly_generated_ideas = parse_ideas(new_ideas_text)

                        # Replace only the unchecked ideas
                        for theme, new_ideas in newly_generated_ideas.items():
                            # Filter out unchecked ideas from the original list
                            kept_ideas = [idea for idea in post_ideas.get(theme, []) if idea["checked"]]
                            # Combine kept ideas with new ideas
                            session["post_ideas"][theme] = kept_ideas + new_ideas
                        
                        st.rerun()
                else:
                    st.warning("Please unselect at least one idea to regenerate.")

            # Refine all ideas with feedback
            refinement_feedback = st.text_area("Provide feedback to refine all ideas:", key="refinement_feedback")
            if st.button("Refine All Ideas with Feedback"):
                if refinement_feedback:
                    with st.spinner("Refining all ideas based on your feedback..."):
                        ideator_agent = agents.content_ideation_agent()
                        refine_task = tasks.refine_ideation_task(ideator_agent, session["strategy"], refinement_feedback)
                        crew = Crew(agents=[ideator_agent], tasks=[refine_task], process=Process.sequential)
                        new_ideas_text = crew.kickoff().raw
                        session["post_ideas"] = parse_ideas(new_ideas_text)
                        st.rerun()
                else:
                    st.warning("Please provide feedback before refining.")

        else:
            st.info("Your generated post ideas will appear here once the strategy is finalized.")


    with writer_tab:
        st.header("Your Final Post")
        if session.get("conversation_state") == "drafting_post" and session.get("selected_idea"):
            with st.spinner("The Ghostwriter is drafting your post..."):
                writer_agent = agents.linkedin_ghostwriter_agent()
                writing_task_instance = tasks.writing_task(writer_agent, session["selected_idea"])
                crew = Crew(agents=[writer_agent], tasks=[writing_task_instance], process=Process.sequential)
                draft = crew.kickoff().raw
                session["draft"] = draft
                session["conversation_state"] = "post_drafted"
                st.rerun()

        if session.get("draft"):
            st.subheader("Drafted Post")
            st.markdown(session["draft"])
            st.divider()

            st.subheader("Quality Check & Refinement")
            if st.button("🔍 Run Quality Check"):
                with st.spinner("The Quality Assurance Agent is reviewing your post..."):
                    qa_agent = agents.quality_assurance_agent()
                    qa_task = tasks.qa_critique_task(qa_agent, session["draft"])
                    crew = Crew(agents=[qa_agent], tasks=[qa_task], process=Process.sequential)
                    critique = crew.kickoff().raw
                    st.session_state.qa_critique = critique
            
            if "qa_critique" in st.session_state:
                with st.chat_message("assistant"):
                    st.markdown(st.session_state.qa_critique)

            feedback = st.text_area("Or, provide your own feedback for refinement:")
            if st.button("Refine Draft"):
                if feedback:
                    with st.spinner("The Ghostwriter is refining the draft based on your feedback..."):
                        writer_agent = agents.linkedin_ghostwriter_agent()
                        refine_task = tasks.refine_writing_task(writer_agent, session["draft"], feedback)
                        crew = Crew(agents=[writer_agent], tasks=[refine_task], process=Process.sequential)
                        new_draft = crew.kickoff().raw
                        session["draft"] = new_draft
                        st.rerun()
                else:
                    st.error("Please provide feedback before refining.")
        else:
            st.info("Select an idea from the 'Post Ideas' tab to start writing.")