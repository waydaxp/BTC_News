# core/indicators.py
import pandas as pd

MA_WINDOW = 20
RSI_WINDOW = 14
ATR_WINDOW = 14

def calc_rsi(series: pd.Series) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(RSI_WINDOW).mean()
    roll_down = down.rolling(RSI_WINDOW).mean()
    rs = roll_up / roll_down
    return 100 - 100 / (1 + rs)

def calc_atr(df: pd.DataFrame) -> pd.Series:
    high = df["High"]
    low = df["Low"]
    prev_close = df["Close"].shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(ATR_WINDOW).mean()

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # 规范列名首字母大写
    df = df.rename(columns=lambda c: c.capitalize())
    # 只保留 OHLC + Volume
    df = df[["Open","High","Low","Close","Volume"]]
    df["Ma20"] = df["Close"].rolling(MA_WINDOW).mean()
    df["Rsi"]  = calc_rsi(df["Close"])
    df["Atr"]  = calc_atr(df)
    return df
