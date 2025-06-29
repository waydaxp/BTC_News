# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)

    # 如果是 MultiIndex（含 ticker 名），则压平为单层列名
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(1)

    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def _judge_signal(df: pd.DataFrame) -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()
    recent = df['Close'].tail(5) > df['MA20'].tail(5)
    above_ma20 = recent.sum() >= 4
    below_ma20 = (df['Close'].tail(5) < df['MA20'].tail(5)).sum() >= 4

    if last['RSI'] < 40 or last['RSI'] > 70:
        return "⚠ 背离信号"
    if abs(last['Close'] - last['MA20']) / last['MA20'] < 0.005:
        return "⏸ 震荡中性"

    if last['Close'] > last['MA20'] and above_ma20 and 45 < last['RSI'] < 65 and last['Close'] > ma5.iloc[-1]:
        return "🟢 做多信号"
    elif last['Close'] < last['MA20'] and below_ma20 and 35 < last['RSI'] < 55 and last['Close'] < ma5.iloc[-1]:
        return "🔻 做空信号"
    else:
        return "⏸ 中性信号"


def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")   # 短线
    df1h = _download_tf("1h", "7d")    # 中期
    df4h = _download_tf("4h", "30d")   # 长期

    signals = {
        '15m': _judge_signal(df15),
        '1h': _judge_signal(df1h),
        '4h': _judge_signal(df4h),
    }

    last = df1h.iloc[-1]  # 中期判断交易
    price = float(last['Close'])
    atr = float(last['ATR'])

    if "多" in signals['1h']:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "空" in signals['1h']:
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
        "signal": f"{signals['4h']} (4h) / {signals['1h']} (1h) / {signals['15m']} (15m)",
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time,
    }
