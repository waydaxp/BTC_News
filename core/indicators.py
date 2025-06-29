# -*- coding: utf-8 -*-
"""
**零依赖** 指标实现：MA、RSI、ATR
可放心跑在 GitHub Actions / 低配 VPS 上
"""

from __future__ import annotations
import pandas as pd
import numpy as np


def add_basic_indicators(df: pd.DataFrame,
                         ma_periods: tuple[int, ...] = (20, 50)) -> pd.DataFrame:
    """就地添加 MA 与 RSI 列"""
    for p in ma_periods:
        df[f"MA{p}"] = df["close"].rolling(p).mean()
    df["RSI"] = calc_rsi(df)
    return df


# ---- RSI（Wilder）----
def calc_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0)


# ---- ATR（True Range 平均）----
def calc_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr.fillna(method="bfill")
