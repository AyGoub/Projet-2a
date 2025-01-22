import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objs as go
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title='Instagram Activity Analysis', layout="wide")
st.title('Instagram Activity Analysis')

# Fonctions de traitement
def process_liked_posts(data):
    likes = []
    if 'likes_media_likes' in data:  # La clé était incorrecte
        for like in data['likes_media_likes']:
            if 'string_list_data' in like:  # Il faut vérifier string_list_data
                string_data = like['string_list_data'][0]
                # Le timestamp est dans string_data
                timestamp = datetime.fromtimestamp(string_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                likes.append({
                    'timestamp': timestamp,
                    'username': like.get('title', ''),  # Le titre contient le nom d'utilisateur
                    'link': string_data.get('href', '')  # L'URL est dans href
                })
    return pd.DataFrame(likes)

def process_liked_comments(data):
    likes = []
    if 'likes_comment_likes' in data:  # La clé était incorrecte
        for like in data['likes_comment_likes']:
            if 'string_list_data' in like:  # Il faut vérifier string_list_data
                string_data = like['string_list_data'][0]
                # Le timestamp est dans string_data
                timestamp = datetime.fromtimestamp(string_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                likes.append({
                    'timestamp': timestamp,
                    'username': like.get('title', ''),  # Le titre contient le nom d'utilisateur
                    'link': string_data.get('href', '')  # L'URL est dans href
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
        
        st.plotly_chart(fig, use_container_width=True)

# Interface utilisateur
st.markdown("""
## Instagram Activity Analysis
Upload your Instagram activity files to analyze your engagement patterns.
""")

uploaded_files = st.file_uploader(
    "Upload Instagram activity files",
    type=['json'],
    accept_multiple_files=True
)

# PARTIE PRINCIPALE - Traitement des fichiers
activity_data = {
    'liked_posts': None,
    'liked_comments': None,
    'post_comments': None,
    'reels_comments': None
}

if uploaded_files:
    for file in uploaded_files:
        try:
            content = json.loads(file.getvalue().decode('utf-8'))
            
            if 'liked_posts' in file.name:
                activity_data['liked_posts'] = process_liked_posts(content)
                st.write(f"Debug liked_posts:")
                st.write(content.keys())  # voir les clés du fichier JSON
                st.write(activity_data['liked_posts'].shape)  # voir la taille du DataFrame
                if not activity_data['liked_posts'].empty:
                    st.write(activity_data['liked_posts'].head())
                    
            elif 'liked_comments' in file.name:
                activity_data['liked_comments'] = process_liked_comments(content)
                st.write(f"Debug liked_comments:")
                st.write(content.keys())
                st.write(activity_data['liked_comments'].shape)
                if not activity_data['liked_comments'].empty:
                    st.write(activity_data['liked_comments'].head())
                    
            elif 'post_comments' in file.name:
                activity_data['post_comments'] = process_comments(content, 'post')
            elif 'reels_comments' in file.name:
                activity_data['reels_comments'] = process_comments(content, 'reel')
                
            st.write(f"Processed {file.name} successfully")
            
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
            st.write("Error details:", str(e))
            continue

    # PARTIE AFFICHAGE - Visualisation des résultats
    if any(v is not None and not v.empty for v in activity_data.values()):
        st.header("Activity Overview")
        
        cols = st.columns(4)
        metrics = {
            'Posts Liked': activity_data['liked_posts'],
            'Comments Liked': activity_data['liked_comments'],
            'Comments on Posts': activity_data['post_comments'],
            'Comments on Reels': activity_data['reels_comments']
        }
        
        for i, (label, data) in enumerate(metrics.items()):
            with cols[i]:
                if data is not None and not data.empty:
                    st.metric(label, len(data))
                    recent_count = len(data[pd.to_datetime(data['timestamp']) > 
                                         pd.Timestamp.now() - pd.Timedelta(days=30)])
                    st.caption(f"Last 30 days: {recent_count}")

        st.header("Activity Timelines")
        tabs = st.tabs(["Posts", "Comments", "Reels"])
        
        with tabs[0]:
            if activity_data['liked_posts'] is not None and not activity_data['liked_posts'].empty:
                st.subheader("Posts Liked Over Time")
                plot_activity_timeline(activity_data['liked_posts'], "Posts Liked")
                
                with st.expander("View Details"):
                    st.dataframe(
                        activity_data['liked_posts']
                        .sort_values('timestamp', ascending=False)
                        .head(100)
                    )
        
        with tabs[1]:
            if activity_data['post_comments'] is not None and not activity_data['post_comments'].empty:
                st.subheader("Comments Activity")
                plot_activity_timeline(activity_data['post_comments'], "Comments on Posts")
                
                if 'comment' in activity_data['post_comments'].columns:
                    comments_sample = activity_data['post_comments'].head(1000)
                    st.subheader("Recent Comments")
                    st.dataframe(
                        comments_sample[['timestamp', 'comment']]
                        .sort_values('timestamp', ascending=False)
                    )
        
        with tabs[2]:
            if activity_data['reels_comments'] is not None and not activity_data['reels_comments'].empty:
                st.subheader("Reels Activity")
                plot_activity_timeline(activity_data['reels_comments'], "Comments on Reels")
                
                with st.expander("View Reels Comments"):
                    st.dataframe(
                        activity_data['reels_comments']
                        .sort_values('timestamp', ascending=False)
                        .head(100)
                    )

        st.header("Daily Activity Patterns")
        for activity_type, df in activity_data.items():
            if df is not None and not df.empty:
                df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
                hourly_activity = df.groupby('hour').size().reset_index(name='count')
                
                fig = px.bar(
                    hourly_activity, 
                    x='hour', 
                    y='count',
                    title=f'{activity_type.replace("_", " ").title()} by Hour of Day',
                    labels={'hour': 'Hour of Day', 'count': 'Number of Interactions'},
                    template="plotly_dark"
                )
                
                fig.update_layout(
                    height=400,
                    bargap=0.2
                )
                
                st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload your Instagram activity files to see the analysis.")