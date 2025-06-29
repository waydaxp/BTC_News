import pandas as pd

MA_WIN_SHORT = 5     # 新增：用于 MA5
MA_WIN_LONG = 20     # 原 MA20
RSI_WIN = 14
ATR_WIN = 14

def calc_rsi(series: pd.Series) -> pd.Series:
    delta = series.diff().dropna()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(RSI_WIN).mean()
    roll_down = down.rolling(RSI_WIN).mean()
    rs = roll_up / roll_down
    rsi = 100 - 100 / (1 + rs)
    # 对齐索引
    rsi = rsi.reindex(series.index, method='pad')
    return rsi

def calc_atr(df: pd.DataFrame) -> pd.Series:
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(ATR_WIN).mean()
    return atr

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['RSI'] = calc_rsi(df['Close'])
    df['ATR'] = calc_atr(df)
    return df
