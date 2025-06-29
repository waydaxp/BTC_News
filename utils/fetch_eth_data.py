import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

from core.indicators import add_basic_indicators
from core.risk       import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "ETH-USD"
TZ   = "Asia/Shanghai"

CFG = {
    "1h":  {"interval": "1h",  "period": "7d"},
    "15m": {"interval": "15m", "period": "1d"},
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=False,
    )
    if df is None or df.empty:
        raise RuntimeError(f"yf.download 返回空数据: {PAIR}, {interval}, {period}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    df.columns = [str(c).capitalize() for c in df.columns]

    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert(TZ)

    return add_basic_indicators(df).dropna()

def get_eth_analysis() -> dict:
    dfs = {tf: _download_tf(**cfg) for tf, cfg in CFG.items()}
    df1h  = dfs["1h"]
    df15m = dfs["15m"]

    ohlc = {
        "Open":  "first",
        "High":  "max",
        "Low":   "min",
        "Close": "last",
        "Volume":"sum",
    }
    df4h = df1h.resample("4h", closed="right", label="right").agg(ohlc).dropna()

    last1h  = df1h.iloc[-1]
    last4h  = df4h.iloc[-1]
    last15m = df15m.iloc[-1]

    price = float(last1h["Close"])
    ma20  = float(last1h["Ma20"])
    rsi   = float(last1h["Rsi"])
    atr   = float(last1h["Atr"])

    trend_up = last4h["Close"] > last4h["Ma20"]

    if trend_up and 30 < rsi < 70 and last15m["Close"] > last15m["Ma20"]:
        signal = "✅ 做多"
        sl     = price - ATR_MULT_SL * atr
        tp     = price + ATR_MULT_TP * atr
        qty    = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif (not trend_up) and 30 < rsi < 70 and last15m["Close"] < last15m["Ma20"]:
        signal = "❌ 做空"
        sl     = price + ATR_MULT_SL * atr
        tp     = price - ATR_MULT_TP * atr
        qty    = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        signal = "⏸ 中性"
        sl = tp = qty = None

    return {
        "price":        price,
        "ma20":         ma20,
        "rsi":          rsi,
        "atr":          atr,
        "signal":       signal,
        "sl":           sl,
        "tp":           tp,
        "qty":          qty,
        "risk_usd":     RISK_USD,
        "update_time":  datetime.now(pytz.timezone(TZ)).strftime("%Y-%m-%d %H:%M"),
    }
