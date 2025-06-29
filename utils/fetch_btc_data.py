# utils/fetch_btc_data.py
import pandas as pd
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "BTC-USD"
TZ = "Asia/Shanghai"

# 拉 1h 时段延长到 5 天以保证至少有一个 4h 数据；15m 保持 1 天
INTERVALS = {
    "1h":  {"interval": "1h",  "period": "5d"},
    "15m": {"interval": "15m", "period": "1d"},
}

def _flatten_ohlc_columns(df: pd.DataFrame) -> pd.DataFrame:
    """将 MultiIndex OHLC 列／不同来源的大小写统一为首字母大写形式"""
    if isinstance(df.columns, pd.MultiIndex):
        # keep only first level ('Open','High'...)
        df.columns = df.columns.get_level_values(0).str.capitalize()
    else:
        df.columns = [str(c).capitalize() for c in df.columns]
    return df

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    # 下载
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten_ohlc_columns(df)
    # 时区处理
    idx = df.index
    if idx.tz is None:
        df.index = idx.tz_localize("UTC").tz_convert(TZ)
    else:
        df.index = idx.tz_convert(TZ)
    # 加指标并清理
    df = add_basic_indicators(df).dropna()
    return df

def get_btc_analysis() -> dict:
    # 下载各周期
    df1h  = _download_tf(**INTERVALS["1h"])
    df15m = _download_tf(**INTERVALS["15m"])

    # 从 1h 重采样得 4h
    ohlc_map = {
        "Open":   "first",
        "High":   "max",
        "Low":    "min",
        "Close":  "last",
        "Volume": "sum",
    }
    df4h = df1h.resample("4h", closed="right", label="right").agg(ohlc_map)
    df4h = add_basic_indicators(df4h).dropna()

    # 取最新
    last1h = df1h.iloc[-1]
    # 如果 4h 没数据就降级为 False
    if not df4h.empty:
        last4h = df4h.iloc[-1]
        trend_up = last4h["Close"] > last4h["MA20"]
    else:
        trend_up = False

    # 指标取值
    price = float(last1h["Close"])
    ma20  = float(last1h["MA20"])
    rsi   = float(last1h["RSI"])
    atr   = float(last1h["ATR"])
    # 15m 连续 12 根站上 MA20
    short_up = (df15m["Close"].tail(12) > df15m["MA20"].tail(12)).all()

    # 信号逻辑
    signal = "✅ 做多" if (price > ma20 and 30 < rsi < 70 and trend_up and short_up) else "⏸ 观望"

    # 止损止盈
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
