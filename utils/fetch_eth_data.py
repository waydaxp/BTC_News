# utils/fetch_eth_data.py
import pandas as pd
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "ETH-USD"
TZ = "Asia/Shanghai"

INTERVALS = {
    "1h":  {"interval": "1h",  "period": "5d"},
    "15m": {"interval": "15m", "period": "1d"},
}

def _flatten_ohlc_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0).str.capitalize()
    else:
        df.columns = [str(c).capitalize() for c in df.columns]
    return df

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten_ohlc_columns(df)
    idx = df.index
    if idx.tz is None:
        df.index = idx.tz_localize("UTC").tz_convert(TZ)
    else:
        df.index = idx.tz_convert(TZ)
    df = add_basic_indicators(df).dropna()
    return df

def get_eth_analysis() -> dict:
    df1h  = _download_tf(**INTERVALS["1h"])
    df15m = _download_tf(**INTERVALS["15m"])

    ohlc_map = {
        "Open":   "first",
        "High":   "max",
        "Low":    "min",
        "Close":  "last",
        "Volume": "sum",
    }
    df4h = df1h.resample("4h", closed="right", label="right").agg(ohlc_map)
    df4h = add_basic_indicators(df4h).dropna()

    last1h = df1h.iloc[-1]
    if not df4h.empty:
        last4h = df4h.iloc[-1]
        trend_up = last4h["Close"] > last4h["MA20"]
    else:
        trend_up = False

    price = float(last1h["Close"])
    ma20  = float(last1h["MA20"])
    rsi   = float(last1h["RSI"])
    atr   = float(last1h["ATR"])
    short_up = (df15m["Close"].tail(12) > df15m["MA20"].tail(12)).all()

    signal = "✅ 做多" if (price > ma20 and 30 < rsi < 70 and trend_up and short_up) else "⏸ 观望"

    sl = price - ATR_MULT_SL * atr
    tp = price + ATR_MULT_TP * atr
    risk_usd = RISK_USD
    qty      = calc_position_size(risk_usd, price, sl)

    return {
        "price"      : price,
        "ma20"       : ma20,
        "rsi"        : rsi,
        "atr"        : atr,
        "signal"     : signal,
        "sl"         : round(sl, 2),
        "tp"         : round(tp, 2),
        "qty"        : round(qty, 4),
        "risk_usd"   : risk_usd,
        "update_time": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M"),
    }
