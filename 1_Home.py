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
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
with st.container():
    st.markdown("""
    <div class="hero-section">
        <h1>Stand Out on LinkedIn. Build Your Personal Brand with AI.</h1>
        <p>Ascent AI turns your career story—and your career ambitions—into content that gets noticed. Share posts that reflect who you are and who you’re becoming, so you can join the right conversations and be seen as a thought leader in your field.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 Try Ascent AI Free", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Ascent_AI_App.py")

# --- Why It Matters Section ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("Your Resume Opens Doors. Your Content Builds Influence.")
    st.markdown("""
    On LinkedIn, your profile shows what you’ve done. Your posts show how you think, where you’re headed, and why you belong in the circles you aspire to.
    
    **Ascent AI helps you:**
    - Showcase expertise you already have.
    - Build credibility in the industries and roles you’re aiming for.
    - Join discussions that grow your visibility and influence.

    This isn’t about “faking it till you make it.” It’s about sharing your authentic perspective—with the consistency and clarity that thought leaders are known for.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- Features Section ---
with st.container():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("Why Ascent AI?")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✨ Content Strategist for LinkedIn")
        st.write("A personalized posting plan designed around your career goals.")
        st.subheader("✍️ Authentic Ghostwriter & Editor")
        st.write("Upload your resume and writing samples so Ascent AI learns your tone and writes in your voice.")
    with col2:
        st.subheader("💡 Engagement-Focused Ideas")
        st.write("AI generates hooks and topics tailored to spark meaningful discussion.")
        st.subheader("⚡ All-in-One Workflow")
        st.write("From strategy → ideas → posts, everything happens in one place.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- Final CTA Section ---
with st.container():
    st.markdown("""
    <div class="hero-section">
        <h2>Ready to Build Influence on LinkedIn?</h2>
        <p>Stop overthinking what to post. Let Ascent AI learn your voice, craft your strategy, and generate content that helps you stand out.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 Get Started Now", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Ascent_AI_App.py")