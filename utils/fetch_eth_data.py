# utils/fetch_eth_data.py
import yfinance as yf
import pandas as pd

def get_eth_analysis():
    eth = yf.Ticker("ETH-USD")
    data = eth.history(period="7d", interval="1h")

    if data.empty or len(data) < 20:
        return {"error": "⚠️ 无法获取足够的 ETH 数据进行分析。"}

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

    entry_price = round(close_price, 2)
    stop_loss = round(entry_price * 0.985, 2)
    take_profit = round(entry_price * 1.03, 2)

    if close_price > ma20 and rsi < 70:
        signal = "✅ 做多信号：突破 MA20 且 RSI 健康"
    elif close_price < ma20 and rsi > 30:
        signal = "🔻 做空信号：跌破 MA20 且 RSI 弱势"
    else:
        signal = "⏸ 中性信号：观望为主"

    account_usd = 1000
    leverage = 20
    risk_per_trade = 0.02
    max_loss = account_usd * risk_per_trade
    per_trade_position = round(max_loss * leverage, 2)

    return {
        "eth_price": f"{close_price:.2f}",
        "eth_ma20": f"{ma20:.2f}",
        "eth_rsi": f"{rsi:.2f}",
        "eth_signal": signal,
        "eth_risk": f"{max_loss:.2f}",
        "eth_position": f"{per_trade_position:.2f}",
        "eth_entry": f"{entry_price}",
        "eth_stop": f"{stop_loss}",
        "eth_target": f"{take_profit}",
    }
