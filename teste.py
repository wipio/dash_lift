import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.graph_objects as go


url = "https://iwnrbylqsyvlthozydfq.supabase.co"
key = '''eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3bnJieWxxc3l2bHRob3p5ZGZxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNjA3NzU4NywiZXhwIjoyMDQxNjUzNTg3fQ.H6bCnk4BOwZgXMKBX8eEjmtCbpxdsWuWDDleH8oXApo'''

supabase: Client = create_client(url, key)

@st.cache_data
def get_data_from_supabase():
    response = supabase.table('yuri_banco_de_dados_disparo').select('*').execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()




data = get_data_from_supabase()
df = pd.DataFrame(data)

st.title("Dashboard de Disparo de Mensagens da IA")



# Filtro por status
status_filter = st.multiselect("Filtrar por status:", options=df['status'].unique(), default=df['status'].unique())
filtered_df = df[df['status'].isin(status_filter)]
filtered_df['telefone'] = df['telefone'].str.split('@').str[0]



st.dataframe(filtered_df,hide_index=True)


# Contar os status
status_a = df[df['status'] == 'ENVIADO']['status'].tolist()
status_b = df[df['status'] == 'SEM WPP']['status'].tolist()
status_c = df[df['status'].isna()]['status'].tolist()

# Contagens
enviados = len(status_a)
sem_wpp = len(status_b)
com_wpp = enviados
nao_tem_wpp =  len(status_c)
unique_values_count = df['pasta'].nunique()
total_contatos = len(status_a) + len(status_b) + len(status_c)


# Layout com colunas
col1, col2 = st.columns(2)

# Gráfico 1: Enviado vs Sem WPP
with col1:
    fig1 = go.Figure(data=[
        go.Pie(
            labels=['ENVIADO', 'NAO ENVIADO'],
            values=[(enviados + sem_wpp), nao_tem_wpp],
            hole=0.5,
            marker=dict(colors=['#B22222', '#FF4500'])  # Vermelho escuro e vermelho laranja
        )
    ])
    fig1.update_traces(direction='clockwise', pull=[0.05, 0], textfont=dict(color='white'))
    fig1.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        title='Total de Enviados',
    )
    st.plotly_chart(fig1)


# Gráfico 2: Tem WPP vs Não Tem WPP
with col2:
    fig2 = go.Figure(data=[
        go.Pie(labels=['TEM WPP', 'NÃO TEM WPP'], values=[com_wpp, sem_wpp], hole=0.5)
    ])
    fig2.update_traces(direction='clockwise', pull=[0.05, 0], textfont=dict(color='white'))
    fig2.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        title='WhatsApp Disponível',
        font=dict(color='white')
    )
    st.plotly_chart(fig2)
    


col1, col2, col3, col4, col5= st.columns(5)

# Definindo o CSS para personalizar o contêiner
css = """
    <style>
        .stMetric {
            background-color: #2e2e2e;  /* Cor de fundo escura */
            border-radius: 10px;  /* Bordas arredondadas */
            padding: 10px;  /* Espaçamento interno */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);  /* Sombra */
            text-align: center;  /* Centralizando o texto */
        }

        .stMetric .stText {
            color: white;  /* Cor do texto */
        }
    </style>
"""

# Aplicando o CSS
st.markdown(css, unsafe_allow_html=True)

with col1:
    st.metric(label="Total Enviado", value=len(status_a))
    
with col2:
    st.metric(label="Total Sem WPP", value=len(status_b))
    
with col3:
    st.metric(label="Nao Enviado", value=len(status_c))
    
with col4:
    st.metric(label="Total Pastas", value=unique_values_count)
    
with col5:
    st.metric(label="Total de Contatos", value=len(df))



   


