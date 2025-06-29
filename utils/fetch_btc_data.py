# utils/fetch_btc_data.py
import yfinance as yf
from datetime import datetime, timezone, timedelta

from core.indicators import add_basic_indicators, calc_atr, calc_rsi

PAIR = "BTC-USD"

CFG = {
    "1h":  {"period": "7d", "interval": "60m"},
    "15m": {"period": "2d", "interval": "15m"},  # 15m 线只能拉 ≤30d
}


def _download_tf(period: str, interval: str):
    df = yf.download(PAIR, period=period, interval=interval, progress=False)
    df = df.rename(columns=str.title)  # Close/High/Low...
    return add_basic_indicators(df)


def get_btc_analysis() -> dict:
    df_1h  = _download_tf(**CFG["1h"])
    df_15m = _download_tf(**CFG["15m"])

    last_1h  = df_1h.iloc[-1]
    last_15m = df_15m.iloc[-1]

    price_1h = float(last_1h["Close"])
    ma20_1h  = float(last_1h["MA20"])
    rsi_1h   = float(last_1h["RSI"])
    atr_1h   = float(last_1h["ATR"])

    # ===== ① 先按 1h 判断方向 =====
    if price_1h > ma20_1h and 30 < rsi_1h < 70:
        dir_1h, sig = "long", "✅ 做多信号：1h 站上 MA20 & RSI 健康"
    elif price_1h < ma20_1h and 30 < rsi_1h < 70:
        dir_1h, sig = "short", "🔻 做空信号：1h 跌破 MA20 & RSI 弱势"
    else:
        dir_1h, sig = "flat",  "⏸ 中性信号：1h 观望"

    # ===== ② 15m 二次确认 =====
    ok_long  = last_15m["Close"] > last_15m["MA20"]
    ok_short = last_15m["Close"] < last_15m["MA20"]

    if dir_1h == "long" and not ok_long:
        dir_final, sig = "flat", "⚠️ 短线背离：15m 未站上 MA20，观望"
    elif dir_1h == "short" and not ok_short:
        dir_final, sig = "flat", "⚠️ 短线背离：15m 未跌破 MA20，观望"
    else:
        dir_final = dir_1h  # 一致或本身就是 flat

    # ===== ③ 风控（ATR 止损 / 1:1.5 TP） =====
    risk_usd = 20
    leverage = 20
    position = risk_usd * leverage

    if dir_final == "long":
        sl = round(price_1h - atr_1h, 2)
        tp = round(price_1h + 1.5 * atr_1h, 2)
    elif dir_final == "short":
        sl = round(price_1h + atr_1h, 2)
        tp = round(price_1h - 1.5 * atr_1h, 2)
    else:
        sl = tp = None

    bj_time = datetime.now(timezone(timedelta(hours=8))).strftime("%F %T")

    return {
        "price": price_1h,
        "ma20":  ma20_1h,
        "rsi":   rsi_1h,
        "atr":   atr_1h,
        "signal": sig,
        "direction": dir_final,
        "entry_price": price_1h,
        "stop_loss":   sl,
        "take_profit": tp,
        "risk_usd":    risk_usd,
        "position":    position,
        "updated_time": bj_time,
    }
