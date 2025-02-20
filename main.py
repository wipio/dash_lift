import streamlit as st
from supabase import create_client, Client
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .main {
        width: 1000px;
        margin: 0 auto;
    }
    </style>
    """, 
    unsafe_allow_html=True
)


# Credenciais do Supabase
url = "https://iwnrbylqsyvlthozydfq.supabase.co"  # Substitua pela sua URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3bnJieWxxc3l2bHRob3p5ZGZxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNjA3NzU4NywiZXhwIjoyMDQxNjUzNTg3fQ.H6bCnk4BOwZgXMKBX8eEjmtCbpxdsWuWDDleH8oXApo"  # Substitua pela sua chave de API

# Definir credenciais fixas
USERNAME = "admin"
PASSWORD = "1234"

# Criar sessão para login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Tela de login
if not st.session_state.logged_in:
    st.title("Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")
else:

    # Conectar ao Supabase
    supabase: Client = create_client(url, key)

    # Função para puxar os dados da tabela
    def get_data_from_supabase():
        # Substitua 'sua_tabela' pelo nome da sua tabela no Supabase
        response = supabase.table('escola_lift').select('*').execute()

        # Verifica se há dados e retorna ou exibe um erro
        if response.data:
            return response.data
        else:
            st.error(f"Erro ao acessar dados: {response.error}")
            return None

    # Puxar os dados
    data = get_data_from_supabase()

    # Exibir os dados em formato de tabela no Streamlit
    if data:   
        df = pd.DataFrame(data)
        
        st.title("📊 Dashboard de Contatos")
        
        df = pd.DataFrame(data)
        df['data_contato'] = pd.to_datetime(df["data_contato"], format='%d/%m/%Y')
        df_sorted = df.sort_values(by='data_contato', ascending=False)
        df['data_contato'] = df['data_contato'].dt.strftime('%d/%m/%Y')
        st.title("Dashboard")
        st.write("### Dados dos Alunos")
        edited_df = st.data_editor(df, hide_index=True,
            num_rows="fixed", 
            key="table_editor", 
            column_config={
                "contato": st.column_config.CheckboxColumn("Contato Efetuado")  # Checkbox interativo
            },
            disabled=["id", "aluno", "data_contato", "numero_contato", "status_cancelamento"]  # Bloqueia edições nessas colunas
        )

        col1, col2 = st.columns(2)

        # 🔹 Gráfico 1: Distribuição de Cancelamentos (Pizza)
        with col1:
            st.subheader("Cancelamentos")
            cancel_counts = df["status_cancelamento"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(cancel_counts, labels=["Ativo", "Cancelado"], autopct="%1.1f%%", colors=["green", "red"])
            ax1.set_title("Distribuição de Cancelamentos")
            st.pyplot(fig1)

        # 🔹 Gráfico 2: Contatos ao Longo do Tempo (Linha)
        with col2:
            st.subheader("Evolução de Contatos")
            contatos_por_dia = df["data_contato"].value_counts().sort_index()
            fig2, ax2 = plt.subplots()
            sns.lineplot(x=contatos_por_dia.index, y=contatos_por_dia.values, ax=ax2, marker="o")
            ax2.set_title("Contatos por Data")
            ax2.set_xlabel("Data")
            ax2.set_ylabel("Número de Contatos")
            ax2.tick_params(axis="x", rotation=45)
            st.pyplot(fig2)

        # Criando segunda linha do layout
        # col3, col4 = st.columns(2)

        # # 🔹 Gráfico 3: Contatos por Aluno (Barras)
        # with col3:
        #     st.subheader("Contatos por Aluno")
        #     contatos_por_aluno = df["aluno"].value_counts().head(10)  # Exibe apenas os 10 primeiros
        #     fig3, ax3 = plt.subplots()
        #     sns.barplot(x=contatos_por_aluno.values, y=contatos_por_aluno.index, ax=ax3, palette="viridis")
        #     ax3.set_title("Top 10 Alunos Mais Contatados")
        #     ax3.set_xlabel("Número de Contatos")
        #     ax3.set_ylabel("Aluno")
        #     st.pyplot(fig3)

        # # 🔹 Gráfico 4: Distribuição dos Prefixos Telefônicos (Histograma)
        # with col4:
        df_col4 = df
        st.subheader("Prefixos de Contato")
        df_col4["prefixo"] = df_col4["numero_contato"].astype(str).str[:4]
        prefixo_counts = df_col4["prefixo"].value_counts()
        fig4, ax4 = plt.subplots()
        sns.barplot(x=prefixo_counts.index, y=prefixo_counts.values, ax=ax4, palette="coolwarm")
        ax4.set_title("Distribuição dos Prefixos")
        ax4.set_xlabel("Prefixo")
        ax4.set_ylabel("Quantidade")
        st.pyplot(fig4)
        
        

