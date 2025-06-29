# utils/fetch_eth_data.py
import yfinance as yf
from core.indicators import add_basic_indicators

PAIR = "ETH-USD"
PERIOD = "7d"
INTERVAL = "60m"


def get_eth_analysis() -> dict:
    df = yf.download(PAIR, period=PERIOD, interval=INTERVAL, progress=False)
    df = df.rename(columns=str.title)
    df = add_basic_indicators(df)

    last = df.iloc[-1]
    price = float(last["Close"])
    ma20 = float(last["MA20"])
    rsi = float(last["RSI"])

    if price > ma20 and 30 < rsi < 70:
        signal = "✅ 做多信号"
    elif price < ma20 and 30 < rsi < 70:
        signal = "🔻 做空信号"
    else:
        signal = "⏸ 观望"

    return {
        "price": price,
        "ma20": ma20,
        "rsi": rsi,
        "signal": signal,
    }
