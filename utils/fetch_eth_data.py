# utils/fetch_eth_data.py
import yfinance as yf
import pandas as pd

def get_eth_analysis():
    """和 BTC 结构完全一致，便于 generate_data.py 统一处理"""
    eth = yf.Ticker("ETH-USD")
    df = eth.history(period="7d", interval="1h")

    if df.empty or len(df) < 20:
        return {k: "N/A" for k in (
            "price", "ma20", "rsi", "signal",
            "entry_price", "stop_loss", "take_profit",
            "max_loss", "per_trade_position", "strategy_text"
        )}

    # === 技术指标 ===
    df["MA20"] = df["Close"].rolling(20).mean()
    delta      = df["Close"].diff()
    gain       = delta.where(delta > 0, 0).rolling(14).mean()
    loss       = -delta.where(delta < 0, 0).rolling(14).mean()
    rs         = gain / loss
    df["RSI"]  = 100 - 100 / (1 + rs)

    last        = df.iloc[-1]
    price       = float(last["Close"])
    ma20        = float(last["MA20"])
    rsi         = float(last["RSI"])

    # === 方向 & 价格区间 ===
    if price > ma20 and 30 < rsi < 70:
        direction = "long"
        signal    = "✅ 做多信号：突破 MA20 且 RSI 健康"
        stop_mul, tp_mul = 0.985, 1.03
        strategy  = "✅ 做多：买入 → 涨\n跌 1.5% 止损\n涨 3% 止盈"
    elif price < ma20 and 30 < rsi < 70:
        direction = "short"
        signal    = "🔻 做空信号：跌破 MA20 且 RSI 弱势"
        stop_mul, tp_mul = 1.015, 0.97
        strategy  = "🔻 做空：卖出 → 跌\n涨 1.5% 止损\n跌 3% 止盈"
    elif rsi >= 70:
        direction = "overbought"
        signal    = "⚠️ 超买风险：谨慎做多"
        stop_mul = tp_mul = None
        strategy  = "⚠️ 超买，请谨慎交易"
    elif rsi <= 30:
        direction = "oversold"
        signal    = "⚠️ 超卖风险：谨慎做空"
        stop_mul = tp_mul = None
        strategy  = "⚠️ 超卖，请谨慎交易"
    else:
        direction = "neutral"
        signal    = "⏸ 中性信号：观望为主"
        stop_mul = tp_mul = None
        strategy  = "⏸ 观望"

    entry   = round(price, 2)
    stop    = round(entry * stop_mul, 2)  if stop_mul else "N/A"
    target  = round(entry * tp_mul, 2)    if tp_mul  else "N/A"

    # === 风控 ===
    acc_usd, lev, risk_pct = 1000, 20, 0.02
    max_loss = round(acc_usd * risk_pct, 2)
    position = round(max_loss * lev, 2)

    return {
        "price": price, "ma20": ma20, "rsi": rsi, "signal": signal,
        "entry_price": entry, "stop_loss": stop, "take_profit": target,
        "max_loss": max_loss, "per_trade_position": position,
        "strategy_text": strategy
    }
