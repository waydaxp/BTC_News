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
        df.columns = df.columns.get_level_values(0)
    df = df[['Open','High','Low','Close','Volume']].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()

def judge_signal(df: pd.DataFrame, timeframe: str) -> str:
    last = df.iloc[-1]
    recent_close = df['Close'].tail(5)
    recent_ma20 = df['MA20'].tail(5)
    above_ma20_count = (recent_close > recent_ma20).sum()
    below_ma20_count = (recent_close < recent_ma20).sum()

    if last['Close'] > last['MA20'] and above_ma20_count >= 4 and 45 < last['RSI'] < 65 and last['Close'] > df['Close'].rolling(5).mean().iloc[-1]:
        return f"🟢 做多信号（{timeframe}）"
    elif last['Close'] < last['MA20'] and below_ma20_count >= 4 and 35 < last['RSI'] < 55 and last['Close'] < df['Close'].rolling(5).mean().iloc[-1]:
        return f"🔻 做空信号（{timeframe}）"
    else:
        return f"⏸ 中性信号：观望（{timeframe}）"

def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")
    df4h = df1h.resample("4h", label="right", closed="right").agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
    }).dropna()
    df4h = add_basic_indicators(df4h)

    last = df1h.iloc[-1]
    price = float(last['Close'])
    ma20 = float(last['MA20'])
    rsi = float(last['RSI'])
    atr = float(last['ATR'])

    trend_short = judge_signal(df15, "15m")
    trend_mid = judge_signal(df1h, "1h")
    trend_long = judge_signal(df4h, "4h")

    # 以中期信号为核心做仓位判断
    if "做多" in trend_mid:
        signal = trend_mid
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "做空" in trend_mid:
        signal = trend_mid
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        signal = trend_mid
        sl = None
        tp = None
        qty = 0.0

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        "trend_short": trend_short,
        "trend_mid": trend_mid,
        "trend_long": trend_long,
    }
