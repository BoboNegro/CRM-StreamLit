import streamlit as st

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "main"


def navigate_to(page):
    st.session_state["current_page"] = page
    st.rerun()


products_page = st.Page("pages/products.py", icon="📦")
agents_page = st.Page("pages/agents.py", icon="👩‍💼")
sectors_page = st.Page("pages/sectors.py", icon="🌍")

products_page = [products_page]
agents_page = [agents_page]
sectors_page = [sectors_page]

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
    height: 300px;
    width: 200px;
    cursor: pointer;
    text-align: center;
    transition: transform 0.2s ease-in-out;
    margin-top: 120px;
    width: 100%

}
.container:hover {
    transform: scale(1.05);
    border-color: #007BFF;
}
.container img {
    width: 100px;
    height: 120px;
    margin: 20px 0;
}
.container h3 {
    margin: 10px 0;
}

h1 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 30px;
    margin-bottom: 50px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Contenu principal


st.markdown("<h1>CRM DASHBOARD ⚙️</h1>", unsafe_allow_html=True)
st.logo=("app/static/crm_image.jpg")


# Création des colonnes
col1, col2, col3 = st.columns(3)

# Contenu des containers
with col1:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer;">'
        '<h3>📦 Produits</h3>'
        '<img src="app/static/products.jpg" alt="Produits">'
        '<button>Visiter</button>'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("produits"):
        navigate_to("products")

with col2:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer;">'
        '<h3>👩‍💼 Agents</h3>'
        '<img src="app/static/agents.jpg" alt="Secteur">'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("Agents"):
        navigate_to("agents")


with col3:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer;">'
        '<h3>🌍 Secteurs</h3>'
        '<img src="app/static/sectors.jpg" alt="Secteur">'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("Secteurs"):
        navigate_to("sectors")


page_dict = {}

if st.session_state["current_page"] == "products":
    page_dict["products"] = products_page
if st.session_state["current_page"] == "agents":
    page_dict["agents"] = agents_page
if st.session_state["current_page"] == "sectors":
    page_dict["sectors"] = sectors_page

if len(page_dict) > 0:
    pg = st.navigation(page_dict)
    pg.run()


