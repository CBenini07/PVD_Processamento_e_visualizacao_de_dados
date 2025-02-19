import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Carregando os dados
df = pd.read_csv("data_processada_final.csv", sep=",", decimal=",", header=0)

# Criando a barra lateral
menu = st.sidebar.selectbox("Escolha uma opção", ["Dataset", "Heatmap", "Comparação de Países", "Comparação de Investimentos"])

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



elif menu == "Comparação de Países":
    st.write("## Comparação de Países")

    # ==================== SELECAO DOS PAISES ====================
    paises_sem_usa = ["Haiti", "Cuba", "Jamaica", "Mexico", "Dominican-Republic", "Peru", "Puerto-Rico", "Honduras", "Ecuador", "El-Salvador", "Guatemala", "Trinadad&Tobago", "Nicaragua", "China", "India", "Philippines", "Cambodia", "Thailand", "Laos", "Taiwan", "Japan", "Vietnam", "Hong", "England", "Germany", "Poland", "Portugal", "France", "Italy", "Scotland", "Greece", "Ireland", "Hungary", "Holand-Netherlands", "Yugoslavia", "Canada", "Iran", "Columbia", "South"]

    paises_latinos = ["Haiti", "Cuba", "Jamaica", "Mexico", "Dominican-Republic", "Peru", "Puerto-Rico", "Honduras", "Ecuador", "El-Salvador", "Guatemala", "Trinadad&Tobago", "Nicaragua"]
    paises_asiaticos = ["China", "India", "Philippines", "Cambodia", "Thailand", "Laos", "Taiwan", "Japan", "Vietnam", "Hong"]
    paises_europeus = ["England", "Germany", "Poland", "Portugal", "France", "Italy", "Scotland", "Greece", "Ireland", "Hungary", "Holand-Netherlands", "Yugoslavia"]

    paises_subdesenvolvidos = ["China", "India", "Iran"]
    paises_desenvolvidos = ["Canada", "United-States", "England", "Germany", "Poland", "Portugal", "France", "Italy", "Japan", "Scotland", "Greece", "Ireland", "Hungary", "Holand-Netherlands"]

    countries = df["native-country-name"].unique()
    
    coluna1_paises, coluna2_paises = st.columns(2)  # Criando duas colunas para organizar os multiselects
    
    with coluna1_paises:
        group_a = st.multiselect("Selecione os países do Grupo A", countries, default=["United-States"])

    # Inicializa o conjunto de países do Grupo B
    selected_countries = set()

    st.write("### Grupos de Seleção")
    st.write("#### Todos os imigrantes")
    select_all_sem_usa = st.checkbox("Selecionar todos os países menos os EUA para o Grupo B", value=False)

    st.write("#### Regiões")
    select_all_latinos = st.checkbox("Selecionar todos os Países **Latinos** para o Grupo B", value=False)
    select_all_asiaticos = st.checkbox("Selecionar todos os Países **Asiáticos** para o Grupo B", value=False)
    select_all_europeus = st.checkbox("Selecionar todos os Países **Europeus** para o Grupo B", value=False)

    # st.write("#### Desenvolvimento Econômico")
    # select_all_subdesenvolvidos = st.checkbox("Selecionar todos os países subdesenvolvidos para o Grupo B", value=False)
    # select_all_desenvolvidos = st.checkbox("Selecionar todos os países desenvolvidos para o Grupo B", value=False)

    # Atualiza os países selecionados conforme os checkboxes são marcados
    if select_all_sem_usa:
        selected_countries.update(paises_sem_usa)
    if select_all_latinos:
        selected_countries.update(paises_latinos)
    if select_all_asiaticos:
        selected_countries.update(paises_asiaticos)
    if select_all_europeus:
        selected_countries.update(paises_europeus)
    # if select_all_subdesenvolvidos:
    #     selected_countries.update(paises_subdesenvolvidos)
    # if select_all_desenvolvidos:
    #     selected_countries.update(paises_desenvolvidos)

    # Agora o multiselect do Grupo B é renderizado com as seleções atualizadas
    with coluna2_paises:
        group_b = st.multiselect("Selecione os países do Grupo B", countries, default=list(selected_countries))

    # Validação para garantir que ambos os grupos tenham pelo menos um país selecionado
    if not group_a or not group_b:
        st.warning("Selecione pelo menos um país em cada grupo.")

    workclasses = [
        "Qualquer área de trabalho",  # Opção para não filtrar
        "workclass_Local-gov", "workclass_Private", "workclass_Self-emp-inc",
        "workclass_Self-emp-not-inc", "workclass_State-gov", "workclass_Without-pay"
    ]

    selected_workclass = st.selectbox("Selecione a classe de trabalho:", workclasses)


    if selected_workclass == "Qualquer área de trabalho":
        df_group_a = df[df['native-country-name'].isin(group_a)].copy()
        df_group_b = df[df['native-country-name'].isin(group_b)].copy()
    else:
        df_group_a = df[(df['native-country-name'].isin(group_a)) & (df[selected_workclass] == 1)].copy()
        df_group_b = df[(df['native-country-name'].isin(group_b)) & (df[selected_workclass] == 1)].copy()


    coluna_paises_grafico_1, coluna_paises_grafico_2 = st.columns(2)

        # ==================== GRAFICO 1 ====================

    df_income_groups = pd.concat([
        pd.DataFrame({'is_from_group_a': "Paises do Grupo A", 'income': df_group_a['income'], 'total': 1}),
        pd.DataFrame({'is_from_group_a': "Paises do Grupo B", 'income': df_group_b['income'], 'total': 1})
    ], ignore_index=True)

    df_income_groups = df_income_groups.groupby(['is_from_group_a', 'income'], as_index=False).sum()
    df_income_groups = df_income_groups.sort_values("income")

    # Atualizar os rótulos para refletir essa mudança
    income_labels = {
        0: "Renda Anual Menor que $50.000",
        1: "Renda Anual Maior que $50.000"
    }
    df_income_groups["income"] = df_income_groups["income"].map(income_labels)

    # Definição de padrões para melhor diferenciação visual
    pattern_shapes = {
        "Renda Anual Menor que $50.000": ".",
        "Renda Anual Maior que $50.000": "x"
    }

    # Calcular o total por grupo para normalizar os valores
    df_income_groups['group_total_income'] = df_income_groups.groupby('is_from_group_a')['total'].transform('sum')
    # Calcular a porcentagem de cada categoria
    df_income_groups['percent'] = df_income_groups['total'] / df_income_groups['group_total_income'] * 100

    # Criar o gráfico usando a coluna 'percent'
    fig_income = px.bar(
        df_income_groups, 
        x="is_from_group_a", 
        y="percent", 
        color="income", 
        title="Distribuição por Renda Anual (Percentual)",
        category_orders={"income": list(income_labels.values())[::-1]},
        pattern_shape="income",  
        pattern_shape_map=pattern_shapes,
        color_discrete_map={
            "Renda Anual Menor que $50.000": "red",   # Cor vermelha para 0
            "Renda Anual Maior que $50.000": "green"  # Cor verde para 1
        }
    )

    fig_income.update_yaxes(title_text="Percentual (%)", range=[0, 100])

    coluna_paises_grafico_1.plotly_chart(fig_income)


    # ==================== GRAFICO 2 ====================

    df_education_groups = pd.concat([
        pd.DataFrame({'is_from_group_a': "Paises do Grupo A", 'education-num': df_group_a['education-num'], 'total': 1}),
        pd.DataFrame({'is_from_group_a': "Paises do Grupo B", 'education-num': df_group_b['education-num'], 'total': 1})
    ], ignore_index=True)

    df_education_groups = df_education_groups.groupby(['is_from_group_a', 'education-num'], as_index=False).sum()
    df_education_groups = df_education_groups.sort_values("education-num")

    # Mapeando os valores de 'education-num' para os rótulos desejados
    df_education_groups['education-num'] = df_education_groups['education-num'].replace(0, 0.125)
    df_education_groups['education-num'] = df_education_groups['education-num'].replace(0.375, 0.625)
    df_education_groups['education-num'] = df_education_groups['education-num'].replace(0.5, 0.625)

    # Atualizar os rótulos para refletir essa mudança
    education_labels = {
        0.125: "Médio Não Iniciado/Incompleto",  # Agrupando 0 e 0.125
        0.25: "Médio Completo",
        0.625: "Superior Incompleto/Técnico", # Agrupando 0.375, 0.5 e 0.625
        0.75: "Bacharel",
        0.875: "Mestrado",
        1: "Doutorado"
    }
    df_education_groups["education-num"] = df_education_groups["education-num"].map(education_labels)

    # Definição de padrões para melhor diferenciação visual
    pattern_shapes = {
        "Médio Não Iniciado/Incompleto": ".",
        "Médio Completo": "x",
        "Superior Incompleto/Técnico": "+",
        # "Técnico Vocacional": "/",
        # "Técnico Administrativo": "\\",
        "Bacharel": "\\",
        "Mestrado": "|",
        "Doutorado": "/"
    }

    # Criando gráfico otimizado com padrões para cada nível de educação
    # Calcular o total por grupo para normalizar os valores
    df_education_groups['group_total_education'] = df_education_groups.groupby('is_from_group_a')['total'].transform('sum')
    # Calcular a porcentagem de cada categoria
    df_education_groups['percent'] = df_education_groups['total'] / df_education_groups['group_total_education'] * 100

    # Criar o gráfico usando a coluna 'percent'
    fig_education = px.bar(
        df_education_groups, 
        x="is_from_group_a", 
        y="percent", 
        color="education-num", 
        title="Distribuição por Educação (Percentual)",
        category_orders={"education-num": list(education_labels.values())},
        pattern_shape="education-num",  
        pattern_shape_map=pattern_shapes
    )

    # Opcional: fixar o eixo y de 0 a 100%
    fig_education.update_yaxes(title_text="Percentual (%)", range=[0, 100])

    coluna_paises_grafico_2.plotly_chart(fig_education)

    # ==================== Quantidade de cada População ====================
    population_a = len(df_group_a)
    population_b = len(df_group_b)

    st.write(f"População total do **Grupo A**: {population_a}")
    st.write(f"População total do **Grupo B**: {population_b}")



if menu == "Comparação de Investimentos":
    st.write("## Comparação de Investimentos")

    # Criar gráficos de distribuição com Plotly
    fig1 = px.histogram(df, x="investment_status_naoDiscretizado", nbins=30, title="Distribuição de Investment Status")
    fig2 = px.histogram(df, x="age_naoDiscretizada", nbins=30, title="Distribuição de Idade")

    # Exibir os gráficos
    coluna_investimento1, coluna_investimento2 = st.columns(2)
    with coluna_investimento1:
        st.plotly_chart(fig1, use_container_width=True)
    with coluna_investimento2:
        st.plotly_chart(fig2, use_container_width=True)

    # Normalização Z-score (média = 0, variância = 1)
    df['investment_status_normalized'] = (df['investment_status_naoDiscretizado'] - df['investment_status_naoDiscretizado'].mean()) / df['investment_status_naoDiscretizado'].std()

    # Selecionar faixa etária
    selected_age_range = st.slider("Selecione uma faixa etária", 
                                   min_value=int(df['age_naoDiscretizada'].min()), 
                                   max_value=int(df['age_naoDiscretizada'].max()), 
                                   value=(int(df['age_naoDiscretizada'].min()), int(df['age_naoDiscretizada'].max())), 
                                   step=5)
    selected_age_min, selected_age_max = selected_age_range
    
    # Caixa de entrada para o valor do investimento
    investment_threshold = st.number_input("Digite o valor do investimento para calcular a probabilidade", 
                                           min_value=0, value=10000, step=1000)
    
    df_filtered = df[(df['age_naoDiscretizada'] >= selected_age_min) & (df['age_naoDiscretizada'] <= selected_age_max)]
    total_people = len(df_filtered)
    people_above_threshold = len(df_filtered[df_filtered['investment_status_naoDiscretizado'] > investment_threshold])
    
    probability = (people_above_threshold / total_people) * 100 if total_people > 0 else 0
    
    st.write(f"A probabilidade de uma pessoa entre {selected_age_min} e {selected_age_max} anos ter mais de {investment_threshold} de investimento é de {probability:.2f}%")
    
    # Gráfico de distribuição de densidade acumulada com base na faixa etária selecionada
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.kdeplot(df_filtered['investment_status_naoDiscretizado'], cumulative=True, fill=True, ax=ax)
    ax.axhline(y=probability / 100, color='r', linestyle='--', label=f'Probabilidade: {probability:.2f}%')
    ax.set_title("Distribuição Acumulada para a Faixa Etária Selecionada")
    ax.set_xlabel("Investment Status")
    ax.set_ylabel("Probabilidade Acumulada")
    ax.legend()
    
    st.pyplot(fig)