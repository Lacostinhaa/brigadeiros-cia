import streamlit as st
import pandas as pd
from datetime import datetime
from database import Database
import plotly.express as px

# Configuração de tema personalizado
st.set_page_config(
    page_title="Brigadeiros & Cia - Controle Financeiro",
    page_icon="🧁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600&display=swap');

    /* Cores principais */
    :root {
        --cor-vinho: #8B1F41;
        --cor-vinho-escuro: #5E1528;
        --cor-vinho-claro: #B54A6C;
        --cor-dourado: #D4AF37;
        --cor-dourado-claro: #F2D675;
        --cor-bege: #F5E6D3;
        --cor-bege-claro: #FFF8F0;
        --cor-texto: #2C1810;
        --cor-texto-claro: #6B4D45;
        --sombra-suave: 0 4px 12px rgba(0,0,0,0.05);
        --sombra-media: 0 6px 16px rgba(0,0,0,0.1);
        --transicao: all 0.3s ease;
    }

    /* Reset e estilos base */
    .stApp {
        background: linear-gradient(135deg, var(--cor-bege-claro) 0%, var(--cor-bege) 100%);
    }

    /* Títulos */
    .main-title {
        font-family: 'Cormorant Garamond', serif;
        color: var(--cor-vinho);
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 2.5rem 0;
        text-shadow: 2px 2px 4px rgba(139, 31, 65, 0.1);
        letter-spacing: 1.5px;
    }

    .subtitle {
        font-family: 'Cormorant Garamond', serif;
        color: var(--cor-vinho-escuro);
        text-align: center;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 2rem 0;
        letter-spacing: 1px;
    }

    /* Cards e Containers */
    .stTabs {
        background-color: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: var(--sombra-media);
        border: 1px solid rgba(212, 175, 55, 0.1);
    }

    /* Métricas */
    div[data-testid="stMetricValue"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 2rem !important;
        color: var(--cor-vinho) !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.1rem !important;
        color: var(--cor-texto-claro) !important;
        font-weight: 500 !important;
    }

    div[data-testid="stMetricDelta"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1rem !important;
    }

    /* Cards de métricas */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: var(--sombra-suave);
        border: 1px solid rgba(212, 175, 55, 0.15);
        transition: var(--transicao);
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--sombra-media);
        border-color: var(--cor-dourado-claro);
    }

    /* Botões */
    .stButton > button {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(45deg, var(--cor-vinho), var(--cor-vinho-claro));
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.4rem 1.2rem;
        border-radius: 6px;
        transition: var(--transicao);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-size: 0.75rem;
        min-height: 0;
        line-height: 1.2;
        margin: 0 0.3rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(139, 31, 65, 0.2);
        background: linear-gradient(45deg, var(--cor-vinho-claro), var(--cor-vinho));
    }

    /* Inputs e Selects */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div {
        font-family: 'Montserrat', sans-serif;
        background-color: white;
        color: var(--cor-texto);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-size: 0.95rem;
        transition: var(--transicao);
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--cor-vinho);
        box-shadow: 0 0 0 2px rgba(139, 31, 65, 0.1);
    }

    /* Labels */
    .stTextInput > label,
    .stNumberInput > label,
    .stDateInput > label,
    .stSelectbox > label {
        font-family: 'Montserrat', sans-serif;
        color: var(--cor-texto-claro);
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.2rem;
        background-color: transparent;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Montserrat', sans-serif;
        background-color: white;
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 10px;
        padding: 0.8rem 2rem;
        color: var(--cor-texto);
        font-weight: 500;
        transition: var(--transicao);
        letter-spacing: 0.5px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--cor-bege);
        border-color: var(--cor-dourado);
        transform: translateY(-1px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, var(--cor-vinho), var(--cor-vinho-claro)) !important;
        color: white !important;
        border: none !important;
        box-shadow: var(--sombra-suave);
    }

    /* Texto de valor total */
    .valor-total {
        font-family: 'Montserrat', sans-serif;
        color: var(--cor-vinho);
        font-size: 1.6rem;
        font-weight: 600;
        text-align: center;
        margin: 1.5rem 0;
        padding: 1.2rem;
        background: linear-gradient(135deg, var(--cor-bege-claro), var(--cor-bege));
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.15);
        box-shadow: var(--sombra-suave);
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: white;
        border-right: 1px solid rgba(212, 175, 55, 0.1);
        padding: 2rem 1.5rem;
    }

    /* Containers de informações */
    .stMarkdown {
        font-family: 'Montserrat', sans-serif;
    }

    .stMarkdown p {
        color: var(--cor-texto);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Mensagens de sucesso e erro */
    .stSuccess, .stError {
        font-family: 'Montserrat', sans-serif;
        padding: 1rem;
        border-radius: 10px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Importação da fonte Playfair Display
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Inicialização do banco de dados
db = Database()

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
            for index, row in ultimas_compras.iterrows():
                with st.container():
                    if st.session_state.get('editando_compra') == row['id']:
                        with st.form(key=f"edit_compra_form_{row['id']}"):
                            data = st.date_input("Data", 
                                datetime.strptime(row['data'], '%Y-%m-%d').date() if isinstance(row['data'], str) else row['data'],
                                key=f"data_compra_{row['id']}")
                            produto = st.text_input("Produto", row['produto'], key=f"produto_compra_{row['id']}")
                            quantidade = st.number_input("Quantidade", min_value=0.0, step=0.1, value=float(row['quantidade']), key=f"qtd_compra_{row['id']}")
                            valor_unitario = st.number_input("Valor Unitário", min_value=0, value=int(row['valor_unitario']), key=f"valor_compra_{row['id']}")
                            valor_total = quantidade * valor_unitario
                            st.write(f"Valor Total: {formatar_moeda(valor_total)}")
                            
                            if st.form_submit_button("💾 Salvar"):
                                if produto and quantidade > 0 and valor_unitario > 0:
                                    db.editar_compra(
                                        row['id'],
                                        data,
                                        produto,
                                        quantidade,
                                        valor_unitario,
                                        valor_total,
                                        row['observacao'],
                                        row['compra_mista']
                                    )
                                    st.session_state.editando_compra = None
                                    st.rerun()
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state.editando_compra = None
                                st.rerun()
                    else:
                        col_info, col_buttons = st.columns([4, 1])
                        with col_info:
                            st.write(f"📅 {row['data']} | 🏷️ {row['produto']} (x{row['quantidade']}) - {formatar_moeda(row['valor_total'])}")
                        with col_buttons:
                            st.write('<div style="display: flex; gap: 0.5rem;">', unsafe_allow_html=True)
                            if st.button("✏️", key=f"edit_compra_{row['id']}"):
                                st.session_state.editando_compra = row['id']
                                st.rerun()
                            if st.button("🗑️", key=f"del_compra_{row['id']}"):
                                if st.session_state.get('confirmar_exclusao') == row['id']:
                                    db.excluir_registro('compras', row['id'])
                                    st.success("✅ Compra excluída com sucesso!")
                                    st.rerun()
                                else:
                                    st.session_state.confirmar_exclusao = row['id']
                                    st.warning("⚠️ Clique novamente para confirmar")
                            st.write('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 class="subtitle" style="font-size: 1.5rem;">📋 Últimas Vendas</h3>', unsafe_allow_html=True)
        ultimas_vendas = db.obter_ultimos_registros('vendas')
        if not ultimas_vendas.empty:
            for index, row in ultimas_vendas.iterrows():
                with st.container():
                    if st.session_state.get('editando_venda') == row['id']:
                        with st.form(key=f"edit_venda_form_{row['id']}"):
                            data = st.date_input("Data", 
                                datetime.strptime(row['data'], '%Y-%m-%d').date() if isinstance(row['data'], str) else row['data'],
                                key=f"data_venda_{row['id']}")
                            produto = st.text_input("Produto", row['produto'], key=f"produto_venda_{row['id']}")
                            quantidade = st.number_input("Quantidade", min_value=1, step=1, value=int(row['quantidade']), key=f"qtd_venda_{row['id']}")
                            preco_unitario = st.number_input("Preço Unitário", min_value=0, value=int(row['preco_unitario']), key=f"preco_venda_{row['id']}")
                            forma_pagamento = st.selectbox(
                                "Forma de Pagamento",
                                ["Dinheiro", "PIX", "Transferência", "Outro"],
                                index=["Dinheiro", "PIX", "Transferência", "Outro"].index(row['forma_pagamento']),
                                key=f"pagamento_venda_{row['id']}"
                            )
                            valor_total = quantidade * preco_unitario
                            st.write(f"Valor Total: {formatar_moeda(valor_total)}")
                            
                            if st.form_submit_button("💾 Salvar"):
                                if produto and quantidade > 0 and preco_unitario > 0:
                                    db.editar_venda(
                                        row['id'],
                                        data,
                                        produto,
                                        quantidade,
                                        preco_unitario,
                                        valor_total,
                                        forma_pagamento,
                                        row['observacao']
                                    )
                                    st.session_state.editando_venda = None
                                    st.rerun()
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state.editando_venda = None
                                st.rerun()
                    else:
                        col_info, col_buttons = st.columns([4, 1])
                        with col_info:
                            st.write(f"📅 {row['data']} | 🧁 {row['produto']} (x{row['quantidade']}) - {formatar_moeda(row['valor_total'])}")
                        with col_buttons:
                            st.write('<div style="display: flex; gap: 0.5rem;">', unsafe_allow_html=True)
                            if st.button("✏️", key=f"edit_venda_{row['id']}"):
                                st.session_state.editando_venda = row['id']
                                st.rerun()
                            if st.button("🗑️", key=f"del_venda_{row['id']}"):
                                if st.session_state.get('confirmar_exclusao') == row['id']:
                                    db.excluir_registro('vendas', row['id'])
                                    st.success("✅ Venda excluída com sucesso!")
                                    st.rerun()
                                else:
                                    st.session_state.confirmar_exclusao = row['id']
                                    st.warning("⚠️ Clique novamente para confirmar")
                            st.write('</div>', unsafe_allow_html=True)

# Aba Compras
with tab2:
    st.markdown('<h2 class="subtitle">Registro de Compras</h2>', unsafe_allow_html=True)
    
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
    st.header("Exportar Relatórios")
    mes = st.selectbox("Mês", range(1, 13), datetime.now().month - 1)
    ano = st.number_input("Ano", min_value=2020, max_value=2030, value=datetime.now().year)
    formato = st.selectbox("Formato", ["csv", "excel"])
    
    if st.button("Exportar Relatório"):
        try:
            compras_file, vendas_file = db.exportar_relatorio_mensal(mes, ano, formato)
            st.success(f"✅ Relatórios exportados com sucesso!\nArquivos gerados:\n- {compras_file}\n- {vendas_file}")
        except Exception as e:
            st.error(f"❌ Erro ao exportar relatórios: {str(e)}")

# Visualizações
if not st.session_state.get('vendas', pd.DataFrame()).empty:
    vendas_por_pagamento = st.session_state.vendas.groupby('forma_pagamento')['valor_total'].sum().reset_index()
    fig_pagamento = px.pie(
        vendas_por_pagamento,
        values='valor_total',
        names='forma_pagamento',
        title='Distribuição de Vendas por Forma de Pagamento',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pagamento)

if not st.session_state.get('vendas', pd.DataFrame()).empty:
    produtos_mais_vendidos = st.session_state.vendas.groupby('produto')['quantidade'].sum().reset_index()
    produtos_mais_vendidos = produtos_mais_vendidos.sort_values('quantidade', ascending=True).tail(10)
    fig_produtos = px.bar(
        produtos_mais_vendidos,
        x='quantidade',
        y='produto',
        title='Top 10 Produtos Mais Vendidos',
        orientation='h',
        color_discrete_sequence=['#800020']
    )
    st.plotly_chart(fig_produtos) 