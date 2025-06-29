# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.columns = df.columns.str.title()
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def _judge_signal(df: pd.DataFrame, label: str = "") -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()
    recent_close = df['Close'].tail(5)
    recent_ma20 = df['MA20'].tail(5)

    above = (recent_close > recent_ma20).sum()
    below = (recent_close < recent_ma20).sum()

    if above >= 4 and last['Close'] > last['MA20'] and 45 < last['RSI'] < 65 and last['Close'] > ma5.iloc[-1]:
        return f"🟢 做多信号"
    elif below >= 4 and last['Close'] < last['MA20'] and 35 < last['RSI'] < 55 and last['Close'] < ma5.iloc[-1]:
        return f"🔻 做空信号"
    elif 40 < last['RSI'] < 60 and abs(last['Close'] - last['MA20']) / last['MA20'] < 0.01:
        return f"🔘 震荡中性"
    elif abs(last['RSI'] - 50) < 3 and abs(last['Close'] - last['MA20']) / last['MA20'] < 0.003:
        return f"⚪ 无趋势"
    elif (last['Close'] > last['MA20'] and last['RSI'] < 45) or (last['Close'] < last['MA20'] and last['RSI'] > 55):
        return f"🌀 指标背离"
    else:
        return f"⏸ 中性信号"


def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")
    df4h = _download_tf("4h", "30d")

    signal15 = _judge_signal(df15)
    signal1h = _judge_signal(df1h)
    signal4h = _judge_signal(df4h)

    last = df1h.iloc[-1]  # 中期信号用于交易建议
    price = float(last['Close'])
    atr = float(last['ATR'])

    if "做多" in signal1h:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "做空" in signal1h:
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        sl, tp, qty = None, None, 0.0

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "ma20": float(last["MA20"]),
        "rsi": float(last["RSI"]),
        "atr": atr,
        "signal": f"{signal4h} (4h) / {signal1h} (1h) / {signal15} (15m)",
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time,
    }
