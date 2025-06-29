import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.columns = df.columns.str.title()
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()

def _generate_signal(df: pd.DataFrame, label: str) -> str:
    last = df.iloc[-1]
    closes = df['Close'].tail(5)
    ma20s = df['MA20'].tail(5)

    above = (closes > ma20s).sum()
    below = (closes < ma20s).sum()

    if last['Close'] > last['MA20'] and last['Close'] > last['MA5'] and above >= 4 and 45 < last['RSI'] < 65:
        return f"📈 {label}做多信号"
    elif last['Close'] < last['MA20'] and last['Close'] < last['MA5'] and below >= 4 and 35 < last['RSI'] < 55:
        return f"📉 {label}做空信号"
    else:
        return f"⏸ {label}中性信号"

def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")    # 短线
    df1h = _download_tf("1h",  "7d")    # 中期
    df4h = df1h.resample("4h").agg({
        'Open': 'first', 'High': 'max', 'Low': 'min',
        'Close': 'last', 'Volume': 'sum'
    }).dropna()
    df4h = add_basic_indicators(df4h)

    last = df1h.iloc[-1]
    price = float(last['Close'])
    ma20 = float(last['MA20'])
    rsi = float(last['RSI'])
    atr = float(last['ATR'])

    # 多周期信号
    short_signal = _generate_signal(df15, "短线")
    mid_signal   = _generate_signal(df1h,  "中期")
    long_signal  = _generate_signal(df4h,  "长期")

    signal = " / ".join([short_signal, mid_signal, long_signal])

    if "做多" in mid_signal:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "做空" in mid_signal:
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        sl, tp, qty = None, None, 0.0

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
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
