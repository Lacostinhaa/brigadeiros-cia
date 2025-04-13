import sqlite3
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria as tabelas se não existirem"""
        self.db_file = 'brigadeiros.db'
        self.create_tables()
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_file)
    
    def create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de compras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data DATE NOT NULL,
                produto TEXT NOT NULL,
                quantidade REAL NOT NULL,
                valor_unitario INTEGER NOT NULL,
                valor_total INTEGER NOT NULL,
                observacao TEXT,
                compra_mista BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        
        # Tabela de vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data DATE NOT NULL,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario INTEGER NOT NULL,
                valor_total INTEGER NOT NULL,
                forma_pagamento TEXT NOT NULL,
                observacao TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def adicionar_compra(self, data, produto, quantidade, valor_unitario, valor_total, observacao, compra_mista):
        """Adiciona uma nova compra ao banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO compras (data, produto, quantidade, valor_unitario, valor_total, observacao, compra_mista)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data, produto, quantidade, valor_unitario, valor_total, observacao, compra_mista))
        
        conn.commit()
        conn.close()
    
    def adicionar_venda(self, data, produto, quantidade, preco_unitario, valor_total, forma_pagamento, observacao):
        """Adiciona uma nova venda ao banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO vendas (data, produto, quantidade, preco_unitario, valor_total, forma_pagamento, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data, produto, quantidade, preco_unitario, valor_total, forma_pagamento, observacao))
        
        conn.commit()
        conn.close()
    
    def obter_total_mes(self, tabela, mes=None, ano=None):
        """Obtém o total de compras ou vendas do mês especificado"""
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year

        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = f'''
            SELECT SUM(valor_total) 
            FROM {tabela} 
            WHERE strftime('%m', data) = ? 
            AND strftime('%Y', data) = ?
        '''
        
        cursor.execute(query, (f"{mes:02d}", str(ano)))
        total = cursor.fetchone()[0] or 0
        
        conn.close()
        return total
    
    def obter_ultimos_registros(self, tabela, limite=5):
        """Obtém os últimos registros de uma tabela específica"""
        conn = self.get_connection()
        query = f"SELECT * FROM {tabela} ORDER BY data DESC LIMIT {limite}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def exportar_relatorio_mensal(self, mes, ano, formato='csv'):
        """Exporta relatório mensal em CSV ou Excel"""
        conn = self.get_connection()
        
        # Obtém dados do mês especificado
        compras_query = f"""
            SELECT * FROM compras 
            WHERE strftime('%m', data) = '{mes:02d}'
            AND strftime('%Y', data) = '{ano}'
        """
        
        vendas_query = f"""
            SELECT * FROM vendas 
            WHERE strftime('%m', data) = '{mes:02d}'
            AND strftime('%Y', data) = '{ano}'
        """
        
        df_compras = pd.read_sql_query(compras_query, conn)
        df_vendas = pd.read_sql_query(vendas_query, conn)
        
        conn.close()
        
        # Cria nome dos arquivos
        compras_file = f'relatorio_compras_{ano}_{mes:02d}.{formato}'
        vendas_file = f'relatorio_vendas_{ano}_{mes:02d}.{formato}'
        
        # Exporta os arquivos
        if formato == 'csv':
            df_compras.to_csv(compras_file, index=False)
            df_vendas.to_csv(vendas_file, index=False)
        else:  # excel
            df_compras.to_excel(compras_file, index=False)
            df_vendas.to_excel(vendas_file, index=False)
        
        return compras_file, vendas_file

    def excluir_registro(self, tabela, id):
        """Exclui um registro específico da tabela"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'DELETE FROM {tabela} WHERE id = ?', (id,))
        
        conn.commit()
        conn.close()
    
    def obter_registro(self, tabela, id):
        """Obtém um registro específico da tabela"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {tabela} WHERE id = ?', (id,))
        registro = cursor.fetchone()
        
        conn.close()
        
        if registro:
            colunas = [description[0] for description in cursor.description]
            return dict(zip(colunas, registro))
        return None
    
    def editar_compra(self, id, data, produto, quantidade, valor_unitario, valor_total, observacao, compra_mista):
        """Edita uma compra existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE compras 
            SET data = ?, produto = ?, quantidade = ?, valor_unitario = ?, 
                valor_total = ?, observacao = ?, compra_mista = ?
            WHERE id = ?
        ''', (data, produto, quantidade, valor_unitario, valor_total, observacao, compra_mista, id))
        
        conn.commit()
        conn.close()
    
    def editar_venda(self, id, data, produto, quantidade, preco_unitario, valor_total, forma_pagamento, observacao):
        """Edita uma venda existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE vendas 
            SET data = ?, produto = ?, quantidade = ?, preco_unitario = ?, 
                valor_total = ?, forma_pagamento = ?, observacao = ?
            WHERE id = ?
        ''', (data, produto, quantidade, preco_unitario, valor_total, forma_pagamento, observacao, id))
        
        conn.commit()
        conn.close() 