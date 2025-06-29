# utils/fetch_btc_data.py
# --------------------------------------------------
# 获取 BTC-USD 最近 7 天 1h K 线 → 计算指标 → 产出交易信号 & 风控
# --------------------------------------------------
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators

# ==== 全局配置（可迁移到 config.yaml） ====
ACCOUNT_USD      = 1000        # 账户本金
LEVERAGE         = 20          # 杠杆倍数
RISK_PER_TRADE   = 0.02        # 单笔风险 2%
ATR_SL_FACTOR    = 1.0         # 止损 = ATR × 1
ATR_TP_FACTOR    = 1.5         # 止盈 = ATR × 1.5


def _position_size() -> tuple[float, float]:
    """
    返回 max_loss(USD)、per_trade_position(USD 计)
    """
    max_loss = round(ACCOUNT_USD * RISK_PER_TRADE, 2)
    position = round(max_loss * LEVERAGE, 2)
    return max_loss, position


def get_btc_analysis() -> dict:
    raw = yf.Ticker("BTC-USD").history(period="7d", interval="1h")

    # 数据不足
    if raw.empty or len(raw) < 40:          # 至少 40 根用于计算 20 & 14
        return {"signal": "⚠️ 数据不足，无法计算指标"}

    df   = add_basic_indicators(raw)
    last = df.iloc[-1]

    price = float(last["Close"])
    ma20  = float(last["MA20"])
    rsi   = float(last["RSI"])
    atr   = float(last["ATR"])

    # ===== 生成交易方向 =====
    if price > ma20 and 40 < rsi < 70:
        direction = "long"
        signal = f"✅ 做多信号：收盘价站上 MA20 且 RSI={rsi:.1f}"
    elif price < ma20 and 30 < rsi < 60:
        direction = "short"
        signal = f"🔻 做空信号：收盘价跌破 MA20 且 RSI={rsi:.1f}"
    else:
        direction = "flat"
        signal = "⏸ 中性信号：观望为主"

    # ===== 风控参数 =====
    if direction == "long":
        stop  = round(price - atr * ATR_SL_FACTOR, 2)
        tp    = round(price + atr * ATR_TP_FACTOR, 2)
        strat = "✅ 做多：\n  · 止损= price-ATR\n  · 止盈= price+1.5×ATR"
    elif direction == "short":
        stop  = round(price + atr * ATR_SL_FACTOR, 2)
        tp    = round(price - atr * ATR_TP_FACTOR, 2)
        strat = "🔻 做空：\n  · 止损= price+ATR\n  · 止盈= price-1.5×ATR"
    else:       # flat
        stop = tp = "N/A"
        strat = "⏸ 观望：不入场"

    max_loss, position = _position_size()

    return {
        # 数据
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "atr":   atr,
        # 信号 & 方向
        "signal": signal,
        # 风控
        "entry_price": price,
        "stop_loss":   stop,
        "take_profit": tp,
        "max_loss":    max_loss,
        "per_trade_position": position,
        "strategy_text": strat,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
    }
