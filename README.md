# 🧠 Finance Agent com Ferramentas Binance via MCP

Este projeto implementa um agente LLM multimodal baseado em ferramentas externas (MCP Tools) para consulta e análise de dados do mercado financeiro, utilizando a API da Binance. A arquitetura usa:

- **smolagents** para agentes com múltiplas etapas e ferramentas
- **MCP (Modular Command Protocol)** para isolar ferramentas externas
- **FastAPI** como backend via `acp_sdk`
- **Ollama + Phi-4** como modelo local (pode ser substituído)

---

## 🚀 Funcionalidades

O agente é capaz de:

- Consultar o **preço atual** de uma criptomoeda (`get_price`)
- Obter o **livro de ofertas** (`get_orderbook`)
- Listar as **últimas negociações (trades)** (`get_recent_trades`)
- Obter **candlesticks (klines)** por período (`get_klines`)
- Gerar **análises técnicas avançadas** com RSI, MACD, etc. em gráfico (`analyze_indicators`)

Todas as ferramentas são chamadas dinamicamente via LLM e retornam informações processadas diretamente do agente.

---
