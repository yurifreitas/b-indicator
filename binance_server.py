from mcp.server.fastmcp import FastMCP
import requests
from pydantic import BaseModel
from io import BytesIO
import base64
from indicadores import analyze_advanced  # sua função existente

# Inicializa o servidor MCP
mcp = FastMCP("binance_server")

# --- Tool 1: Consulta de preço ---

@mcp.tool()
def get_price(symbol: str = "BTCUSDT") -> str:
    """Consulta o preço atual de uma criptomoeda.
    Args:
        symbol: símbolo do par (ex: BTCUSDT, ETHUSDT)
    Returns:
        Preço atual da moeda
    """
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url, params={"symbol": symbol.upper()})
    return response.text

# --- Tool 2: Livro de ofertas ---

@mcp.tool()
def get_orderbook(symbol: str = "BTCUSDT", limit: int = 5) -> str:
    """Retorna o livro de ofertas (order book) da criptomoeda.
    Args:
        symbol: símbolo do par
        limit: número de níveis (5, 10, 20, 50, 100, 500, 1000, 5000)
    """
    url = "https://api.binance.com/api/v3/depth"
    response = requests.get(url, params={"symbol": symbol.upper(), "limit": limit})
    return response.text

# --- Tool 3: Últimos trades ---

@mcp.tool()
def get_recent_trades(symbol: str = "BTCUSDT", limit: int = 5) -> str:
    """Consulta últimas negociações executadas.
    Args:
        symbol: par
        limit: número de trades
    """
    url = "https://api.binance.com/api/v3/trades"
    response = requests.get(url, params={"symbol": symbol.upper(), "limit": limit})
    return response.text

# --- Tool 4: Candles (Klines) ---

@mcp.tool()
def get_klines(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 10) -> str:
    """Consulta candles de preço.
    Args:
        symbol: par de moedas
        interval: intervalo dos candles (1m, 5m, 15m, 1h, 4h, 1d, etc.)
        limit: número de candles
    """
    url = "https://api.binance.com/api/v3/klines"
    response = requests.get(url, params={"symbol": symbol.upper(), "interval": interval, "limit": limit})
    return response.text

# --- Tool 5: Análise técnica com gráfico base64 ---

class IndicatorInput(BaseModel):
    symbol: str

@mcp.tool()
def analyze_indicators(input: IndicatorInput) -> str:
    """
    Gera análise técnica avançada e retorna imagem base64 com RSI, MACD, etc.
    """
    img_buffer = BytesIO()
    analyze_advanced(input.symbol, output_path=img_buffer)
    img_buffer.seek(0)
    b64 = base64.b64encode(img_buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{b64}"

# Inicia o servidor MCP
if __name__ == "__main__":
    mcp.run(transport="stdio")
