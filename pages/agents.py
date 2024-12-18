import streamlit as st
import requests
import calendar
import locale
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

# Fonction pour récupérer les données des agents
def fetch_agent_stats_sales_by_month(month):
    try:
        response = requests.get(f"{API_URL}/top-agents/sales/{month}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données des agents : {str(e)}")
        return None

def fetch_agent_stats_rate_by_month(month):
    try:
        response = requests.get(f"{API_URL}/top-agents/conv_rate/{month}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données des agents : {str(e)}")
        return None

def fetch_deals_stats_by_month(month):
    try:
        response = requests.get(f"{API_URL}/deals/{month}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données des agents : {str(e)}")
        return None

def fetch_agent_stats_by_month(month):
    try:
        response = requests.get(f"{API_URL}/agents/{month}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données des agents : {str(e)}")
        return None

# Fonction pour afficher une carte d'agent
def display_agent_card(title, agent_name, value, metric):
    st.markdown(
        f"""
        <div style="background-color:#f9f9f9;padding:15px;border-radius:10px;border:1px solid #ddd;">
            <h3 style="text-align:center;color:#4CAF50;">{title}</h3>
            <h4 style="text-align:center;">{agent_name}</h4>
            <p style="text-align:center;font-size:16px;">{metric} : <strong>{value}</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Fonction pour récupérer les données des deals
def fetch_deals_by_month(month):
    try:
        response = requests.get(f"{API_URL}/deals/{month}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {str(e)}")
        return None

def run():
    # Configuration de la langue française
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # 'fr_FR.UTF-8' pour Linux/Mac ou 'fr_FR' pour Windows

    # Titre de l'application
    st.title("Performances des Agents de Vente")

    # URL de l'API
    API_URL = "http://localhost:8000"

    # Sidebar : Sélection du mois
    st.sidebar.header("Filtrer par mois")
    selected_month = st.sidebar.selectbox(
        "Sélectionnez un mois",
        options=list(range(3, 13)),
        format_func=lambda x: calendar.month_name[x].capitalize()
    )

    # Récupération des données des agents
    top_agent_data = fetch_agent_stats_by_month(selected_month)
    top_agent_rate_data = fetch_agent_stats_by_month(selected_month)
    deals_data = fetch_agent_stats_by_month(selected_month)
    agent_data = fetch_agent_stats_by_month(selected_month)

    # Affichage des meilleures performances en haut
    if top_agent_data and "agent_stats" in agent_data:
        agent_stats = pd.DataFrame(agent_data["agent_stats"])
        if not agent_stats.empty:
            top_sales_agent = agent_stats.loc[agent_stats['total_sales'].idxmax()]
            top_conversion_agent = agent_stats.loc[agent_stats['success_rate'].idxmax()]

            col1, col2 = st.columns(2)
            with col1:
                display_agent_card("Meilleur Agent (en terme de ventes)",
                                   top_sales_agent['agent_name'],
                                   f"{int(top_sales_agent['total_sales'])} €",
                                   "Total des ventes")
            with col2:
                display_agent_card("Meilleur Agent (en % de conversion)",
                                   top_conversion_agent['agent_name'],
                                   f"{top_conversion_agent['success_rate']:.2f}%",
                                   "Taux de conversion")
        else:
            st.info("Aucune donnée disponible pour les agents ce mois-ci.")
    else:
        st.error("Les données des agents ne sont pas disponibles.")

    # Récupération des données des deals
    deals_data = fetch_deals_by_month(selected_month)

    # Affichage des graphiques en bas
    col1, col2 = st.columns(2)

    # Graphique des deals gagnés et perdus
    if deals_data and "daily_deals" in deals_data:
        daily_deals = pd.DataFrame(deals_data["daily_deals"])
        if not daily_deals.empty:
            with col1:
                fig = px.bar(
                    daily_deals,
                    x="day",
                    y=["won_deals", "lost_deals"],
                    title=f"Deals Gagnés et Perdus - {calendar.month_name[selected_month].capitalize()}",
                    labels={"value": "Nombre de deals", "day": "Jour"},
                    color_discrete_sequence=["#4CAF50", "#F44336"]
                )
                fig.update_layout(
                    barmode='group',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(245, 245, 245, 1)',
                    xaxis=dict(title="Jour", tickmode="linear"),
                    yaxis=dict(title="Nombre de Deals")
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            with col1:
                st.info("Aucune donnée de deals disponible pour ce mois.")
    else:
        with col1:
            st.error("Les données des deals ne sont pas disponibles.")

    # Graphique des ventes par agent
    if agent_data and "agent_stats" in agent_data:
        agent_stats = pd.DataFrame(agent_data["agent_stats"])
        if not agent_stats.empty:
            with col2:
                fig = px.bar(
                    agent_stats,
                    x="agent_name",
                    y="total_sales",
                    title=f"Ventes par Agent - {calendar.month_name[selected_month].capitalize()}",
                    labels={"total_sales": "Total des ventes (€)", "agent_name": "Agent"},
                    color="success_rate",
                    color_continuous_scale="Viridis",
                    text="success_rate",
                )
                fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(245, 245, 245, 1)',
                    xaxis=dict(title="Agent"),
                    yaxis=dict(title="Total des ventes (€)")
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            with col2:
                st.info("Aucune donnée de ventes par agent disponible pour ce mois.")
    else:
        with col2:
            st.error("Les données des ventes par agent ne sont pas disponibles.")