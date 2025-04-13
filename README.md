# Brigadeiros & Cia - Sistema de Controle Financeiro 🧁

Sistema de gerenciamento financeiro desenvolvido para controle de vendas e compras de brigadeiros e outros doces.

## Funcionalidades 📊

- Dashboard com métricas de vendas e compras
- Registro de vendas com detalhes do produto e forma de pagamento
- Controle de compras de insumos
- Relatórios mensais exportáveis
- Interface moderna e intuitiva

## Requisitos 📋

- Python 3.8 ou superior
- Bibliotecas necessárias listadas em `requirements.txt`

## Como Instalar 🚀

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar 💻

1. Navegue até a pasta do projeto:
```bash
cd python_app/src
```

2. Execute o aplicativo:
```bash
streamlit run main.py
```

3. Acesse o sistema no navegador através do endereço: http://localhost:8501

## Estrutura do Projeto 📁

- `python_app/src/` - Código fonte principal
  - `main.py` - Aplicativo Streamlit principal
  - `database.py` - Gerenciamento do banco de dados
- `requirements.txt` - Dependências do projeto

## Funcionalidades Principais 🎯

- **Dashboard**: Visualização rápida de métricas importantes
- **Registro de Vendas**: Controle detalhado das vendas realizadas
- **Controle de Compras**: Gestão de insumos e gastos
- **Relatórios**: Exportação de dados em diferentes formatos
- **Banco de Dados**: Armazenamento seguro e persistente das informações

## 🎨 Interface

- Interface web local via Streamlit
- Design responsivo e amigável
- Cores e estilos personalizados
- Ícones intuitivos

## 🔧 Tecnologias

- Python 3.8+
- Streamlit
- SQLite
- Pandas
- Plotly

## 📊 Banco de Dados

- SQLite local (brigadeiros.db)
- Tabelas:
  - compras
  - vendas

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 