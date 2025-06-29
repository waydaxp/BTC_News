# === fetch_btc_data.py ===

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False, auto_adjust=True)
    df.columns = df.columns.droplevel(1) if isinstance(df.columns, pd.MultiIndex) else df.columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()

def get_btc_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h",  "7d")

    df4h = df1h.resample("4h", label="right", closed="right").agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()
    df4h = add_basic_indicators(df4h).dropna()

    last15 = df15.iloc[-1]
    last1  = df1h.iloc[-1]
    last4  = df4h.iloc[-1]

    price = float(last1['Close'])
    ma20  = float(last1['MA20'])
    rsi   = float(last1['RSI'])
    atr   = float(last1['ATR'])

    trend_up = (
        (last4['Close'] > last4['MA20']) and
        (df15['Close'].tail(12) > df15['MA20'].tail(12)).all()
    )

    if trend_up and 30 < rsi < 70:
        signal = "✅ 做多信号"
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    else:
        signal = "⏸ 中性信号：观望"
        sl = None
        tp = None
        qty = 0.0

    update_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "ma20": ma20,
        "rsi": rsi,
        "atr": atr,
        "signal": signal,
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time,
    }
