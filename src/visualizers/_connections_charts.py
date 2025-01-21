import plotly.graph_objs as go
import pandas as pd
import streamlit as st

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