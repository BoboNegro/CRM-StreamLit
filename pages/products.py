import calendar

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
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
    "Choisissez un mois", options=list(range(1, 13)), format_func=lambda x: mois[x - 1]
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

                # Définir l'index de manière appropriée
                daily_sales = daily_sales.set_index("day")

                # Tracer le graphique des ventes
                st.line_chart(daily_sales["total_sales"], use_container_width=True)

                # Afficher l'évolution des ventes sous forme de texte ou d'autres graphiques si nécessaire
                st.write("Évolution des ventes par rapport au jour précédent :")
                st.write(daily_sales[["percentage_change_day"]])


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
                st.line_chart(
                    daily_conversion_rates.set_index("day")["conversion_rate"],
                    use_container_width=True,
                )
            else:
                st.warning("Les données des taux de conversion quotidiens sont manquantes ou mal formatées.")
        else:
            st.warning("Les données des taux de conversion ne sont pas disponibles.")

    st.sidebar.success("Visualisation mise à jour !")
else:
    st.error("Les données ne sont pas disponibles.")


def get_sales_volume_by_month(month: int):
    try:
        url = f"http://127.0.0.1:8000/sales/volume/{month}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

sales_volume_data = get_sales_volume_by_month(selected_month)

print(sales_volume_data)

if sales_volume_data:
    st.title(f"Classement des Produits par Volume de Ventes - {mois[selected_month - 1]}")

    if sales_volume_data:
        # Créer un DataFrame à partir des données reçues
        sales_df = pd.DataFrame(sales_volume_data.items(), columns=["Produit", "Volume de ventes"])

        sales_df = sales_df.sort_values("Volume de ventes", ascending=False)

        # Affichage du graphique à barres
        st.bar_chart(sales_df.set_index("Produit")["Volume de ventes"],horizontal=True, use_container_width=True)

        # Affichage des données sous forme de tableau pour plus de détails
        st.write("Détails des produits et volumes de ventes :")
        st.dataframe(sales_df, hide_index=True)
    else:
        st.write("Aucun produit n'a été vendu ce mois-ci.")
else:
    st.write("Impossible de récupérer les données.")


with st.container():
    # Sélecteur de catégorie
    category = st.selectbox(
        "Sélectionnez une catégorie",
        options=["Manager", "Sales Agent", "Account"]
    )

    # Appel à l'API
    try:
        response = requests.get(f"http://127.0.0.1:8000/sales/{category}/{selected_month}")
        if response.status_code == 200:
            sales_data = response.json()

            # Conversion des données en DataFrame
            df = pd.DataFrame(list(sales_data.items()), columns=["Catégorie", "Valeur des ventes"])


            locale.setlocale(locale.LC_TIME, 'fr_FR')  # Remplacez par 'fr_FR' pour le français

            month_name = calendar.month_name[selected_month].capitalize()
            st.subheader(f"Ventes pour {category} en {month_name}")
            # Affichage du tableau

            # Graphique
            fig = px.bar(
                df,
                x="Catégorie",
                y="Valeur des ventes",
                title=f"Statistiques des ventes - {category}",
                labels={"Valeur des ventes": "Ventes (€)", "Catégorie": "Catégories de produits"}
            )
            st.plotly_chart(fig)
        else:
            st.error(f"Erreur lors de la récupération des données : {response.status_code}")
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")