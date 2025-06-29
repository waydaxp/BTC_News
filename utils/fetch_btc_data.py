# utils/fetch_btc_data.py
import pandas as pd
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "BTC-USD"
TZ = "Asia/Shanghai"

# 配置各周期下载参数
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
    # 时区处理
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(TZ)
    else:
        df.index = df.index.tz_convert(TZ)
    df = add_basic_indicators(df).dropna()
    return df

def get_btc_analysis() -> dict:
    # 下载 1h 和 15m 数据
    df1h  = _download_tf(**INTERVALS["1h"])
    df15m = _download_tf(**INTERVALS["15m"])

    # 从 1h 重采样出 4h
    ohlc_map = {"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}
    df4h = df1h.resample("4h", closed="right", label="right").agg(ohlc_map)
    df4h = add_basic_indicators(df4h).dropna()

    # 最新 K 线
    last1h = df1h.iloc[-1]
    if not df4h.empty:
        last4h = df4h.iloc[-1]
        trend_up = last4h["Close"] > last4h["MA20"]
    else:
        trend_up = False

    # 指标取值
    price    = float(last1h["Close"])
    ma20     = float(last1h["MA20"])
    rsi      = float(last1h["RSI"])
    atr      = float(last1h["ATR"])
    short_up = (df15m["Close"].tail(12) > df15m["MA20"].tail(12)).all()

    # 信号逻辑
    signal = "✅ 做多" if (price>ma20 and 30<rsi<70 and trend_up and short_up) else "⏸ 观望"

    # 止损止盈（ATR + 系数）
    sl = price - ATR_MULT_SL*atr
    tp = price + ATR_MULT_TP*atr

    # 按 ATR 风控仓位：传入 atr_value 和 side="long"
    risk_usd = RISK_USD
    qty      = calc_position_size(risk_usd, price, atr, "long")

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
