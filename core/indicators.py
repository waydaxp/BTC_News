# core/indicators.py
import numpy as np
import pandas as pd

C = {
    "MA_WIN":    20,
    "ATR_WIN":   14,
    "RSI_WIN":   14,
}

# ---------- 计算函数 ----------
def calc_atr(df: pd.DataFrame, win: int = C["ATR_WIN"]) -> pd.Series:
    tr = pd.concat(
        [
            df["High"] - df["Low"],
            (df["High"] - df["Close"].shift()).abs(),
            (df["Low"] - df["Close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.rolling(win).mean()


def calc_rsi(series: pd.Series, win: int = C["RSI_WIN"]) -> pd.Series:
    # 保证是一维
    series = series.squeeze()

    diff = series.diff().dropna()
    gain = np.where(diff > 0, diff, 0.0)
    loss = np.where(diff < 0, -diff, 0.0)
    roll_up  = pd.Series(gain, index=series.index[1:]).rolling(win).mean()
    roll_down= pd.Series(loss, index=series.index[1:]).rolling(win).mean()
    rs  = roll_up / roll_down.replace(0, np.nan)
    rsi = 100 - 100 / (1 + rs)
    return rsi.reindex(series.index).fillna(method="bfill")


def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA20"] = df["Close"].rolling(C["MA_WIN"]).mean()
    df["ATR"]  = calc_atr(df)
    df["RSI"]  = calc_rsi(df["Close"])
    return df
