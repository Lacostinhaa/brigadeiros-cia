# 🧁 Brigadeiros & Cia - Sistema de Controle Financeiro

Sistema de controle financeiro local para gerenciamento de compras e vendas de uma empresa de brigadeiros e bolos.

## 📋 Funcionalidades

- Dashboard com visão geral financeira
- Registro de compras de matérias-primas
- Registro de vendas de produtos
- Relatórios mensais exportáveis em CSV ou Excel
- Controle de compras mistas (pessoal/empresa)
- Acompanhamento de lucro estimado

## 🚀 Como Instalar

1. Certifique-se de ter o Python 3.8 ou superior instalado
2. Clone este repositório
3. Instale as dependências:

```bash
pnpm install
cd brigadeiros_app
pip install -r requirements.txt
```

## 💻 Como Usar

1. Entre no diretório do projeto:
```bash
cd brigadeiros_app
```

2. Inicie a aplicação:
```bash
streamlit run src/main.py
```

3. Acesse a interface web que será aberta automaticamente no seu navegador

## 📊 Estrutura do Projeto

```
brigadeiros_app/
├── src/
│   ├── main.py         # Aplicação principal (Streamlit)
│   └── database.py     # Gerenciamento do banco de dados
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 💾 Banco de Dados

O sistema utiliza SQLite como banco de dados local. O arquivo `brigadeiros.db` será criado automaticamente na primeira execução.

## 📱 Interface

- **Dashboard**: Visão geral financeira com totais do mês e últimas transações
- **Compras**: Registro de compras de matérias-primas
- **Vendas**: Registro de vendas de produtos
- **Relatórios**: Exportação de dados mensais em CSV ou Excel

## 🔒 Segurança

Todos os dados são armazenados localmente no seu computador através do SQLite.

## 📈 Relatórios

Os relatórios podem ser exportados em dois formatos:
- CSV: Para uso em planilhas e análises
- Excel: Para visualização e impressão 