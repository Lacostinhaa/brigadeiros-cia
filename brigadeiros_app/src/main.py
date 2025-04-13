import streamlit as st
import pandas as pd
from datetime import datetime
from database import Database
import plotly.graph_objects as go

# Configuração inicial do Streamlit
st.set_page_config(
    page_title="Brigadeiros & Cia - Controle Financeiro",
    page_icon="🧁",
    layout="wide"
)

# Inicialização do banco de dados
db = Database()

# Função para formatar valores monetários
def format_currency(value):
    return f"$ {value:,.0f} CLP"

# Título principal
st.title("🧁 Brigadeiros & Cia - Controle Financeiro")

# Criação das abas
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🛍️ Compras", "💰 Vendas"])

# Aba Dashboard
with tab1:
    st.header("Dashboard Financeiro")
    
    # Métricas do mês atual
    col1, col2, col3 = st.columns(3)
    
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    total_compras = db.obter_total_mes('compras', mes_atual, ano_atual)
    total_vendas = db.obter_total_mes('vendas', mes_atual, ano_atual)
    lucro = total_vendas - total_compras
    
    with col1:
        st.metric("Total de Compras", format_currency(total_compras))
    with col2:
        st.metric("Total de Vendas", format_currency(total_vendas))
    with col3:
        st.metric("Lucro Estimado", format_currency(lucro))
    
    # Últimas transações
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Últimas Compras")
        ultimas_compras = db.obter_ultimos_registros('compras')
        if not ultimas_compras.empty:
            st.dataframe(ultimas_compras[['data', 'produto', 'quantidade', 'valor_total']])
    
    with col2:
        st.subheader("Últimas Vendas")
        ultimas_vendas = db.obter_ultimos_registros('vendas')
        if not ultimas_vendas.empty:
            st.dataframe(ultimas_vendas[['data', 'produto', 'quantidade', 'valor_total']])

# Aba Compras
with tab2:
    st.header("Registro de Compras")
    
    with st.form("form_compras"):
        col1, col2 = st.columns(2)
        
        with col1:
            data_compra = st.date_input("Data da Compra", datetime.now())
            produto = st.text_input("Produto Comprado")
            quantidade = st.number_input("Quantidade", min_value=0.0, step=0.1)
        
        with col2:
            valor_unitario = st.number_input("Valor Unitário (CLP)", min_value=0)
            compra_mista = st.checkbox("Compra Mista (mercado de casa junto)")
            observacao = st.text_area("Observação", height=100)
        
        valor_total = quantidade * valor_unitario
        st.write(f"Valor Total: {format_currency(valor_total)}")
        
        submitted = st.form_submit_button("Registrar Compra")
        
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
                st.success("Compra registrada com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

# Aba Vendas
with tab3:
    st.header("Registro de Vendas")
    
    with st.form("form_vendas"):
        col1, col2 = st.columns(2)
        
        with col1:
            data_venda = st.date_input("Data da Venda", datetime.now())
            produto = st.text_input("Produto Vendido")
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
        
        with col2:
            preco_unitario = st.number_input("Preço Unitário (CLP)", min_value=0)
            forma_pagamento = st.selectbox(
                "Forma de Pagamento",
                ["Dinheiro", "PIX", "Transferência", "Outro"]
            )
            observacao = st.text_area("Observação", height=100)
        
        valor_total = quantidade * preco_unitario
        st.write(f"Valor Total: {format_currency(valor_total)}")
        
        submitted = st.form_submit_button("Registrar Venda")
        
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
                st.success("Venda registrada com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

# Sidebar para exportação de relatórios
with st.sidebar:
    st.header("Exportar Relatórios")
    mes = st.selectbox("Mês", range(1, 13), datetime.now().month - 1)
    ano = st.number_input("Ano", min_value=2020, max_value=2030, value=datetime.now().year)
    formato = st.selectbox("Formato", ["csv", "excel"])
    
    if st.button("Exportar Relatório"):
        try:
            compras_file, vendas_file = db.exportar_relatorio_mensal(mes, ano, formato)
            st.success(f"Relatórios exportados com sucesso!\nArquivos gerados:\n- {compras_file}\n- {vendas_file}")
        except Exception as e:
            st.error(f"Erro ao exportar relatórios: {str(e)}") 