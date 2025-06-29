# -*- coding: utf-8 -*-
"""
生成方向 & 风控参数
-------------------------------------------------
规则（可在 CONFIG 调整）：
1. 1h 价格 > MA20 & RSI>50 且连续 N 根满足才给多
2. 4h、1d 均在 MA20 之上 → 共振确认
3. 15m 必须再度站上 MA20 → 二次确认
4. 多头： SL = price - ATR,  TP = price + ATR * RR
   空头： SL = price + ATR,  TP = price - ATR * RR
5. 若高频回落：最新 3 根 K 总跌幅 > ATR * 2 直接 neutral
"""

from __future__ import annotations

import pandas as pd
from datetime import datetime

# core/signal.py
from core.indicators import add_basic_indicators, calc_atr, calc_rsi

# ========= CONFIG ========= #
TREND_LEN = 3       # 连续 K 数
CONFIRM_PERIODS = ["4h", "1d"]
RR = 1.5            # risk-reward，TP = ATR * RR
FAST_CANDLE_WINDOW = 3      # 回落检测用
FAST_CANDLE_FACTOR = 2      # 跌幅 > 2×ATR 过滤
# ========================== #


def _price_above_ma(df: pd.DataFrame, n: int = TREND_LEN) -> bool:
    """最近 n 根收盘价均 > MA20"""
    recent = df.tail(n)
    return (recent["close"] > recent["MA20"]).all()


def _rsi_strong(df: pd.DataFrame, n: int = TREND_LEN) -> bool:
    """最近 n 根 RSI > 50"""
    return (df.tail(n)["RSI"] > 50).all()


def make_signal(df_1h: pd.DataFrame,
                df_4h: pd.DataFrame,
                df_1d: pd.DataFrame,
                df_15m: pd.DataFrame) -> dict:
    """
    返回：
    {
        "direction":  "long" | "short" | "neutral",
        "sl":         float | None,
        "tp":         float | None,
        "atr":        float
    }
    """
    # ░░ 预处理 ░░
    for df in (df_1h, df_4h, df_1d, df_15m):
        add_basic_indicators(df)

    last_1h = df_1h.iloc[-1]
    atr = calc_atr(df_1h).iloc[-1]
    price = last_1h["close"]

    # ░░ 高频快速回落 ░░
    drop_3 = (df_1h.tail(FAST_CANDLE_WINDOW)["close"].iloc[-1]
              - df_1h.tail(FAST_CANDLE_WINDOW)["open"].iloc[0])
    if abs(drop_3) > atr * FAST_CANDLE_FACTOR:
        return {"direction": "neutral", "sl": None, "tp": None, "atr": atr}

    # ░░ 多头条件 ░░
    long_ok = (
        _price_above_ma(df_1h) and _rsi_strong(df_1h)
        and all(df.tail(1)["close"].iat[0] > df.tail(1)["MA20"].iat[0]
                for df in (df_4h, df_1d))  # 共振
        and df_15m.iloc[-1]["close"] > df_15m.iloc[-1]["MA20"]  # 二次确认
    )

    # ░░ 空头条件 ░░
    short_ok = (
        _price_above_ma(df_1h, n=1) is False  # 刚跌破 MA20
        and last_1h["close"] < last_1h["MA20"]
    )

    if long_ok:
        return {
            "direction": "long",
            "sl": round(price - atr, 2),
            "tp": round(price + atr * RR, 2),
            "atr": atr
        }
    if short_ok:
        return {
            "direction": "short",
            "sl": round(price + atr, 2),
            "tp": round(price - atr * RR, 2),
            "atr": atr
        }

    return {"direction": "neutral", "sl": None, "tp": None, "atr": atr}
