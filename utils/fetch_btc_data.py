# utils/fetch_btc_data.py
import yfinance as yf
import pandas as pd

def analyze_btc():
    btc = yf.Ticker("BTC-USD")
    df = btc.history(period="7d", interval="1h")
    df["MA20"] = df["Close"].rolling(window=20).mean()
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    last = df.iloc[-1]
    msg = f"\n📊【BTC 分析】\n当前价格: ${last['Close']:.2f}\nMA20: ${last['MA20']:.2f}\nRSI: {last['RSI']:.2f}"
    if last['Close'] > last['MA20'] and last['RSI'] < 70:
        msg += "\n✅ 建议：顺势轻仓做多"
    elif last['Close'] < last['MA20'] and last['RSI'] > 30:
        msg += "\n⚠️ 建议：趋势转弱，观望或轻仓做空"
    else:
        msg += "\n⏸ 建议：震荡行情，耐心等待突破"
    return msg
