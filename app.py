import streamlit as st
import sys
import os
# Ajouter le répertoire parent au chemin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pages.connections_analyzer import run_connections_analysis
from src.pages.activity_analyzer import run_activity_analysis
from src.pages.preferences_analyzer import run_preferences_analysis

# Configuration principale
st.set_page_config(page_title='Instagram Data Analyzer', layout="wide")

# Interface principale avec onglets
tab1, tab2,tab3 = st.tabs(["Connections Analysis", "Activity Analysis","Preferences Analysis"])

# Chaque onglet correspond à un module différent
with tab1:
    run_connections_analysis()

with tab2:
    run_activity_analysis()

with tab3:
    run_preferences_analysis()