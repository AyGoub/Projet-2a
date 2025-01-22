import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objs as go

st.set_page_config(page_title='Instagram Connections Analysis')
st.title('Instagram Connections Analysis')

# Fonction de traitement des followers/following directement dans le même fichier
def process_connections(data, connection_type):
    users = []
    json_data = data[connection_type]
    
    for item in json_data:
        user_data = item['string_list_data'][0]
        timestamp = datetime.fromtimestamp(user_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        users.append({
            'timestamp': timestamp,
            'username': user_data['value'],
            'profile_url': user_data['href']
        })
    return pd.DataFrame(users)

def plot_connections_timeline(df, connection_type):
    if df is not None and not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=daily_counts['date'], 
                      y=daily_counts['count'],
                      mode='lines+markers',
                      name=connection_type)
        )
        fig.update_layout(
            title=f"{connection_type} Over Time",
            xaxis_title="Date",
            yaxis_title="Count",
            showlegend=True
        )
        st.plotly_chart(fig)

uploaded_files = st.file_uploader(
    "Upload Instagram connections files (followers.json, following.json)",
    type=['json'],
    accept_multiple_files=True
)

if uploaded_files:
    connections_data = {
        'followers': None,
        'following': None
    }
    
    for file in uploaded_files:
        try:
            content = file.read()
            data = json.loads(content)
            
            if 'followers.json' in file.name:
                connections_data['followers'] = process_connections(data, 'relationships_followers')
            elif 'following.json' in file.name:
                connections_data['following'] = process_connections(data, 'relationships_following')
                
            file.seek(0)  # Reset file pointer
            
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
            continue

    # Affichage des statistiques
    if connections_data['followers'] is not None or connections_data['following'] is not None:
        st.header("Connections Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            if connections_data['followers'] is not None:
                st.metric("Total Followers", len(connections_data['followers']))
        with col2:
            if connections_data['following'] is not None:
                st.metric("Total Following", len(connections_data['following']))
        
        # Visualisations
        st.header("Connections Timeline")
        for connection_type, df in connections_data.items():
            if df is not None and not df.empty:
                plot_connections_timeline(df, connection_type.capitalize())
                
                with st.expander(f"View {connection_type.capitalize()} Details"):
                    st.dataframe(df)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        f"Download {connection_type} data",
                        csv,
                        f"instagram_{connection_type}.csv",
                        "text/csv",
                        key=f'download_{connection_type}'
                    )