import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import BrandingAgents
from tasks import BrandingTasks
from utils import process_uploaded_files
import uuid
import re
from datetime import datetime

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
if "qa_critique" not in st.session_state:
    st.session_state.qa_critique = ""


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
        "strategy_history": [],
        "post_ideas": {},
        "draft_history": [],
        "draft": "", 
        "selected_idea": None
    }
    st.session_state.editing_session_id = None
    st.session_state.active_tab = "📝 Brand Strategy"

def create_mock_session():
    """Creates a pre-populated session for testing purposes."""
    session_id = str(uuid.uuid4())
    st.session_state.current_session_id = session_id
    st.session_state.sessions[session_id] = {
        "title": "Mock Testing Session",
        "messages": [{"role": "assistant", "content": "Mock session loaded. Ready for testing!"}],
        "conversation_state": "strategy_approved",
        "context": {
            "user_context": "Sample user background.",
            "target_role": "AI Product Manager",
            "target_audience": "Tech executives and VCs",
            "positioning": "Innovative and data-driven",
            "duration": "4",
            "platform": "LinkedIn"
        },
        "strategy_history": [{
            "version": 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content": "A simple 4-week strategy for an AI Product Manager."
        }],
        "post_ideas": {
            "Future of PM in the Age of Generative AI": [
                {"text": "As Generative AI reshapes our world, how will PMs adapt to leverage its power for transformative innovation?", "checked": False},
                {"text": "Imagine PMs as AI strategists - what would be the most critical skillsets for success?", "checked": False},
                {"text": "Will AI-generated insights revolutionize product decision-making - share your thoughts!", "checked": False}
            ],
            "Quantifying Innovation's Impact at Genentech": [
                {"text": "From zero to hero: how a simple data product transformed productivity at Genentech.", "checked": False},
                {"text": "26 FTEs freed to focus on strategy - what innovative solutions have you unlocked?", "checked": False},
                {"text": "Unlocking the numbers: how data-driven innovation improved process efficiency.", "checked": False}
            ]
        },
        "draft_history": [],
        "draft": "",
        "selected_idea": None
    }
    st.session_state.editing_session_id = None
    st.session_state.active_tab = "💡 Post Ideas"
    st.toast("Mock session created successfully! You can now test the Post Ideas tab.")
    st.rerun()

def parse_ideas(text):
    """Parses the AI's text output into a dictionary of themes and ideas."""
    ideas_dict = {}
    current_theme = None
    sections = re.split(r'THEME:\s*', text, flags=re.IGNORECASE)[1:]
    
    for section in sections:
        lines = section.strip().split('\n')
        
        if len(lines) > 0 and not lines[0].strip().startswith('-'):
            current_theme = lines[0].strip()
            lines = lines[1:]
        else:
            last_line = lines[-1].strip() if lines else ""
            if "THEME:" in last_line:
                current_theme = last_line.replace("THEME:", "").strip()
                lines.pop()
            else:
                current_theme = "Uncategorized Ideas"
        
        if current_theme not in ideas_dict:
            ideas_dict[current_theme] = []

        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                idea = line[2:].strip()
                ideas_dict[current_theme].append({"text": idea, "checked": False})
            elif len(ideas_dict[current_theme]) > 0:
                ideas_dict[current_theme][-1]["text"] += " " + line
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
    
    if st.button("🧪 Load Test Session", use_container_width=True):
        create_mock_session()

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
                    st.session_state.qa_critique = "" # Clear critique
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
                    st.session_state.qa_critique = "" # Clear critique
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
    st.title("Create Your Personal Branding Strategy") 

    strategy_tab, posts_tab, writer_tab = st.tabs(["📝 Brand Strategy", "💡 Post Ideas", "✍️ Final Post"])

    with strategy_tab:

        all_states = [
            "start", "awaiting_resume_choice", "awaiting_resume_upload", "awaiting_intro",
            "awaiting_confirmation", "awaiting_target", "awaiting_audience",
            "awaiting_positioning", "awaiting_samples", "awaiting_duration",
            "generating_strategy", "awaiting_outline_approval", "awaiting_refinement", "strategy_approved", "drafting_post", "post_drafted"
        ]

        # Define the states that are part of the core strategy progress
        strategy_states = [
            "start", "awaiting_resume_choice", "awaiting_resume_upload", "awaiting_intro",
            "awaiting_confirmation", "awaiting_target", "awaiting_audience",
            "awaiting_positioning", "awaiting_samples", "awaiting_duration",
            "generating_strategy", "awaiting_outline_approval", "awaiting_refinement", "strategy_approved"
        ]
        
        progress_steps = [
            "Resume & Background", "Goals & Positioning",
            "Strategy Generation", "Strategy Approval"
        ]

        current_state = session.get("conversation_state", "start")
        
        # Calculate progress based only on strategy-related states
        if current_state in strategy_states:
            current_state_index = strategy_states.index(current_state)
            progress_value = current_state_index / (len(strategy_states) - 1)
        else:
            # Once the strategy is approved, the progress bar is considered full
            progress_value = 1.0

        st.progress(progress_value)

        cols = st.columns(len(progress_steps))
        for i, step_title in enumerate(progress_steps):
            with cols[i]:
                is_active = False
                if step_title == "Resume & Background" and current_state in ["awaiting_resume_choice", "awaiting_resume_upload", "awaiting_intro", "awaiting_confirmation"]:
                    is_active = True
                elif step_title == "Goals & Positioning" and current_state in ["awaiting_target", "awaiting_audience", "awaiting_positioning", "awaiting_samples", "awaiting_duration"]:
                    is_active = True
                elif step_title == "Strategy Generation" and current_state in ["generating_strategy", "awaiting_outline_approval"]:
                    is_active = True
                elif step_title == "Strategy Approval" and current_state in ["awaiting_refinement", "strategy_approved"]:
                    is_active = True
                
                if is_active:
                    st.markdown(f"**{step_title}**")
                else:
                    st.markdown(f"_{step_title}_")

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
                "awaiting_audience": "Who is your target audience? (e.g., Hiring managers at top tech firms, fellow developers in the open-source community, venture capitalists interested in AI)",
                "awaiting_positioning": "How do you want to come across? (e.g., authoritative, data-driven, innovative, visionary, approachable and community-focused)",
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
                    session["context"]["writing_samples"] = ""
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
                with st.spinner("Perfect, I have everything I need. The Strategist is now crafting a high-level outline..."):
                    if "platform" not in session["context"]:
                        session["context"]["platform"] = "LinkedIn"
                    
                    outline_context = {k: v for k, v in session["context"].items() if k != 'writing_samples'}
                    
                    strategist_agent = agents.personal_branding_strategist()
                    intermediate_outline_task = tasks.intermediate_outline_task(strategist_agent, **outline_context)
                    crew = Crew(agents=[strategist_agent], tasks=[intermediate_outline_task], process=Process.sequential)
                    intermediate_outline = crew.kickoff().raw
                    
                    response = f"Here is a high-level outline for your content strategy:\n\n---\n\n{intermediate_outline}\n\n---\n\nDoes this feel like the right direction? Please provide feedback for refinement, or type 'looks good' to proceed with the full strategy."
                    st.markdown(response)
                    session["messages"].append({"role": "assistant", "content": response})
                    session["conversation_state"] = "awaiting_outline_approval"
                    st.rerun()

        elif state == "awaiting_outline_approval":
            if prompt := st.chat_input("Provide feedback to refine the outline, or type 'looks good' to approve..."):
                session["messages"].append({"role": "user", "content": prompt})
                if any(word in prompt.lower() for word in ["good", "approve", "perfect", "continue"]):
                    with st.spinner("Great! Now creating the detailed strategy based on the outline..."):
                        strategist_agent = agents.personal_branding_strategist()
                        strategy_task = tasks.strategy_task(strategist_agent, **session["context"])
                        crew = Crew(agents=[strategist_agent], tasks=[strategy_task], process=Process.sequential)
                        strategy = crew.kickoff().raw
                        
                        # Save the first detailed strategy to history
                        session["strategy_history"].append({
                            "version": len(session["strategy_history"]) + 1,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "content": strategy
                        })

                        title_agent = agents.title_agent()
                        title_task = tasks.title_task(title_agent, strategy)
                        title_crew = Crew(agents=[title_agent], tasks=[title_task], process=Process.sequential)
                        session["title"] = title_crew.kickoff().raw
                        st.toast(f"Session renamed to: {session['title']}")
                        
                        response = f"Here is the detailed brand strategy:\n\n---\n\n{strategy}\n\n---\n\nDoes this feel like the right direction? Please provide feedback for refinement, or type 'looks good' to approve."
                        st.markdown(response)
                        session["messages"].append({"role": "assistant", "content": response})
                        session["conversation_state"] = "awaiting_refinement"
                        st.rerun()
                else:
                    with st.spinner("Refining the outline based on your feedback..."):
                        strategist_agent = agents.personal_branding_strategist()
                        refine_task = tasks.refine_strategy_task(strategist_agent, session["strategy_history"][-1]["content"] if session["strategy_history"] else "", prompt, **session["context"])
                        crew = Crew(agents=[strategist_agent], tasks=[refine_task], process=Process.sequential)
                        new_outline = crew.kickoff().raw
                        
                        # Save refined outline to history
                        session["strategy_history"].append({
                            "version": len(session["strategy_history"]) + 1,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "content": new_outline
                        })
                        
                        response = f"I've updated the outline based on your feedback:\n\n---\n\n{new_outline}\n\n---\n\nHow does this new version look?"
                    session["messages"].append({"role": "assistant", "content": response})
                    st.rerun()

        elif state == "awaiting_refinement":
            if prompt := st.chat_input("Provide feedback to refine the strategy, or type 'looks good' to approve..."):
                session["messages"].append({"role": "user", "content": prompt})
                if any(word in prompt.lower() for word in ["good", "approve", "perfect", "continue"]):
                    with st.spinner("Finalizing strategy and brainstorming post ideas..."):
                        ideator_agent = agents.content_ideation_agent()
                        ideation_task = tasks.ideation_task(ideator_agent, session["strategy_history"][-1]["content"])
                        crew = Crew(agents=[ideator_agent], tasks=[ideation_task], process=Process.sequential)
                        ideas_text = crew.kickoff().raw
                        session["post_ideas"] = parse_ideas(ideas_text)
                        response = "Great! The strategy is finalized. I've also generated some initial post ideas for you. You can view them now in the **💡 Post Ideas** tab."
                        st.toast("Post ideas generated!")
                        session["conversation_state"] = "strategy_approved"
                else:
                    with st.spinner("Refining the strategy based on your feedback..."):
                        current_strategy = session["strategy_history"][-1]["content"]
                        strategist_agent = agents.personal_branding_strategist()
                        refine_task = tasks.refine_strategy_task(strategist_agent, current_strategy, prompt, **session["context"])
                        crew = Crew(agents=[strategist_agent], tasks=[refine_task], process=Process.sequential)
                        new_strategy = crew.kickoff().raw
                        
                        # Append new strategy to history
                        session["strategy_history"].append({
                            "version": len(session["strategy_history"]) + 1,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "content": new_strategy
                        })

                        response = f"I've updated the strategy based on your feedback:\n\n---\n\n{new_strategy}\n\n---\n\nHow does this new version look?"

                session["messages"].append({"role": "assistant", "content": response})
                st.rerun()

        elif state == "strategy_approved":
            st.success("Strategy approved! You can now generate post ideas or proceed to the other tabs.")

        # --- Display Strategy History ---
        if session["strategy_history"]:
            st.markdown("---")
            st.subheader("Strategy History")
            
            history_options = [
                f"Version {item['version']} ({item['timestamp']})"
                for item in session["strategy_history"]
            ]
            selected_index = st.selectbox("Select a version to view:", range(len(history_options)), format_func=lambda i: history_options[i])
            
            selected_strategy = session["strategy_history"][selected_index]["content"]
            st.text_area("Selected Strategy", value=selected_strategy, height=500, key=f"strategy_display_{selected_index}")
            
    with posts_tab:
        st.header("Your Content Ideas")
        st.markdown("These ideas are based on your personal branding strategy. Use the options below to refine and select your favorites.")

        if session.get("post_ideas"):
            post_ideas = session["post_ideas"]

            # Loop through each theme to display per-theme sections and ideas
            for theme_index, (theme, ideas) in enumerate(post_ideas.items()):
                st.subheader(f"{theme_index + 1}. {theme}")
                
                # Loop through each idea within the theme
                for i, idea in enumerate(ideas):
                    col1, col2, col3, col4, col5 = st.columns([0.05, 0.65, 0.05, 0.20, 0.10])
                    
                    with col1:
                        idea["checked"] = st.checkbox("", value=idea["checked"], key=f"check_{theme}_{i}")
                    
                    with col2:
                        st.markdown(f'"{idea["text"]}"')
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_{theme}_{i}", use_container_width=True):
                            st.session_state.sessions[st.session_state.current_session_id]["post_ideas"][theme].pop(i)
                            st.rerun()

                    with col4:
                        if st.button("➕3 More like this", key=f"more_{theme}_{i}", use_container_width=True):
                            with st.spinner("Generating more ideas..."):
                                ideator_agent = agents.content_ideation_agent()
                                similar_ideas_task = tasks.generate_similar_ideas_task(ideator_agent, session["strategy_history"][-1]["content"], theme, idea["text"])
                                crew = Crew(agents=[ideator_agent], tasks=[similar_ideas_task], process=Process.sequential)
                                similar_ideas_text = crew.kickoff().raw
                                
                                newly_generated_ideas = parse_ideas(similar_ideas_text)
                                new_ideas_list = newly_generated_ideas.get(theme, [])
                                
                                session["post_ideas"][theme].extend(new_ideas_list)
                                st.rerun()
                                
                    with col5:
                        if st.button("✍️ Write", key=f"write_{theme}_{i}"):
                            session["selected_idea"] = idea['text']
                            session["conversation_state"] = "drafting_post"
                            st.session_state.qa_critique = "" # Clear critique
                            st.rerun()

                # Per-theme refinement section
                with st.container():
                    st.markdown(f"**Refine Ideas for This Theme**")
                    
                    refinement_feedback = st.text_area("Provide feedback:", key=f"per_theme_feedback_{theme}")
                    
                    refinement_cols = st.columns(2)
                    with refinement_cols[0]:
                        if st.button("Refine Selected Topics", key=f"refine_{theme}", use_container_width=True):
                            selected_ideas_to_refine = [idea["text"] for idea in post_ideas[theme] if idea["checked"]]
                            
                            if selected_ideas_to_refine and refinement_feedback:
                                with st.spinner("Refining selected ideas..."):
                                    ideator_agent = agents.content_ideation_agent()
                                    refine_task = tasks.refine_ideas_with_feedback_task(ideator_agent, session["strategy_history"][-1]["content"], refinement_feedback, selected_ideas_to_refine)
                                    crew = Crew(agents=[ideator_agent], tasks=[refine_task], process=Process.sequential)
                                    refined_ideas_text = crew.kickoff().raw
                                    
                                    refined_ideas_dict = parse_ideas(refined_ideas_text)
                                    
                                    refined_ideas_list = list(refined_ideas_dict.values())[0] if refined_ideas_dict else []
                                    
                                    kept_ideas = [idea for idea in post_ideas[theme] if not idea["checked"]]
                                    
                                    session["post_ideas"][theme] = kept_ideas + refined_ideas_list
                                
                                st.rerun()
                            else:
                                st.warning("Please select topics and provide feedback to refine.")

                    with refinement_cols[1]:
                        if st.button("🔄 Generate New Ideas for Unselected Topics", key=f"regenerate_{theme}", use_container_width=True):
                            unselected_ideas_count = sum(1 for idea in post_ideas[theme] if not idea["checked"])
                            if unselected_ideas_count > 0:
                                with st.spinner(f"Generating {unselected_ideas_count} new ideas..."):
                                    ideator_agent = agents.content_ideation_agent()
                                    generate_task = tasks.generate_new_ideas_for_theme_task(ideator_agent, session["strategy_history"][-1]["content"], theme, unselected_ideas_count)
                                    crew = Crew(agents=[ideator_agent], tasks=[generate_task], process=Process.sequential)
                                    new_ideas_text = crew.kickoff().raw
                                    newly_generated_ideas = parse_ideas(new_ideas_text)

                                    kept_ideas = [idea for idea in post_ideas[theme] if idea["checked"]]
                                    session["post_ideas"][theme] = kept_ideas + newly_generated_ideas.get(theme, [])
                                    st.rerun()
                            else:
                                st.warning("Please unselect at least one idea to regenerate.")
    

                   
            # Start of the Overall Strategy Refinement section
            st.subheader("Overall Strategy Refinement")
            st.markdown("Actions that apply across all themes.")

            overall_feedback = st.text_area("Provide feedback to refine all topics or generate new ones only for the unselected topics. Feedback will modify the selected ideas; generating new ideas will replace all unselected ones with a fresh batch.", key="overall_feedback_area")
            overall_cols = st.columns(2)

            with overall_cols[0]:
                if st.button("Refine All Ideas with Feedback", key="refine_all_selected_btn", use_container_width=True):
                    selected_ideas = []
                    for theme, ideas in session["post_ideas"].items():
                        for idea in ideas:
                            if idea["checked"]:
                                selected_ideas.append(f"THEME: {theme}\n- {idea['text']}")

                    if selected_ideas and overall_feedback:
                        with st.spinner("Refining all selected ideas..."):
                            ideator_agent = agents.content_ideation_agent()
                            refine_task = tasks.refine_selected_ideas_across_themes_task(ideator_agent, session["strategy_history"][-1]["content"], overall_feedback, selected_ideas)
                            crew = Crew(agents=[ideator_agent], tasks=[refine_task], process=Process.sequential)
                            refined_ideas_text = crew.kickoff().raw
                            refined_ideas = parse_ideas(refined_ideas_text)

                            for refined_theme, new_ideas in refined_ideas.items():
                                ideas_to_keep = [idea for idea in session["post_ideas"][refined_theme] if idea["text"] not in [s.replace(f"THEME: {refined_theme}\n- ", "") for s in selected_ideas]]
                                session["post_ideas"][refined_theme] = ideas_to_keep + new_ideas
                            st.rerun()
                    else:
                        st.warning("Please select ideas and provide feedback to refine.")

            with overall_cols[1]:
                if st.button("🔄 Generate New Ideas for All Unselected Topics", key="regenerate_all_unselected_btn", use_container_width=True):
                    themes_to_regenerate = []
                    for theme, ideas in session["post_ideas"].items():
                        if not any(idea["checked"] for idea in ideas):
                            themes_to_regenerate.append(theme)
                    
                    if themes_to_regenerate:
                        with st.spinner("Generating new ideas for all unselected themes..."):
                            ideator_agent = agents.content_ideation_agent()
                            regenerate_task = tasks.regenerate_ideas_for_all_unselected_topics_task(ideator_agent, session["strategy_history"][-1]["content"], themes_to_regenerate)
                            crew = Crew(agents=[ideator_agent], tasks=[regenerate_task], process=Process.sequential)
                            new_ideas_text = crew.kickoff().raw
                            newly_generated_ideas = parse_ideas(new_ideas_text)

                            for theme, new_ideas in newly_generated_ideas.items():
                                kept_ideas = [idea for idea in session["post_ideas"][theme] if idea["checked"]]
                                session["post_ideas"][theme] = kept_ideas + new_ideas
                            st.rerun()
                    else:
                        st.warning("All ideas are selected. Please unselect ideas to regenerate.")

        else:
            st.info("Your generated post ideas will appear here once the strategy is finalized.")

    with writer_tab:
        st.subheader("Your Final Workspace ✨")
        st.markdown("Review, refine, and save drafts of your content. Use the tools below to get AI-powered feedback and download a local copy of your work.")

        # This single block now handles drafting AND critiquing
        if session.get("conversation_state") == "drafting_post" and session.get("selected_idea"):
            with st.spinner("The Ghostwriter is drafting your post..."):
                try:
                    # 1. Draft the post
                    writer_agent = agents.linkedin_ghostwriter_agent()
                    writing_task_instance = tasks.writing_task(writer_agent, session["selected_idea"])
                    writing_crew = Crew(agents=[writer_agent], tasks=[writing_task_instance], process=Process.sequential)
                    draft = writing_crew.kickoff().raw
                    session["draft"] = draft

                    # 2. Immediately run the QA check on the new draft
                    qa_agent = agents.quality_assurance_agent()
                    qa_task = tasks.qa_critique_task(qa_agent, draft)
                    qa_crew = Crew(agents=[qa_agent], tasks=[qa_task], process=Process.sequential)
                    critique = qa_crew.kickoff().raw
                    st.session_state.qa_critique = critique

                    session["conversation_state"] = "post_drafted"
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred. Please try again. Error: {e}")
                    session["conversation_state"] = "strategy_approved" # Revert state
                    session["selected_idea"] = None # Clear selected idea
                    st.session_state.qa_critique = ""
                    st.rerun()

        if session.get("draft"):
            # Post Preview and Actions
            st.subheader("Post Preview")
            st.markdown(f"""
                <div style="border:1px solid #ddd; border-radius:8px; padding:20px; background-color:#fafafa; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    {session['draft']}
                </div>
            """, unsafe_allow_html=True)
            
            copy_col, save_col, download_col = st.columns(3)
            with copy_col:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.code(session["draft"], language="text")
                    st.toast("Post copied! Use CTRL+C to paste.")
            with save_col:
                if st.button("💾 Save Draft", use_container_width=True):
                    session["draft_history"].append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "content": session["draft"]
                    })
                    st.success("Draft saved successfully!")
            with download_col:
                st.download_button("⬇️ Download as Text", 
                                    data=session["draft"], 
                                    file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d%H%M')}.txt",
                                    mime="text/plain",
                                    use_container_width=True)
            
            # Quality Check & Refinement Expander
            with st.expander("🛠️ Quality Check & Refinement", expanded=True):
                st.markdown("#### Agent Feedback")
                if st.session_state.qa_critique:
                    st.markdown(f"""
                        <div style="border:1px solid #ccc; border-radius:6px; padding:12px; background-color:#f9f9f9; font-style:italic;">
                            {st.session_state.qa_critique}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Show this message if the QA has been cleared or not run yet
                    st.info("The QA agent will provide feedback here after the draft is created or refined.")
                
                st.markdown("#### Refine with Your Own Feedback")
                feedback = st.text_area("✏️ What would you like to change?", height=100)
                
                if st.button("✨ Refine Draft", use_container_width=True):
                    if feedback:
                        with st.spinner("Refining draft based on your feedback..."):
                            writer_agent = agents.linkedin_ghostwriter_agent()
                            refine_task = tasks.refine_writing_task(writer_agent, session["draft"], feedback)
                            refine_crew = Crew(agents=[writer_agent], tasks=[refine_task], process=Process.sequential)
                            try:
                                new_draft = refine_crew.kickoff().raw
                                session["draft"] = new_draft
                                st.session_state.qa_critique = "" # Clear critique
                                st.success("Draft refined!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to refine draft. Please try again. Error: {e}")
                    else:
                        st.error("Please provide feedback before refining.")

            # Saved Drafts History
            with st.expander("📜 Saved Drafts History"):
                if session.get("draft_history"):
                    for i, draft_entry in enumerate(reversed(session["draft_history"])):
                        display_index = len(session['draft_history']) - i
                        st.markdown(f"**Draft {display_index}** saved at `{draft_entry['timestamp']}`")
                        
                        hist_col1, hist_col2 = st.columns([0.8, 0.2])
                        with hist_col1:
                            with st.expander("View Content"):
                                st.markdown(draft_entry['content'])
                        with hist_col2:
                            if st.button("↩️ Restore", key=f"restore_{display_index}"):
                                session["draft"] = draft_entry["content"]
                                st.session_state.qa_critique = ""
                                st.success("Draft restored!")
                                st.rerun()
                else:
                    st.info("No drafts have been saved yet. Click the 'Save Draft' button to create a history.")
        else:
            st.info("💡 Select an idea from the 'Post Ideas' tab to start writing.")