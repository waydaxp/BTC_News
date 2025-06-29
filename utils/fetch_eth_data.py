# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.columns = df.columns.str.title()  # 标准化列名
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def _judge_signal(df: pd.DataFrame, window: int, rsi_low: int, rsi_high: int) -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()

    recent = df['Close'].tail(window) > df['MA20'].tail(window)
    above_ma20 = recent.sum() >= int(window * 0.8)

    below_recent = df['Close'].tail(window) < df['MA20'].tail(window)
    below_ma20 = below_recent.sum() >= int(window * 0.8)

    rsi = last['RSI']

    # 背离预警
    if (df['Close'].diff().tail(3).mean() > 0 and df['RSI'].diff().tail(3).mean() < 0) or \
       (df['Close'].diff().tail(3).mean() < 0 and df['RSI'].diff().tail(3).mean() > 0):
        return "⚠️ 背离预警"

    # 无趋势：涨跌相等
    last_10 = df['Close'].diff().tail(10)
    ups = (last_10 > 0).sum()
    downs = (last_10 < 0).sum()
    if abs(ups - downs) <= 2:
        return "😶 无趋势"

    # 震荡中性
    if 45 <= rsi <= 55:
        return "📉 震荡中性"

    if last['Close'] > last['MA20'] and above_ma20 and rsi_low < rsi < rsi_high and last['Close'] > ma5.iloc[-1]:
        return "🟢 做多信号"
    elif last['Close'] < last['MA20'] and below_ma20 and (rsi - 5) < 55 and last['Close'] < ma5.iloc[-1]:
        return "🔻 做空信号"
    else:
        return "⏸ 中性信号"


def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")    # 短线
    df1h = _download_tf("1h", "7d")      # 中期
    df4h = _download_tf("4h", "30d")     # 长期

    signal15 = _judge_signal(df15, window=5, rsi_low=45, rsi_high=65)
    signal1h = _judge_signal(df1h, window=10, rsi_low=45, rsi_high=65)
    signal4h = _judge_signal(df4h, window=8, rsi_low=50, rsi_high=65)

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
