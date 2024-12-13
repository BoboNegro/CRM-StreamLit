import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import calendar
import locale


locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Titre de l'application
st.title("Statistiques des ventes par région")

# URL de l'API
API_URL = "http://localhost:8000/regions"

# Sidebar : Sélection du mois
st.sidebar.header("Filtrer par mois")
selected_month = st.sidebar.selectbox(
    "Sélectionnez un mois",
    options=list(range(1, 13)),
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
        st.dataframe(df)

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
