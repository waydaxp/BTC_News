# utils/fetch_eth_data.py
# --------------------------------------------------
# ETH-USD 与 BTC 流程相同，代码几乎一致；如需改动阈值可单独调
# --------------------------------------------------
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators

ACCOUNT_USD      = 1000
LEVERAGE         = 20
RISK_PER_TRADE   = 0.02
ATR_SL_FACTOR    = 1.0
ATR_TP_FACTOR    = 1.5


def _position_size():
    max_loss = round(ACCOUNT_USD * RISK_PER_TRADE, 2)
    position = round(max_loss * LEVERAGE, 2)
    return max_loss, position


def get_eth_analysis() -> dict:
    raw = yf.Ticker("ETH-USD").history(period="7d", interval="1h")

    if raw.empty or len(raw) < 40:
        return {"signal": "⚠️ 数据不足，无法计算指标"}

    df   = add_basic_indicators(raw)
    last = df.iloc[-1]

    price = float(last["Close"])
    ma20  = float(last["MA20"])
    rsi   = float(last["RSI"])
    atr   = float(last["ATR"])

    if price > ma20 and 40 < rsi < 70:
        direction = "long"
        signal = f"✅ 做多信号：收盘价站上 MA20 且 RSI={rsi:.1f}"
    elif price < ma20 and 30 < rsi < 60:
        direction = "short"
        signal = f"🔻 做空信号：收盘价跌破 MA20 且 RSI={rsi:.1f}"
    else:
        direction = "flat"
        signal = "⏸ 中性信号：观望为主"

    if direction == "long":
        stop  = round(price - atr * ATR_SL_FACTOR, 2)
        tp    = round(price + atr * ATR_TP_FACTOR, 2)
        strat = "✅ 做多：\n  · 止损= price-ATR\n  · 止盈= price+1.5×ATR"
    elif direction == "short":
        stop  = round(price + atr * ATR_SL_FACTOR, 2)
        tp    = round(price - atr * ATR_TP_FACTOR, 2)
        strat = "🔻 做空：\n  · 止损= price+ATR\n  · 止盈= price-1.5×ATR"
    else:
        stop = tp = "N/A"
        strat = "⏸ 观望：不入场"

    max_loss, position = _position_size()

    return {
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "atr":   atr,
        "signal": signal,
        "entry_price": price,
        "stop_loss":   stop,
        "take_profit": tp,
        "max_loss":    max_loss,
        "per_trade_position": position,
        "strategy_text": strat,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
    }
