import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objs as go

def process_connections(data):
    users = []
    json_data = data
    
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
        return fig


def load_connections_data(tempFileManager):
    connections_data = {
        'followers': None,
        'following': None
    }

    try:
        followers_1_file = tempFileManager.load_json('followers_1.json')
        if followers_1_file:
            connections_data['followers'] = process_connections(followers_1_file)

        following_file = tempFileManager.load_json('following.json')
        if following_file:
            connections_data['following'] = process_connections(following_file['relationships_following'])
            
    except Exception as e:
        st.error(f"Error loading connections data following: {str(e)}")

    return connections_data

def run_connections_analysis():
    st.title('Instagram Connections Analysis')
    
    if "tempFileManager" in st.session_state:
        tempFileManager = st.session_state["tempFileManager"]
        
        connections_data = load_connections_data(tempFileManager)

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
                    fig = plot_connections_timeline(df, connection_type.capitalize())
                    st.plotly_chart(fig)
                    
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

# Ce bloc permet d'exécuter le module directement                        
if __name__ == "__main__":
    run_connections_analysis()