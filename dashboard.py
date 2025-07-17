import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Configuração inicial
st.set_page_config(page_title="Dados socioeconômicos", layout="wide", page_icon="📊")

# Estilização customizada do multiselect
st.markdown("""
    <style>
    /* Cor de fundo dos itens selecionados (padrão é vermelho) */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: lightblue !important;  /* light sky blue */
        color: black !important;
    }

    /* Aumentar largura e quantidade visível de caracteres */
    .stMultiSelect {
        max-width: 100% !important;
        width: 100% !important;
    }

    .stMultiSelect div[role="combobox"] {
        min-height: 38px;
        font-size: 16px !important;
        border: 1px solid lightblue !important; 
    }

    /* Aumentar fonte das opções */
    .stMultiSelect span {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Carregar o dataset
df = pd.read_csv("sgdata.csv", sep=";")

st.sidebar.title("🎛️ Opções do Dashboard")

opcoes_graficos = [
    "Distribuição por Sexo",
    "Média de Renda por Sexo",
    "Distribuição por Educação e Idade",
    "Distribuição por Idade e Sexo",
    "Distribuição das Idades",
    "Distribuição da Renda"
]

selecionados = st.sidebar.multiselect("Selecione os gráficos que deseja visualizar:", opcoes_graficos)

# Preparações
df_filtrado = df[df['Education'] != 'other / unknown']
agrupado = df_filtrado.groupby(['Age', 'Education']).size().reset_index(name='Quantidade')
agrupadoAS = df.groupby(['Age', 'Sex']).size().reset_index(name='Quantidade')
sexo_map = {0: "Feminino", 1: "Masculino"}
agrupadoAS['Sexo'] = agrupadoAS['Sex'].map(sexo_map)
df["Sexo"] = df["Sex"].map(sexo_map)

# Gráfico 1 e 2: lado a lado se ambos forem selecionados
if "Distribuição por Sexo" in selecionados and "Média de Renda por Sexo" in selecionados:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição por Sexo")
        sexo_fig = px.histogram(df, x="Sexo", color="Sexo",
                                color_discrete_map={"Feminino": "pink", "Masculino": "lightblue"})
        sexo_fig.update_yaxes(title_text="Quantidade de pessoas")
        st.plotly_chart(sexo_fig, use_container_width=True)

    with col2:
        st.subheader("Média de Renda por Sexo")
        renda_fig = px.bar(df.groupby("Sexo")["Income"].mean().reset_index(),
                           x="Sexo", y="Income", color="Sexo",
                           labels={"Income": "Média da Renda", "Sexo": "Sexo"},
                           color_discrete_map={"Feminino": "pink", "Masculino": "lightblue"})
        st.plotly_chart(renda_fig, use_container_width=True)

# Se apenas um dos dois for selecionado
elif "Distribuição por Sexo" in selecionados:
    st.subheader("Distribuição por Sexo")
    sexo_fig = px.histogram(df, x="Sexo", color="Sexo",
                            color_discrete_map={"Feminino": "pink", "Masculino": "lightblue"})
    sexo_fig.update_yaxes(title_text="Quantidade de pessoas")
    st.plotly_chart(sexo_fig, use_container_width=True)

elif "Média de Renda por Sexo" in selecionados:
    st.subheader("Média de Renda por Sexo")
    renda_fig = px.bar(df.groupby("Sexo")["Income"].mean().reset_index(),
                       x="Sexo", y="Income", color="Sexo",
                       labels={"Income": "Média da Renda", "Sexo": "Sexo"},
                       color_discrete_map={"Feminino": "pink", "Masculino": "lightblue"})
    st.plotly_chart(renda_fig, use_container_width=True)

# Gráfico 3
if "Distribuição por Educação e Idade" in selecionados:
    st.subheader("Distribuição de Pessoas por Educação e Idade")
    fig = px.line(
        agrupado,
        x='Age',
        y='Quantidade',
        color='Education',
        markers=True,
        labels={'Age': 'Idade', 'Quantidade': 'Quantidade de Pessoas', 'Education': 'Nível de Educação'},
        color_discrete_map={"high school": "deepskyblue", "graduate school": "orange", "university": "green"}
    )
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis=dict(title='Quantidade de Pessoas'),
        legend_title_text='Nível de Educação',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico 4
if "Distribuição por Idade e Sexo" in selecionados:
    st.subheader("Distribuição de Pessoas por Idade e Sexo")
    fig = px.line(
        agrupadoAS,
        x='Age',
        y='Quantidade',
        color='Sexo',
        labels={'Age': 'Idade', 'Quantidade': 'Quantidade de Pessoas', 'Sexo': 'Sexo'},
        color_discrete_map={'Feminino': 'pink', 'Masculino': 'lightblue'},
        markers=True
    )
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis_title='Quantidade de Pessoas',
        legend_title_text='Sexo',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráficos 5 e 6: lado a lado se ambos forem selecionados
if "Distribuição das Idades" in selecionados and "Distribuição da Renda" in selecionados:
    st.title("Distribuições")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Distribuição das Idades")
        fig_idade = px.histogram(
            df,
            x="Age",
            nbins=30,
            color_discrete_sequence=["lightblue"],
            title="Distribuição das idades"
        )
        fig_idade.update_traces(marker_line_color="black", marker_line_width=1)
        fig_idade.update_layout(
            xaxis_title="Idades",
            yaxis_title="Quantidade de Pessoas",
            template="plotly_white"
        )
        st.plotly_chart(fig_idade, use_container_width=True)

    with col4:
        st.subheader("Distribuição da Renda")
        fig_renda = px.histogram(
            df,
            x="Income",
            nbins=30,
            color_discrete_sequence=["pink"],
            title="Distribuição da Renda"
        )
        fig_renda.update_traces(marker_line_color="black", marker_line_width=1)
        fig_renda.update_layout(
            xaxis_title="Renda",
            yaxis_title="Quantidade de Pessoas",
            template="plotly_white"
        )
        st.plotly_chart(fig_renda, use_container_width=True)

# Apenas um dos dois selecionado
elif "Distribuição das Idades" in selecionados:
    st.subheader("Distribuição das Idades")
    fig_idade = px.histogram(
        df,
        x="Age",
        nbins=30,
        color_discrete_sequence=["lightblue"],
        title="Distribuição das idades"
    )
    fig_idade.update_traces(marker_line_color="black", marker_line_width=1)
    fig_idade.update_layout(
        xaxis_title="Idades",
        yaxis_title="Quantidade de Pessoas",
        template="plotly_white"
    )
    st.plotly_chart(fig_idade, use_container_width=True)

elif "Distribuição da Renda" in selecionados:
    st.subheader("Distribuição da Renda")
    fig_renda = px.histogram(
        df,
        x="Income",
        nbins=30,
        color_discrete_sequence=["pink"],
        title="Distribuição da Renda"
    )
    fig_renda.update_traces(marker_line_color="black", marker_line_width=1)
    fig_renda.update_layout(
        xaxis_title="Renda",
        yaxis_title="Quantidade de Pessoas",
        template="plotly_white"
    )
    st.plotly_chart(fig_renda, use_container_width=True)

st.sidebar.markdown("## 🧠 Agrupamentos")

mostrar_cluster_completo = st.sidebar.checkbox("Agrupamento: Idade + Renda + Educação")
mostrar_cluster_simples = st.sidebar.checkbox("Agrupamento: Idade + Educação")
mostrar_cluster_sexo = st.sidebar.checkbox("Agrupamento: Sexo + Educação + Renda")

# Agrupamento COMPLETO (Idade, Renda, Educação)
if mostrar_cluster_completo:
    st.subheader("🧠 Agrupamento Completo com KMeans")
    st.markdown("Agrupamento baseado em **Idade**, **Renda** e **Educação**.")

    df_cluster = df[["Age", "Income", "Education"]].copy()
    df_cluster["EducationLimpo"] = df_cluster["Education"].str.strip().str.lower()

    education_map = {
        "high school": 1,
        "university": 2,
        "graduate school": 3
    }
    df_cluster["EducationCode"] = df_cluster["EducationLimpo"].map(education_map)

    # Remover valores ausentes ou não mapeados
    df_cluster = df_cluster.dropna(subset=["Age", "Income", "EducationCode"])

    features = df_cluster[["Age", "Income", "EducationCode"]]

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df_cluster["Cluster"] = kmeans.fit_predict(features_scaled)

    reverse_education_map = {v: k for k, v in education_map.items()}
    df_cluster["EducationNome"] = df_cluster["EducationCode"].map(reverse_education_map)

    tipo_grafico = st.radio("Escolha o tipo de gráfico:", ["Gráfico 2D", "Gráfico 3D"])

    if tipo_grafico == "Gráfico 2D":
        fig_cluster_2d = px.scatter(
            df_cluster,
            x="Age",
            y="Income",
            color="Cluster",
            hover_data=["EducationNome"],
            labels={"Age": "Idade", "Income": "Renda", "EducationNome": "Educação"},
            title="Agrupamento Socioeconômico (2D)"
        )
        st.plotly_chart(fig_cluster_2d, use_container_width=True)

    elif tipo_grafico == "Gráfico 3D":
        fig_cluster_3d = px.scatter_3d(
            df_cluster,
            x="Age",
            y="Income",
            z="EducationCode",
            color="Cluster",
            hover_data=["EducationNome"],
            labels={"Age": "Idade", "Income": "Renda", "EducationCode": "Educação"},
            title="Agrupamentos Socioeconômicos (3D)"
        )
        fig_cluster_3d.update_layout(scene=dict(
            zaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3],
                ticktext=["Ensino Médio", "Universidade", "Pós-graduação"]
            )
        ))
        st.plotly_chart(fig_cluster_3d, use_container_width=True)

# Agrupamento SIMPLES (Idade, Educação)
if mostrar_cluster_simples:
    st.subheader("🧠 Agrupamento Simples (Idade + Educação)")

    df_simples = df[["Age", "Education"]].copy()
    df_simples["EducationLimpo"] = df_simples["Education"].str.strip().str.lower()

    education_map = {
        "high school": 1,
        "university": 2,
        "graduate school": 3
    }
    df_simples["EducationCode"] = df_simples["EducationLimpo"].map(education_map)

    df_simples = df_simples.dropna(subset=["Age", "EducationCode"])

    features_simples = df_simples[["Age", "EducationCode"]]

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_simples)

    kmeans_simples = KMeans(n_clusters=3, random_state=42)
    df_simples["Cluster"] = kmeans_simples.fit_predict(features_scaled)

    fig_simples = px.scatter(
        df_simples,
        x="Age",
        y="EducationCode",
        color="Cluster",
        labels={"Age": "Idade", "EducationCode": "Educação"},
        title="Agrupamento Simples (2D)",
        color_continuous_scale="Viridis"
    )
    fig_simples.update_layout(yaxis=dict(
        tickmode='array',
        tickvals=[1, 2, 3],
        ticktext=["Ensino Médio", "Universidade", "Pós-graduação"]
    ))
    st.plotly_chart(fig_simples, use_container_width=True)

# Agrupamento: Sexo + Educação + Renda
if mostrar_cluster_sexo:
    st.subheader("🧠 Agrupamento: Sexo + Educação + Renda")

    df_sexo = df[["Sex", "Education", "Income"]].copy()
    df_sexo["EducationLimpo"] = df_sexo["Education"].str.strip().str.lower()

    education_map = {
        "high school": 1,
        "university": 2,
        "graduate school": 3
    }
    sexo_map_num = {
        0: 0,  # feminino
        1: 1   # masculino
    }

    # Mapear sexo numérico
    df_sexo = df_sexo.dropna(subset=["Sex", "Education", "Income"])
    df_sexo["SexCode"] = df_sexo["Sex"].map(sexo_map_num)
    df_sexo["EducationCode"] = df_sexo["EducationLimpo"].map(education_map)

    # Remover linhas com dados faltantes após mapear
    df_sexo = df_sexo.dropna(subset=["SexCode", "EducationCode", "Income"])

    features_sexo = df_sexo[["SexCode", "EducationCode", "Income"]]

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_sexo)

    kmeans_sexo = KMeans(n_clusters=3, random_state=42)
    df_sexo["Cluster"] = kmeans_sexo.fit_predict(features_scaled)

    reverse_education_map = {v: k for k, v in education_map.items()}
    df_sexo["EducationNome"] = df_sexo["EducationCode"].map(reverse_education_map)

    tipo_grafico_sexo = st.radio(
        "Escolha o tipo de gráfico:",
        ["Gráfico 2D", "Gráfico 3D"],
        key="tipo_grafico_sexo"
    )

    if tipo_grafico_sexo == "Gráfico 2D":
        fig_sexo_2d = px.scatter(
            df_sexo,
            x="SexCode",
            y="Income",
            color="Cluster",
            hover_data=["EducationNome"],
            labels={
                "SexCode": "Sexo",
                "Income": "Renda",
                "EducationNome": "Educação",
                "Cluster": "Cluster"
            },
            title="Agrupamento: Sexo + Educação + Renda (2D)"
        )
        fig_sexo_2d.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=["Feminino", "Masculino"]
            ),
            yaxis_title="Renda"
        )
        st.plotly_chart(fig_sexo_2d, use_container_width=True)

    elif tipo_grafico_sexo == "Gráfico 3D":
        fig_sexo_3d = px.scatter_3d(
            df_sexo,
            x="SexCode",
            y="EducationCode",
            z="Income",
            color="Cluster",
            hover_data=["EducationNome"],
            labels={
                "SexCode": "Sexo",
                "EducationCode": "Educação",
                "Income": "Renda",
                "Cluster": "Cluster"
            },
            title="Agrupamento: Sexo + Educação + Renda (3D)"
        )
        fig_sexo_3d.update_layout(scene=dict(
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=["Feminino", "Masculino"]
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3],
                ticktext=["Ensino Médio", "Universidade", "Pós-graduação"]
            ),
            zaxis=dict(
                title="Renda"
            )
        ))
        st.plotly_chart(fig_sexo_3d, use_container_width=True)


