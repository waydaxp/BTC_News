# utils/fetch_btc_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.columns = df.columns.str.title()  # 标准化列名
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def _judge_signal(df: pd.DataFrame, scope: str = "short") -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()
    close = last['Close']
    ma20 = last['MA20']
    rsi = last['RSI']

    if scope == "short":
        recent_n = 5
        required_hits = 4
        rsi_range = (45, 65)
    elif scope == "mid":
        recent_n = 10
        required_hits = 6
        rsi_range = (45, 65)
    else:  # long
        recent_n = 8
        required_hits = 5
        rsi_range = (50, 65)

    recent = df['Close'].tail(recent_n)
    ma20_recent = df['MA20'].tail(recent_n)
    above = (recent > ma20_recent).sum()
    below = (recent < ma20_recent).sum()

    if close > ma20 and above >= required_hits and rsi_range[0] < rsi < rsi_range[1] and close > ma5.iloc[-1]:
        return "🟢 做多信号"
    elif close < ma20 and below >= required_hits and (rsi - ma5.iloc[-1]) < 0 and rsi < rsi_range[1]:
        return "🔻 做空信号"
    elif abs(rsi - 50) < 5:
        return "📉 震荡中性"
    elif above == below:
        return "😶 无趋势"
    elif (close > ma20 and rsi < 40) or (close < ma20 and rsi > 60):
        return "⚠️ 背离预警"
    else:
        return "⏸ 中性信号"


def get_btc_analysis() -> dict:
    df15 = _download_tf("15m", "3d")   # 短线
    df1h = _download_tf("1h", "7d")     # 中期
    df4h = _download_tf("4h", "30d")    # 长期

    signal15 = _judge_signal(df15, "short")
    signal1h = _judge_signal(df1h, "mid")
    signal4h = _judge_signal(df4h, "long")

    last = df1h.iloc[-1]  # 中期信号用于交易建议
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
        "signal": f"{signal4h} (4h) / {signal1h} (1h) / {signal15} (15m)",
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time
    }
