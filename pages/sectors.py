from urllib import response

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import calendar
import locale


@st.cache_data
def get_sales_data(month):
    response = requests.get(f"http://127.0.0.1:8000/sales-by-location/{month}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération des données : {response.status_code}")
        return None

def run():
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    # Titre de l'application
    st.title("Statistiques des ventes par région")

    # URL de l'API
    API_URL_REGIONS = "http://localhost:8000/regions"
    API_URL_LOCATIONS = "http://localhost:8000/sales-by-location"
    API_URL_ANALYSIS = "http://localhost:8000/sector-analysis"

    # Sidebar : Sélection du mois
    st.sidebar.header("Filtrer par mois")
    selected_month = st.sidebar.selectbox(
        "Sélectionnez un mois",
        options=list(range(3, 13)),  # Mois de mars à décembre
        format_func=lambda x: calendar.month_name[x].capitalize()  # Le nom du mois en français
    )

    def fetch_region_sales_by_month(month):
        try:
            response = requests.get(f"{API_URL_REGIONS}/{month}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la récupération des données des régions : {str(e)}")
            return None

    # Récupération des données des meilleures locations
    def fetch_top_locations_by_month(month):
        try:
            response = requests.get(f"{API_URL_LOCATIONS}/{month}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la récupération des meilleures locations : {str(e)}")
            return None

    # Récupération des données pour les ventes par région et par emplacement
    region_sales_data = fetch_region_sales_by_month(selected_month)
    location_sales_data = fetch_top_locations_by_month(selected_month)

    # Appel API et affichage
    try:
        col1, col2 = st.columns(2)
        # Récupération des données depuis l'API
        region_sales_data = fetch_region_sales_by_month(selected_month)
        if region_sales_data:
            sales_data = region_sales_data

            df_region = pd.DataFrame([
                {"Région": region, "Valeur Totale des Ventes (€)": stats["total_sales_value"],
                 "Pourcentage des Ventes (%)": stats["sales_percentage"]}
                for region, stats in region_sales_data.items()
            ])

            with col1:
                # Graphique en cercle (Pie Chart)
                fig_region = px.pie(
                    df_region,
                    values="Pourcentage des Ventes (%)",
                    names="Région",
                    title=f"Répartition des ventes par région - {calendar.month_name[selected_month]}",
                    hole=0.4  # Pour un graphique en "donut"
                )
                st.plotly_chart(fig_region)
        if location_sales_data and "location_sales" in location_sales_data:
            # Conversion des données en DataFrame
            df_location = pd.DataFrame(location_sales_data["location_sales"])

            with col2:
                # Graphique à barres des ventes par emplacement
                fig_location = px.bar(
                    df_location,
                    x="location",
                    y="total_sales",
                    title=f"Top des emplacements par ventes - {calendar.month_name[selected_month]}",
                    labels={"location": "Emplacement", "total_sales": "Ventes Totales (€)"},
                    color="total_sales",  # Coloration par le montant des ventes
                    color_continuous_scale="Viridis"  # Palette de couleurs
                )
                fig_location.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
                    paper_bgcolor="rgba(245, 245, 245, 1)",  # Couleur du papier
                    xaxis=dict(title="Emplacement"),
                    yaxis=dict(title="Ventes Totales (€)")
                )
                st.plotly_chart(fig_location)


        else:
            st.error(f"Erreur lors de la récupération des données ")
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")

    data = get_sales_data(selected_month)

    # Afficher la carte si les données sont disponibles
    if data and "location_sales" in data:
        df = pd.DataFrame(data["location_sales"])

        # Vérifier si les données contiennent une colonne "location"
        if not df.empty:
            # Ici, nous supposons que "location" contient les noms de lieux compatibles avec Plotly
            st.subheader(f"Carte des ventes pour {calendar.month_name[selected_month].capitalize()}")

            # Utiliser Plotly pour tracer la carte
            fig = px.scatter_geo(
                df,
                locations="location",  # Les noms de lieux ou codes géographiques (ISO Alpha-3)
                locationmode="country names",  # Mode de correspondance des lieux
                size="total_sales",  # Taille des bulles basée sur les ventes
                projection="natural earth",
                title=f"Répartition des ventes par localisation - {calendar.month_name[selected_month].capitalize()}",
                hover_name="location",
                hover_data={"total_sales": True},
            )

            # Afficher la carte dans Streamlit
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Aucune donnée de ventes pour {calendar.month_name[selected_month].capitalize()}.")

    st.title("Secteur d'activité")

    valid_parameters = ["Conversion Rate", "Won Deals", "Lost Deals", "Total Opportunities", "Total Sales"]
    selected_parameter = st.selectbox(
        "Sélectionnez le paramètre à analyser",
        options=valid_parameters
    )

    # Récupération des données de l'API pour l'analyse des secteurs
    def fetch_sector_analysis(month, parameter):
        try:
            response = requests.get(f"{API_URL_ANALYSIS}/{month}/{parameter}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la récupération des données : {str(e)}")
            return None

    # Récupération des données pour le secteur
    sector_data = fetch_sector_analysis(selected_month, selected_parameter)

    # Conteneur pour afficher le graphique
    with st.container():
        if sector_data and "sector_analysis" in sector_data:
            # Conversion des données en DataFrame
            df_sector = pd.DataFrame(sector_data["sector_analysis"])

            if not df_sector.empty:
                # Création du graphique
                fig = px.bar(
                    df_sector,
                    x="sector",
                    y=selected_parameter,
                    title=f"Analyse des secteurs - {calendar.month_name[selected_month]}",
                    labels={"sector": "Secteur", selected_parameter: selected_parameter},
                    color=selected_parameter,  # Couleur en fonction du paramètre sélectionné
                    color_continuous_scale="Viridis"  # Palette de couleurs
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
                    paper_bgcolor="rgba(245, 245, 245, 1)",  # Couleur du papier
                    xaxis=dict(title="Secteur"),
                    yaxis=dict(title=selected_parameter)
                )
                st.plotly_chart(fig)
            else:
                st.info(
                    f"Aucune donnée disponible pour le paramètre '{selected_parameter}' en {calendar.month_name[selected_month]}.")
        else:
            st.error("Les données de l'analyse des secteurs ne sont pas disponibles.")