import streamlit as st
import sys
import os
# Ajouter le répertoire parent au chemin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pages.connections_analyzer import run_connections_analysis
from src.pages.activity_analyzer import run_activity_analysis
from src.pages.preferences_analyzer import run_preferences_analysis
from src.pages.time_analyzer import run_time_analysis
from constants.file_paths import CONNECTIONS_FILES, ACTIVITY_FILES, PREFERENCES_FILES

# Configuration principale
st.set_page_config(page_title='Instagram Data Analyzer', layout="wide")

# Section d'importation commune
st.title("Instagram Data Analyzer")
with st.expander("Guide d'importation des fichiers", expanded=True):
    st.markdown("""
    ### Comment télécharger et importer vos données Instagram
    
    1. **Téléchargez vos données** : Allez dans vos paramètres Instagram → Confidentialité et sécurité → Télécharger vos données
    2. **Décompressez** le fichier ZIP que vous recevrez par email
    3. **Importez les fichiers** pertinents selon l'analyse que vous souhaitez faire :
       
    **Pour l'analyse des connexions** :
    - `followers_1.json` : Vos abonnés
    - `following.json` : Les comptes que vous suivez
    - `recently_unfollowed_accounts.json` : Comptes que vous avez cessé de suivre
    
    **Pour l'analyse d'activité** :
    - `liked_posts.json` : Les publications que vous avez aimées
    - `liked_comments.json` : Les commentaires que vous avez aimés
    - `post_comments_1.json` / `reels_comments.json` : Vos commentaires
    
    **Pour l'analyse des préférences** :
    - `recommended_topics.json` ou `your_topics.json` : Vos centres d'intérêt selon Instagram
    
    Naviguez entre les onglets pour analyser différentes facettes de vos données.
    """)




# Interface principale avec onglets (ajout de l'onglet Time Analysis)
tab1, tab2, tab3, tab4 = st.tabs(["Connections", "Activité", "Préférences", "Temps & FOCUS"])

# Chaque onglet correspond à un module différent
with tab1:
    run_connections_analysis()

with tab2:
    run_activity_analysis()

with tab3:
    run_preferences_analysis()

with tab4:
    # Utiliser les données chargées si disponibles
    instagram_data = None
    if 'instagram_data' in st.session_state:
        instagram_data = st.session_state.instagram_data
    
    run_time_analysis(instagram_data)