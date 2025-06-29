# core/signal.py
# =========================================================
# 生成做多 / 做空 / 观望 信号的统一模块
# =========================================================
from typing import Literal
import pandas as pd

# 4H 趋势均线长度；默认 MA50，可按策略调整
TREND_LEN: int = 50

Signal = Literal["long", "short", "neutral"]


def make_signal(df_1h: pd.DataFrame, df_4h: pd.DataFrame) -> Signal:
    """
    根据 1H + 4H K 线数据，综合 MA20 / MA{TREND_LEN} + RSI 判定方向

    参数
    ----
    df_1h : pd.DataFrame
        必须包含 ["Close", "MA20", "RSI"]
    df_4h : pd.DataFrame
        必须包含 ["Close", f"MA{TREND_LEN}"]

    返回值
    ------
    "long"     → 做多
    "short"    → 做空
    "neutral"  → 观望
    """
    # 若数据不足，直接观望
    if df_1h.empty or df_4h.empty:
        return "neutral"

    last_1h = df_1h.iloc[-1]
    last_4h = df_4h.iloc[-1]

    close_1h = float(last_1h["Close"])
    ma20_1h  = float(last_1h["MA20"])
    rsi_1h   = float(last_1h["RSI"])

    close_4h = float(last_4h["Close"])
    ma_trend = float(last_4h[f"MA{TREND_LEN}"])

    # ────────── 条件拆解 ──────────
    above_ma20   = close_1h > ma20_1h
    below_ma20   = close_1h < ma20_1h
    rsi_normal   = 30 < rsi_1h < 70          # 超买 >70 / 超卖 <30 过滤
    trend_up     = close_4h > ma_trend
    trend_down   = close_4h < ma_trend

    # ────────── 判定 ──────────
    if above_ma20 and rsi_normal and trend_up:
        return "long"

    if below_ma20 and rsi_normal and trend_down:
        return "short"

    return "neutral"
