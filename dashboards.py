import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carregando os dados
df = pd.read_csv("data_processada.csv", sep=",", decimal=",", header=0)

# Exibindo o DataFrame no Streamlit
st.write("## Dataset Processado")
st.dataframe(df)
