import streamlit as st

st.set_page_config(
    page_title="Ascent AI - AI-Powered Personal Branding",
    page_icon="🚀",
    layout="wide"
)

# --- Custom CSS for styling ---
st.markdown("""
<style>
    .hero-section {
        padding: 4rem 2rem;
        text-align: center;
    }
    .hero-section h1 {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .hero-section p {
        font-size: 1.25rem;
        color: #4A5568;
        max-width: 600px;
        margin: 1rem auto;
    }
    .cta-button {
        display: inline-block;
        padding: 0.8rem 2rem;
        background-color: #4299E1;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 1rem;
    }
    .section {
        padding: 3rem 2rem;
    }
    .feature-card {
        background-color: #F7FAFC;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #E2E8F0;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    .feature-item {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .feature-item h3 {
        color: #1A202C;
    }
    .workflow-flow {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .flow-step {
        background-color: #E2E8F0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        white-space: nowrap;
    }
    .flow-arrow {
        font-size: 1.5rem;
        color: #4A5568;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
with st.container():
    st.markdown("""
    <div class="hero-section">
        <h1>Ascent AI: Your Co-Pilot for Professional Branding</h1>
        <p>Turn your career story into a powerful online presence. Ascent AI helps you share posts in your authentic voice, join the right conversations, and grow your influence as a thought leader on LinkedIn.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 Start Your Branding Journey", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Ascent_AI_App.py")

st.markdown("---")

# --- App Navigation & Workflow Section ---
with st.container():
    #st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("How It Works: Navigating the Workflow")
    st.markdown("""
    Ascent AI is structured around two main workflows, accessed via the sidebar. Each workflow guides you through a specific content creation process, using a sequence of tabs.
    """)
    
    # Strategic Branding Workflow
    st.subheader("📝 Strategic Branding Workflow")
    st.markdown("""
    This is a guided, multi-step process for building a long-term content strategy. This workflow uses the different tabs to help you define your professional brand, generate a detailed content strategy, brainstorm ideas from that strategy, and draft final posts.
    
    <div class="workflow-flow">
        <div class="flow-step">Start Brand Strategy button</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">📝 Brand Strategy tab</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">💡 Post Ideas tab</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">✍️ Final Post tab</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Ideas Workflow
    st.markdown("---")
    st.subheader("✨ Quick Ideas Workflow")
    st.markdown("""
    Using this on-demand workflow you can instantly generate single-post ideas or a 3-part series on any topic without a full strategy. The **Final Post** tab is always available to help you draft and refine your posts, regardless of the workflow you chose.
    
    <div class="workflow-flow">
        <div class="flow-step">Quick Ideas button</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">✨ Quick Ideas tab</div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">✍️ Final Post tab</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- Core Features Section ---
with st.container():
    #st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("Why Ascent AI Stands Out")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✨ Personalized Strategy & Ideas")
        st.write("We go beyond basic prompts. Our AI crafts a personalized posting plan designed around your unique career goals and professional background.")
    with col2:
        st.subheader("💡 Human-in-the-Loop Feedback")
        st.write("You are in control. Our interactive system allows you to critique and refine every AI-generated strategy, idea, or draft until it perfectly matches your vision.")
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("✍️ Authentic Voice Generation")
        st.write("Upload your resume and writing samples, and Ascent AI learns and writes in your authentic tone and style, ensuring every post truly reflects you.")
    with col4:
        st.subheader("⚡ A Complete AI Crew")
        st.write("Powered by a multi-agent CrewAI system, Ascent AI uses specialized agents for each task, from summarizing your resume to generating polished, ready-to-publish posts.")
        
    #st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- Final CTA Section ---
with st.container():
    st.markdown("""
    <div class="hero-section">
        <h2>Ready to Build Influence on LinkedIn?</h2>
        <p>Stop overthinking what to post. Let Ascent AI learn your voice, craft your strategy, and generate content that helps you stand out from the crowd.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 Get Started Now", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Ascent_AI_App.py")