# utils/fetch_eth_data.py
# -----------------------------------------------------------
# ETH 技术分析（返回字段与 BTC 相同）
# 默认 still 使用 ATR × 1 止损 / 1.8 R 止盈
# -----------------------------------------------------------

import yfinance as yf
import pandas  as pd

from core.signal import make_signal, TREND_LEN
from core.risk   import get_sl_tp


# ─────────── 工具函数 ─────────── #
def _fetch_ohlc(interval: str, lookback: str) -> pd.DataFrame:
    df = yf.Ticker("ETH-USD").history(period=lookback, interval=interval)
    df.rename(columns=str.lower, inplace=True)
    return df


def _ensure_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if "ma20" not in df:
        df["ma20"] = df["close"].rolling(20, min_periods=20).mean()

    if "rsi" not in df:
        delta = df["close"].diff()
        up    = delta.clip(lower=0).rolling(14).mean()
        down  = -delta.clip(upper=0).rolling(14).mean()
        rs    = up / down
        df["rsi"] = 100 - 100 / (1 + rs)

    return df
# ─────────────────────────────── #


def get_eth_analysis() -> dict:
    df_1h = _fetch_ohlc("1h", "14d")
    df_4h = _fetch_ohlc("4h", "60d")

    if df_1h.empty or df_4h.empty:
        return {"signal": "⚠️ 数据不足", "strategy_text": "无"}

    df_1h = _ensure_indicators(df_1h)
    df_4h = _ensure_indicators(df_4h)

    direction = make_signal(df_1h, df_4h)

    last  = df_1h.iloc[-1]
    price = float(last["close"])
    ma20  = float(last["ma20"])
    rsi   = float(last["rsi"])

    # 动态 SL / TP
    sl, tp, strat_txt = get_sl_tp(
        direction, price, df_1h,
        mode="atr",
        atr_mul=1.0,
        rr=1.8
    )

    if direction == "long":
        sig = f"✅ 做多信号：连续{TREND_LEN}根站上 MA20"
    elif direction == "short":
        sig = f"🔻 做空信号：连续{TREND_LEN}根跌破 MA20"
    else:
        sig = "⏸ 中性信号：观望为主"

    acct_usd = 1000
    leverage = 20
    max_loss = round(acct_usd * 0.02, 2)
    pos_size = round(max_loss * leverage, 2)

    return {
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "signal": sig,

        "entry_price":  price,
        "stop_loss":    sl,
        "take_profit":  tp,
        "max_loss":     max_loss,
        "per_trade_position": pos_size,

        "strategy_text": strat_txt,
    }
