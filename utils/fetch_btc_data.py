### 文件1: utils/fetch_btc_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.columns = df.columns.str.title()
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()

def _judge_signal(df: pd.DataFrame) -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()
    recent = df['Close'].tail(5) > df['MA20'].tail(5)
    above_ma20 = recent.sum() >= 4

    if last['Close'] > last['MA20'] and above_ma20 and 45 < last['RSI'] < 65 and last['Close'] > ma5.iloc[-1]:
        return "🟢 做多信号"
    elif last['Close'] < last['MA20'] and (df['Close'].tail(5) < df['MA20'].tail(5)).sum() >= 4 and 35 < last['RSI'] < 55 and last['Close'] < ma5.iloc[-1]:
        return "🔻 做空信号"
    else:
        return "⏸ 中性信号"

def _trade_details(df: pd.DataFrame, signal: str) -> tuple:
    last = df.iloc[-1]
    price = float(last['Close'])
    atr = float(last['ATR'])
    if "多" in signal:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "空" in signal:
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        sl, tp, qty = None, None, 0.0
    return price, sl, tp, qty

def get_btc_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")
    df4h = _download_tf("4h", "30d")

    signal15 = _judge_signal(df15)
    signal1h = _judge_signal(df1h)
    signal4h = _judge_signal(df4h)

    price15, sl15, tp15, qty15 = _trade_details(df15, signal15)
    price1h, sl1h, tp1h, qty1h = _trade_details(df1h, signal1h)
    price4h, sl4h, tp4h, qty4h = _trade_details(df4h, signal4h)

    last = df1h.iloc[-1]
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": float(last['Close']),
        "ma20": float(last['MA20']),
        "rsi": float(last['RSI']),
        "atr": float(last['ATR']),
        "signal": f"{signal4h} (4h) / {signal1h} (1h) / {signal15} (15m)",
        "update_time": update_time,

        "btc15_price": price15, "btc15_sl": sl15, "btc15_tp": tp15,
        "btc1h_price": price1h, "btc1h_sl": sl1h, "btc1h_tp": tp1h,
        "btc4h_price": price4h, "btc4h_sl": sl4h, "btc4h_tp": tp4h,
        "btc_qty": qty1h, "btc_risk": RISK_USD
    }
