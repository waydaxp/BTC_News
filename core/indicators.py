# core/indicators.py

import pandas as pd

# 指标窗口
C = {
    "MA_WIN": 20,
    "RSI_WIN": 14,
    "ATR_WIN": 14,
}


def calc_rsi(series: pd.Series) -> pd.Series:
    """计算 RSI 指标"""
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(C["RSI_WIN"]).mean()
    roll_down = down.rolling(C["RSI_WIN"]).mean()
    rs = roll_up / roll_down
    return 100 - (100 / (1 + rs))


def calc_atr(df: pd.DataFrame) -> pd.Series:
    """计算 ATR 指标"""
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(C["ATR_WIN"]).mean()


def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    1) 扁平化列名到首字母大写；
    2) 提取必需的 OHLCV 五列；
    3) 依次计算 MA20、RSI、ATR 并加入到 DataFrame。
    """
    df = df.copy()

    # —— 1) 扁平化列名到首字母大写 —— 
    df = df.rename(columns={c: str(c).capitalize() for c in df.columns})

    # —— 2) 取 Open/High/Low/Close/Volume —— 
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    # —— 3) 计算指标 —— 
    df["Ma20"] = df["Close"].rolling(C["MA_WIN"]).mean()
    df["Rsi"]  = calc_rsi(df["Close"])
    df["Atr"]  = calc_atr(df)

    return df
