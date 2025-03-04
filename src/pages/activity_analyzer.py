import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objs as go
import plotly.express as px

def process_liked_posts(data):
    likes = []
    if 'likes_media_likes' in data:
        for like in data['likes_media_likes']:
            if 'string_list_data' in like:
                string_data = like['string_list_data'][0]
                timestamp = datetime.fromtimestamp(string_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                likes.append({
                    'timestamp': timestamp,
                    'username': like.get('title', ''),
                    'link': string_data.get('href', '')
                })
    return pd.DataFrame(likes)

def process_liked_comments(data):
    likes = []
    if 'likes_comment_likes' in data:
        for like in data['likes_comment_likes']:
            if 'string_list_data' in like:
                string_data = like['string_list_data'][0]
                timestamp = datetime.fromtimestamp(string_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                likes.append({
                    'timestamp': timestamp,
                    'username': like.get('title', ''),
                    'link': string_data.get('href', '')
                })
    return pd.DataFrame(likes)

def process_comments(data, comment_type='post'):
    comments = []
    if 'comments_media_comments' in data:
        for comment in data['comments_media_comments']:
            if isinstance(comment, dict) and 'string_list_data' in comment:
                string_data = comment['string_list_data'][0]
                timestamp = datetime.fromtimestamp(string_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                comments.append({
                    'timestamp': timestamp,
                    'comment': string_data.get('value', ''),
                    'link': string_data.get('href', ''),
                    'type': comment_type
                })
    return pd.DataFrame(comments)

def plot_activity_timeline(df, activity_type):
    if df is not None and not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=daily_counts['date'], 
                y=daily_counts['count'],
                mode='lines+markers',
                name=activity_type,
                line=dict(width=2),
                marker=dict(size=8)
            )
        )
        
        fig.update_layout(
            title=dict(
                text=f"{activity_type} Activity Over Time",
                x=0.5,
                y=0.95
            ),
            xaxis_title="Date",
            yaxis_title="Number of Interactions",
            showlegend=True,
            height=500,
            template="plotly_dark"
        )
        
        return fig
def plot_activity_by_hour(df, activity_type):
    """
    Crée un graphique montrant l'activité par heure de la journée et met en évidence
    les heures de faible activité.
    """
    if df is not None and not df.empty:
        # Conversion du timestamp en heure
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        hourly_activity = df.groupby('hour').size().reset_index(name='count')
        
        # Créer un dataframe complet avec toutes les heures (0-23)
        all_hours = pd.DataFrame({'hour': range(24)})
        hourly_activity = pd.merge(all_hours, hourly_activity, on='hour', how='left').fillna(0)
        
        # Trouver l'heure avec le minimum d'activité (non nulle)
        non_zero_min = hourly_activity[hourly_activity['count'] > 0]['count'].min()
        min_activity_hour = hourly_activity[hourly_activity['count'] == non_zero_min].iloc[0]
        
        # Créer un graphique avec des barres de couleurs différentes
        fig = go.Figure()
        
        # Ajouter les barres
        colors = ['rgba(64, 135, 206, 0.7)'] * 24  # Couleur bleue par défaut
        min_hour = min_activity_hour['hour']
        colors[int(min_hour)] = 'rgba(255, 87, 51, 0.9)'  # Couleur rouge pour le minimum
        
        fig.add_trace(go.Bar(
            x=hourly_activity['hour'],
            y=hourly_activity['count'],
            marker_color=colors,
            name=activity_type
        ))
        
        # Ajouter une annotation pour le minimum
        if non_zero_min > 0:
            fig.add_annotation(
                x=min_hour,
                y=min_activity_hour['count'],
                text=f"Minimum: {int(min_activity_hour['count'])} interactions à {int(min_hour)}h",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )
        
        fig.update_layout(
            title=f"Distribution Horaire - {activity_type}",
            xaxis_title="Heure de la journée",
            yaxis_title="Nombre d'interactions",
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1,
                tickfont=dict(size=12),
                range=[-0.5, 23.5]  # Assure que toutes les heures sont affichées
            ),
            template="plotly_dark",
            height=500
        )
        
        return fig
    return None

def run_activity_analysis():
    st.title('Instagram Activity Analysis')
    
    uploaded_files = st.file_uploader(
        "Upload Instagram activity files",
        type=['json'],
        accept_multiple_files=True
    )

    activity_data = {
        'liked_posts': None,
        'liked_comments': None,
        'post_comments': None,
        'reels_comments': None
    }

    if uploaded_files:
        # Traitement des fichiers d'abord
        for file in uploaded_files:
            try:
                content = json.loads(file.getvalue().decode('utf-8'))
                
                if 'liked_posts' in file.name:
                    activity_data['liked_posts'] = process_liked_posts(content)
                elif 'liked_comments' in file.name:
                    activity_data['liked_comments'] = process_liked_comments(content)
                elif 'post_comments' in file.name:
                    activity_data['post_comments'] = process_comments(content, 'post')
                elif 'reels_comments' in file.name:
                    activity_data['reels_comments'] = process_comments(content, 'reel')
                    
                st.write(f"Processed {file.name} successfully")
                
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                st.write("Error details:", str(e))
                continue

        # Puis vérification des données et affichage
        if any(v is not None and not v.empty for v in activity_data.values()):
            # Affichage des métriques et des graphiques existants...
            
            # Ajout de l'analyse horaire
            st.header("Analyse Horaire des Activités")
            st.markdown("""
            Cette section montre à quelles heures de la journée vous êtes le plus actif sur Instagram.
            L'heure avec le minimum d'activité est mise en évidence en rouge.
            """)
            
            activity_tabs = st.tabs(["Tous Types", "Posts", "Comments", "Reels"])
            
            # Onglet pour toutes les activités combinées
            with activity_tabs[0]:
                all_data = pd.concat([df for df in activity_data.values() if df is not None and not df.empty], ignore_index=True)
                if not all_data.empty:
                    fig = plot_activity_by_hour(all_data, "Toutes Activités")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Calcul des meilleures heures pour poster
                    st.subheader("Meilleures heures pour poster")
                    all_data['hour'] = pd.to_datetime(all_data['timestamp']).dt.hour
                    hourly_counts = all_data.groupby('hour').size().reset_index(name='count')
                    best_hours = hourly_counts.sort_values('count', ascending=False).head(3)
                    worst_hours = hourly_counts.sort_values('count').head(3)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("#### Heures de forte activité\n" + 
                                "\n".join([f"- **{hour}h**: {count} interactions" for hour, count in 
                                           zip(best_hours['hour'], best_hours['count'])]))
                    with col2:
                        st.warning("#### Heures de faible activité\n" + 
                                   "\n".join([f"- **{hour}h**: {count} interactions" for hour, count in 
                                             zip(worst_hours['hour'], worst_hours['count'])]))
            
            # Onglets pour chaque type d'activité
            activity_types = {
                1: ('liked_posts', 'Posts Liked'),
                2: ('liked_comments', 'Comments Liked'),
                3: ('post_comments', 'Post Comments')
            }
            
            for tab_idx, (data_key, display_name) in activity_types.items():
                with activity_tabs[tab_idx]:
                    if activity_data[data_key] is not None and not activity_data[data_key].empty:
                        fig = plot_activity_by_hour(activity_data[data_key], display_name)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info(f"Aucune donnée disponible pour {display_name}")


# Ce bloc permet d'exécuter le module directement
if __name__ == "__main__":
    run_activity_analysis()