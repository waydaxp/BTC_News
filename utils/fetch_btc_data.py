"""
BTC 数据抓取 + 技术分析
--------------------------------
返回结构示例：
{
    "price": 107000,
    "ma20":  106800,
    "rsi":   55.1,
    "signal":"✅ 做多信号：连续3根站上 MA20",
    ...
}
"""

import yfinance as yf
import pandas  as pd

from core.signal import make_signal, TREND_LEN


def _fetch_ohlc(interval: str, lookback: str) -> pd.DataFrame:
    btc = yf.Ticker("BTC-USD")
    df  = btc.history(period=lookback, interval=interval)
    df.rename(columns=str.lower, inplace=True)          # 统一字段：open/close/...
    return df


def get_btc_analysis() -> dict:
    # 拉取 1h / 4h K 线
    df_1h = _fetch_ohlc("1h", "7d")
    df_4h = _fetch_ohlc("4h", "30d")

    if df_1h.empty or df_4h.empty:
        return {"signal": "⚠️ 数据不足"}

    # 信号方向
    direction = make_signal(df_1h, df_4h)

    last = df_1h.iloc[-1]
    price = float(last["close"])
    ma20  = float(last["MA20"])
    rsi   = float(last["RSI"])

    # === 统一风控示例 ===
    account_usd = 1000
    leverage    = 20
    max_loss    = round(account_usd * 0.02, 2)        # 2 % 账户风险
    pos_size    = round(max_loss * leverage, 2)

    entry = price
    if direction == "long":
        stop = round(price * 0.985, 2)
        tp   = round(price * 1.03, 2)
        sig_txt = f"✅ 做多信号：连续{TREND_LEN}根站上 MA20"
    elif direction == "short":
        stop = round(price * 1.015, 2)
        tp   = round(price * 0.97, 2)
        sig_txt = f"🔻 做空信号：连续{TREND_LEN}根跌破 MA20"
    else:
        stop = tp = "N/A"
        sig_txt = "⏸ 中性信号：观望为主"

    return {
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "signal": sig_txt,

        "entry_price":  entry,
        "stop_loss":    stop,
        "take_profit":  tp,
        "max_loss":     max_loss,
        "per_trade_position": pos_size,
    }
