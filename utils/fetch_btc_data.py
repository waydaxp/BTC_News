# utils/fetch_btc_data.py
import pandas as pd
import yfinance as yf
from datetime import datetime
from core.indicators  import add_basic_indicators
from core.risk        import RISK_USD, ATR_MULT_SL, ATR_MULT_TP, calc_position_size

PAIR = "BTC-USD"
TZ   = "Asia/Shanghai"

# 各周期下载配置
INTERVALS = {
    "1h":  {"interval": "1h",  "period": "3d"},
    "4h":  {"interval": "1h",  "period": "10d"},  # 先 1h 拉取再重采样
    "15m": {"interval": "15m", "period": "1d"},
}

def _flatten_ohlc_columns(df: pd.DataFrame) -> pd.DataFrame:
    """扁平化 MultiIndex 列，然后首字母大写"""
    if isinstance(df.columns, pd.MultiIndex):
        # 只保留第一层名称
        df.columns = df.columns.get_level_values(0).str.capitalize()
    else:
        df.columns = [str(c).capitalize() for c in df.columns]
    return df

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """下载、扁平化、时区转换、指标计算并丢弃空值"""
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten_ohlc_columns(df)
    # 时区：如果已经带 tz，则直接转；否则先标记 UTC 再转
    idx = df.index
    df.index = idx.tz_convert(TZ) if idx.tzinfo else idx.tz_localize("UTC").tz_convert(TZ)
    df = add_basic_indicators(df).dropna()
    return df

def get_btc_analysis() -> dict:
    """
    返回键：
      price, ma20, rsi, atr,
      signal, sl, tp, qty, risk_usd,
      update_time
    """
    # 拉取各周期
    df1h  = _download_tf(**INTERVALS["1h"])
    # 用 1h 数据重采样到 4h
    ohlc = {"open":"first","high":"max","low":"min","close":"last","volume":"sum"}
    df4h  = _flatten_ohlc_columns(df1h.resample("4h", closed="right", label="right").agg(ohlc))
    df4h  = add_basic_indicators(df4h).dropna()
    df15m = _download_tf(**INTERVALS["15m"])

    # 最新值
    last1h = df1h.iloc[-1]
    last4h = df4h.iloc[-1]

    price = float(last1h["Close"])
    ma20  = float(last1h["Ma20"])
    rsi   = float(last1h["Rsi"])
    atr   = float(last1h["Atr"])

    # 趋势与短周期确认
    trend_up    = last4h["Close"] > last4h["Ma20"]
    short_up    = (df15m["Close"].tail(12) > df15m["Ma20"].tail(12)).all()

    # 信号逻辑
    if price > ma20 and 30 < rsi < 70 and trend_up and short_up:
        signal = "✅ 做多"
    else:
        signal = "⏸ 观望"

    # 止损/止盈
    sl = price - ATR_MULT_SL  * atr
    tp = price + ATR_MULT_TP  * atr

    # 按固定美元风险计算仓位
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
