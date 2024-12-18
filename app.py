import streamlit as st

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "main"

# Configuration de la page
st.set_page_config(layout="wide")

def navigate_to(page):
    st.session_state["current_page"] = page
    st.rerun()

custom_css = """
<style>
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 2px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    height: 300px; /* Ajusté pour s'adapter à une disposition large */
    width: 100%; /* Utiliser toute la largeur de la colonne */
    text-align: center;
    margin-top: 20px; /* Réduit l'espacement vertical */
}
.container:hover {
    transform: scale(1.05);
    border-color: #007BFF;
}
.container img {
    max-width: 100%; /* Empêche le dépassement horizontal */
    max-height: 150px; /* Limite la hauteur */
    object-fit: contain; /* Maintient les proportions de l'image */
    margin: 10px 0;
}
.container h3 {
    margin: 10px 0;
}

h1 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 30px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# Contenu principal


st.markdown("<h1>CRM DASHBOARD ⚙️</h1>", unsafe_allow_html=True)
st.logo=("app/static/hetic.webp")


# Création des colonnes
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

# Contenu des containers
with col1:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer; text-align: center; display: flex; flex-direction: column; align-items: center;">'
        '<p style="font-size: 24px; margin-bottom: 0px;">📦</p>'
        '<p style="font-size: 24px; margin-top: 0;">Produits</p>'
        '<img src="app/static/products.jpg" alt="Produits" style="width:90%; height:auto;">'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
    if st.button("Produits"):
        navigate_to("products")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer; text-align: center; display: flex; flex-direction: column; align-items: center;">'
        '<p style="font-size: 24px; margin-bottom: 0px;">👩‍💼</p>'
        '<p style="font-size: 24px; margin-top: 0;">Agents</p>'
        '<img src="app/static/agents.jpg" alt="Agents" style="width:90%; height:auto;">'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
    if st.button("Agents"):
        navigate_to("agents")
    st.markdown('</div>', unsafe_allow_html=True)


with col3:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer; text-align: center; display: flex; flex-direction: column; align-items: center;">'
        '<p style="font-size: 24px; margin-bottom: 5px;">🌍</p>'
        '<p style="font-size: 24px; margin-top: 0;">Secteurs</p>'
        '<img src="app/static/sectors.jpg" alt="Secteurs" style="width:90%; height:auto;">'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
    if st.button("Secteurs"):
        navigate_to("sectors")
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state["current_page"] == "products":
    from pages import products
    products.run()

elif st.session_state["current_page"] == "agents":
    from pages import agents
    agents.run()

elif st.session_state["current_page"] == "sectors":
    from pages import sectors
    sectors.run()