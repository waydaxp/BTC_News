from __future__ import annotations

import pandas as pd
from typing import Final

# === 参数集中管理（也可放 config.yaml） ============
C: Final = {
    "MA_WIN": 20,
    "ATR_WIN": 14,
    "RSI_WIN": 14,
}
# ====================================================


def calc_rsi(series: pd.Series, win: int = C["RSI_WIN"]) -> pd.Series:
    """原生实现 RSI，避免依赖 ta-lib。"""
    diff = series.diff().dropna()
    gain = diff.clip(lower=0)
    loss = (-diff).clip(lower=0)

    roll_up = gain.rolling(win).mean()
    roll_dn = loss.rolling(win).mean()

    rs = roll_up / roll_dn.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    return rsi.reindex(series.index)


def calc_atr(df: pd.DataFrame, win: int = C["ATR_WIN"]) -> pd.Series:
    high, low, close = df["High"], df["Low"], df["Close"]
    tr = pd.concat(
        [
            (high - low),
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.rolling(win).mean()


def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """在 df 上追加 MA20 / ATR / RSI 等列并返回。"""
    df = df.copy()
    df["MA20"] = df["Close"].rolling(C["MA_WIN"]).mean()
    df["ATR"]  = calc_atr(df)
    df["RSI"]  = calc_rsi(df["Close"])
    return df
