# utils/fetch_btc_data.py
import pandas as pd
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "BTC-USD"
TZ = "Asia/Shanghai"

# 只拉取 1h 和 15m，多周期通过重采样得到 4h
INTERVALS = {
    "1h":  {"interval": "1h",  "period": "3d"},
    "15m": {"interval": "15m", "period": "1d"},
}

def _flatten_ohlc_columns(df: pd.DataFrame) -> pd.DataFrame:
    """扁平化 MultiIndex 列，然后首字母大写"""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0).str.capitalize()
    else:
        df.columns = [str(c).capitalize() for c in df.columns]
    return df

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """下载原始 OHLCV、扁平化列名、时区转换、添加指标并去空"""
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten_ohlc_columns(df)
    idx = df.index
    df.index = idx.tz_convert(TZ) if idx.tzinfo else idx.tz_localize("UTC").tz_convert(TZ)
    df = add_basic_indicators(df).dropna()
    return df

def get_btc_analysis() -> dict:
    """返回 BTC 各项分析结果"""
    # 拉 1h 和 15m
    df1h  = _download_tf(**INTERVALS["1h"])
    df15m = _download_tf(**INTERVALS["15m"])

    # 从 1h 重采样出 4h
    ohlc_map = {
        "Open":   "first",
        "High":   "max",
        "Low":    "min",
        "Close":  "last",
        "Volume": "sum",
    }
    df4h = df1h.resample("4h", closed="right", label="right").agg(ohlc_map)
    df4h = add_basic_indicators(df4h).dropna()

    # 最新点
    last1h = df1h.iloc[-1]
    last4h = df4h.iloc[-1]

    price = float(last1h["Close"])
    ma20  = float(last1h["Ma20"])
    rsi   = float(last1h["Rsi"])
    atr   = float(last1h["Atr"])

    trend_up = last4h["Close"] > last4h["Ma20"]
    short_up = (df15m["Close"].tail(12) > df15m["Ma20"].tail(12)).all()

    # 信号逻辑
    signal = "✅ 做多" if (price > ma20 and 30 < rsi < 70 and trend_up and short_up) else "⏸ 观望"

    # 止损 / 止盈
    sl = price - ATR_MULT_SL * atr
    tp = price + ATR_MULT_TP * atr

    # 头寸计算
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
