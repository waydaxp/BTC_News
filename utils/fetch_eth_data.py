import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df.columns = [c.title() for c in df.columns]

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()


def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")

    last15 = df15.iloc[-1]
    last1 = df1h.iloc[-1]

    price = float(last1['Close'])
    ma20 = float(last1['MA20'])
    ma5 = float(last1['MA5'])
    rsi = float(last1['RSI'])
    atr = float(last1['ATR'])

    closes = df15['Close'].tail(5)
    ma20s = df15['MA20'].tail(5)

    trend_up = (price > ma20) and (closes > ma20s).sum() >= 4 and price > ma5 and 45 < rsi < 65
    trend_down = (price < ma20) and (closes < ma20s).sum() >= 4 and price < ma5 and 35 < rsi < 55

    if trend_up:
        signal = "✅ 做多信号"
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif trend_down:
        signal = "❌ 做空信号"
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        signal = "⏸ 中性信号：观望"
        sl = None
        tp = None
        qty = 0.0

    update_time = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

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
