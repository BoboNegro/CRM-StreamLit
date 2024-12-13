import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import calendar
import locale
import plotly.graph_objects as go


locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Titre de l'application
st.title("Statistiques des ventes par région")

# URL de l'API
API_URL = "http://localhost:8000/regions"

# Sidebar : Sélection du mois
st.sidebar.header("Filtrer par mois")
selected_month = st.sidebar.selectbox(
    "Sélectionnez un mois",
    options=list(range(3, 13)),  # Mois de mars à décembre
    format_func=lambda x: calendar.month_name[x].capitalize()  # Le nom du mois en français
)

# Appel API et affichage
try:
    # Récupération des données depuis l'API
    response = requests.get(f"{API_URL}/{selected_month}")
    if response.status_code == 200:
        sales_data = response.json()

        # Conversion des données en DataFrame
        df = pd.DataFrame([
            {"Région": region, "Valeur Totale des Ventes (€)": stats["total_sales_value"], "Pourcentage des Ventes (%)": stats["sales_percentage"]}
            for region, stats in sales_data.items()
        ])

        # Affichage des statistiques
        st.subheader(f"Statistiques des ventes pour {calendar.month_name[selected_month]}")

        # Graphique en cercle (Pie Chart)
        fig = px.pie(
            df,
            values="Pourcentage des Ventes (%)",
            names="Région",
            title=f"Répartition des ventes par région - {calendar.month_name[selected_month]}",
            hole=0.4  # Pour un graphique en "donut"
        )
        st.plotly_chart(fig)

    else:
        st.error(f"Erreur lors de la récupération des données : {response.status_code}")
except Exception as e:
    st.error(f"Une erreur est survenue : {str(e)}")

@st.cache_data
def get_sales_data(month):
    response = requests.get(f"http://127.0.0.1:8000/sales-by-location/{month}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération des données : {response.status_code}")
        return None

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
