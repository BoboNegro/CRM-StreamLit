import streamlit as st

st.set_page_config(
    page_title="CRM Dashboard",
    page_icon="🧊",
    layout="wide",
)

pages = [
        st.Page("pages/products.py", title="All about Products"),
        st.Page("pages/agents.py", title="All about Agents"),
        st.Page("pages/sectors.py", title="All about Sectors"),
]


pg = st.navigation(pages, position="hidden", expanded=False)

# pg.run()

current_page=""

# Définition des styles CSS globaux
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
    if current_page == "products":
       st.switch_page("pages/products.py", True)

with col2:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer;">'
        '<h3>👩‍💼 Agents</h3>'
        '<img src="app/static/agents.jpg" alt="Secteur">'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("Aller", key="agents_button"):
        st.switch_page("pages/agents.py")


with col3:
    st.markdown(
        '<div class="container" onclick="window.location.href=\'#\'" style="cursor: pointer;">'
        '<h3>🌍 Secteurs</h3>'
        '<img src="app/static/sectors.jpg" alt="Secteur">'
        '</div>',
        unsafe_allow_html=True
    )
    st.page_link(st.Page("pages/sectors.py"), label="Google", use_container_width=True)
