import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

st.set_page_config(layout="wide")

# Carregando os dados
df = pd.read_csv("data_processada_final.csv", sep=",", decimal=",", header=0)

# Criando a barra lateral
# menu = st.sidebar.selectbox("Escolha uma opção", ["Dataset", "Heatmap", "Comparação de Países", "Comparação de Gênero", "Comparação de Investimentos", "Distribuição PCA dos Dados", "Comparação de Horas"])
menu = st.sidebar.selectbox("Escolha uma opção", ["Dataset", "Hipotese 1", "Hipotese 2", "Hipotese 3", "Hipotese 4", "Hipotese 5"])

# ################## PÁGINA DO DATASET ##################
if menu == "Dataset":
    st.write("## Dataset Processado")
    st.dataframe(df)


# ################## PÁGINA DO HEATMAP ##################
elif menu == "Hipotese 1":
    st.write("## Heatmap dos Atributos - Hipótese 1 - A renda dos indivíduos está diretamente relacionada a sua educação e seu gênero")

    # Criando a tabela em Markdown
    markdown_table = """
    | antecedents | consequents | support  | confidence | lift     |
    |-------------|-------------|----------|------------|----------|
    | (income)    | (sex_Male)  | 0.213311 | 0.842445   | 1.260901 |
    """



    # Exibindo a tabela no Streamlit
    st.title('Tabela de Regras de Associação')
    st.markdown(markdown_table)

    # Descrição abaixo da tabela
    apriori_desc = f"""
        **Descrição da Tabela:**
        É apresentado acima uma tabela de regras de associação Apriori comparando as variáveis income, 
        que é uma variável booleana indicando se uma uma pessoa recebe um valor acima de \$50.000 anuais como antecedente,
        e a variável sex_Male, que indica se a pessoa é do gênero Masculino ou Feminino.
        Como principais resultados coletados nessa tabela, visualiza-se o suporte, que nos mostra que a combinação entre income e sex_Male
        aparece em 21% do dataset, 
        e também temos que o confidence é de 0.84, ou seja, que quando uma pessoa tem o
        income maior dos \$50.000 anuais, a chance dessa pessoa ser homem é de 84%.
    """
    st.markdown(apriori_desc)


    # HEATMAP

    default_features = ['income', 'sex_Male', 'education-num', 'age', 'investment_status', 'race_Black', 'race_White']
    selected_features = st.multiselect("Selecione os atributos para o Heatmap", df.columns.tolist(), default=default_features)
    
    st.title('Matriz de Correlação Heatmap')
    if selected_features:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[selected_features].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Selecione pelo menos um atributo para exibir o Heatmap.")

    desc_placeholder_heatmap = st.empty()

    heatmap_desc = f"""
        **Descrição do Heatmap:**
        O Gráfico de correlação Heatmap mostrado acima apresenta as correlações entre as seguintes variáveis: {', '.join(selected_features)}.
        As correlações presentes vão de -1 a 1, em que quando a correlação entre 2 atributos é mais perto de 1, indica-se uma correlação positiva,
        enquanto uma correlação mais perto de -1, obtemos uma correlação negativa entre essas 2 variáveis.
        Como destque nesse gráfico, percebe-se uma correlação de 0.22 entre os atributos “Income” e “sex_male”, e de 0.35 entre “Income” e “education”,
        que representando relações fraca e moderada respectivamente, assim ressaltando a hipotese de haver uma correlação significativa entre essas variáveis. 

        """
    desc_placeholder_heatmap.markdown(heatmap_desc)

# ################## PÁGINA DA Distribuição PCA dos Dados ##################
    st.write("## Distribuição PCA dos Dados - Hipótese 1 - A renda dos indivíduos está diretamente relacionada a sua educação e seu gênero")

    chart_placeholder_pca = st.empty()
    desc_placeholder_pca = st.empty()

    # Obtém a lista de colunas numéricas
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    # Define os índices padrão para "income" e "sex_Male"
    default_color_index = numeric_columns.index("income") if "income" in numeric_columns else 0
    default_shape_index = numeric_columns.index("sex_Male") if "sex_Male" in numeric_columns else 0

    # Seleção interativa das colunas para colorir e definir o símbolo dos pontos
    color_feature = st.selectbox("Escolha a coluna para colorir os pontos:", numeric_columns, index=default_color_index)
    shape_feature = st.selectbox("Escolha a coluna para definir a forma dos pontos:", numeric_columns, index=default_shape_index)
    
    # Cria uma cópia do DataFrame para realizar o PCA
    dataPCA = df.copy()
    numerical_features = dataPCA.select_dtypes(include=['number'])
    
    # Padroniza os dados
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numerical_features)
    
    # Aplica o PCA para reduzir os dados a 3 componentes principais
    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(scaled_data)
    
    # Adiciona os componentes principais ao DataFrame
    dataPCA['PC1'] = pca_result[:, 0]
    dataPCA['PC2'] = pca_result[:, 1]
    dataPCA['PC3'] = pca_result[:, 2]
    
    # Cria o gráfico 3D interativo usando Plotly Express com novas cores e bordas nos pontos
    figPCA = px.scatter_3d(
        dataPCA, 
        x='PC1', y='PC2', z='PC3',
        color=color_feature,
        symbol=shape_feature,
        color_continuous_scale="Viridis",  # Paleta de cores
        title="Visualização 3D dos Componentes Principais",
        labels={"PC1": "Componente Principal 1", "PC2": "Componente Principal 2", "PC3": "Componente Principal 3"}
    )

    # Adiciona borda aos pontos
    figPCA.update_traces(marker=dict(size=6, line=dict(width=2, color='black')))  

    # Atualiza o layout para melhor contraste
    figPCA.update_layout(
        width=1000, height=800,
        scene=dict(
            xaxis=dict(backgroundcolor="rgb(230, 230, 230)"),  # Fundo do eixo X
            yaxis=dict(backgroundcolor="rgb(230, 230, 230)"),  # Fundo do eixo Y
            zaxis=dict(backgroundcolor="rgb(230, 230, 230)"),  # Fundo do eixo Z
        ),
        coloraxis_colorbar=dict(title=color_feature)  # Ajusta legenda da cor
    )

    # Exibe o gráfico no Streamlit
    chart_placeholder_pca.plotly_chart(figPCA, use_container_width=True)

    # Adiciona a descrição
    pca_desc = f"""
        **Descrição do Gráfico PCA:**
        O gráfico acima apresenta uma visualização em 3 dimensões de todos os dados presentes na dataframe.
        Esse gráfico foi gerado com o Principal Component Analysis, onde é realizada uma redução (resumo) de todas as
        features presentes para apenas 3, permitindo assim essa visualização.
        Através do gráfico também podemos observar que as cores e as formas mudam conforme a variável selecionada.
        Nesse caso, as variáveis escolhidas para essa visualização são {color_feature} para cores e {shape_feature} para formato.
        Com base nesse gráfico, quando selecionamos para ver o contraste entre o income e o sex_Male, conseguimos ver de modo ainda melhor
        que os pontos azuis (renda anual superior a \$50.000) possuem mais círculos (homens) do que quadrados (mulheres). 
    """
    desc_placeholder_pca.markdown(pca_desc)




# ################## PÁGINA DA COMPARAÇÃO DOS IMIGRANTES ##################
elif menu == "Hipotese 2":
    st.write("## Comparação de Países - Hipótese 2 - Imigrantes recebem menos que norte-americanos")

    # Initialize default values
    countries = df["native-country-name"].unique()
    default_group_a = ["United-States"]
    default_group_b = []
    
    # Create placeholders for the charts
    chart_placeholder_1 = st.empty()
    desc_placeholder_1 = st.empty()
    chart_placeholder_2 = st.empty()
    desc_placeholder_2 = st.empty()
    
    # Population info placeholder
    # population_info = st.empty()

    # ==================== SELECAO DOS PAISES ====================
    st.write("### Configuração da Análise")
    
    paises_sem_usa = ["Haiti", "Cuba", "Jamaica", "Mexico", "Dominican-Republic", "Peru", "Puerto-Rico", "Honduras", "Ecuador", "El-Salvador", "Guatemala", "Trinadad&Tobago", "Nicaragua", "China", "India", "Philippines", "Cambodia", "Thailand", "Laos", "Taiwan", "Japan", "Vietnam", "Hong", "England", "Germany", "Poland", "Portugal", "France", "Italy", "Scotland", "Greece", "Ireland", "Hungary", "Holand-Netherlands", "Yugoslavia", "Canada", "Iran", "Columbia", "South"]
    paises_latinos = ["Haiti", "Cuba", "Jamaica", "Mexico", "Dominican-Republic", "Peru", "Puerto-Rico", "Honduras", "Ecuador", "El-Salvador", "Guatemala", "Trinadad&Tobago", "Nicaragua"]
    paises_asiaticos = ["China", "India", "Philippines", "Cambodia", "Thailand", "Laos", "Taiwan", "Japan", "Vietnam", "Hong"]
    paises_europeus = ["England", "Germany", "Poland", "Portugal", "France", "Italy", "Scotland", "Greece", "Ireland", "Hungary", "Holand-Netherlands", "Yugoslavia"]
    
    coluna1_paises, coluna2_paises = st.columns(2)
    
    with coluna1_paises:
        group_a = st.multiselect("Selecione os países do Grupo A", countries, default=default_group_a)

    # Initialize selected countries set
    selected_countries = set()

    st.write("### Grupos de Seleção")
    st.write("#### Todos os imigrantes")
    select_all_sem_usa = st.checkbox("Selecionar todos os países menos os EUA para o Grupo B", value=True)

    st.write("#### Regiões")
    select_all_latinos = st.checkbox("Selecionar todos os Países **Latinos** para o Grupo B", value=False)
    select_all_asiaticos = st.checkbox("Selecionar todos os Países **Asiáticos** para o Grupo B", value=False)
    select_all_europeus = st.checkbox("Selecionar todos os Países **Europeus** para o Grupo B", value=False)

    if select_all_sem_usa:
        selected_countries.update(paises_sem_usa)
    if select_all_latinos:
        selected_countries.update(paises_latinos)
    if select_all_asiaticos:
        selected_countries.update(paises_asiaticos)
    if select_all_europeus:
        selected_countries.update(paises_europeus)

    with coluna2_paises:
        group_b = st.multiselect("Selecione os países do Grupo B", countries, default=list(selected_countries))

    workclassesPais = [
        "Qualquer área de trabalho",
        "workclass_Local-gov", "workclass_Private", "workclass_Self-emp-inc",
        "workclass_Self-emp-not-inc", "workclass_State-gov", "workclass_Without-pay"
    ]

    selected_workclass = st.selectbox("Selecione a classe de trabalho:", workclassesPais)

    # Data processing
    if selected_workclass == "Qualquer área de trabalho":
        df_group_a = df[df['native-country-name'].isin(group_a)].copy()
        df_group_b = df[df['native-country-name'].isin(group_b)].copy()
    else:
        df_group_a = df[(df['native-country-name'].isin(group_a)) & (df[selected_workclass] == 1)].copy()
        df_group_b = df[(df['native-country-name'].isin(group_b)) & (df[selected_workclass] == 1)].copy()

    # Update population info
    population_a = len(df_group_a)
    population_b = len(df_group_b)
    
    # population_info.markdown(f"""
    # População total do **Grupo A**: {population_a}  
    # População total do **Grupo B**: {population_b}
    # """)

    # Validation check
    if not group_a or not group_b:
        st.warning("⚠️ Selecione pelo menos um país em cada grupo. ⚠️")

    # ==================== GRAFICO 1 ====================
    df_income_groups = pd.concat([
        pd.DataFrame({'is_from_group_a': "Paises do Grupo A", 'income': df_group_a['income'], 'total': 1}),
        pd.DataFrame({'is_from_group_a': "Paises do Grupo B", 'income': df_group_b['income'], 'total': 1})
    ], ignore_index=True)

    df_income_groups = df_income_groups.groupby(['is_from_group_a', 'income'], as_index=False).sum()
    df_income_groups = df_income_groups.sort_values("income")

    income_labels = {
        0: "Renda Anual Menor que $50.000",
        1: "Renda Anual Maior que $50.000"
    }
    df_income_groups["income"] = df_income_groups["income"].map(income_labels)

    pattern_shapes = {
        "Renda Anual Menor que $50.000": ".",
        "Renda Anual Maior que $50.000": "x"
    }

    df_income_groups['group_total_income'] = df_income_groups.groupby('is_from_group_a')['total'].transform('sum')
    df_income_groups['percent'] = df_income_groups['total'] / df_income_groups['group_total_income'] * 100

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
            "Renda Anual Menor que $50.000": "red",
            "Renda Anual Maior que $50.000": "green"
        }
    )

    fig_income.update_yaxes(title_text="Percentual (%)", range=[0, 100])

    # ==================== GRAFICO 2 ====================
    df_education_groups = pd.concat([
        pd.DataFrame({'is_from_group_a': "Paises do Grupo A", 'education-num': df_group_a['education-num'], 'total': 1}),
        pd.DataFrame({'is_from_group_a': "Paises do Grupo B", 'education-num': df_group_b['education-num'], 'total': 1})
    ], ignore_index=True)

    df_education_groups = df_education_groups.groupby(['is_from_group_a', 'education-num'], as_index=False).sum()
    df_education_groups = df_education_groups.sort_values("education-num")

    df_education_groups['education-num'] = df_education_groups['education-num'].replace(0, 0.125)
    df_education_groups['education-num'] = df_education_groups['education-num'].replace(0.375, 0.625)
    df_education_groups['education-num'] = df_education_groups['education-num'].replace(0.5, 0.625)

    education_labels = {
        0.125: "Médio Não Iniciado/Incompleto",
        0.25: "Médio Completo",
        0.625: "Superior Incompleto/Técnico",
        0.75: "Bacharel",
        0.875: "Mestrado",
        1: "Doutorado"
    }
    df_education_groups["education-num"] = df_education_groups["education-num"].map(education_labels)

    pattern_shapes = {
        "Médio Não Iniciado/Incompleto": ".",
        "Médio Completo": "x",
        "Superior Incompleto/Técnico": "+",
        "Bacharel": "\\",
        "Mestrado": "|",
        "Doutorado": "/"
    }

    df_education_groups['group_total_education'] = df_education_groups.groupby('is_from_group_a')['total'].transform('sum')
    df_education_groups['percent'] = df_education_groups['total'] / df_education_groups['group_total_education'] * 100

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

    fig_education.update_yaxes(title_text="Percentual (%)", range=[0, 100])

    # ==================== PLOTS E DESCRICOES ====================
    col1_placeholder_pais, col2_placeholder_pais = st.columns(2)

    with col1_placeholder_pais:
        chart_placeholder_1.plotly_chart(fig_income)

        subset_a = df_income_groups[df_income_groups['is_from_group_a'] == 'Paises do Grupo A']['percent']
        porcentagem_a_mais50k = 0
        if len(subset_a) > 1:
            porcentagem_a_mais50k = subset_a.iloc[1]
        
        subset_b = df_income_groups[df_income_groups['is_from_group_a'] == 'Paises do Grupo B']['percent']
        porcentagem_b_mais50k = 0
        if len(subset_b) > 1:
            porcentagem_b_mais50k = subset_b.iloc[1]

        
        income_desc = f"""
        **Descrição do Gráfico de Renda:**
        Este gráfico compara a distribuição de renda entre as populações originárias de diferentes grupos de países e que estão vivendo nos Estados Unidos da América.
        Para o primeiro grupo, entitulado de **Grupo A** e composto por: {', '.join(group_a)}; Temos as informações de **{population_a}** pessoas, das quais 
        **{porcentagem_a_mais50k:.1f}%** da população ganha mais de \$50.000 por ano.
        Enquanto isso, no **Grupo B**, formado por: {', '.join(group_b)}; Observa-se que das **{population_b}** pessoas desse grupo, apenas 
        **{porcentagem_b_mais50k:.1f}%** delas ganham mais de \$50.000 por ano.
        """
        desc_placeholder_1.markdown(income_desc)

    with col2_placeholder_pais:
        chart_placeholder_2.plotly_chart(fig_education)

        if not group_a or not group_b:
            education_desc = f""" Selecione os paises nos dois Grupos para obter a descrição completa """
        else:
            education_desc = f"""
            **Descrição do Gráfico de Educação:**
            Este gráfico compara os níveis educacionais entre os dois grupos de países selecioandos.
            No primeiro grupo, chamado de **Grupo A**, temos os dados de **{population_a}** pessoas originárias de: {', '.join(group_a)}. 
            E para o segundo grupo, entitulado de **Grupo B**, apresenta-se os dados de **{population_b}** pessoas nascidas no(s) seguinte(s) país(es): {', '.join(group_b)}.
            Através das proporções apresentadas nos gráficos, 
            percebe-se que no Grupo A, **{(df_education_groups['percent'][0]+df_education_groups['percent'][1]):.1f}%** da população nem sequer possui o Ensino Médio Completo,
            em comparação, no Grupo B, **{(df_education_groups['percent'][9]+df_education_groups['percent'][10]):.1f}%** da população está nessa mesma categoria.
            Observa-se também, com relação ao número de pessoas que apenas possuem o Ensino Médio, que **{df_education_groups['percent'][2]:.1f}%** das pessoas do Grupo A e **{df_education_groups['percent'][11]:.1f}%** das pessoas no Grupo B se encontram nessa categoria.
            Já no Ensino Técnico ou Superior Incompleto, encontram-se **{(df_education_groups['percent'][3]+df_education_groups['percent'][4]+df_education_groups['percent'][5]):.1f}%** das pessoas do Grupo A e **{(df_education_groups['percent'][12]+df_education_groups['percent'][13]+df_education_groups['percent'][14]):.1f}%** das pessoas no Grupo B.
            Agora com o Ensino Superior Completo, **{df_education_groups['percent'][6]:.1f}%** das pessoas do Grupo A possuem esse diploma enquanto essa proporção é de **{df_education_groups['percent'][15]:.1f}%** no Grupo B.
            E com relação a Pós-Graduações, o Grupo A é composto em **{df_education_groups['percent'][7]:.1f}% de mestres e {df_education_groups['percent'][8]:.1f}%** de doutores.
            Enquanto no Grupo B esse valor é de **{df_education_groups['percent'][16]:.1f}%** e **{df_education_groups['percent'][17]:.1f}%** respectivamente.
            """
        
        desc_placeholder_2.markdown(education_desc)





# ################## PÁGINA DA Distribuição DA COMPARAÇÃO DE HORAS ##################
if menu == "Hipotese 3":
    st.write("## Comparação de Horas - Hipótese 3 - A quantidade de horas trabalhadas por semana não está relacionada à renda do indivíduo")

    # Use columns to display the two figures side by side at the top of the page
    col1, col2 = st.columns(2)
    chart_placeholder_horas = col1.empty()
    stats_placeholder_horas = col2.empty()

    desc_placeholder_horas = st.empty()

    # Opções de filtro
    workclassesHoras = [
        "Qualquer área de trabalho", "workclass_Local-gov", "workclass_Private", "workclass_Self-emp-inc",
        "workclass_Self-emp-not-inc", "workclass_State-gov", "workclass_Without-pay"
    ]
    selected_workclass = st.selectbox("Selecione a classe de trabalho:", workclassesHoras)

    education_labels = {
        0.125: "Médio Não Iniciado/Incompleto",
        0.25: "Médio Completo",
        0.625: "Superior Incompleto/Técnico",
        0.75: "Bacharel",
        0.875: "Mestrado",
        1: "Doutorado"
    }

    # Slider que permite selecionar um intervalo (range) dentre os valores definidos
    education_range = st.select_slider(
        "Selecione o intervalo de education-num:",
        options=list(education_labels.keys()),
        value=(min(education_labels.keys()), max(education_labels.keys())),
        format_func=lambda x: education_labels[x]
    )

    # Filtragem dos dados com base no intervalo selecionado
    filtered_df = df[(df["education-num"] >= education_range[0]) & (df["education-num"] <= education_range[1])]

    # Filtragem por classe de trabalho (lembrando que os dados estão distribuídos em colunas)
    if selected_workclass != "Qualquer área de trabalho":
        filtered_df = filtered_df[filtered_df[selected_workclass] == 1]
    
    # Criar o violin plot
    figHoras, ax = plt.subplots(figsize=(7, 5))
    sns.violinplot(x="income", y="hours-per-week", data=filtered_df, ax=ax)
    
    # Gerar a tabela de estatísticas
    # st.write("### Estatísticas dos Dados Filtrados")
    income_groups = [0, 1]
    stats_summary = {
        "Total de pessoas selecionadas": {},
        "Faixa de educação escolhida": {},
        "Área de trabalho escolhida": {},
        "Menos de 40h Semanais (%)": {},
        "Exatamente 40h Semanais (%)": {},
        "Mais de 40h Semanais (%)": {}
    }

    for income_value in income_groups:
        income_df = filtered_df[filtered_df["income"] == income_value]
        total = len(income_df)
        stats_summary["Total de pessoas selecionadas"][income_value] = total
        stats_summary["Faixa de educação escolhida"][income_value] = f"{education_range}"
        stats_summary["Área de trabalho escolhida"][income_value] = selected_workclass

        percent_0 = (income_df["hours-per-week"] == 0).sum() / total * 100 if total > 0 else 0
        percent_0_5 = (income_df["hours-per-week"] == 0.5).sum() / total * 100 if total > 0 else 0
        percent_1 = (income_df["hours-per-week"] == 1).sum() / total * 100 if total > 0 else 0

        stats_summary["Menos de 40h Semanais (%)"][income_value] = f"{percent_0:.1f}%"
        stats_summary["Exatamente 40h Semanais (%)"][income_value] = f"{percent_0_5:.1f}%"
        stats_summary["Mais de 40h Semanais (%)"][income_value] = f"{percent_1:.1f}%"

    stats_summary_df = pd.DataFrame(stats_summary).T
    stats_summary_df.columns = ["Renda Anual Inferior a $50.000", "Renda Anual Superior a $50.000"]

    chart_placeholder_horas.pyplot(figHoras)
    stats_placeholder_horas.write(stats_summary_df)

    horas_desc = f"""
        **Descrição do Violin Plot e da Tabela dos dados com base nas Horas:**
        O gráfico Violin Plot apresentado acima mostra a comparação entre as distribuições da quantidade de pessoas que 
        trabalham menos de 40 horas semanais, exatamante 40 horas semanais e mais de 40 horas semanais com base na renda
        que elas possuem, podendo ser mais de \$50.000 anuais ou menos de \$50.000 anuais.
        Neste Gráfico específico, em conjunto com a tabela ao lado, pode-se observar que considerando apenas as pessoas
        que trabalham na área de: {selected_workclass}, e, possuem um nível de escolaridade entre {education_range[0]}
        e {education_range[1]}, temos que para as pessoas com renda inferior a \$50.000 anuais, 
        {stats_summary["Menos de 40h Semanais (%)"][0]} delas trabalham menos de 40 horas semanais, 
        {stats_summary["Exatamente 40h Semanais (%)"][0]} delas trabalham exatamente 40 horas semanais e
        {stats_summary["Mais de 40h Semanais (%)"][0]} delas trabalham mais de 40 horas semanais.
        Já no grupo das pessoas que tem renda anual superior a \$50.000, observa-se que: 
        {stats_summary["Menos de 40h Semanais (%)"][1]} delas trabalham menos de 40 horas semanais, 
        {stats_summary["Exatamente 40h Semanais (%)"][1]} delas trabalham exatamente 40 horas semanais e
        {stats_summary["Mais de 40h Semanais (%)"][1]} delas trabalham mais de 40 horas semanais.
        """
    desc_placeholder_horas.markdown(horas_desc)




# ################## PÁGINA DA COMPARAÇÃO DE GENERO ##################
if menu == "Hipotese 4":
    st.write("## Comparação de Gênero - Hipótese 4 - Mulheres recebem menos que homens mesmo se filtrarmos por horas trabalhadas e nível de escolaridade")

    chart_placeholder_genero = st.empty()
    desc_placeholder_genero = st.empty()

    # Lista de classes de trabalho
    workclassesGenero = [
        "Qualquer área de trabalho",
        "workclass_Local-gov", "workclass_Private", "workclass_Self-emp-inc",
        "workclass_Self-emp-not-inc", "workclass_State-gov", "workclass_Without-pay"
    ]

    # Caixa de seleção para escolher a classe de trabalho
    selected_workclass = st.selectbox("Selecione a classe de trabalho:", workclassesGenero)

    # Caixa de seleção para escolher o valor de hours-per-week
    hours_values = [0, 0.5, 1, "Todos"] # menos de 40h, igual a 40h, mais de 40h
    selected_hours = st.selectbox("Selecione a carga horária (hours-per-week):", hours_values)

    # Filtragem por classe de trabalho
    if selected_workclass != "Qualquer área de trabalho":
        df_filtered = df[df[selected_workclass] == 1]  # Filtra pela classe de trabalho selecionada
    else:
        df_filtered = df  # Considera todos os dados

    # Filtragem por hours-per-week
    if selected_hours != "Todos":
        df_filtered = df_filtered[df_filtered["hours-per-week"] == selected_hours]

    # Contagem total de homens e mulheres no conjunto filtrado
    total_women = len(df_filtered[df_filtered['sex_Male'] == 0])
    total_men = len(df_filtered[df_filtered['sex_Male'] == 1])

    # Contagem de mulheres e homens com income == 1
    women_with_income = len(df_filtered[(df_filtered['sex_Male'] == 0) & (df_filtered['income'] == 1)])
    men_with_income = len(df_filtered[(df_filtered['sex_Male'] == 1) & (df_filtered['income'] == 1)])

    # Cálculo da porcentagem
    women_income_percentage = (women_with_income / total_women) * 100 if total_women > 0 else 0
    men_income_percentage = (men_with_income / total_men) * 100 if total_men > 0 else 0

    # Exibição dos resultados
    st.write(f"🔹 **De um total de {total_women} mulheres, {women_income_percentage:.2f}% delas ganham mais de \$50k, trabalham na área de: {selected_workclass}, por {selected_hours} horas/semana):**")
    st.write(f"🔹 **De um total de {total_men} homens, {men_income_percentage:.2f}% delas ganham mais de \$50k, trabalham na área de: {selected_workclass}, por {selected_hours} horas/semana):**")

    procentagem_pizza_mulher = (women_income_percentage * 100) / (women_income_percentage+men_income_percentage)
    procentagem_pizza_homem = (men_income_percentage * 100) / (women_income_percentage+men_income_percentage)


    # Criando o gráfico de pizza
    fig_genero, ax = plt.subplots(figsize=(2, 2))
    labels = ["Mulheres", "Homens"]
    sizes = [women_income_percentage, men_income_percentage]
    colors = ["#ff9999", "#66b3ff"]  # Cores para mulheres e homens
    explode = (0.1, 0)  # Destacar fatia das mulheres
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90, explode=explode, shadow=True)
    ax.set_title("Comparação de Probabilidade de Renda Anual Superior a $50.000")


    chart_placeholder_genero.pyplot(fig_genero)

    genero_desc = f"""
        **Descrição do Gráfico de Renda por Gênero:**
        O gráfico mostrado acima é um gráfico de Pizza que apresenta a proporção entre Homens e Mulheres que ganham salários anuais superiores a \$50.000 anuais.
        Ele foi construído com base na probabilidade de Homens e Mulheres, que trabalham na mesma área de atuação ({selected_workclass}),
        e com a mesma quantidade de Horas Semanais ({selected_hours}) ganharem mais de \$50.000 anuais.
        Nessa representação específica, temos que das {total_women} mulheres que atuam nessa área por essas horas, apenas {women_income_percentage:.1f}% ganham acima dos \$50.000 anuais.
        Enquanto para os Homens nessa mesma área de atuação e que trabalham pela mesma área, verificamos que existem {total_men} homens nessa categoria,
        dos quais {men_income_percentage:.1f}% recebem acima dos \$50.000 anuais.
        Assim, considerando a soma dessas porcentagens ({women_income_percentage:.1f} e {men_income_percentage:.1f}), é feita a construção do Gráfico de Pizza.
        Dessa forma, as porcentagens contidas nesse gráfico indicam que:
        A proporção dos indivíduos mulheres que recebem mais de \$50.000, trabalha na área da {selected_workclass}, por {selected_hours} semanais é de: {procentagem_pizza_mulher:.1f}%.
        Enquanto a proporção dos homens com essas mesmas características é de: {procentagem_pizza_homem:.1f}%.
        """
    desc_placeholder_genero.markdown(genero_desc)



# ################## PÁGINA DA COMPARAÇÃO DE INVESTIMENTOS ##################
if menu == "Hipotese 5":
    st.write("## Comparação de Investimentos - Hipótese 5 - Indivíduos mais jovens se arriscam mais com investimentos do que indivíduos que são mais velhos")

    chart_placeholder_investimento = st.empty()
    desc_placeholder_investimentos = st.empty()

    # Exibir os gráficos
    # coluna_investimento1, coluna_investimento2 = st.columns(2)
    # with coluna_investimento1:
    #     st.plotly_chart(fig1, use_container_width=True)
    # with coluna_investimento2:
    #     st.plotly_chart(fig2, use_container_width=True)

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
    
    fig_investimento, (ax_cdf, ax_pdf) = plt.subplots(ncols=2, figsize=(12, 4))

    # Gráfico CDF (Distribuição Acumulada)
    sns.kdeplot(df_filtered['investment_status_naoDiscretizado'], cumulative=True, fill=True, ax=ax_cdf)
    ax_cdf.axhline(y=probability / 100, color='r', linestyle='--', label=f'Probabilidade: {probability:.2f}%')
    ax_cdf.set_title("CDF: Distribuição Acumulada")
    ax_cdf.set_xlabel("Investment Status")
    ax_cdf.set_ylabel("Probabilidade Acumulada")
    ax_cdf.legend()

    # Gráfico PDF (Densidade de Probabilidade)
    sns.kdeplot(df_filtered['investment_status_naoDiscretizado'], cumulative=False, fill=True, ax=ax_pdf)
    ax_pdf.axvline(x=investment_threshold, color='r', linestyle='--', label=f'Investimento: ${investment_threshold}')
    ax_pdf.set_title("PDF: Densidade de Probabilidade")
    ax_pdf.set_xlabel("Investment Status")
    ax_pdf.set_ylabel("Densidade")
    ax_pdf.legend()
    
    chart_placeholder_investimento.pyplot(fig_investimento)

    investimento_desc = f"""
        **Descrição do Gráfico de Renda:**
        O gráfico presente apresenta a Distribuição Acumulada dos valores obtidos com investimentos pelas população que participiou do Senso Demográfico.
        Nessa amostragem estão inclusas as pessoas cuja idade é superior a {selected_age_min} anos de idade e inferior a {selected_age_max} anos de idade.
        Também é mostrado um valor de limite mínimo de lucro obtido com investimentos para servir como base para cálculos de probabilidade.
        O limite selecionado é de \${investment_threshold}, ou seja, através do gráfico é demonstrado que a probabilidade de alguém entre {selected_age_min} e {selected_age_max} anos
        possuir um lucro superior a \${investment_threshold} é de {probability:.2f}%.
        """
    desc_placeholder_investimentos.markdown(investimento_desc)
