# utils/fetch_eth_data.py
import yfinance as yf
import pandas as pd

def get_eth_analysis():
    eth = yf.Ticker("ETH-USD")
    data = eth.history(period="7d", interval="1h")

    if data.empty or len(data) < 20:
        return "⚠️ 无法获取足够的 ETH 数据进行分析。"

    data["MA20"] = data["Close"].rolling(window=20).mean()
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]
    close_price = latest["Close"]
    ma20 = latest["MA20"]
    rsi = latest["RSI"]

    signal = ""
    if close_price > ma20 and rsi < 70:
        signal = "✅ 做多信号"
    elif close_price < ma20 and rsi > 30:
        signal = "🔻 做空信号"
    else:
        signal = "⏸ 中性观望"

    return f"""📉【ETH 技术分析】\n当前价格: ${close_price:.2f}\nMA20: ${ma20:.2f}\nRSI: {rsi:.2f}\n技术信号: {signal}\n"""
