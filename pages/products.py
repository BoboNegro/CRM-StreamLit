import calendar

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale

# Configurer la page Streamlit
st.set_page_config(
    page_title="Produits - Tableau de bord",
    layout="wide",
)

# Fonction pour récupérer les données de l'API
def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Liste des mois en français
mois = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

# Selectbox pour choisir le mois
st.sidebar.header("Filtrer par mois")
selected_month = st.sidebar.selectbox(
    "Choisissez un mois", options=list(range(3, 13)), format_func=lambda x: mois[x - 1]
)

# API Endpoints
sales_url = f"http://127.0.0.1:8000/products/{selected_month}"
conversion_rate_url = f"http://127.0.0.1:8000/sales/conversion_rate/{selected_month}"

# Récupération des données de l'API
sales_data = fetch_data(sales_url)
conversion_rate_data = fetch_data(conversion_rate_url)

def get_top_product_by_month(month: int):
    try:
        url = f"http://127.0.0.1:8000/top-product/{month}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Récupérer les informations du produit le plus vendu
top_product_data = get_top_product_by_month(selected_month)

# Afficher les informations dans la page principale
if top_product_data:
    st.title(f"Produit le plus vendu en {mois[selected_month - 1]}")

    if top_product_data["top_product"]:
        top_product = top_product_data["top_product"]
        st.subheader(f"Nom du produit : {top_product['product_name']}")
        st.write(f"Unités vendues : {top_product['units_sold']}")
    else:
        st.write("Aucun produit n'a été vendu ce mois-ci.")
else:
    st.write("Impossible de récupérer les données.")

# Si les données sont disponibles
if sales_data and conversion_rate_data:
    # Mise en page : deux colonnes principales
    col1, col2 = st.columns(2)

    # Première colonne : Ventes
    with col1:
        st.header("Ventes")

        # Vente totale du mois
        monthly_sales = sales_data.get("monthly_total", 0)
        sales_change = sales_data.get("percentage_change_month", 0)
        st.metric(
            label="Ventes totales",
            value=f"{monthly_sales} €",
            delta=f"{sales_change}%",
        )

        # Graphique des ventes quotidiennes avec évolution
        if "data" in sales_data and isinstance(sales_data["data"], list):
            daily_sales = pd.DataFrame(sales_data["data"])

            if not daily_sales.empty and "day" in daily_sales.columns and "total_sales" in daily_sales.columns and "percentage_change_day" in daily_sales.columns:
                # Tracer le graphique des ventes
                fig = px.line(
                    daily_sales,
                    x="day",
                    y="total_sales",
                    title="Ventes quotidiennes",
                    labels={"day": "Jour", "total_sales": "Ventes (€)", "percentage_change_day": "Chiffre %"},
                    hover_data={"day": False, "total_sales": True, "percentage_change_day": True}
                    # Afficher uniquement 'total_sales' et 'percentage_change_day' au survol
                )
                fig.update_traces(line=dict(color="royalblue", width=3))
                fig.update_layout(
                    paper_bgcolor="rgb(240,240,255)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Les données des ventes quotidiennes sont manquantes ou mal formatées.")

        else:
            st.warning("Les données des ventes ne sont pas disponibles.")

    # Deuxième colonne : Taux de conversion
    with col2:
        st.header("Taux de conversion")

        # Taux de conversion mensuel
        monthly_conversion_rate = conversion_rate_data.get("monthly_conversion_rate", 0)
        conversion_rate_change = conversion_rate_data.get("percentage_change_month", 0)
        st.metric(
            label="Taux de conversion",
            value=f"{monthly_conversion_rate}%",
            delta=f"{conversion_rate_change}%",
        )

        # Graphique des taux de conversion quotidiens
        if "daily_conversion_rates" in conversion_rate_data and isinstance(conversion_rate_data["daily_conversion_rates"], list):
            daily_conversion_rates = pd.DataFrame(conversion_rate_data["daily_conversion_rates"])
            if not daily_conversion_rates.empty and "day" in daily_conversion_rates.columns and "conversion_rate" in daily_conversion_rates.columns:
                fig = px.line(
                    daily_conversion_rates,
                    x="day",
                    y="conversion_rate",
                    title="Taux de conversion quotidiens",
                    labels={"day": "Jour", "conversion_rate": "Taux de conversion (%)"},
                )
                fig.update_traces(line=dict(color="seagreen", width=3))
                fig.update_layout(
                    paper_bgcolor="rgb(240,255,240)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Les données des taux de conversion quotidiens sont manquantes ou mal formatées.")
        else:
            st.warning("Les données des taux de conversion ne sont pas disponibles.")

    st.sidebar.success("Visualisation mise à jour !")
else:
    st.error("Les données ne sont pas disponibles.")

# Classement des produits
sales_volume_data = fetch_data(f"http://127.0.0.1:8000/sales/volume/{selected_month}")
if sales_volume_data:
    st.title(f"Classement des Produits par Volume de Ventes - {mois[selected_month - 1]}")
    sales_df = pd.DataFrame(sales_volume_data.items(), columns=["Produit", "Volume de ventes"])
    sales_df = sales_df.sort_values("Volume de ventes", ascending=False)
    fig = px.bar(
        sales_df,
        x="Produit",
        y="Volume de ventes",
        title="Volume de ventes par produit",
        labels={"Volume de ventes": "Volume de ventes", "Produit": "Produit"},
        color="Volume de ventes",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        paper_bgcolor="rgb(245,245,255)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Les données des volumes de ventes sont indisponibles.")
