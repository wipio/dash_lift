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
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

# Definir credenciais fixas
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["SENHA"]

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
        
        st.markdown("<h1 style='color: #BD93F9;'>📊 Dashboard de Contatos</h1>", unsafe_allow_html=True)
        
        df = pd.DataFrame(data)
        df['data_contato'] = pd.to_datetime(df["data_contato"], format='%d/%m/%Y')
        df = df.sort_values(by='data_contato', ascending=False)
        df['data_contato'] = df['data_contato'].dt.strftime('%d/%m/%Y')
        
        st.markdown("<h3 style='color: #BD93F9;'>Dados dos alunos</h1>", unsafe_allow_html=True)

        
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
            
            st.markdown("<h3 style='color: #BD93F9;'>Cancelamentos</h1>", unsafe_allow_html=True)
                  
            cancel_counts = df["status_cancelamento"].value_counts()
        
            fig1, ax1 = plt.subplots(figsize=(12, 8), facecolor='#1E1E2E')

            # Definindo as cores
            cores = ['#5B2E91', '#A57BB5']  # Roxo escuro e roxo claro

            # Configurar o gráfico
            wedges, texts, autotexts = ax1.pie(
                cancel_counts, 
                labels=["Ativo", "Cancelado"], 
                autopct='%1.1f%%', 
                startangle=140,
                colors=cores,  # Usando as cores personalizadas
                wedgeprops={'edgecolor': '#44475A', 'linewidth': 2},
                textprops={'fontsize': 12, 'color': '#F8F8F2'},
                pctdistance=0.85
            )

            # Adicionar círculo central para transformar em gráfico de rosca
            fig1.patch.set_alpha(0)

            # Adicionar título e estilo visual
            ax1.set_title('Distribuição de Cancelamentos', fontsize=18, fontweight='bold', pad=20, color='#BD93F9')

            # Adicionar um rodapé
            fig1.text(0.5, 0.02, 'Análise de Cancelamentos - 2024', ha='center', fontsize=12, color='#6272A4')

            plt.tight_layout()

            # Exibir o gráfico
            st.pyplot(fig1)

        # 🔹 Gráfico 2: Contatos ao Longo do Tempo (Linha)
        with col2:
            st.markdown("<h3 style='color: #BD93F9;'>Evolução de Contatos</h1>", unsafe_allow_html=True)
            
            contatos_por_dia = df["data_contato"].value_counts().sort_index()

            # Criando a figura e o gráfico
            fig2, ax2 = plt.subplots()

            # Criando o gráfico de linha
            sns.lineplot(x=contatos_por_dia.index, y=contatos_por_dia.values, ax=ax2, marker="o", color='#5B2E91')

            # Remover fundo
            fig2.patch.set_facecolor('none')  # Remove o fundo da figura
            ax2.patch.set_facecolor('none')   # Remove o fundo da área de plotagem

            # Alterando cor das referências para roxo
            ax2.set_title("Contatos por Data", color='#BD93F9')
            ax2.set_xlabel("Data", color='#BD93F9')
            ax2.set_ylabel("Número de Contatos", color='#BD93F9')
            
            # Modificando as bordas
            ax2.spines['top'].set_visible(False)  # Remove a borda superior
            ax2.spines['right'].set_visible(False)  # Remove a borda direita
            ax2.spines['left'].set_linewidth(2)  # Aumenta a espessura da borda esquerda
            ax2.spines['left'].set_color('#BD93F9')  # Cor da borda esquerda
            ax2.spines['bottom'].set_linewidth(2)  # Aumenta a espessura da borda inferior
            ax2.spines['bottom'].set_color('#BD93F9')  # Cor da borda inferior
            
            # Modificando as ticks (referências) dos eixos
            ax2.tick_params(axis="x", rotation=45, labelcolor='#BD93F9', labelsize=10)
            ax2.tick_params(axis="y", labelcolor='#BD93F9', labelsize=10)
            
            # Forçar o eixo Y para ser inteiros
            ax2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            
            ax2.set_xticks(contatos_por_dia.index[::10])
            

            # Rotacionando as labels do eixo X
            ax2.tick_params(axis="x", rotation=45)

            # Exibindo o gráfico no Streamlit
            st.pyplot(fig2)

        # # 🔹 Gráfico 4: Distribuição dos Prefixos Telefônicos (Histograma)
        # Criando a coluna "prefixo"
        df_col4 = df
        st.markdown("<h3 style='color: #BD93F9;'>Prefixos de Contato</h1>", unsafe_allow_html=True)

        # Criando a coluna "prefixo"
        regioes = { '11': '(SP)', '12': '(SP)', '13': '(SP)', '14': '(SP)', '15': '(SP)', '16': '(SP)', '17': '(SP)', '18': '(SP)', '19': '(SP)', 
            '21': '(RJ)', '22': '(RJ)', '24': '(RJ)', 
            '31': '(MG)', '32': '(MG)', '33': '(MG)', '34': '(MG)', '35': '(MG)', '37': '(MG)', '38': '(MG)', 
            '41': '(PR)', '42': '(PR)', '43': '(PR)', '44': '(PR)', '45': '(PR)', '46': '(PR)', 
            '51': '(RS)', '53': '(RS)', '54': '(RS)', '55': '(RS)', 
            '61': '(DF)', '62': '(GO)', '63': '(TO)', '64': '(GO)', '65': '(MT)', '66': '(MT)', '67': '(MS)', 
            '71': '(BA)', '73': '(BA)', '74': '(BA)', '75': '(BA)', '77': '(BA)', 
            '81': '(PE)', '82': '(AL)', '83': '(PB)', '84': '(RN)', '85': '(CE)', '86': '(PI)', '87': '(PE)', '88': '(CE)', 
            '91': '(PA)', '92': '(AM)', '93': '(PA)', '94': '(PA)', '95': '(RR)', '96': '(AP)', '97': '(AM)', '98': '(MA)', '99': '(MA)' }



        # Criando a coluna 'prefixo' com os primeiros 2 dígitos do número
        df_col4["prefixo"] = df_col4["numero_contato"].astype(str).str[:2]

        # Adicionando a coluna de 'região' com base no prefixo
        df_col4["regiao"] = df_col4["prefixo"].map(regioes).fillna("Outros")

        # Contagem das regiões
        regiao_counts = df_col4["regiao"].value_counts()

        # Criando a figura e o gráfico de barras
        fig4, ax4 = plt.subplots()

        # Gráfico de barras com a paleta de cores "coolwarm"
        sns.barplot(x=regiao_counts.index, y=regiao_counts.values, ax=ax4, palette="coolwarm")

        # Removendo o fundo
        fig4.patch.set_facecolor('none')  # Remove o fundo da figura
        ax4.patch.set_facecolor('none')   # Remove o fundo da área de plotagem

        # Alterando o título e as labels
        ax4.set_title("Distribuição dos Prefixos por Região", color='#BD93F9')
        ax4.set_xlabel("Região", color='#BD93F9', fontsize=12)
        ax4.set_ylabel("Quantidade", color='#BD93F9', fontsize=12)

        # Modificando as bordas
        ax4.spines['top'].set_visible(False)  # Remove a borda superior
        ax4.spines['right'].set_visible(False)  # Remove a borda direita
        ax4.spines['left'].set_linewidth(2)  # Aumenta a espessura da borda esquerda
        ax4.spines['left'].set_color('#BD93F9')  # Cor da borda esquerda
        ax4.spines['bottom'].set_linewidth(2)  # Aumenta a espessura da borda inferior
        ax4.spines['bottom'].set_color('#BD93F9')  # Cor da borda inferior

        # Modificando as ticks (referências) dos eixos
        ax4.tick_params(axis="x", rotation=45, labelcolor='#BD93F9', labelsize=10)
        ax4.tick_params(axis="y", labelcolor='#BD93F9', labelsize=10)

        # Forçar o eixo Y para ser inteiros
        ax4.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

        # Exibindo o gráfico no Streamlit
        st.pyplot(fig4)


        

