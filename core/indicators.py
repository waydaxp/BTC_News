# core/indicators.py
"""
仅用 NumPy + Pandas 手写的 MA20 / RSI14 / ATR14 计算，不依赖 TA-Lib。
"""
import pandas as pd
import numpy as np


def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # === MA20 ===
    out["MA20"] = out["Close"].rolling(20).mean()

    # === RSI14 ===
    delta = out["Close"].diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    roll_up = pd.Series(gain).rolling(14).mean()
    roll_dn = pd.Series(loss).rolling(14).mean()
    rs = roll_up / roll_dn
    out["RSI"] = 100 - 100 / (1 + rs)

    # === ATR14 ===
    high_low = out["High"] - out["Low"]
    high_close = np.abs(out["High"] - out["Close"].shift())
    low_close = np.abs(out["Low"] - out["Close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    out["ATR"] = tr.rolling(14).mean()

    return out.dropna()


def calc_rsi(series: pd.Series) -> float:  # 末值
    return float(series.iloc[-1])


def calc_atr(series: pd.Series) -> float:  # 末值
    return float(series.iloc[-1])
