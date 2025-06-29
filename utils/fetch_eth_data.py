"""
ETH 数据抓取 & 技术分析
------------------------------------------------------------
依赖同 fetch_btc_data.py
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf
from datetime import datetime, timezone

from core.indicators import add_basic_indicators, calc_atr
from core.signal      import make_signal
from core.risk        import calc_position_size, ATR_MULT_SL, ATR_MULT_TP

PAIR        = "ETH-USD"
ACCOUNT_USD = 1_000
RISK_PCT    = 0.02

INTERVALS = {
    "15m": dict(interval="15m", period="3d"),
    "1h" : dict(interval="60m", period="7d"),
    "4h" : dict(interval="4h",  period="60d"),
}


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
    )

    clean_cols = []
    for c in df.columns:
        if isinstance(c, tuple):
            c = c[0]
        clean_cols.append(str(c).capitalize())
    df.columns = clean_cols

    df = add_basic_indicators(df)
    return df.dropna().copy()


def get_eth_analysis() -> dict:
    dfs = {k: _download_tf(**kw) for k, kw in INTERVALS.items()}
    df_15m, df_1h, df_4h = dfs["15m"], dfs["1h"], dfs["4h"]

    signal, trend_up = make_signal(df_1h, df_4h, df_15m)

    last    = df_1h.iloc[-1]
    price   = float(last["Close"])
    ma20    = float(last["Ma20"])
    rsi     = float(last["Rsi"])
    atr     = float(last["Atr"])

    risk_usd    = round(ACCOUNT_USD * RISK_PCT, 2)
    entry_price = price
    stop_loss   = round(price - ATR_MULT_SL * atr, 2)
    take_profit = round(price + ATR_MULT_TP * atr, 2)
    qty         = calc_position_size(risk_usd, entry_price, stop_loss)

    return {
        "price"       : price,
        "ma20"        : ma20,
        "rsi"         : rsi,
        "atr"         : atr,
        "signal"      : signal,
        "trend_up"    : trend_up,
        "entry_price" : entry_price,
        "stop_loss"   : stop_loss,
        "take_profit" : take_profit,
        "risk_usd"    : risk_usd,
        "position_qty": qty,
        "update_time" : datetime.now(timezone.utc).strftime("%F %T UTC"),
    }
