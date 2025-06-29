"""
BTC 技术分析 —— 统一给 generate_data.py 使用
------------------------------------------------
1. 先取 1h / 4h K 线
2. 若 DF 尚未有 MA20 / RSI ⇒ 立即计算
3. 调用 core.signal.make_signal(df_1h, df_4h) 生成方向
4. 输出字段与 ETH 保持一致
"""

import yfinance as yf
import pandas  as pd

from core.signal import make_signal, TREND_LEN


# ---------- 工具 ---------- #
def _fetch_ohlc(interval: str, lookback: str) -> pd.DataFrame:
    df = yf.Ticker("BTC-USD").history(period=lookback, interval=interval)
    df.rename(columns=str.lower, inplace=True)          # open/high/low/close
    return df


def _ensure_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """如没有 MA20 / RSI 就现场计算——避免 KeyError。"""
    if "ma20" not in df:
        df["ma20"] = df["close"].rolling(20, min_periods=20).mean()
    if "rsi" not in df:
        delta = df["close"].diff()
        up    = delta.clip(lower=0).rolling(14).mean()
        down  = -delta.clip(upper=0).rolling(14).mean()
        rs    = up / down
        df["rsi"] = 100 - 100 / (1 + rs)
    return df
# -------------------------- #


def get_btc_analysis() -> dict:

    df_1h = _fetch_ohlc("1h", "10d")
    df_4h = _fetch_ohlc("4h", "40d")

    if df_1h.empty or df_4h.empty:
        return {"signal": "⚠️ 数据不足"}

    df_1h = _ensure_indicators(df_1h)
    df_4h = _ensure_indicators(df_4h)

    # === 方向判断 ===
    direction = make_signal(df_1h, df_4h)

    last  = df_1h.iloc[-1]
    price = float(last["close"])
    ma20  = float(last["ma20"])
    rsi   = float(last["rsi"])

    # === 风控参数 ===
    acct_usd = 1000
    leverage = 20
    max_loss = round(acct_usd * 0.02, 2)
    pos_size = round(max_loss * leverage, 2)

    entry = price
    if direction == "long":
        stop = round(price * 0.985, 2)
        tp   = round(price  * 1.03, 2)
        sig  = f"✅ 做多信号：连续{TREND_LEN}根站上 MA20"
    elif direction == "short":
        stop = round(price * 1.015, 2)
        tp   = round(price * 0.97, 2)
        sig  = f"🔻 做空信号：连续{TREND_LEN}根跌破 MA20"
    else:
        stop = tp = "N/A"
        sig  = "⏸ 中性信号：观望为主"

    return {
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "signal": sig,

        "entry_price":  entry,
        "stop_loss":    stop,
        "take_profit":  tp,
        "max_loss":     max_loss,
        "per_trade_position": pos_size,
    }
