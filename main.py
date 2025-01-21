import streamlit as st

st.set_page_config(
    page_title="Instagram Data Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration du style CSS personnalisé
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 2rem;
}
.card {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem;
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<p class="main-header">Instagram Data Analyzer 📱</p>', unsafe_allow_html=True)

# Introduction
st.markdown("""
Welcome to Instagram Data Analyzer! This tool helps you analyze your Instagram data in detail.
To get started, download your Instagram data and use our different analysis tools.
""")

# Instructions pour obtenir les données
with st.expander("How to get your Instagram data"):
    st.markdown("""
    1. Go to Instagram Settings
    2. Click on 'Privacy and Security'
    3. Scroll to 'Data Download' and click 'Request Download'
    4. Choose JSON format
    5. Wait for the email with your data
    6. Upload the relevant files in each section of this analyzer
    """)

# Section principale avec les différentes analyses disponibles
st.header("Available Analyses")

# Utilisation de colonnes pour afficher les différentes options
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Connections Analysis")
    st.markdown("""
    Analyze your Instagram connections:
    - Followers count and history
    - Following patterns
    - Unfollowed accounts
    - Follow requests
    """)
    st.page_link("pages/1_connections.py", label="Go to Connections Analysis", icon="👥")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💬 Messages Analysis")
    st.markdown("""
    Analyze your direct messages:
    - Message frequency
    - Most active conversations
    - Media shared
    - Time patterns
    """)
    st.page_link("pages/4_messages.py", label="Go to Messages Analysis", icon="💬")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("❤️ Activity Analysis")
    st.markdown("""
    Analyze your Instagram activity:
    - Likes history
    - Comments analysis
    - Story interactions
    - Post engagement
    """)
    st.page_link("pages/2_activity.py", label="Go to Activity Analysis", icon="📈")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Preferences Analysis")
    st.markdown("""
    Analyze your Instagram preferences:
    - Account settings
    - Privacy settings
    - Notification preferences
    - Profile changes
    """)
    st.page_link("pages/5_preferences.py", label="Go to Preferences Analysis", icon="⚙️")
    st.markdown('</div>', unsafe_allow_html=True)

# Informations supplémentaires
st.sidebar.header("About")
st.sidebar.info("""
This tool is designed to help you understand your Instagram data better.
All analysis is done locally on your machine - no data is stored or sent anywhere.
""")

# Version et contact
st.sidebar.markdown("---")
st.sidebar.markdown("Version 1.0.0")