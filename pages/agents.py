import streamlit as st
import requests
import calendar
import locale

# Configuration de la langue française
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # 'fr_FR.UTF-8' pour Linux/Mac ou 'fr_FR' pour Windows

# Titre de l'application
st.title("Meilleur agent de ventes")

# URL de l'API
API_URL = "http://localhost:8000/top-agent/sales"

# Sidebar : Sélection du mois
st.sidebar.header("Filtrer par mois")
selected_month = st.sidebar.selectbox(
    "Sélectionnez un mois",
    options=list(range(1, 13)),
    format_func=lambda x: calendar.month_name[x].capitalize()  # Affiche le nom du mois en français
)

# Conteneur pour le meilleur agent
with st.container():
    st.subheader(f"Meilleur agent en {calendar.month_name[selected_month].capitalize()}")

    # Appel API pour récupérer le meilleur agent
    try:
        response = requests.get(f"{API_URL}/{selected_month}")
        if response.status_code == 200:
            data = response.json()

            if data.get("top_agent"):
                agent_name = data["top_agent"]["agent_name"]
                total_sales = data["top_agent"]["total_sales"]

                # Affichage des informations dans une carte
                st.markdown(
                    f"""
                    <div style="background-color:#f9f9f9;padding:15px;border-radius:10px;border:1px solid #ddd;">
                        <h3 style="text-align:center;color:#4CAF50;">🏆 {agent_name}</h3>
                        <p style="text-align:center;font-size:16px;">Total des ventes : <strong>{total_sales} €</strong></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.info(f"Aucun agent n'a réalisé de ventes en {calendar.month_name[selected_month].capitalize()}.")
        else:
            st.error(f"Erreur lors de la récupération des données : {response.status_code}")
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")
