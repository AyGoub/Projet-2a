import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta
import numpy as np
import random
from dateutil import parser

def process_time_data(data_dict):
    """
    Analyse le temps passé sur Instagram à partir des différentes activités.
    Combine les timestamps de toutes les activités pour estimer l'utilisation.
    """
    all_timestamps = []
    
    # Extraire les timestamps de connections
    for key, df in data_dict.get('connections', {}).items():
        if df is not None and not df.empty and 'timestamp' in df.columns:
            all_timestamps.extend(pd.to_datetime(df['timestamp']).tolist())
    
    # Extraire les timestamps d'activité
    for key, df in data_dict.get('activity', {}).items():
        if df is not None and not df.empty and 'timestamp' in df.columns:
            all_timestamps.extend(pd.to_datetime(df['timestamp']).tolist())
    
    # Si nous n'avons pas assez de données, on ne peut pas procéder
    if len(all_timestamps) < 10:
        return None
    
    # Convertir en DataFrame
    time_df = pd.DataFrame({'timestamp': all_timestamps})
    time_df.sort_values('timestamp', inplace=True)
    
    # Extraire des informations temporelles
    time_df['date'] = time_df['timestamp'].dt.date
    time_df['hour'] = time_df['timestamp'].dt.hour
    time_df['day_of_week'] = time_df['timestamp'].dt.day_name()
    time_df['month'] = time_df['timestamp'].dt.month_name()
    time_df['year'] = time_df['timestamp'].dt.year
    time_df['week'] = time_df['timestamp'].dt.isocalendar().week
    
    # Estimer les sessions (une session est définie comme une série d'actions 
    # avec moins de 30 minutes entre chaque action)
    time_df['time_diff'] = time_df['timestamp'].diff().dt.total_seconds().fillna(0)
    time_df['new_session'] = time_df['time_diff'] > 1800  # 30 minutes en secondes
    time_df['session_id'] = time_df['new_session'].cumsum()
    
    # Calculer la durée estimée des sessions
    session_durations = []
    for session_id, group in time_df.groupby('session_id'):
        if len(group) > 1:
            # La durée est la différence entre le premier et le dernier timestamp
            # plus une durée moyenne estimée pour la dernière action (5 minutes)
            duration = (group['timestamp'].max() - group['timestamp'].min()).total_seconds() + 300
        else:
            # S'il n'y a qu'une seule action, on estime à 5 minutes
            duration = 300
        
        for _ in range(len(group)):
            session_durations.append(duration)
    
    time_df['session_duration'] = session_durations
    
    # Enrichir avec des thématiques si on a des données de préférences
    if 'preferences' in data_dict and 'topics' in data_dict['preferences'] and data_dict['preferences']['topics'] is not None:
        topics_df = data_dict['preferences']['topics']
        if not topics_df.empty and 'topic' in topics_df.columns:
            topics = topics_df['topic'].unique().tolist()
            
            # Assigner aléatoirement des thématiques aux sessions pour la démonstration
            # Dans une vraie implémentation, ces liens seraient basés sur l'analyse du contenu
            time_df['theme'] = time_df['session_id'].apply(lambda x: random.choice(topics))
    
    return time_df

def load_example_time_data():
    """
    Génère des données d'exemple pour l'analyse du temps passé sur Instagram.
    """
    # Période sur 6 mois
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Générer ~500 points de données
    timestamps = []
    for _ in range(500):
        # Date aléatoire dans la période
        random_days = random.randint(0, 180)
        random_time = start_date + timedelta(
            days=random_days,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        timestamps.append(random_time)
    
    # Plus d'activité le soir et weekend
    for _ in range(300):
        # Date aléatoire weekend
        random_days = random.randint(0, 25) * 7 + random.choice([5, 6])  # Samedi ou dimanche
        random_time = start_date + timedelta(
            days=random_days,
            hours=random.randint(18, 23),  # Soirée
            minutes=random.randint(0, 59)
        )
        timestamps.append(random_time)
    
    # Créer un DataFrame
    time_df = pd.DataFrame({'timestamp': timestamps})
    time_df.sort_values('timestamp', inplace=True)
    
    # Extraire des informations temporelles
    time_df['date'] = time_df['timestamp'].dt.date
    time_df['hour'] = time_df['timestamp'].dt.hour
    time_df['day_of_week'] = time_df['timestamp'].dt.day_name()
    time_df['month'] = time_df['timestamp'].dt.month_name()
    time_df['year'] = time_df['timestamp'].dt.year
    time_df['week'] = time_df['timestamp'].dt.isocalendar().week
    
    # Définir les sessions
    time_df['time_diff'] = time_df['timestamp'].diff().dt.total_seconds().fillna(0)
    time_df['new_session'] = time_df['time_diff'] > 1800  # 30 minutes
    time_df['session_id'] = time_df['new_session'].cumsum()
    
    # Durées de session
    session_durations = []
    for session_id, group in time_df.groupby('session_id'):
        if len(group) > 1:
            # Calculer durée réelle + 5 min pour la dernière action
            duration = (group['timestamp'].max() - group['timestamp'].min()).total_seconds() + 300
        else:
            duration = 300  # 5 minutes par défaut
        
        for _ in range(len(group)):
            session_durations.append(duration)
    
    time_df['session_duration'] = session_durations
    
    # Thématiques fictives
    themes = ['Sports', 'Food', 'Fashion', 'Travel', 'Technology', 'Entertainment', 'Art', 'Music']
    time_df['theme'] = time_df['session_id'].apply(lambda x: themes[int(x) % len(themes)])
    
    return time_df

def plot_time_heatmap(df):
    """
    Crée une heatmap du temps passé par heure et jour de la semaine.
    """
    # Grouper par jour et heure
    heatmap_data = df.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
    
    # Créer un pivot pour le format heatmap
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pd.pivot_table(
        heatmap_data, 
        values='count', 
        index='day_of_week',
        columns='hour', 
        fill_value=0
    )
    
    # Réordonner les jours correctement
    pivot_data = pivot_data.reindex(days_order)
    
    # Créer la heatmap
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Heure de la journée", y="Jour de la semaine", color="Activité"),
        x=pivot_data.columns,
        y=pivot_data.index,
        color_continuous_scale="viridis",
        aspect="auto"
    )
    
    fig.update_layout(
        title="Heatmap d'activité par jour et heure",
        xaxis_title="Heure de la journée",
        yaxis_title="Jour de la semaine",
        height=500,
        template="plotly_dark"
    )
    
    return fig

def plot_daily_sessions(df):
    """
    Trace le nombre et la durée des sessions par jour.
    """
    # Agréger par date
    daily_data = df.groupby('date').agg({
        'session_id': 'nunique',
        'session_duration': 'mean'
    }).reset_index()
    
    daily_data.columns = ['date', 'nb_sessions', 'avg_duration']
    daily_data['avg_duration_min'] = daily_data['avg_duration'] / 60  # Convertir en minutes
    
    # Créer le graphique à deux axes
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=daily_data['date'],
        y=daily_data['nb_sessions'],
        name="Nombre de sessions",
        marker_color='rgba(55, 83, 109, 0.7)',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_data['date'],
        y=daily_data['avg_duration_min'],
        name="Durée moyenne (min)",
        marker_color='rgba(255, 182, 77, 1)',
        mode='lines+markers',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Nombre et durée des sessions par jour",
        xaxis=dict(title="Date"),
        yaxis=dict(
            title="Nombre de sessions",
            titlefont=dict(color="rgba(55, 83, 109, 1)"),
            tickfont=dict(color="rgba(55, 83, 109, 1)")
        ),
        yaxis2=dict(
            title="Durée moyenne (min)",
            titlefont=dict(color="rgba(255, 182, 77, 1)"),
            tickfont=dict(color="rgba(255, 182, 77, 1)"),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        height=500,
        template="plotly_dark",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def plot_theme_distribution(df):
    """
    Crée un graphique de la distribution des thématiques au fil du temps.
    """
    if 'theme' not in df.columns:
        return None
    
    # Agréger par semaine et thème
    weekly_themes = df.groupby(['year', 'week', 'theme']).size().reset_index(name='count')
    weekly_themes['year_week'] = weekly_themes['year'].astype(str) + '-W' + weekly_themes['week'].astype(str)
    
    # Créer le graphique
    fig = px.area(
        weekly_themes, 
        x='year_week', 
        y='count', 
        color='theme',
        title="Distribution des thématiques au fil du temps",
        labels={'year_week': 'Semaine', 'count': 'Activité', 'theme': 'Thématique'},
    )
    
    fig.update_layout(
        xaxis_title="Semaine",
        yaxis_title="Niveau d'activité",
        height=500,
        template="plotly_dark"
    )
    
    return fig

def run_time_analysis(instagram_data=None):
    st.title("Analyse du Temps sur Instagram")
    
    time_data = None
    
    # Option pour charger des données d'exemple
    if st.button("📊 Charger des données d'exemple"):
        time_data = load_example_time_data()
        st.session_state.time_example = time_data
        st.success("Données d'exemple chargées ! Explorez votre utilisation d'Instagram dans le temps.")
    
    # Utiliser les données d'exemple si disponibles
    if 'time_example' in st.session_state:
        time_data = st.session_state.time_example
    # Sinon, traiter les données réelles si disponibles
    elif instagram_data is not None:
        time_data = process_time_data(instagram_data)
    
    if time_data is not None and not time_data.empty:
        # Période disponible
        min_date = time_data['date'].min()
        max_date = time_data['date'].max()
        
        st.info(f"Données disponibles du {min_date.strftime('%d/%m/%Y')} au {max_date.strftime('%d/%m/%Y')}")
        
        # Filtres pour FOCUS
        st.subheader("FOCUS - Filtres d'analyse")
        
        col1, col2 = st.columns(2)
        with col1:
            # Sélection de la période
            date_range = st.date_input(
                "Sélectionner une période",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        with col2:
            # Sélection des thématiques si disponibles
            if 'theme' in time_data.columns:
                themes = time_data['theme'].unique().tolist()
                selected_themes = st.multiselect(
                    "Filtrer par thématique",
                    options=themes,
                    default=themes
                )
        
        # Appliquer les filtres
        filtered_data = time_data.copy()
        
        # Filtre de date
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_data = filtered_data[
                (filtered_data['date'] >= start_date) & 
                (filtered_data['date'] <= end_date)
            ]
        
        # Filtre de thématique
        if 'theme' in time_data.columns and selected_themes:
            filtered_data = filtered_data[filtered_data['theme'].isin(selected_themes)]
        
        if filtered_data.empty:
            st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
            return
        
        # Métriques principales
        st.subheader("Métriques Clés")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sessions = filtered_data['session_id'].nunique()
            st.metric("Sessions", total_sessions)
        
        with col2:
            avg_duration = filtered_data.groupby('session_id')['session_duration'].mean().mean() / 60
            st.metric("Durée Moyenne", f"{avg_duration:.1f} min")
        
        with col3:
            total_duration = filtered_data['session_duration'].sum() / 3600
            st.metric("Temps Total", f"{total_duration:.1f} heures")
        
        with col4:
            daily_avg = filtered_data.groupby('date')['session_duration'].sum().mean() / 60
            st.metric("Temps Quotidien", f"{daily_avg:.1f} min")
        
        # Visualisations
        st.subheader("Distribution de l'Activité")
        
        # Heatmap jour/heure
        heatmap_fig = plot_time_heatmap(filtered_data)
        st.plotly_chart(heatmap_fig, use_container_width=True)
        st.markdown("""
        *Cette heatmap montre à quelles heures de la journée et quels jours de la semaine vous êtes le plus actif sur Instagram.*
        """)
        
        # Sessions quotidiennes
        sessions_fig = plot_daily_sessions(filtered_data)
        st.plotly_chart(sessions_fig, use_container_width=True)
        st.markdown("""
        *Ce graphique montre le nombre de sessions par jour (barres) et leur durée moyenne (ligne).*
        """)
        
        # Distribution des thématiques
        if 'theme' in filtered_data.columns:
            theme_fig = plot_theme_distribution(filtered_data)
            if theme_fig:
                st.plotly_chart(theme_fig, use_container_width=True)
                st.markdown("""
                *Ce graphique montre l'évolution de vos centres d'intérêt au fil du temps.*
                """)
        
        # Tableau détaillé des sessions (avec option d'export)
        st.subheader("Détail des Sessions")
        
        # Agréger les sessions
        session_detail = filtered_data.groupby('session_id').agg({
            'timestamp': 'min',
            'session_duration': 'mean',
            'theme': lambda x: x.iloc[0] if 'theme' in filtered_data.columns else None
        }).reset_index()
        
        # Version corrigée
        session_detail = session_detail.reset_index()  # S'assurer que session_id est une colonne
        session_detail['date'] = session_detail['timestamp'].dt.date
        session_detail['heure'] = session_detail['timestamp'].dt.strftime('%H:%M')
        session_detail['durée_min'] = (session_detail['session_duration'] / 60).round(1)

        # Colonnes à afficher
        display_cols = ['date', 'heure', 'durée_min']
        if 'theme' in filtered_data.columns:
            display_cols.append('theme')

        # Ensure 'timestamp' exists before sorting
        if 'timestamp' in session_detail.columns:
            session_detail_display = session_detail[display_cols].sort_values('timestamp', ascending=False)
        else:
            # Sort by 'date' and 'heure' if 'timestamp' is not available
            session_detail_display = session_detail[display_cols].sort_values(['date', 'heure'], ascending=False)

        st.dataframe(
            session_detail_display,
            use_container_width=True
        )
        
        # Export CSV
        csv = session_detail[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button(
                "Télécharger les détails de session (CSV)",
                csv,
                "instagram_sessions.csv",
                "text/csv",
                key='download_sessions'
            )
    
    else:
        st.info("""
        Aucune donnée temporelle disponible. Veuillez soit :
        1. Charger des données d'exemple avec le bouton ci-dessus
        2. Importer vos propres fichiers Instagram pour une analyse personnalisée
        """)