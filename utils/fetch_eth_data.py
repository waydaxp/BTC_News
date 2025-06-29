# -*- coding: utf-8 -*-
"""
ETH 版，与 BTC 逻辑完全一致，仅修改代号与风险金额
"""
from __future__ import annotations
import yfinance as yf
import pandas as pd
from core.indicators import add_basic_indicators
from core.signal import make_signal
from core.config import DAYTRADE_CFG as C

PAIR = "ETH-USD"
INTERVALS = {
    "5m":  dict(interval="5m",  period="3d"),
    "15m": dict(interval="15m", period="7d"),
    "1h":  dict(interval="60m", period="60d"),
    "4h":  dict(interval="240m",period="360d"),
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.index = df.index.tz_localize(None)
    return add_basic_indicators(df)

def get_eth_analysis() -> dict:
    dfs = {k: _download_tf(**v) for k, v in INTERVALS.items()}
    sig = make_signal(dfs["5m"], dfs["15m"], dfs["1h"], dfs["4h"])

    last  = dfs["1h"].iloc[-1]
    price = float(last["Close"])
    ma20  = float(last["MA20"])
    rsi   = float(last["RSI"])

    risk_usd = C["RISK_USD"]
    if sig["direction"] != "neutral":
        qty = risk_usd / (abs(sig["entry"] - sig["sl"]) * C["LEVERAGE"])
        qty = round(qty, 4)
    else:
        qty = "N/A"

    strategy = "✅ 做多" if sig.get("direction") == "long" else \
               "🚫 做空" if sig.get("direction") == "short" else "⏸ 观望"

    return {
        "price":  price,
        "ma20":   ma20,
        "rsi":    rsi,
        "strategy_text": strategy,
        "risk_usd": risk_usd,
        "qty": qty,
        "entry": sig.get("entry", "N/A"),
        "sl":    sig.get("sl",    "N/A"),
        "tp":    sig.get("tp",    "N/A"),
    }
