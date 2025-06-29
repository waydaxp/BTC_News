"""
统一风控函数
============================================
提供:
    • calc_atr(df, period=14)
    • get_sl_tp(direction, entry, df,
                mode="atr", atr_mul=1, rr=1.8,
                lookback=20, buffer_pct=0.003)
--------------------------------------------
mode:
    "atr"        -> 固定 ATR×mul 止损，TP = SL × rr
    "structure"  -> 最近 swing high/low ± buffer 止损
                     TP = entry ± (risk × rr)
返回:
    sl_price, tp_price, text_str
"""

import pandas as pd
import numpy  as np


# ────────────────────────────────────────────
def calc_atr(df: pd.DataFrame, period: int = 14) -> float:
    high, low, close = df["high"], df["low"], df["close"]
    tr = np.maximum.reduce([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ])
    return tr.rolling(period).mean().iloc[-1]


def get_sl_tp(
    direction: str,
    entry: float,
    df: pd.DataFrame,
    *,
    mode: str = "atr",
    atr_mul: float = 1.0,
    rr: float = 1.8,                 # TP = SL × rr
    lookback: int = 20,
    buffer_pct: float = 0.003
):
    """
    direction: "long" / "short"
    mode     : "atr" / "structure"
    """
    if direction not in ("long", "short"):
        return "N/A", "N/A", "⏸ 无方向，观望"

    # --- ATR 止损 ----------------------------------
    if mode == "atr":
        atr = calc_atr(df, 14)
        sl = entry - atr * atr_mul if direction == "long" else entry + atr * atr_mul
        tp = entry + atr * atr_mul * rr if direction == "long" else entry - atr * atr_mul * rr

        text = (
            f"{'✅ 做多' if direction=='long' else '🔻 做空'}\n"
            f"止损 = ATR×{atr_mul:.1f} ≈ {abs(entry-sl):.2f}\n"
            f"止盈 = {rr:.1f}R ≈ {abs(tp-entry):.2f}"
        )
        return round(sl, 2), round(tp, 2), text

    # --- 结构止损 ----------------------------------
    swing_buf = 1 - buffer_pct if direction == "long" else 1 + buffer_pct
    if direction == "long":
        swing = df["low"].rolling(lookback).min().iloc[-2]     # 前一根内最低点
        sl = round(swing * swing_buf, 2)
        risk = entry - sl
        tp = round(entry + risk * rr, 2)
    else:
        swing = df["high"].rolling(lookback).max().iloc[-2]
        sl = round(swing * swing_buf, 2)
        risk = sl - entry
        tp = round(entry - risk * rr, 2)

    text = (
        f"{'✅ 做多' if direction=='long' else '🔻 做空'}\n"
        f"结构止损@前{lookback}根 swing ±{buffer_pct*100:.1f}%\n"
        f"TP = {rr:.1f}R"
    )
    return sl, tp, text
