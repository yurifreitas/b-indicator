import pandas as pd
import numpy as np
import requests
import matplotlib
import matplotlib.pyplot as plt

# Descomente essa linha abaixo caso esteja em ambiente gráfico
# matplotlib.use("TkAgg")

from ta.trend import MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochRSIIndicator, WilliamsRIndicator
from scipy.stats import linregress


def compute_hurst_exponent(ts, max_lag=20):
    lags = range(2, max_lag)
    tau = []
    for lag in lags:
        diff = np.subtract(ts[lag:], ts[:-lag])
        std = np.std(diff)
        tau.append(std if std > 0 else 1e-8)  # Evita log(0)
    m = np.polyfit(np.log(lags), np.log(tau), 1)
    return m[0]


def compute_fdi(prices, window=10):
    fdi = []
    for i in range(window, len(prices)):
        segment = prices[i - window:i]
        diffs = np.abs(np.diff(segment))
        total_length = np.sum(np.sqrt(diffs**2 + 1))
        linear_length = np.sqrt((segment[-1] - segment[0])**2 + window**2)
        fdi_value = np.log10(total_length / linear_length) / np.log10(2)
        fdi.append(fdi_value)
    return [np.nan] * window + fdi


def get_binance_klines(symbol="BTCUSDT", interval="1w", limit=1000):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    return df


def analyze_advanced(symbol="BTCUSDT", output_path="indicadores_avancados.png"):
    df = get_binance_klines(symbol)

    close = df["close"]
    high = df["high"]
    low = df["low"]

    rsi = RSIIndicator(close, window=14).rsi()
    stoch = StochRSIIndicator(close, window=14).stochrsi_k()
    wpr = WilliamsRIndicator(high, low, close, lbp=14).williams_r()
    macd = MACD(close)
    adx = ADXIndicator(high, low, close)

    fdi = compute_fdi(close.values, window=10)
    hurst = [np.nan] * 19 + [compute_hurst_exponent(close[i-19:i]) for i in range(19, len(close))]

    plt.figure(figsize=(18, 12))

    plt.subplot(4, 1, 1)
    plt.plot(df.index, close, label="Preço", linewidth=2)
    plt.title(f"{symbol} - Preço")
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(df.index, rsi, label="RSI")
    plt.plot(df.index, stoch, label="Stoch RSI")
    plt.plot(df.index, wpr, label="Williams %R")
    plt.axhline(70, color='r', linestyle='--', alpha=0.3)
    plt.axhline(30, color='g', linestyle='--', alpha=0.3)
    plt.title("Momentum (RSI, Stoch RSI, W%R)")
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(df.index, macd.macd(), label="MACD")
    plt.plot(df.index, macd.macd_signal(), label="Signal")
    plt.plot(df.index, adx.adx(), label="ADX", linestyle="--")
    plt.title("Tendência (MACD, ADX)")
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(df.index, fdi, label="FDI")
    plt.plot(df.index, hurst, label="Hurst Exponent")
    plt.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
    plt.title("Fractalidade (FDI, Hurst)")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"✅ Gráfico salvo como: {output_path}")

    # Para ambientes gráficos:
    # plt.show()


if __name__ == "__main__":
    analyze_advanced("BTCUSDT")
