# -*- coding: utf-8 -*-
"""
日内信号生成：输入多周期 K 线 → 输出方向 & 交易参数
"""
from __future__ import annotations
import pandas as pd
from core.config import DAYTRADE_CFG as C

# ────────────────────────────────────
def make_signal(df_5m: pd.DataFrame,
                df_15m: pd.DataFrame,
                df_1h: pd.DataFrame,
                df_4h: pd.DataFrame) -> dict:
    """
    返回:
        {'direction': long|short|neutral,
         'entry': float,
         'sl': float,
         'tp': float}
    """
    # ① 15m 趋势段
    cond_long  = (df_15m["Close"].tail(C["TREND_LEN"]) > df_15m["MA20"].tail(C["TREND_LEN"])).all() \
                 and df_15m["RSI"].iloc[-1] > 50
    cond_short = (df_15m["Close"].tail(C["TREND_LEN"]) < df_15m["MA20"].tail(C["TREND_LEN"])).all() \
                 and df_15m["RSI"].iloc[-1] < 50

    # ② 1h & 4h 共振
    trend_up   = (df_1h["Close"].iloc[-1] > df_1h["MA20"].iloc[-1]) and \
                 (df_4h["Close"].iloc[-1] > df_4h["MA20"].iloc[-1])
    trend_down = (df_1h["Close"].iloc[-1] < df_1h["MA20"].iloc[-1]) and \
                 (df_4h["Close"].iloc[-1] < df_4h["MA20"].iloc[-1])

    # ③ 5m 二次确认
    ok_long  = (df_5m["Close"].tail(C["N5M_LEN"]) > df_5m["MA20"].tail(C["N5M_LEN"])).all()
    ok_short = (df_5m["Close"].tail(C["N5M_LEN"]) < df_5m["MA20"].tail(C["N5M_LEN"])).all()

    # ④ 快速波动过滤
    rng_5m  = df_5m["High"].tail(C["N5M_LEN"]).max() - df_5m["Low"].tail(C["N5M_LEN"]).min()
    atr_1h  = df_1h["ATR"].iloc[-1]
    calm_enough = rng_5m <= C["VOL_FILTER"] * atr_1h

    # ───── 最终方向 ─────
    if cond_long and trend_up and ok_long and calm_enough:
        direction = "long"
    elif cond_short and trend_down and ok_short and calm_enough:
        direction = "short"
    else:
        return {"direction": "neutral"}

    # ───── 计算 Entry / SL / TP ─────
    price = df_5m["Close"].iloc[-1]
    atr   = df_15m["ATR"].iloc[-1]
    if direction == "long":
        sl = price - C["ATR_SL"] * atr
        tp = price + C["ATR_TP"] * atr
    else:
        sl = price + C["ATR_SL"] * atr
        tp = price - C["ATR_TP"] * atr

    return {
        "direction": direction,
        "entry": round(price, 2),
        "sl":    round(sl,    2),
        "tp":    round(tp,    2),
    }
