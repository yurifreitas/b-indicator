import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from ta.trend import MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochRSIIndicator, WilliamsRIndicator
from io import BytesIO
from datetime import datetime
from scipy.stats import linregress

def compute_hurst_exponent(ts, max_lag=20):
    lags = range(2, max_lag)
    tau = []
    for lag in lags:
        diff = np.subtract(ts[lag:], ts[:-lag])
        std = np.std(diff)
        tau.append(std if std > 0 else 1e-8)
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

def get_binance_klines(symbol="BTCUSDT", interval="1w", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar dados da Binance: {e}")

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    return df

def analyze_advanced(symbol="BTCUSDT", output_path=None):
    df = get_binance_klines(symbol)
    close, high, low = df["close"], df["high"], df["low"]

    # Indicadores
    rsi = RSIIndicator(close, window=14).rsi()
    stoch = StochRSIIndicator(close, window=14).stochrsi_k()
    wpr = WilliamsRIndicator(high, low, close, lbp=14).williams_r()
    macd = MACD(close)
    adx = ADXIndicator(high, low, close)
    fdi = compute_fdi(close.values, window=10)
    hurst = [np.nan] * 19 + [
        compute_hurst_exponent(close[i - 19:i]) if len(close[i - 19:i]) >= 19 else np.nan
        for i in range(19, len(close))
    ]

    # Plot
    plt.figure(figsize=(18, 12))

    # Preço
    plt.subplot(4, 1, 1)
    plt.plot(df.index, close, label="Preço", linewidth=2, color="black")
    plt.title(f"{symbol} - Preço histórico ({df.index[0].date()} até {df.index[-1].date()})")
    plt.legend()

    # Momentum
    plt.subplot(4, 1, 2)
    plt.plot(df.index, rsi, label="RSI")
    plt.plot(df.index, stoch, label="Stoch RSI")
    plt.plot(df.index, wpr, label="Williams %R")
    plt.axhline(70, color='red', linestyle='--', alpha=0.4)
    plt.axhline(30, color='green', linestyle='--', alpha=0.4)
    plt.title("Indicadores de Momentum")
    plt.legend()

    # Tendência
    plt.subplot(4, 1, 3)
    plt.plot(df.index, macd.macd(), label="MACD", color='blue')
    plt.plot(df.index, macd.macd_signal(), label="Signal", color='orange')
    plt.plot(df.index, adx.adx(), label="ADX", linestyle="--", color='purple')
    plt.title("Tendência (MACD, ADX)")
    plt.legend()

    # Fractalidade
    plt.subplot(4, 1, 4)
    plt.plot(df.index, fdi, label="FDI", color='darkgreen')
    plt.plot(df.index, hurst, label="Hurst", color='darkred')
    plt.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
    plt.title("Fractalidade (FDI, Hurst Exponent)")
    plt.legend()

    plt.tight_layout()

    # Exporta
    if isinstance(output_path, BytesIO):
        plt.savefig(output_path, format="png", dpi=300, bbox_inches="tight")
    else:
        out_path = output_path or f"{symbol}_analysis.png"
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
