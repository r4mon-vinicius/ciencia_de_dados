import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Billionaires Statistics (2023)",
    page_icon="💲",
    layout="wide"
)

st .title("Análise do Dataset Billionaires Statistics (2023)")
st.markdown("""
Este dashboard foi criado para analisar o dataset **Billionaires Statistics (2023)**, que
contém informações sobre bilionários de todo o mundo, incluindo dados demográficos, fontes de riqueza e classificações.
""")

@st.cache_data
def load_data():
    df = pd.read_csv()