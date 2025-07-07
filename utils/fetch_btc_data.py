# fetch_btc_data.py

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_btc_analysis():
    data = yf.download("BTC-USD", interval="1h", period="7d", progress=False)

    # 清洗
    data.dropna(inplace=True)
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["RSI"] = compute_rsi(data["Close"], 14)
    data["ATR"] = compute_atr(data, 14)

    # 模拟资金费率（替换为真实 API 可接）
    funding_rate = 0.018 if data.iloc[-1]["Close"] > data.iloc[-1]["MA20"] else -0.015
    volume = float(data.iloc[-1]["Volume"])

    return {
        "price": round(data.iloc[-1]["Close"], 2),
        "ma20": round(data.iloc[-1]["MA20"], 2),
        "rsi": round(data.iloc[-1]["RSI"], 2),
        "atr": round(data.iloc[-1]["ATR"], 2),
        "funding_rate": funding_rate,
        "volume": round(volume, 2),
        "entry_15m": estimate_entry_price(data, tf="15m"),
        "sl_15m": estimate_sl(data),
        "tp_15m": estimate_tp(data),
        "entry_1h": estimate_entry_price(data, tf="1h"),
        "sl_1h": estimate_sl(data),
        "tp_1h": estimate_tp(data),
        "entry_4h": estimate_entry_price(data, tf="4h"),
        "sl_4h": estimate_sl(data),
        "tp_4h": estimate_tp(data),
        "signal_15m": detect_signal(data, tf="15m"),
        "signal_1h": detect_signal(data, tf="1h"),
        "signal_4h": detect_signal(data, tf="4h"),
        "reason_15m": explain_signal(data, tf="15m"),
        "reason_1h": explain_signal(data, tf="1h"),
        "reason_4h": explain_signal(data, tf="4h"),
        "update_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

def compute_rsi(series, period):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_atr(data, period=14):
    high_low = data["High"] - data["Low"]
    high_close = np.abs(data["High"] - data["Close"].shift())
    low_close = np.abs(data["Low"] - data["Close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def estimate_entry_price(data, tf):
    return round(data["Low"].tail(3).mean(), 2)

def estimate_sl(data):
    return round(data["Close"].iloc[-1] - 1.5 * data["ATR"].iloc[-1], 2)

def estimate_tp(data):
    return round(data["Close"].iloc[-1] + 2.0 * data["ATR"].iloc[-1], 2)

def detect_signal(data, tf):
    rsi = data["RSI"].iloc[-1]
    price = data["Close"].iloc[-1]
    ma = data["MA20"].iloc[-1]
    if rsi > 60 and price > ma:
        return "强烈短线做多"
    elif rsi < 40 and price < ma:
        return "做空趋势延续"
    else:
        return "震荡中性"

def explain_signal(data, tf):
    rsi = data["RSI"].iloc[-1]
    price = data["Close"].iloc[-1]
    ma = data["MA20"].iloc[-1]
    if rsi > 60 and price > ma:
        return "RSI 强势，价格突破 MA20，趋势向上"
    elif rsi < 40 and price < ma:
        return "RSI 弱势，价格跌破 MA20，空头延续"
    else:
        return "价格围绕 MA20 震荡，暂无明显趋势"
