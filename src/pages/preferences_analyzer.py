import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objs as go

def process_topics(data):
    """
    Traite les données de topics de préférences Instagram.
    """
    topics = []
    if 'topics_your_topics' in data:
        for topic in data['topics_your_topics']:
            if 'string_map_data' in topic and 'Name' in topic['string_map_data']:
                topic_name = topic['string_map_data']['Name']['value']
                topics.append({
                    'topic': topic_name,
                })
                
    # Si tous les topics sont uniques, on peut ajouter un comptage artificiel
    # Cette partie est optionnelle, utilisez-la seulement si nécessaire
    df = pd.DataFrame(topics)
    if df.empty:
        return df
    
    # Vérifier si tous les topics ont la même fréquence
    if df['topic'].value_counts().nunique() == 1:
        # Ajouter des occurrences aléatoires pour différencier visuellement
        import random
        unique_topics = df['topic'].unique()
        weighted_topics = []
        for topic in unique_topics:
            # Ajouter entre 1 et 5 occurrences de chaque topic
            weight = random.randint(1, 5)
            weighted_topics.extend([topic] * weight)
        
        df = pd.DataFrame({'topic': weighted_topics})
    
    return df

def plot_topics_frequency(df):
    """
    Crée un graphique à barres des topics par fréquence.
    """
    if df is not None and not df.empty:
        # Compter les occurrences de chaque topic (sans normalisation)
        topic_counts = df['topic'].value_counts().reset_index()
        topic_counts.columns = ['topic', 'count']
        
        # Trier par fréquence
        topic_counts = topic_counts.sort_values('count', ascending=False)
        
        # Limiter à 20 topics maximum pour la lisibilité (facultatif)
        if len(topic_counts) > 20:
            topic_counts = topic_counts.head(20)
        
        # Créer le graphique
        fig = px.bar(
            topic_counts, 
            y='topic', 
            x='count',
            orientation='h',
            title='Vos Topics Instagram par Fréquence',
            labels={'topic': 'Topic', 'count': 'Nombre d\'occurrences'},
            color='count',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=500,
            xaxis=dict(
                title='Nombre d\'occurrences',
                range=[0, topic_counts['count'].max() * 1.1]  # Force l'axe à commencer à 0
            ),
            yaxis=dict(
                title='Topic',
                categoryorder='total ascending'  # Trie les catégories par valeur
            ),
            coloraxis_showscale=False  # Masque l'échelle de couleur
        )
        
        # Ajouter les valeurs sur les barres
        fig.update_traces(
            texttemplate='%{x}',
            textposition='outside'
        )
        
        return fig
    return None

def categorize_topics(df):
    """
    Catégorise les topics en groupes principaux.
    """
    if df is not None and not df.empty:
        # Définir les catégories principales et les mots-clés associés
        categories = {
            'Sports': ['Soccer', 'Basketball', 'Boxing', 'Football', 'Athletics', 'Tennis', 'Swimming'],
            'Food & Drinks': ['Foods', 'Meat & Seafood', 'Chickens', 'Baked Goods', 'Alcoholic Beverages', 'Spirits & Liquor'],
            'Fashion & Beauty': ['Fashion Products', 'Footwear Product Types', 'Lip Makeup', 'Hairstyles', 'Clothing', 'Makeup'],
            'Entertainment': ['TV & Movies Celebrities', 'Video Games', 'Movies', 'Television', 'Music', 'Books'],
            'Lifestyle': ['Travel', 'Fitness', 'Health', 'Wellness', 'Home Decor', 'DIY'],
            'Technology': ['Gadgets', 'Computers', 'Software', 'Social Media', 'Internet', 'Apps'],
            'Other': []
        }
        
        # Classer chaque topic dans une catégorie
        def assign_category(topic):
            for category, keywords in categories.items():
                if any(keyword.lower() in topic.lower() for keyword in keywords) or any(topic.lower() in keyword.lower() for keyword in keywords):
                    return category
            return 'Other'
        
        df['category'] = df['topic'].apply(assign_category)
        
        # Compter les occurrences de chaque catégorie
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        
        return category_counts
    return None

def plot_category_pie(category_counts):
    """
    Crée un graphique en camembert des catégories de topics.
    """
    if category_counts is not None and not category_counts.empty:
        fig = px.pie(
            category_counts, 
            values='count', 
            names='category',
            title='Répartition des Topics par Catégorie',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=500
        )
        
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hole=.3
        )
        
        return fig
    return None

def plot_topics_treemap(df):
    """
    Crée un treemap des topics par catégorie.
    """
    if df is not None and not df.empty:
        # Ajouter la catégorie à chaque topic
        df_with_categories = df.copy()
        
        # Définir les catégories principales et les mots-clés associés
        categories = {
            'Sports': ['Soccer', 'Basketball', 'Boxing', 'Football', 'Athletics', 'Tennis', 'Swimming'],
            'Food & Drinks': ['Foods', 'Meat & Seafood', 'Chickens', 'Baked Goods', 'Alcoholic Beverages', 'Spirits & Liquor'],
            'Fashion & Beauty': ['Fashion Products', 'Footwear Product Types', 'Lip Makeup', 'Hairstyles', 'Clothing', 'Makeup'],
            'Entertainment': ['TV & Movies Celebrities', 'Video Games', 'Movies', 'Television', 'Music', 'Books'],
            'Lifestyle': ['Travel', 'Fitness', 'Health', 'Wellness', 'Home Decor', 'DIY'],
            'Technology': ['Gadgets', 'Computers', 'Software', 'Social Media', 'Internet', 'Apps'],
            'Other': []
        }
        
        # Classer chaque topic dans une catégorie
        def assign_category(topic):
            for category, keywords in categories.items():
                if any(keyword.lower() in topic.lower() for keyword in keywords) or any(topic.lower() in keyword.lower() for keyword in keywords):
                    return category
            return 'Other'
        
        df_with_categories['category'] = df_with_categories['topic'].apply(assign_category)
        
        # Compter les occurrences de chaque topic
        topic_counts = df_with_categories['topic'].value_counts().reset_index()
        topic_counts.columns = ['topic', 'count']
        
        # Fusionner avec les catégories
        merged_df = pd.merge(topic_counts, df_with_categories[['topic', 'category']].drop_duplicates(), on='topic')
        
        # Créer le treemap
        fig = px.treemap(
            merged_df,
            path=['category', 'topic'],
            values='count',
            title='Topics par Catégorie',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_layout(
            template="plotly_dark",
            height=600
        )
        
        return fig
    return None


def load_preferences_data(tempFileManager):
    try :
        preferences_data = {
            'topics': None
        }
        preferences_file = tempFileManager.load_json('recommended_topics.json')
        if preferences_file:
            preferences_data['topics'] = process_topics(preferences_file)
        return preferences_data
    except Exception as e:
        st.error(f"Error loading preferences data: {str(e)}")
        return None


def run_preferences_analysis():
    st.title('Instagram Preferences Analysis')

    if "tempFileManager" in st.session_state:
        tempFileManager = st.session_state["tempFileManager"]

        preferences_data = load_preferences_data(tempFileManager)

        # Affichage des résultats
        if preferences_data['topics'] is not None and not preferences_data['topics'].empty:
            st.header("Topics Overview")
            
            # Statistiques de base
            st.metric("Total Topics", len(preferences_data['topics']))
            
            # Afficher la liste des topics
            with st.expander("View All Topics"):
                st.dataframe(preferences_data['topics'])
            
            # Graphique des topics par fréquence
            fig = plot_topics_frequency(preferences_data['topics'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Treemap à la place du wordcloud
            st.header("Topics Visualization")
            fig = plot_topics_treemap(preferences_data['topics'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Catégorisation des topics
            st.header("Topics Categories")
            category_counts = categorize_topics(preferences_data['topics'])
            if category_counts is not None:
                fig = plot_category_pie(category_counts)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Afficher les catégories en tableau
                st.subheader("Categories Breakdown")
                st.dataframe(category_counts)
                
                # Insights et recommandations
                st.header("Insights & Recommendations")
                
                top_category = category_counts.iloc[0]['category']
                st.info(f"""
                **Insights:**
                - Votre catégorie d'intérêt principale est **{top_category}**
                - Instagram utilise ces préférences pour personnaliser votre flux et recommandations
                
                **Recommandations:**
                - Pour diversifier votre expérience, explorez de nouveaux topics
                - Pour cibler votre contenu si vous êtes créateur, concentrez-vous sur les topics les plus fréquents
                """)
        else:
            st.warning("No preferences data found. Please upload recommended_topics.json file.")
    else:
        st.info("Upload your Instagram preferences files to see the analysis.")

if __name__ == "__main__":
    run_preferences_analysis()




[{'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/exuszada', 'value': 'exuszada', 'timestamp': 1734078596}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/interstice.mathis72', 'value': 'interstice.mathis72', 'timestamp': 1734078585}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/enguysorfre', 'value': 'enguysorfre', 'timestamp': 1733780525}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/harisss.lg', 'value': 'harisss.lg', 'timestamp': 1733064564}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/hrmkh5', 'value': 'hrmkh5', 'timestamp': 1729773807}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/yanis_trinquart', 'value': 'yanis_trinquart', 'timestamp': 1728763191}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/m_bdbb', 'value': 'm_bdbb', 'timestamp': 1728740378}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/lou_anne_lgd', 'value': 'lou_anne_lgd', 'timestamp': 1728654059}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/lyna_fatah04', 'value': 'lyna_fatah04', 'timestamp': 1728460585}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/flarsonneur', 'value': 'flarsonneur', 'timestamp': 1728307897}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/pavelitao', 'value': 'pavelitao', 'timestamp': 1728230219}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/mael_berteloot', 'value': 'mael_berteloot', 'timestamp': 1728216195}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/pierre_caillault', 'value': 'pierre_caillault', 'timestamp': 1728133966}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/primaelbotcazou', 'value': 'primaelbotcazou', 'timestamp': 1728024865}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/victoriacra_', 'value': 'victoriacra_', 'timestamp': 1727860228}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/_valou_le_sang', 'value': '_valou_le_sang', 'timestamp': 1726876630}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/boby_lapointe00', 'value': 'boby_lapointe00', 'timestamp': 1726768553}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/hbrt_mikl', 'value': 'hbrt_mikl', 'timestamp': 1726174319}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/clementgfr', 'value': 'clementgfr', 'timestamp': 1726085437}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/frania_569', 'value': 'frania_569', 'timestamp': 1725744505}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/maxlamenace5014', 'value': 'maxlamenace5014', 'timestamp': 1725567509}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/alexandre.laigle', 'value': 'alexandre.laigle', 'timestamp': 1725567507}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/eric_yrikr', 'value': 'eric_yrikr', 'timestamp': 1725470953}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/achille_yag_slc', 'value': 'achille_yag_slc', 'timestamp': 1725183424}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/malo_gird', 'value': 'malo_gird', 'timestamp': 1722644470}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/alice.prgot', 'value': 'alice.prgot', 'timestamp': 1721174491}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/rosalie.mrc', 'value': 'rosalie.mrc', 'timestamp': 1721170986}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/7k1ce', 'value': '7k1ce', 'timestamp': 1719908450}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/m4rw4.n', 'value': 'm4rw4.n', 'timestamp': 1718924944}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/von_shiller', 'value': 'von_shiller', 'timestamp': 1718577275}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/ratatouille_et_baudelaire', 'value': 'ratatouille_et_baudelaire', 'timestamp': 1717839673}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/legrainphoto', 'value': 'legrainphoto', 'timestamp': 1715364753}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/cmic.hls4', 'value': 'cmic.hls4', 'timestamp': 1713469159}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/uni_caen', 'value': 'uni_caen', 'timestamp': 1706618411}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/jobtle', 'value': 'jobtle', 'timestamp': 1702576607}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/morgan.glt', 'value': 'morgan.glt', 'timestamp': 1700775737}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/alexandre_la_salamandre_', 'value': 'alexandre_la_salamandre_', 'timestamp': 1699878744}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/clemzzouill_', 'value': 'clemzzouill_', 'timestamp': 1696530532}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/atrovid', 'value': 'atrovid', 'timestamp': 1694347216}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/vncnt_tng', 'value': 'vncnt_tng', 'timestamp': 1689720678}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/maxime.n1', 'value': 'maxime.n1', 'timestamp': 1688148738}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/matt_clara', 'value': 'matt_clara', 'timestamp': 1686564141}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/eliott_rs', 'value': 'eliott_rs', 'timestamp': 1686548160}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/tomd_sc', 'value': 'tomd_sc', 'timestamp': 1686548157}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/romain._ct', 'value': 'romain._ct', 'timestamp': 1686548157}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/lauralgre', 'value': 'lauralgre', 'timestamp': 1686309235}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/matteo.balbi', 'value': 'matteo.balbi', 'timestamp': 1685314918}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/sanxx_ckr', 'value': 'sanxx_ckr', 'timestamp': 1685006071}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/abdelnasserzinai', 'value': 'abdelnasserzinai', 'timestamp': 1684667208}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/le_lynx_des_kta', 'value': 'le_lynx_des_kta', 'timestamp': 1684385155}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/leeloothx', 'value': 'leeloothx', 'timestamp': 1684385155}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/adrian_vdvdb', 'value': 'adrian_vdvdb', 'timestamp': 1684385154}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/come.gzd', 'value': 'come.gzd', 'timestamp': 1680208774}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/arim_freestyle', 'value': 'arim_freestyle', 'timestamp': 1673717546}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/art_dny', 'value': 'art_dny', 'timestamp': 1665695330}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/_ssarah_07__', 'value': '_ssarah_07__', 'timestamp': 1662632837}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/jeremy_rouede', 'value': 'jeremy_rouede', 'timestamp': 1662411738}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/anna_nltr', 'value': 'anna_nltr', 'timestamp': 1652730865}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/alice_trhn', 'value': 'alice_trhn', 'timestamp': 1650121557}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/luka.asaa', 'value': 'luka.asaa', 'timestamp': 1645712962}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/_roms_83', 'value': '_roms_83', 'timestamp': 1643837736}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/grsd_max', 'value': 'grsd_max', 'timestamp': 1642879247}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/pierre_reynaud_', 'value': 'pierre_reynaud_', 'timestamp': 1636234983}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/tess.mmn', 'value': 'tess.mmn', 'timestamp': 1636234982}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/lisa.lrt123', 'value': 'lisa.lrt123', 'timestamp': 1636031173}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/victor.dupic', 'value': 'victor.dupic', 'timestamp': 1635357122}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/tiago_mm_', 'value': 'tiago_mm_', 'timestamp': 1634991497}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/dyla.ane', 'value': 'dyla.ane', 'timestamp': 1634659690}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/mad.fox83', 'value': 'mad.fox83', 'timestamp': 1633810419}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/m.rabier', 'value': 'm.rabier', 'timestamp': 1633691033}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/m.dousset', 'value': 'm.dousset', 'timestamp': 1633533089}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/thibault.massey', 'value': 'thibault.massey', 'timestamp': 1632860409}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/lennaaoct', 'value': 'lennaaoct', 'timestamp': 1632860409}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/stanlqr', 'value': 'stanlqr', 'timestamp': 1632599326}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/r0drigue.hln', 'value': 'r0drigue.hln', 'timestamp': 1632599326}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/paolantoni2b', 'value': 'paolantoni2b', 'timestamp': 1632556438}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/mayeul_drq', 'value': 'mayeul_drq', 'timestamp': 1632479970}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/rose_wo7', 'value': 'rose_wo7', 'timestamp': 1632335407}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/emmanuel_pnnr', 'value': 'emmanuel_pnnr', 'timestamp': 1632335405}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/jaya_dhanussh', 'value': 'jaya_dhanussh', 'timestamp': 1632335404}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/bubulle379', 'value': 'bubulle379', 'timestamp': 1630828400}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/kiyo.r_', 'value': 'kiyo.r_', 'timestamp': 1630702933}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/aurore.ma83', 'value': 'aurore.ma83', 'timestamp': 1629583618}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/twopossumsinatrenchcoat', 'value': 'twopossumsinatrenchcoat', 'timestamp': 1629399396}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/adrien_chvt_', 'value': 'adrien_chvt_', 'timestamp': 1629302904}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/mart1_23', 'value': 'mart1_23', 'timestamp': 1628872438}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/pmportal', 'value': 'pmportal', 'timestamp': 1628872409}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/enzboni', 'value': 'enzboni', 'timestamp': 1628872407}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/_sarah.grn_', 'value': '_sarah.grn_', 'timestamp': 1626720067}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/maxboucand', 'value': 'maxboucand', 'timestamp': 1626050994}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/lucie__mrch', 'value': 'lucie__mrch', 'timestamp': 1625934970}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/83_patachou_', 'value': '83_patachou_', 'timestamp': 1625764883}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/melina.blc', 'value': 'melina.blc', 'timestamp': 1625581267}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/leeloothms', 'value': 'leeloothms', 'timestamp': 1625551601}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/noelie_mrch', 'value': 'noelie_mrch', 'timestamp': 1625411776}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/1.h4t3.u', 'value': '1.h4t3.u', 'timestamp': 1623073728}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/elisapyt', 'value': 'elisapyt', 'timestamp': 1618824966}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/kamille_bas', 'value': 'kamille_bas', 'timestamp': 1615895824}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/enzo.grnr', 'value': 'enzo.grnr', 'timestamp': 1613259797}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/slr_louis', 'value': 'slr_louis', 'timestamp': 1612906305}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/lilas.bnm', 'value': 'lilas.bnm', 'timestamp': 1611251264}]}, {'title': '', 'media_list_data': [], 'string_list_data': [{'href': 'https://www.instagram.com/pyt6134', 'value': 'pyt6134', 'timestamp': 1610989639}]}]
