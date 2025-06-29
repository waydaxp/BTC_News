"""
基础技术指标：MA / ATR / RSI
不依赖 TA-Lib，仅用 pandas / numpy
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# 全局窗口配置，可改写为从 config.yaml 读取
C = dict(
    MA_WIN=20,
    ATR_WIN=14,
    RSI_WIN=14,
)

# --------------------------------------------------------------------------- #
# ▍RSI
def calc_rsi(series: pd.Series, win: int = C["RSI_WIN"]) -> pd.Series:
    delta = series.diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    roll_up  = gain.rolling(win).mean()
    roll_dn  = loss.rolling(win).mean()
    rs       = roll_up / roll_dn
    rsi      = 100 - 100 / (1 + rs)
    return rsi

# ▍ATR
def calc_atr(high: pd.Series, low: pd.Series,
             close: pd.Series, win: int = C["ATR_WIN"]) -> pd.Series:
    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low  - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.rolling(win).mean()

# --------------------------------------------------------------------------- #
# ▍统一指标添加
def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # 1. 统一列名大小写
    rename_map = {c: c.capitalize() for c in df.columns
                  if c.lower() in {"open", "high", "low", "close", "volume"}}
    df = df.rename(columns=rename_map)

    # 2. 计算指标
    df["MA20"] = df["Close"].rolling(C["MA_WIN"]).mean()
    df["ATR"]  = calc_atr(df["High"], df["Low"], df["Close"], C["ATR_WIN"])
    df["RSI"]  = calc_rsi(df["Close"], C["RSI_WIN"])
    return df
