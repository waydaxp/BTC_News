# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)

    # 如果是多重索引，重新设置列名
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = df.columns.str.title()  # 标准化列名
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def _judge_signal(df: pd.DataFrame, window: int = 5) -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(window).mean()
    above_ma20 = (df['Close'].tail(window) > df['MA20'].tail(window)).sum()
    below_ma20 = (df['Close'].tail(window) < df['MA20'].tail(window)).sum()

    if above_ma20 >= window - 1 and last['Close'] > last['MA20'] and last['Close'] > ma5.iloc[-1] and 45 < last['RSI'] < 65:
        return "🟢 多头趋势"
    elif below_ma20 >= window - 1 and last['Close'] < last['MA20'] and last['Close'] < ma5.iloc[-1] and 35 < last['RSI'] < 55:
        return "🔻 空头趋势"
    elif abs(last['RSI'] - 50) < 3 and abs(last['Close'] - last['MA20']) / last['MA20'] < 0.01:
        return "📊 震荡中性"
    elif (last['RSI'] > 70 and last['Close'] < last['MA20']) or (last['RSI'] < 30 and last['Close'] > last['MA20']):
        return "⚠️ 技术背离"
    else:
        return "⏸ 中性信号"


def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")
    df4h = _download_tf("4h", "30d")

    signal15 = _judge_signal(df15)
    signal1h = _judge_signal(df1h)
    signal4h = _judge_signal(df4h)

    last = df1h.iloc[-1]  # 用中期信号做风控建议
    price = float(last["Close"])
    atr = float(last["ATR"])

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
        "signal": f"{signal4h}（4h） / {signal1h}（1h） / {signal15}（15m）",
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time
    }
