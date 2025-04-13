import streamlit as st
import pandas as pd
from datetime import datetime
from database import Database
import plotly.express as px
import io

# Configuração de tema personalizado
st.set_page_config(
    page_title="Brigadeiros & Cia - Controle Financeiro",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    /* Cores principais */
    :root {
        --cor-vinho: #800020;
        --cor-dourado: #D4AF37;
        --cor-bege-claro: #FFF8E7;
        --cor-marrom-claro: #F5E6E8;
        --cor-texto: #2C1810;
        --cor-destaque: #B76E79;
    }

    /* Reset de alguns estilos do Streamlit */
    .stApp {
        background: linear-gradient(135deg, var(--cor-bege-claro) 0%, var(--cor-marrom-claro) 100%);
    }

    .main-title {
        color: var(--cor-vinho);
        font-family: 'Playfair Display', serif;
        text-align: center;
        font-size: 3rem;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: 1px;
    }

    .subtitle {
        color: var(--cor-vinho);
        font-family: 'Playfair Display', serif;
        text-align: center;
        font-size: 2rem;
        margin: 1.5rem 0;
        opacity: 0.9;
    }

    /* Cards e Containers */
    .stTabs {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Métricas */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: var(--cor-vinho) !important;
        font-weight: bold !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: var(--cor-texto) !important;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }

    /* Cards de métricas */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    /* Botões */
    .stButton > button {
        background: linear-gradient(45deg, var(--cor-vinho), var(--cor-destaque));
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, var(--cor-destaque), var(--cor-vinho));
    }

    /* Inputs e Selects */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: white;
        color: var(--cor-texto);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
        padding: 0.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--cor-vinho);
        box-shadow: 0 0 0 2px rgba(128, 0, 32, 0.1);
    }

    /* DataFrames */
    .stDataFrame {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .stDataFrame [data-testid="stTable"] {
        width: 100%;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 8px;
        padding: 0.5rem 2rem;
        color: var(--cor-texto);
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--cor-marrom-claro);
        border-color: var(--cor-vinho);
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--cor-vinho) !important;
        color: white !important;
        border-color: var(--cor-vinho) !important;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: white;
        padding: 2rem 1rem;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }

    /* Forms */
    form {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Texto de valor total */
    .valor-total {
        color: var(--cor-vinho);
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background-color: var(--cor-marrom-claro);
        border-radius: 8px;
    }

    /* Mensagens de sucesso e erro */
    .stSuccess, .stError {
        padding: 1rem;
        border-radius: 8px;
        font-weight: 500;
    }

    /* Estilo para os containers de registros */
    .registro-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    /* Estilo para o botão de editar */
    .edit-button {
        background-color: var(--cor-vinho);
        color: white;
        border: none;
        padding: 0.15rem 0.3rem;
        border-radius: 4px;
        font-size: 0.6rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .edit-button:hover {
        background-color: var(--cor-destaque);
        transform: translateY(-1px);
    }

    /* Estilo para os valores nos registros */
    .valor-registro {
        font-family: 'Roboto Mono', monospace;
        color: var(--cor-vinho);
        font-weight: 500;
    }

    .data-registro {
        color: #666;
        font-size: 0.9rem;
    }

    .produto-registro {
        color: var(--cor-texto);
        font-weight: 500;
    }

    .quantidade-registro {
        color: var(--cor-destaque);
        font-weight: 500;
    }

    /* Estilo para as métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    .metric-value {
        font-size: 1.8rem;
        color: var(--cor-vinho);
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 1rem;
        color: var(--cor-texto);
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# Importação da fonte Playfair Display
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Inicialização do banco de dados
db = Database()

# Inicialização das variáveis de estado
if 'editando_compra' not in st.session_state:
    st.session_state.editando_compra = None
if 'editando_venda' not in st.session_state:
    st.session_state.editando_venda = None

# Função para carregar dados de um arquivo
def carregar_dados(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    return None

# Sidebar com opções de upload/download
with st.sidebar:
    st.header("Gerenciamento de Dados")
    
    # Upload de dados
    st.subheader("Carregar Dados")
    uploaded_compras = st.file_uploader("Carregar Compras (CSV)", type=['csv'], key='upload_compras')
    uploaded_vendas = st.file_uploader("Carregar Vendas (CSV)", type=['csv'], key='upload_vendas')
    
    if uploaded_compras:
        df_compras = carregar_dados(uploaded_compras)
        if df_compras is not None:
            st.session_state.compras = df_compras
            st.success("Dados de compras carregados com sucesso!")
    
    if uploaded_vendas:
        df_vendas = carregar_dados(uploaded_vendas)
        if df_vendas is not None:
            st.session_state.vendas = df_vendas
            st.success("Dados de vendas carregados com sucesso!")
    
    # Download de dados
    st.subheader("Baixar Dados")
    if st.button("Baixar Compras (CSV)"):
        csv = st.session_state.compras.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Compras",
            data=csv,
            file_name='compras.csv',
            mime='text/csv'
        )
    
    if st.button("Baixar Vendas (CSV)"):
        csv = st.session_state.vendas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Vendas",
            data=csv,
            file_name='vendas.csv',
            mime='text/csv'
        )

# Função para formatar valores monetários
def formatar_moeda(value):
    return f"CLP {value:,.0f}"

# Título principal com estilo personalizado
st.markdown('<h1 class="main-title">🧁 Brigadeiros & Cia</h1>', unsafe_allow_html=True)

# Criação das abas
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🛍️ Compras", "💰 Vendas"])

# Aba Dashboard
with tab1:
    st.markdown('<h2 class="subtitle">Dashboard Financeiro</h2>', unsafe_allow_html=True)
    
    # Métricas do mês atual em cards elegantes
    col1, col2, col3 = st.columns(3)
    
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    total_compras = db.obter_total_mes('compras', mes_atual, ano_atual)
    total_vendas = db.obter_total_mes('vendas', mes_atual, ano_atual)
    lucro = total_vendas - total_compras
    
    with col1:
        st.metric("💳 Total de Compras", formatar_moeda(total_compras))
    with col2:
        st.metric("💰 Total de Vendas", formatar_moeda(total_vendas))
    with col3:
        st.metric("📈 Lucro Estimado", formatar_moeda(lucro))
    
    # Últimas transações
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="subtitle" style="font-size: 1.5rem;">📋 Últimas Compras</h3>', unsafe_allow_html=True)
        ultimas_compras = db.obter_ultimos_registros('compras')
        if not ultimas_compras.empty:
            for idx, compra in ultimas_compras.iterrows():
                st.markdown(f"""
                <div class="registro-container">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="data-registro">{compra['data']}</span><br>
                            <span class="produto-registro">{compra['produto']}</span><br>
                            <span class="quantidade-registro">Qtd: {compra['quantidade']}</span>
                            <span class="valor-registro">{formatar_moeda(compra['valor_total'])}</span>
                        </div>
                        <button class="edit-button" onclick="editar_compra_{compra['id']}()">✏️</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão invisível que será acionado pelo JavaScript
                if st.button('✏️', key=f'edit_compra_{compra["id"]}', help="Editar compra"):
                    st.session_state.editando_compra = compra['id']
                    st.rerun()
    
    with col2:
        st.markdown('<h3 class="subtitle" style="font-size: 1.5rem;">📋 Últimas Vendas</h3>', unsafe_allow_html=True)
        ultimas_vendas = db.obter_ultimos_registros('vendas')
        if not ultimas_vendas.empty:
            for idx, venda in ultimas_vendas.iterrows():
                st.markdown(f"""
                <div class="registro-container">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="data-registro">{venda['data']}</span><br>
                            <span class="produto-registro">{venda['produto']}</span><br>
                            <span class="quantidade-registro">Qtd: {venda['quantidade']}</span>
                            <span class="valor-registro">{formatar_moeda(venda['valor_total'])}</span>
                        </div>
                        <button class="edit-button" onclick="editar_venda_{venda['id']}()">✏️</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão invisível que será acionado pelo JavaScript
                if st.button('✏️', key=f'edit_venda_{venda["id"]}', help="Editar venda"):
                    st.session_state.editando_venda = venda['id']
                    st.rerun()

# Aba Compras
with tab2:
    st.markdown('<h2 class="subtitle">Registro de Compras</h2>', unsafe_allow_html=True)
    
    # Se estiver editando uma compra
    if st.session_state.editando_compra is not None:
        compra = db.obter_compra_por_id(st.session_state.editando_compra)
        st.subheader("✏️ Editando Compra")
        
        with st.form("form_editar_compra"):
            col1, col2 = st.columns(2)
            
            with col1:
                data_compra = st.date_input("Data da Compra", value=pd.to_datetime(compra['data']).date())
                produto = st.text_input("Produto Comprado", value=compra['produto'])
                quantidade = st.number_input("Quantidade", min_value=0.0, step=0.1, value=float(compra['quantidade']))
            
            with col2:
                valor_unitario = st.number_input("Valor Unitário (CLP)", min_value=0, value=int(compra['valor_unitario']))
                compra_mista = st.checkbox("Compra Mista", value=compra['compra_mista'])
                observacao = st.text_area("Observação", value=compra['observacao'], height=100)
            
            valor_total = quantidade * valor_unitario
            st.markdown(f'<p class="valor-total">Valor Total: {formatar_moeda(valor_total)}</p>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Salvar Alterações"):
                    db.editar_compra(
                        st.session_state.editando_compra,
                        data_compra,
                        produto,
                        quantidade,
                        valor_unitario,
                        valor_total,
                        observacao,
                        compra_mista
                    )
                    st.session_state.editando_compra = None
                    st.success("✅ Compra atualizada com sucesso!")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancelar Edição"):
                    st.session_state.editando_compra = None
                    st.rerun()
    
    # Se não estiver editando, mostra o formulário normal de compras
    else:
        with st.form("form_compras"):
            col1, col2 = st.columns(2)
            
            with col1:
                data_compra = st.date_input("📅 Data da Compra", datetime.now())
                produto = st.text_input("🏷️ Produto Comprado")
                quantidade = st.number_input("📦 Quantidade", min_value=0.0, step=0.1)
            
            with col2:
                valor_unitario = st.number_input("💲 Valor Unitário (CLP)", min_value=0)
                compra_mista = st.checkbox("🛒 Compra Mista (mercado de casa junto)")
                observacao = st.text_area("📝 Observação", height=100)
            
            valor_total = quantidade * valor_unitario
            st.markdown(f'<p class="valor-total">Valor Total: {formatar_moeda(valor_total)}</p>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("💾 Registrar Compra")
            
            if submitted:
                if produto and quantidade > 0 and valor_unitario > 0:
                    db.adicionar_compra(
                        data_compra,
                        produto,
                        quantidade,
                        valor_unitario,
                        valor_total,
                        observacao,
                        compra_mista
                    )
                    st.success("✅ Compra registrada com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Por favor, preencha todos os campos obrigatórios.")

# Aba Vendas
with tab3:
    st.markdown('<h2 class="subtitle">Registro de Vendas</h2>', unsafe_allow_html=True)
    
    # Se estiver editando uma venda
    if st.session_state.editando_venda is not None:
        venda = db.obter_venda_por_id(st.session_state.editando_venda)
        st.subheader("✏️ Editando Venda")
        
        with st.form("form_editar_venda"):
            col1, col2 = st.columns(2)
            
            with col1:
                data_venda = st.date_input("Data da Venda", value=pd.to_datetime(venda['data']).date())
                produto = st.text_input("Produto Vendido", value=venda['produto'])
                quantidade = st.number_input("Quantidade", min_value=1, step=1, value=int(venda['quantidade']))
            
            with col2:
                preco_unitario = st.number_input("Preço Unitário (CLP)", min_value=0, value=int(venda['preco_unitario']))
                forma_pagamento = st.selectbox(
                    "Forma de Pagamento",
                    ["Dinheiro", "PIX", "Transferência", "Outro"],
                    index=["Dinheiro", "PIX", "Transferência", "Outro"].index(venda['forma_pagamento'])
                )
                observacao = st.text_area("Observação", value=venda['observacao'], height=100)
            
            valor_total = quantidade * preco_unitario
            st.markdown(f'<p class="valor-total">Valor Total: {formatar_moeda(valor_total)}</p>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Salvar Alterações"):
                    db.editar_venda(
                        st.session_state.editando_venda,
                        data_venda,
                        produto,
                        quantidade,
                        preco_unitario,
                        valor_total,
                        forma_pagamento,
                        observacao
                    )
                    st.session_state.editando_venda = None
                    st.success("✅ Venda atualizada com sucesso!")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancelar Edição"):
                    st.session_state.editando_venda = None
                    st.rerun()
    
    # Se não estiver editando, mostra o formulário normal de vendas
    else:
        with st.form("form_vendas"):
            col1, col2 = st.columns(2)
            
            with col1:
                data_venda = st.date_input("📅 Data da Venda", datetime.now())
                produto = st.text_input("🧁 Produto Vendido")
                quantidade = st.number_input("📦 Quantidade", min_value=1, step=1)
            
            with col2:
                preco_unitario = st.number_input("💲 Preço Unitário (CLP)", min_value=0)
                forma_pagamento = st.selectbox(
                    "💳 Forma de Pagamento",
                    ["Dinheiro", "PIX", "Transferência", "Outro"]
                )
                observacao = st.text_area("📝 Observação", height=100)
            
            valor_total = quantidade * preco_unitario
            st.markdown(f'<p class="valor-total">Valor Total: {formatar_moeda(valor_total)}</p>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("💾 Registrar Venda")
            
            if submitted:
                if produto and quantidade > 0 and preco_unitario > 0:
                    db.adicionar_venda(
                        data_venda,
                        produto,
                        quantidade,
                        preco_unitario,
                        valor_total,
                        forma_pagamento,
                        observacao
                    )
                    st.success("✅ Venda registrada com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Por favor, preencha todos os campos obrigatórios.")

# Sidebar para exportação de relatórios
with st.sidebar:
    st.markdown('<h2 class="subtitle" style="font-size: 1.5rem;">📊 Relatórios</h2>', unsafe_allow_html=True)
    mes = st.selectbox("📅 Mês", range(1, 13), datetime.now().month - 1)
    ano = st.number_input("📅 Ano", min_value=2020, max_value=2030, value=datetime.now().year)
    formato = st.selectbox("📑 Formato", ["csv", "excel"])
    
    if st.button("📥 Exportar Relatório"):
        try:
            compras_file, vendas_file = db.exportar_relatorio_mensal(mes, ano, formato)
            st.success(f"""✅ Relatórios exportados com sucesso!
            \nArquivos gerados:
            \n📄 {compras_file}
            \n📄 {vendas_file}""")
        except Exception as e:
            st.error(f"❌ Erro ao exportar relatórios: {str(e)}")

# Gráficos
st.markdown("---")
st.header("Análise de Dados")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de vendas por forma de pagamento
    if not st.session_state.vendas.empty:
        vendas_por_pagamento = st.session_state.vendas.groupby('forma_pagamento')['valor_total'].sum().reset_index()
        fig = px.pie(
            vendas_por_pagamento,
            values='valor_total',
            names='forma_pagamento',
            title='Vendas por Forma de Pagamento'
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Gráfico de produtos mais vendidos
    if not st.session_state.vendas.empty:
        produtos_mais_vendidos = st.session_state.vendas.groupby('produto')['quantidade'].sum().reset_index()
        fig = px.bar(
            produtos_mais_vendidos,
            x='produto',
            y='quantidade',
            title='Produtos Mais Vendidos'
        )
        st.plotly_chart(fig, use_container_width=True)

# Estilo CSS personalizado
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .st-emotion-cache-16idsys p {
        font-size: 16px;
    }
    .st-emotion-cache-1v0mbdj > img {
        width: 64px;
        height: 64px;
    }
</style>
""", unsafe_allow_html=True) 