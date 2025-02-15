import streamlit as st
import pandas as pd 
import plotly.express as px 

st.set_page_config(layout="wide")

# Carregando os dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df
