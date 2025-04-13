import streamlit as st
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self):
        # Inicializa as tabelas no session_state se não existirem
        if 'compras' not in st.session_state:
            st.session_state.compras = pd.DataFrame(columns=[
                'id', 'data', 'produto', 'quantidade', 'valor_unitario',
                'valor_total', 'observacao', 'compra_mista', 'created_at'
            ])
        
        if 'vendas' not in st.session_state:
            st.session_state.vendas = pd.DataFrame(columns=[
                'id', 'data', 'produto', 'quantidade', 'preco_unitario',
                'valor_total', 'forma_pagamento', 'observacao', 'created_at'
            ])

    def adicionar_compra(self, data, produto, quantidade, valor_unitario, valor_total, observacao, compra_mista):
        """Adiciona uma nova compra"""
        nova_compra = pd.DataFrame([{
            'id': len(st.session_state.compras) + 1,
            'data': data,
            'produto': produto,
            'quantidade': quantidade,
            'valor_unitario': valor_unitario,
            'valor_total': valor_total,
            'observacao': observacao,
            'compra_mista': compra_mista,
            'created_at': datetime.now()
        }])
        st.session_state.compras = pd.concat([st.session_state.compras, nova_compra], ignore_index=True)

    def adicionar_venda(self, data, produto, quantidade, preco_unitario, valor_total, forma_pagamento, observacao):
        """Adiciona uma nova venda"""
        nova_venda = pd.DataFrame([{
            'id': len(st.session_state.vendas) + 1,
            'data': data,
            'produto': produto,
            'quantidade': quantidade,
            'preco_unitario': preco_unitario,
            'valor_total': valor_total,
            'forma_pagamento': forma_pagamento,
            'observacao': observacao,
            'created_at': datetime.now()
        }])
        st.session_state.vendas = pd.concat([st.session_state.vendas, nova_venda], ignore_index=True)

    def editar_compra(self, id, data, produto, quantidade, valor_unitario, valor_total, observacao, compra_mista):
        """Edita uma compra existente"""
        idx = st.session_state.compras.index[st.session_state.compras['id'] == id].tolist()[0]
        st.session_state.compras.at[idx, 'data'] = data
        st.session_state.compras.at[idx, 'produto'] = produto
        st.session_state.compras.at[idx, 'quantidade'] = quantidade
        st.session_state.compras.at[idx, 'valor_unitario'] = valor_unitario
        st.session_state.compras.at[idx, 'valor_total'] = valor_total
        st.session_state.compras.at[idx, 'observacao'] = observacao
        st.session_state.compras.at[idx, 'compra_mista'] = compra_mista

    def editar_venda(self, id, data, produto, quantidade, preco_unitario, valor_total, forma_pagamento, observacao):
        """Edita uma venda existente"""
        idx = st.session_state.vendas.index[st.session_state.vendas['id'] == id].tolist()[0]
        st.session_state.vendas.at[idx, 'data'] = data
        st.session_state.vendas.at[idx, 'produto'] = produto
        st.session_state.vendas.at[idx, 'quantidade'] = quantidade
        st.session_state.vendas.at[idx, 'preco_unitario'] = preco_unitario
        st.session_state.vendas.at[idx, 'valor_total'] = valor_total
        st.session_state.vendas.at[idx, 'forma_pagamento'] = forma_pagamento
        st.session_state.vendas.at[idx, 'observacao'] = observacao

    def obter_compra_por_id(self, id):
        """Obtém uma compra pelo ID"""
        return st.session_state.compras[st.session_state.compras['id'] == id].iloc[0]

    def obter_venda_por_id(self, id):
        """Obtém uma venda pelo ID"""
        return st.session_state.vendas[st.session_state.vendas['id'] == id].iloc[0]

    def obter_total_mes(self, tabela, mes=None, ano=None):
        """Obtém o total de compras ou vendas do mês especificado"""
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year

        df = st.session_state[tabela]
        if not df.empty:
            df['data'] = pd.to_datetime(df['data'])
            mask = (df['data'].dt.month == mes) & (df['data'].dt.year == ano)
            return df[mask]['valor_total'].sum()
        return 0

    def obter_ultimos_registros(self, tabela, limite=5):
        """Obtém os últimos registros de uma tabela específica"""
        df = st.session_state[tabela]
        if not df.empty:
            return df.sort_values('created_at', ascending=False).head(limite)
        return pd.DataFrame()

    def exportar_relatorio_mensal(self, mes, ano, formato='csv'):
        """Exporta relatório mensal em CSV ou Excel"""
        # Filtra os dados do mês
        df_compras = st.session_state.compras
        df_vendas = st.session_state.vendas

        if not df_compras.empty:
            df_compras['data'] = pd.to_datetime(df_compras['data'])
            mask = (df_compras['data'].dt.month == mes) & (df_compras['data'].dt.year == ano)
            df_compras = df_compras[mask]

        if not df_vendas.empty:
            df_vendas['data'] = pd.to_datetime(df_vendas['data'])
            mask = (df_vendas['data'].dt.month == mes) & (df_vendas['data'].dt.year == ano)
            df_vendas = df_vendas[mask]

        # Prepara os arquivos para download
        if formato == 'csv':
            compras_file = df_compras.to_csv(index=False).encode('utf-8')
            vendas_file = df_vendas.to_csv(index=False).encode('utf-8')
        else:  # excel
            compras_file = df_compras.to_excel(index=False)
            vendas_file = df_vendas.to_excel(index=False)

        return compras_file, vendas_file 