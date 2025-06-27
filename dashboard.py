import streamlit as st
import pandas as pd
import plotly.express as px

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

st.title("Dados socioeconômicos")

# Filtro de seleção de gráficos
opcoes_graficos = [
    "Distribuição por Sexo",
    "Média de Renda por Sexo",
    "Distribuição por Educação e Idade",
    "Distribuição por Idade e Sexo",
    "Distribuição das Idades",
    "Distribuição da Renda"
]

selecionados = st.multiselect("Selecione os gráficos que deseja visualizar:", opcoes_graficos)

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