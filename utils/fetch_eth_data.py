# utils/fetch_eth_data.py
import yfinance as yf
import pandas as pd

def analyze_eth():
    eth = yf.Ticker("ETH-USD")
    df = eth.history(period="7d", interval="1h")
    df["MA20"] = df["Close"].rolling(window=20).mean()
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    last = df.iloc[-1]
    msg = f"\n🟣【ETH 分析】\n当前价格: ${last['Close']:.2f}\nMA20: ${last['MA20']:.2f}\nRSI: {last['RSI']:.2f}"
    if last['Close'] > last['MA20'] and last['RSI'] < 70:
        msg += "\n✅ 建议：ETH 同步 BTC 做多"
    elif last['Close'] < last['MA20'] and last['RSI'] > 30:
        msg += "\n⚠️ 建议：ETH 存在回调风险"
    else:
        msg += "\n⏸ 建议：ETH 当前处于震荡区"
    return msg
