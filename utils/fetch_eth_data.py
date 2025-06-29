# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)  # 修复多层列名
    df.columns = df.columns.str.title()
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def _judge_signal(df: pd.DataFrame, label: str) -> str:
    last = df.iloc[-1]
    close = last['Close']
    rsi = last['RSI']
    ma20 = last['MA20']
    ma5 = df['Close'].rolling(5).mean().iloc[-1]

    above_ma20_count = (df['Close'].tail(5) > df['MA20'].tail(5)).sum()
    below_ma20_count = (df['Close'].tail(5) < df['MA20'].tail(5)).sum()

    if close > ma20 and above_ma20_count >= 4 and 45 < rsi < 65 and close > ma5:
        return f"🟢 做多信号（{label}）"
    elif close < ma20 and below_ma20_count >= 4 and 35 < rsi < 55 and close < ma5:
        return f"🔻 做空信号（{label}）"
    elif 45 <= rsi <= 55:
        return f"🔘 震荡中性（{label}）"
    elif rsi > 70 or rsi < 30:
        return f"⚠️ 背离风险（{label}）"
    else:
        return f"⏸ 无趋势（{label}）"


def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")
    df4h = _download_tf("4h", "30d")

    signal15 = _judge_signal(df15, "15m")
    signal1h = _judge_signal(df1h, "1h")
    signal4h = _judge_signal(df4h, "4h")

    last = df1h.iloc[-1]
    price = float(last['Close'])
    atr = float(last['ATR'])

    if "多" in signal1h:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "空" in signal1h:
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        sl, tp, qty = None, None, 0.0

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "ma20": float(last['MA20']),
        "rsi": float(last['RSI']),
        "atr": atr,
        "signal": f"{signal4h} / {signal1h} / {signal15}",
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time
    }
