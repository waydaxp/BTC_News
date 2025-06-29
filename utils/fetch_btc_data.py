# utils/fetch_btc_data.py

import pandas as pd
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "BTC-USD"
TZ   = "Asia/Shanghai"

# 各周期参数
INTERVALS = {
    "1h":  {"interval": "1h",  "period": "5d"},
    "15m": {"interval": "15m", "period": "1d"},
}

def _flatten_ohlc_columns(df: pd.DataFrame) -> pd.DataFrame:
    # 如果是 MultiIndex，取第一个层级，否则首字母大写
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0).str.capitalize()
    else:
        df.columns = [str(c).capitalize() for c in df.columns]
    return df

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten_ohlc_columns(df)
    # 时区处理：先 localize，再 convert
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(TZ)
    else:
        df.index = df.index.tz_convert(TZ)
    # 加入基本技术指标，去掉 NaN
    return add_basic_indicators(df).dropna()

def get_btc_analysis() -> dict:
    # 读取 1h 与 15m
    df1h  = _download_tf(**INTERVALS["1h"])
    df15m = _download_tf(**INTERVALS["15m"])

    # 从 1h 重采样出 4h K 线
    ohlc_map = {"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}
    df4h = df1h.resample("4h", closed="right", label="right").agg(ohlc_map)
    df4h = add_basic_indicators(df4h).dropna()

    last1h = df1h.iloc[-1]
    # 趋势：4h 收盘站上/下 MA20
    trend_up = False
    if not df4h.empty:
        last4h = df4h.iloc[-1]
        trend_up = last4h["Close"] > last4h["MA20"]

    # 基本数值
    price    = float(last1h["Close"])
    ma20     = float(last1h["MA20"])
    rsi      = float(last1h["RSI"])
    atr      = float(last1h["ATR"])
    # 15m 看短周期持续性
    short_up = (df15m["Close"].tail(12) > df15m["MA20"].tail(12)).all()

    # 信号生成
    signal = "✅ 做多" if (price > ma20 and 30 < rsi < 70 and trend_up and short_up) else "⏸ 观望"

    # 止损 / 止盈 计算
    sl = price - ATR_MULT_SL * atr
    tp = price + ATR_MULT_TP * atr

    # 仓位：传入 atr_value 和 side="long"
    qty      = calc_position_size(RISK_USD, price, atr, "long")

    return {
        "price"      : round(price, 2),
        "ma20"       : round(ma20, 2),
        "rsi"        : round(rsi, 2),
        "atr"        : round(atr, 2),
        "signal"     : signal,
        "sl"         : round(sl, 2),
        "tp"         : round(tp, 2),
        "qty"        : round(qty, 6),
        "risk_usd"   : RISK_USD,
        "update_time": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M"),
    }
