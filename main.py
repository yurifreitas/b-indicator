from acp_sdk.server import create_app
from fastapi.middleware.cors import CORSMiddleware
from smolagents import ToolCallingAgent, ToolCollection, LiteLLMModel
from mcp import StdioServerParameters
from acp_sdk.server.agent import agent
from acp_sdk.models import Message, MessagePart
from collections.abc import AsyncGenerator

# Define o servidor MCP externo (binance_server.py deve estar separado e rodando com `uv run`)
binance_server = StdioServerParameters(command="uv", args=["run", "binance_server.py"])

# Inicializa o modelo LLM
model = LiteLLMModel(
    model_id="ollama_chat/phi4",
    api_base="http://localhost:11434",
    num_ctx=8192,
)

# Cache para os MCP tools
tools_collection: ToolCollection | None = None
agent_instance: ToolCallingAgent | None = None


@agent(name="finance_agent", description="Ferramentas Binance via MCP")
async def finance_agent(input: list[Message], context) -> AsyncGenerator:
    with ToolCollection.from_mcp(binance_server, trust_remote_code=True) as tools:
        agent = ToolCallingAgent(tools=[*tools.tools], model=model)
        result = agent.run(input[0].parts[0].content)
    yield Message(parts=[MessagePart(content=str(result))])


# Cria o app FastAPI
app = create_app(finance_agent)

# Habilita CORS (ajuste para ambiente de produção se necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Recomendado restringir em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o app com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
