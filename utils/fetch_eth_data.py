# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.columns = df.columns.to_flat_index()
    df.columns = [c[0].title() if isinstance(c, tuple) else c for c in df.columns]
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def judge_signal(df: pd.DataFrame, interval: str) -> tuple:
    close = df.iloc[-1]['Close']
    ma20 = df.iloc[-1]['MA20']
    rsi = df.iloc[-1]['RSI']
    atr = df.iloc[-1]['ATR']
    ma5 = df['Close'].rolling(5).mean()
    df['MA5'] = ma5

    last5 = df['Close'].tail(5)
    ma5_last = ma5.iloc[-1]

    long_cond = (close > ma20 and (last5 > df['MA20'].tail(5)).sum() >= 4 and 45 < rsi < 65 and close > ma5_last)
    short_cond = (close < ma20 and (last5 < df['MA20'].tail(5)).sum() >= 4 and 35 < rsi < 55 and close < ma5_last)

    if long_cond:
        signal = f"🟢 做多信号（{interval}）"
    elif short_cond:
        signal = f"🔻 做空信号（{interval}）"
    else:
        signal = f"⏸ 中性信号（{interval}）"

    return signal, close, ma20, rsi, atr


def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")
    df4h = _download_tf("4h", "30d")

    sig15, close15, _, _, _ = judge_signal(df15, "15m")
    sig1h, close1h, _, _, _ = judge_signal(df1h, "1h")
    sig4h, close4h, ma20, rsi, atr = judge_signal(df4h, "4h")

    # 默认基于 1h 做风控
    price = close1h
    if "做多" in sig1h:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "做空" in sig1h:
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        sl, tp, qty = None, None, 0.0

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "ma20": ma20,
        "rsi": rsi,
        "atr": atr,
        "signal": f"{sig4h} / {sig1h} / {sig15}",
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time,
    }
