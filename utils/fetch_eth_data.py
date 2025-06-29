# utils/fetch_eth_data.py
import yfinance as yf
from core.indicators import add_basic_indicators

PAIR = "ETH-USD"

CFG = {
    "1h":  {"period": "7d", "interval": "60m"},
    "15m": {"period": "2d", "interval": "15m"},
}


def _download_tf(period: str, interval: str):
    df = yf.download(PAIR, period=period, interval=interval, progress=False)
    df = df.rename(columns=str.title)
    return add_basic_indicators(df)


def get_eth_analysis() -> dict:
    df_1h  = _download_tf(**CFG["1h"])
    df_15m = _download_tf(**CFG["15m"])

    last_1h  = df_1h.iloc[-1]
    last_15m = df_15m.iloc[-1]

    price = float(last_1h["Close"])
    ma20  = float(last_1h["MA20"])
    rsi   = float(last_1h["RSI"])

    if price > ma20 and 30 < rsi < 70 and last_15m["Close"] > last_15m["MA20"]:
        sig = "✅ 做多（1h+15m 一致）"
    elif price < ma20 and 30 < rsi < 70 and last_15m["Close"] < last_15m["MA20"]:
        sig = "🔻 做空（1h+15m 一致）"
    else:
        sig = "⏸ 背离 / 观望"

    return {
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "signal": sig,
    }
