# utils/fetch_btc_data.py
import yfinance as yf
import pandas as pd

def get_btc_analysis():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")

    if data.empty or len(data) < 20:
        return {
            "price": "N/A",
            "ma20": "N/A",
            "rsi": "N/A",
            "signal": "⚠️ 数据不足",
            "entry_price": "N/A",
            "stop_loss": "N/A",
            "take_profit": "N/A",
            "max_loss": "N/A",
            "per_trade_position": "N/A",
            "strategy_text": "N/A",
            "direction": "neutral"
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

    # 默认策略方向
    direction = "neutral"

    if close_price > ma20 and 30 < rsi < 70:
        signal = "✅ 做多信号：突破 MA20 且 RSI 健康"
        entry = round(close_price, 2)
        stop = round(entry * 0.985, 2)
        target = round(entry * 1.03, 2)
        strategy_text = "✅ 做多\n买入 → 涨\n跌 1.5% 止损\n涨 3% 止盈"
        direction = "long"
    elif close_price < ma20 and 30 < rsi < 70:
        signal = "🔻 做空信号：跌破 MA20 且 RSI 弱势"
        entry = round(close_price, 2)
        stop = round(entry * 1.015, 2)
        target = round(entry * 0.97, 2)
        strategy_text = "🔻 做空\n卖出 → 跌\n涨 1.5% 止损\n跌 3% 止盈"
        direction = "short"
    elif rsi >= 70:
        signal = "⚠️ 超买风险：谨慎做多"
        entry = stop = target = strategy_text = "N/A"
    elif rsi <= 30:
        signal = "⚠️ 超卖风险：谨慎做空"
        entry = stop = target = strategy_text = "N/A"
    else:
        signal = "⏸ 中性信号：观望为主"
        entry = stop = target = strategy_text = "N/A"

    account_usd = 1000
    leverage = 20
    risk_per_trade = 0.02
    risk = round(account_usd * risk_per_trade, 2)
    position = round(risk * leverage, 2)

    return {
        "price": close_price,
        "ma20": ma20,
        "rsi": rsi,
        "signal": signal,
        "entry_price": entry,
        "stop_loss": stop,
        "take_profit": target,
        "max_loss": risk,
        "per_trade_position": position,
        "strategy_text": strategy_text,
        "direction": direction
    }
