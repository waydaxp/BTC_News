import yfinance as yf
import pandas as pd

def get_eth_analysis():
    eth = yf.Ticker("ETH-USD")
    data = eth.history(period="7d", interval="1h")

    if data.empty or len(data) < 20:
        return {
            "price": "N/A",
            "ma20": "N/A",
            "rsi": "N/A",
            "signal": "⚠️ 数据不足",
        }

    data["MA20"] = data["Close"].rolling(window=20).mean()
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]
    close_price = float(latest["Close"])
    ma20 = float(latest["MA20"])
    rsi = float(latest["RSI"])

    signal = (
        "✅ 做多信号：突破 MA20 且 RSI 健康" if close_price > ma20 and rsi < 70
        else "🔻 做空信号：跌破 MA20 且 RSI 弱势" if close_price < ma20 and rsi > 30
        else "⏸ 中性信号：观望为主"
    )

    return {
        "price": close_price,
        "ma20": ma20,
        "rsi": rsi,
        "signal": signal,
    }
