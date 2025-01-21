import streamlit as st
from src.utils.data_processors._connections_processor import analyze_connections
from utils.visualizers.connections_charts import plot_connections_timeline

st.set_page_config(page_title='Instagram Connections Analysis')
st.title('Instagram Connections Analysis')

st.markdown("""
## Instagram Connections Analysis
Upload your Instagram connections files to analyze your followers and following patterns.
""")

uploaded_files = st.file_uploader(
    "Upload Instagram connections files",
    type=['json'],
    accept_multiple_files=True
)

if uploaded_files:
    connections_data = analyze_connections(uploaded_files)
    
    # Affichage des statistiques globales
    st.header("Connections Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if connections_data['followers'] is not None:
            st.metric("Total Followers", len(connections_data['followers']))
    with col2:
        if connections_data['following'] is not None:
            st.metric("Total Following", len(connections_data['following']))
    with col3:
        if connections_data['unfollowed'] is not None:
            st.metric("Recent Unfollows", len(connections_data['unfollowed']))
    with col4:
        if connections_data['follow_requests'] is not None:
            st.metric("Follow Requests", len(connections_data['follow_requests']))
    
    # Visualisations temporelles
    st.header("Connections Timelines")
    
    for connection_type, df in connections_data.items():
        if df is not None and not df.empty:
            plot_connections_timeline(df, connection_type.capitalize())
            
            # Affichage des données détaillées
            with st.expander(f"View {connection_type.capitalize()} Details"):
                st.dataframe(df)
                
                # Option de téléchargement
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    f"Download {connection_type} data",
                    csv,
                    f"instagram_{connection_type}.csv",
                    "text/csv",
                    key=f'download_{connection_type}'
                )

else:
    st.info("Please upload your Instagram connections JSON files to begin analysis.")