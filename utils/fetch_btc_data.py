# -*- coding: utf-8 -*-
"""
抓取 BTC K 线 → 计算指标 → 产出信号 + 风控数据
"""
from __future__ import annotations
import yfinance as yf
import pandas as pd
from core.indicators import add_basic_indicators
from core.signal import make_signal
from core.config import DAYTRADE_CFG as C

PAIR = "BTC-USD"
INTERVALS = {
    "5m":  dict(interval="5m",  period="3d"),
    "15m": dict(interval="15m", period="7d"),
    "1h":  dict(interval="60m", period="60d"),
    "4h":  dict(interval="240m",period="360d"),
}

# ────────────────────────────────────
def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(
        PAIR, interval=interval, period=period, progress=False
    )
    df.index = df.index.tz_localize(None)   # 去掉时区信息
    return add_basic_indicators(df)

def get_btc_analysis() -> dict:
    dfs = {k: _download_tf(**v) for k, v in INTERVALS.items()}
    sig = make_signal(dfs["5m"], dfs["15m"], dfs["1h"], dfs["4h"])

    # 基础展示数据（取最近 1h 收盘）
    last = dfs["1h"].iloc[-1]
    price = float(last["Close"])
    ma20  = float(last["MA20"])
    rsi   = float(last["RSI"])

    risk_usd = C["RISK_USD"]
    if sig["direction"] != "neutral":
        # 手数 = 风险 / (|Entry-SL| × 杠杆)
        qty = risk_usd / (abs(sig["entry"] - sig["sl"]) * C["LEVERAGE"])
        qty = round(qty, 4)
    else:
        qty = "N/A"

    strategy = "✅ 做多" if sig.get("direction") == "long" else \
               "🚫 做空" if sig.get("direction") == "short" else "⏸ 观望"

    return {
        # 技术面
        "price":  price,
        "ma20":   ma20,
        "rsi":    rsi,
        "strategy_text": strategy,
        # 交易面
        "risk_usd": risk_usd,
        "qty": qty,
        "entry": sig.get("entry", "N/A"),
        "sl":    sig.get("sl",    "N/A"),
        "tp":    sig.get("tp",    "N/A"),
    }
