"""
信号判定核心模块
----------------
- 计算常用技术指标（MA / RSI / ADX / ATR）
- 根据 1h 图 + 4h 图给出做多 / 做空 / 观望 信号
"""

import pandas as pd
import numpy  as np
import talib

# ====== ★ 全局参数（其他文件只需要 import 即可） ===================== #
TREND_LEN  = 3     # 连续 N 根 K 线确认
ADX_TH     = 20    # ADX > 20 说明存在趋势
ATR_WIN    = 14
# ======================================================================= #


def _add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """给 DataFrame 添加常用指标列（就地修改后返回）"""
    df["MA20"] = df["close"].rolling(20).mean()
    df["RSI"]  = talib.RSI(df["close"], timeperiod=14)
    df["ADX"]  = talib.ADX(df["high"], df["low"], df["close"], timeperiod=14)
    df["ATR"]  = talib.ATR(df["high"], df["low"], df["close"], timeperiod=ATR_WIN)
    return df


def make_signal(df_1h: pd.DataFrame, df_4h: pd.DataFrame) -> str:
    """
    综合 1h 与 4h 数据判断方向
    ------------------------------------
    return: {"long" | "short" | "neutral"}
    """
    if df_1h.empty or df_4h.empty:
        return "neutral"

    df_1h = _add_indicators(df_1h.copy())
    df_4h = _add_indicators(df_4h.copy())

    last_1h = df_1h.iloc[-1]
    last_4h = df_4h.iloc[-1]

    # 1⃣️  高周期方向确认
    up_4h   = last_4h["close"] > last_4h["MA20"]
    down_4h = last_4h["close"] < last_4h["MA20"]

    # 2⃣️  连续 N 根 K 线同向
    long_ok  = (df_1h["close"] > df_1h["MA20"]).tail(TREND_LEN).all()
    short_ok = (df_1h["close"] < df_1h["MA20"]).tail(TREND_LEN).all()

    # 3⃣️  趋势强度过滤
    has_trend = last_1h["ADX"] > ADX_TH

    if long_ok and up_4h and has_trend and 30 < last_1h["RSI"] < 70:
        return "long"
    if short_ok and down_4h and has_trend and 30 < last_1h["RSI"] < 70:
        return "short"
    return "neutral"
