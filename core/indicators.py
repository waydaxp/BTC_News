# -*- coding: utf-8 -*-
"""
基础技术指标封装：MA20 / RSI / ATR
"""
from __future__ import annotations
import pandas as pd
import numpy as np
from core.config import DAYTRADE_CFG as C

__all__ = ["add_basic_indicators", "calc_atr", "calc_rsi"]

# ────────────────────────────────────
def calc_rsi(series: pd.Series, win: int = C["RSI_WIN"]) -> pd.Series:
    diff = series.diff().dropna()
    gain = np.where(diff > 0, diff, 0.0)
    loss = np.where(diff < 0, -diff, 0.0)
    roll_up  = pd.Series(gain, index=series.index[1:]).rolling(win).mean()
    roll_down= pd.Series(loss, index=series.index[1:]).rolling(win).mean()
    rs = roll_up / (roll_down.replace(0, np.nan))
    rsi = 100 - (100 / (1 + rs))
    return rsi.reindex(series.index).fillna(method="bfill")

def calc_atr(df: pd.DataFrame, win: int = C["ATR_WIN"]) -> pd.Series:
    high, low, close = df["High"], df["Low"], df["Close"]
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(win).mean()

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA20"] = df["Close"].rolling(C["MA_WIN"]).mean()
    df["RSI"]  = calc_rsi(df["Close"])
    df["ATR"]  = calc_atr(df)
    return df.dropna()
