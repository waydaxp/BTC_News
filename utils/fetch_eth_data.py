"""
拉取 ETH 多周期 K 线 → 计算指标 → 生成交易信号 & 风控建议
"""
from __future__ import annotations

import pandas as pd
import yfinance as yf
from datetime import datetime
from zoneinfo import ZoneInfo

from core.indicators import add_basic_indicators
from core.signal      import make_signal
from core.risk        import calc_position_size, ATR_MULT_SL, ATR_MULT_TP

PAIR       = "ETH-USD"
TZ         = ZoneInfo("Asia/Shanghai")

INTERVALS = {
    "1h" : dict(interval="60m", period="90d"),
    "4h" : dict(interval="240m", period="360d"),
    "15m": dict(interval="15m", period="30d"),
}


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    df.columns = [str(c).capitalize() for c in df.columns]
    if "Adj close" in df.columns and "Close" not in df.columns:
        df = df.rename(columns={"Adj close": "Close"})
    elif "Adj close" in df.columns:
        df = df.drop(columns=["Adj close"])
    return df


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(
        PAIR, interval=interval, period=period, progress=False
    )
    df = _flatten_columns(df)
    df.index = df.index.tz_localize("UTC").tz_convert(TZ)
    return add_basic_indicators(df).dropna()


def get_eth_analysis() -> dict:
    dfs = {k: _download_tf(**cfg) for k, cfg in INTERVALS.items()}
    df_1h, df_4h, df_15m = dfs["1h"], dfs["4h"], dfs["15m"]

    signal, trend_up = make_signal(df_1h, df_4h, df_15m)

    last_1h = df_1h.iloc[-1]
    price   = float(last_1h["Close"])
    atr     = float(last_1h["ATR"])

    risk_usd, pos_qty = calc_position_size(price, atr)

    if signal == "long":
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
    elif signal == "short":
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
    else:
        sl = tp = None

    return {
        "pair":          "ETH/USDT",
        "update_time":   datetime.now(TZ).strftime("%Y-%m-%d %H:%M"),
        "price":         round(price, 2),
        "atr":           round(atr, 2),
        "signal":        signal,
        "trend_up":      trend_up,
        "risk_usd":      risk_usd,
        "position_qty":  pos_qty,
        "sl":            round(sl, 2) if sl else "N/A",
        "tp":            round(tp, 2) if tp else "N/A",
    }
