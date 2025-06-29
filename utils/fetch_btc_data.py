# ✅ 修改后的 utils/fetch_btc_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)

    # 兼容多层列名结构，统一为单层列名
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def get_btc_analysis() -> dict:
    df15 = _download_tf("15m", "3d")  # 短线
    df1h = _download_tf("1h", "7d")   # 中期
    df4h = _download_tf("4h", "30d")  # 长期

    last15 = df15.iloc[-1]
    last1 = df1h.iloc[-1]
    last4 = df4h.iloc[-1]

    price = float(last1['Close'])
    atr = float(last1['ATR'])

    def check_signal(df, last, tf_name):
        ma20 = float(last['MA20'])
        rsi = float(last['RSI'])
        ma5 = float(last['MA5']) if 'MA5' in last else last['Close'].rolling(5).mean().iloc[-1]

        above_ma20 = (df['Close'].tail(5) > df['MA20'].tail(5)).sum()
        below_ma20 = (df['Close'].tail(5) < df['MA20'].tail(5)).sum()

        if last['Close'] > ma20 and above_ma20 >= 4 and 45 < rsi < 65 and last['Close'] > ma5:
            return f"✅ 短线做多信号 ({tf_name})"
        elif last['Close'] < ma20 and below_ma20 >= 4 and 35 < rsi < 55 and last['Close'] < ma5:
            return f"🔻 短线做空信号 ({tf_name})"
        else:
            return f"⏸ 中性信号 ({tf_name})"

    signal15 = check_signal(df15, last15, "15m")
    signal1h = check_signal(df1h, last1, "1h")
    signal4h = check_signal(df4h, last4, "4h")

    signal = f"{signal4h} / {signal1h} / {signal15}"

    if "做多" in signal1h:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "做空" in signal1h:
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        sl = None
        tp = None
        qty = 0.0

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "ma20": float(last1['MA20']),
        "rsi": float(last1['RSI']),
        "atr": atr,
        "signal": signal,
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time,
    }
