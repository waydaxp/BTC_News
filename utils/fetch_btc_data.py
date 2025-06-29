# utils/fetch_btc_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

from core.indicators import add_basic_indicators
from core.risk import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "BTC-USD"
TZ = "Asia/Shanghai"

# 定义你要拉哪些周期的数据
CFG = {
    "1h":   {"interval": "1h",  "period": "7d"},
    "4h":   {"interval": "1h",  "period": "7d"},   # 拉1h后再resample成4h
    "15m":  {"interval": "15m", "period": "1d"},
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    # 拉取
    df: pd.DataFrame = yf.download(PAIR, interval=interval, period=period, progress=False)
    # 转本地时区
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(TZ)
    else:
        df.index = df.index.tz_convert(TZ)
    return add_basic_indicators(df).dropna()

def get_btc_analysis() -> dict:
    # 1h, 4h, 15m 三张表
    df_1h  = _download_tf(**CFG["1h"])
    # 4h：从1h重采样
    ohlc = {"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}
    df_4h = df_1h.resample("4h", closed="right", label="right").agg(ohlc).dropna()
    df_4h = add_basic_indicators(df_4h)
    df_15m = _download_tf(**CFG["15m"])

    # 拿最后一根数据
    last_1h = df_1h.iloc[-1]
    last_4h = df_4h.iloc[-1]
    last_15m = df_15m.iloc[-1]

    price = float(last_1h["Close"])
    ma20  = float(last_1h["MA20"])
    rsi   = float(last_1h["RSI"])
    atr   = float(last_1h["ATR"])

    # 多头条件：4h 和 15m 都在均线上方
    trend_up = (last_4h["Close"] > last_4h["MA20"]) and (last_15m["Close"] > last_15m["MA20"])
    if trend_up and 30 < rsi < 70:
        side = "long"
        signal = "✅ 做多"
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
    else:
        side = "short"
        signal = "⛔ 观望"
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr

    # 计算仓位
    qty = calc_position_size(
        price,        # 当前价格
        RISK_USD,     # 风险美元
        ATR_MULT_SL,  # 止损ATR倍数
        atr,          # ATR本身
        side          # long/short
    )

    return {
        "price": price,
        "ma20": ma20,
        "rsi":  rsi,
        "atr":  atr,
        "signal": signal,
        "sl":   round(sl, 2),
        "tp":   round(tp, 2),
        "qty":  round(qty, 4),
        "risk_usd": RISK_USD,
        "update_time": datetime.now(pytz.timezone(TZ)).strftime("%Y-%m-%d %H:%M"),
    }
