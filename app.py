import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
import plotly.graph_objs as go
import os

st.set_page_config(page_title='Instagram Activity Analysis')
st.title('Instagram Activity Analysis')

def process_comments(data):
    if 'comments_media_comments' in data:
        comments = []
        for comment in data['comments_media_comments']:
            timestamp = datetime.fromtimestamp(comment['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            comments.append({
                'timestamp': timestamp,
                'text': comment.get('text', ''),
                'media_type': comment.get('media_type', '')
            })
        return pd.DataFrame(comments)
    return pd.DataFrame()

def process_likes(data):
    if 'liked_posts' in data:
        likes = []
        for like in data['liked_posts']:
            timestamp = datetime.fromtimestamp(like['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            likes.append({
                'timestamp': timestamp,
                'username': like.get('username', ''),
                'media_type': like.get('media_type', '')
            })
        return pd.DataFrame(likes)
    return pd.DataFrame()

def process_messages(data):
    if 'messages' in data:
        messages = []
        for msg in data['messages']:
            timestamp = datetime.fromtimestamp(msg['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            messages.append({
                'timestamp': timestamp,
                'sender': msg.get('sender', ''),
                'content': msg.get('content', '')
            })
        return pd.DataFrame(messages)
    return pd.DataFrame()

def process_stories(data):
    if 'story_activities' in data:
        stories = []
        for story in data['story_activities']:
            timestamp = datetime.fromtimestamp(story['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            stories.append({
                'timestamp': timestamp,
                'type': story.get('type', ''),
                'interaction': story.get('interaction', '')
            })
        return pd.DataFrame(stories)
    return pd.DataFrame()

def analyze_activity(uploaded_files):
    activity_data = {
        'comments': None,
        'likes': None,
        'messages': None,
        'stories': None,
        'shopping': None
    }

    for file in uploaded_files:
        try:
            content = file.read()
            data = json.loads(content)
            
            file_name = file.name.lower()
            
            if 'comments' in file_name:
                activity_data['comments'] = process_comments(data)
            elif 'likes' in file_name:
                activity_data['likes'] = process_likes(data)
            elif 'messages' in file_name:
                activity_data['messages'] = process_messages(data)
            elif 'story' in file_name:
                activity_data['stories'] = process_stories(data)
            
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
            continue

    return activity_data

def plot_activity_timeline(df, activity_type):
    if df is not None and not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=daily_counts['date'], 
                      y=daily_counts['count'],
                      mode='lines+markers',
                      name=activity_type)
        )
        
        fig.update_layout(
            title=f"{activity_type} Activity Over Time",
            xaxis_title="Date",
            yaxis_title="Count",
            showlegend=True
        )
        
        st.plotly_chart(fig)

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

if uploaded_files:
    activity_data = analyze_activity(uploaded_files)
    
    # Affichage des statistiques globales
    st.header("Activity Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if activity_data['comments'] is not None:
            st.metric("Total Comments", len(activity_data['comments']))
    with col2:
        if activity_data['likes'] is not None:
            st.metric("Total Likes", len(activity_data['likes']))
    with col3:
        if activity_data['messages'] is not None:
            st.metric("Total Messages", len(activity_data['messages']))
    with col4:
        if activity_data['stories'] is not None:
            st.metric("Total Story Interactions", len(activity_data['stories']))
    
    # Visualisations temporelles
    st.header("Activity Timelines")
    
    for activity_type, df in activity_data.items():
        if df is not None and not df.empty:
            plot_activity_timeline(df, activity_type.capitalize())
            
            # Affichage des données détaillées
            with st.expander(f"View {activity_type.capitalize()} Details"):
                st.dataframe(df)
                
                # Option de téléchargement
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    f"Download {activity_type} data",
                    csv,
                    f"instagram_{activity_type}.csv",
                    "text/csv",
                    key=f'download_{activity_type}'
                )

else:
    st.info("Please upload your Instagram activity JSON files to begin analysis.")