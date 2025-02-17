import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Carregando os dados
df = pd.read_csv("data_processada.csv", sep=",", decimal=",", header=0)

# Criando a barra lateral
menu = st.sidebar.selectbox("Escolha uma opção", ["Dataset", "Heatmap"])

if menu == "Dataset":
    st.write("## Dataset Processado")
    st.dataframe(df)

elif menu == "Heatmap":
    st.write("## Heatmap dos Atributos")
    default_features = ['income', 'sex_Male', 'education-num', 'age', 'investment_status', 'race_Black', 'race_White']
    selected_features = st.multiselect("Selecione os atributos para o Heatmap", df.columns.tolist(), default=default_features)
    
    if selected_features:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[selected_features].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Selecione pelo menos um atributo para exibir o Heatmap.")
