import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Análise de dados", layout="wide")
st.markdown("<h1 style='font-size: 30px;'>Dashboard de vendas e investimentos</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 20px;'>Análise do desempenho das vendas e investimentos</h3>", unsafe_allow_html=True)
st.sidebar.title("Filtros")

caminho_arquivo = "Dashboard de investimento.csv"
df=pd.read_csv(caminho_arquivo)
print(df)



st.columns(4)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de  Investimento\n(Custo)", f"$ {df['Investimento (Custo)'].sum():,.0f}")   
with col2:
    st.metric("Total de Lucro", f"$ {df['Lucro'].sum():,.0f}")
with col3:
    total = df["Descrição do Trabalho"].count()
    st.metric("Total de Trabalhos", f"{total}")
with col4:
    st.metric("Lucro média por\nprojecto", f"$ {df['Lucro'].mean():,.0f}")    

# ======================
# CSS e helpers de estilo
# ======================
st.markdown("""
    <style>
        /* Fundo principal da aplicação */
        .stApp {
            background-color: #add8e6 !important; /* Azul claro do teu tema */
        }

        /* SIDEBAR (fundo e texto) */
        [data-testid="stSidebar"] {
            background-color: #1e3d59 !important; /* Azul escuro */
            color: white !important;
        }
        /* Garantir que todo texto no sidebar fique branco */
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* REMOVER fundo branco do container do multiselect / selectbox */
        [data-baseweb="select"],            /* baseweb select container */
        [data-testid="stSidebar"] .stSelectbox, 
        [data-testid="stSidebar"] .stMultiSelect,
        div[role="combobox"],               /* alguns selects usam combobox */
        div[role="listbox"],
        ul[role="listbox"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Dropdown aberto (lista de opções) */
        ul[role="listbox"], div[role="listbox"], div[role="option"], li[role="option"] {
            background-color: #1e3d59 !important; /* mesmo azul da sidebar */
            color: white !important;
        }

        /* Chips / tags (os botões com 'Projeto A' etc.) */
        [data-baseweb="tag"], .baseweb-tag, .css-1r6slb3 {
            background-color: #ff4d4d !important;  /* cor do chip (vermelho) */
            color: white !important;
            border-radius: 6px !important;
            padding: 4px 10px !important;
            margin: 3px !important;
        }

        /* Forçar entradas (inputs) transparentes no sidebar */
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea {
            background-color: transparent !important;
            color: white !important;
        }

        /* BOTÕES */
        div.stButton > button {
            background-color: #0a0a0a !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.5em 1.2em !important;
            border-radius: 8px !important;
            border: none !important;
        }
        div.stButton > button:hover {
            background-color: #3742fa !important;
        }

        /* KPI (st.metric) - ajustar cores conforme fundo claro do app */
        [data-testid="stMetric"] {
            background: transparent !important;
        }
        [data-testid="stMetric"] label {
            color: #0b0b0b !important;   /* título da métrica (para contraste no fundo claro) */
        }
        [data-testid="stMetric"] > div:nth-child(2) {
            color: #0b0b0b !important;   /* valor da métrica */
        }

        /* Plotly / containers de gráfico - forçar transparente */
        .stPlotlyChart, .plotly-graph-div, .js-plotly-plot {
            background: transparent !important;
        }

        /* Tabelas / dataframes: remover fundo branco */
        .stTable, .stDataFrame, table {
            background-color: transparent !important;
        }
        .stDataFrame > div, .stTable > div {
            background-color: transparent !important;
        }

        /* Proteções gerais para sombras e bordas brancas */
        .css-1v3fvcr, .css-1d391kg, .css-1v0mbdj {
            background-color: transparent !important;
            box-shadow: none !important;
        }
    </style>
""", unsafe_allow_html=True)


# Função helper para garantir que figuras Plotly sejam transparentes e com texto adequado
def style_plotly(fig, text_color="#0b0b0b"):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",   # fundo interno do gráfico = transparente
        paper_bgcolor="rgba(0,0,0,0)",  # fundo externo (área ao redor) = transparente
        font=dict(color=text_color),
        margin=dict(l=30, r=10, t=40, b=30)
    )
    # também remove qualquer configuração branca residual
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


# Filtros
filtro_Localização = st.sidebar.multiselect(
    "Selecione a Localização",
    options=df["Localização"].unique(),
    default=df["Localização"].unique(),
)

filtro_Trabalhos = st.sidebar.multiselect(
    "Selecione o trabalho",
    options=df["Descrição do Trabalho"].unique(),
    default=df["Descrição do Trabalho"].unique(),
)
filtro_Responsável = st.sidebar.multiselect(
    "Selecione o Responsável", 
    options=df["Responsável"].unique(),
    default=df["Responsável"].unique(),
)

df["Data de Início"] = pd.to_datetime(df['Data de Início'], dayfirst=True)
df["Data de Conclusão"] = pd.to_datetime(df['Data de Conclusão'],dayfirst=True )
df["Período do Projeto"] = (df['Data de Conclusão'] - df['Data de Início']).dt.days
df["Período"] = df["Período do Projeto"].astype(str) + " dias"        

filtro_Período = st.sidebar.multiselect(
    "Selecione o Período do Projeto", 
    options=df["Período"].unique(),
    default=df["Período"].unique(),
)

df_filtrado = df[
    df["Localização"].isin(filtro_Localização) &
    df["Descrição do Trabalho"].isin(filtro_Trabalhos) &
    df["Responsável"].isin(filtro_Responsável) &
    df["Período"].isin(filtro_Período)
]
df_filtrado = df_filtrado.assign(
    **{
        "Data de Início": df_filtrado["Data de Início"].dt.date,
        "Data de Conclusão": df_filtrado["Data de Conclusão"].dt.date
    }
)

st.write("📋 Tabela filtrada")
st.dataframe(df_filtrado[["Localização", "Descrição do Trabalho", "Responsável", "Investimento (Custo)", "Lucro", "Data de Início", "Data de Conclusão", "Período"]], use_container_width=True)

# Gráficos
st.write("📊 Gráficos de análise")
colunas_numericas = df_filtrado.select_dtypes(include="number").columns
df_agrupado = df_filtrado.groupby("Localização")[colunas_numericas].sum().reset_index()
fig_Investimento = px.bar(
    data_frame= df_agrupado ,
    x="Localização",
    y=["Investimento (Custo)", "Lucro"],
    title="<b>Investimento vs Lucro por Localização</b>",
    labels={"value": "Valor em MZN", "Localização": "Localização", "variable": "Legenda"},
    barmode="group",
    
)
fig_Trabalho = px.pie(
    df_filtrado.groupby("Descrição do Trabalho").sum().reset_index(),
    names="Descrição do Trabalho",
    values="Lucro",
    title="<b>Distribuição do Lucro por Tipo de Trabalho</b>",
    labels={"Descrição do Trabalho": "Tipo de Trabalho", "value": "Lucro em MZN"},
)
fig_Trabalho.update_layout(
    legend_title_text="Legenda"
)
df['Data de Início'] = pd.to_datetime(df['Data de Início'], dayfirst=True)
df_agrupado = df.groupby("Data de Início")["Investimento (Custo)"].sum().reset_index()
fig = px.line(
    df_agrupado,
    x="Data de Início", 
    y="Investimento (Custo)",
    title="<b>Investimento ao longo do tempo</b>",
    labels={"Data de Início": "Data", "Investimento (Custo)": "volor em MZN"},
)
fig.update_traces(mode="markers+lines")

fig.update_layout(
    xaxis_title="Data",
    yaxis_title="Investimento em MZN",
    legend_title_text="Legenda",
    xaxis = dict(
        rangeselector = dict(
            buttons = list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider = dict(visible=True),
        type = "date"
    )    
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_Trabalho , use_container_width=True)
with col2:
    st.plotly_chart(fig_Investimento, use_container_width=True)

st.plotly_chart(fig, use_container_width=True)