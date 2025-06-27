# utils/fetch_btc_data.py

import yfinance as yf
import pandas as pd

def get_btc_analysis():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")

    if data.empty or len(data) < 20:
        return {
            "error": "⚠️ 无法获取足够的 BTC 数据进行分析。"
        }

    # 计算技术指标
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

    # 信号判断
    if close_price > ma20 and rsi < 70:
        signal = "✅ 做多信号：突破 MA20 且 RSI 健康"
    elif close_price < ma20 and rsi > 30:
        signal = "🔻 做空信号：跌破 MA20 且 RSI 弱势"
    else:
        signal = "⏸ 中性信号：观望为主"

    # 仓位控制建议
    account_usd = 1000
    leverage = 20
    risk_per_trade = 0.02
    max_loss = round(account_usd * risk_per_trade, 2)
    per_trade_position = round(max_loss * leverage, 2)
    entry_price = round(close_price, 2)
    stop_loss = round(entry_price * 0.985, 2)
    take_profit = round(entry_price * 1.03, 2)

    return {
        "price": f"{close_price:.2f}",
        "ma20": f"{ma20:.2f}",
        "rsi": f"{rsi:.2f}",
        "signal": signal,
        "risk": f"${max_loss:.2f}",
        "position": f"${per_trade_position:.2f}",
        "entry": f"${entry_price}",
        "stop": f"${stop_loss}",
        "target": f"${take_profit}",
        "text": f"""📈【BTC 技术分析】
当前价格: ${close_price:.2f}
MA20: ${ma20:.2f}
RSI: {rsi:.2f}
技术信号: {signal}

📊 操作建议：
- 💰 建议单笔风险金额: ${max_loss:.2f}（账户总额的2%）
- 🔧 杠杆后下单量: ${per_trade_position:.2f}
- 📌 建议建仓价: ${entry_price}
- 🛑 止损设定: ${stop_loss}
- 🎯 止盈目标: ${take_profit}
"""
    }
