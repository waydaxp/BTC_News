import yfinance as yf
import pandas as pd

def get_btc_analysis():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="7d", interval="1h")

    if data.empty or len(data) < 20:
        return {
        "price": price,
        "ma20": ma20,
        "rsi": rsi,
        "signal": signal_text,
        "entry_price": entry,
        "stop_loss": stop,
        "take_profit": target,
        "max_loss": loss_amount,
        "per_trade_position": position,
    }

    # 技术指标计算
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

    # 仓位建议
    entry = round(close_price, 2)
    stop = round(entry * 0.985, 2)
    target = round(entry * 1.03, 2)
    signal = (
        "✅ 做多信号：突破 MA20 且 RSI 健康" if close_price > ma20 and rsi < 70
        else "🔻 做空信号：跌破 MA20 且 RSI 弱势" if close_price < ma20 and rsi > 30
        else "⏸ 中性信号：观望为主"
    )

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
        "entry": entry,
        "stop": stop,
        "target": target,
        "risk": risk,
        "position": position
    }
