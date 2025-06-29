# utils/fetch_btc_data.py
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

from core.indicators import add_basic_indicators
from core.risk       import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "BTC-USD"
TZ   = "Asia/Shanghai"

CFG = {
    "1h":  {"interval":"1h",  "period":"7d"},
    "15m": {"interval":"15m", "period":"1d"},
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=False,
    )
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert(TZ)
    return add_basic_indicators(df).dropna()

def get_btc_analysis() -> dict:
    df1h  = _download_tf(**CFG["1h"])
    # 从 1h 合成 4h
    ohlc = {"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}
    df4h = df1h.resample("4h", closed="right", label="right").agg(ohlc).dropna()
    df4h = add_basic_indicators(df4h)

    df15m = _download_tf(**CFG["15m"])

    last1h  = df1h.iloc[-1]
    last4h  = df4h.iloc[-1]
    last15m = df15m.iloc[-1]

    price = float(last1h["Close"])
    ma20  = float(last1h["Ma20"])
    rsi   = float(last1h["Rsi"])
    atr   = float(last1h["Atr"])

    # 多头信号：4h & 15m 双均线之上 且 RSI 在 30~70
    if last4h["Close"] > last4h["Ma20"] and last15m["Close"] > last15m["Ma20"] and 30 < rsi < 70:
        side   = "long"
        signal = "✅ 做多"
        sl     = price - ATR_MULT_SL * atr
        tp     = price + ATR_MULT_TP * atr
    else:
        side   = "short"
        signal = "⛔ 观望"
        sl     = price + ATR_MULT_SL * atr
        tp     = price - ATR_MULT_TP * atr

    qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, side)

    return {
        "price":       round(price,2),
        "ma20":        round(ma20,2),
        "rsi":         round(rsi,2),
        "atr":         round(atr,2),
        "signal":      signal,
        "sl":          round(sl,2),
        "tp":          round(tp,2),
        "qty":         round(qty,4),
        "risk_usd":    round(RISK_USD,2),
        "update_time": datetime.now(pytz.timezone(TZ)).strftime("%Y-%m-%d %H:%M"),
    }
