import pandas as pd

MA_WIN_SHORT = 5     # MA5 均线窗口
MA_WIN_LONG = 20     # MA20 均线窗口
RSI_WIN = 14
ATR_WIN = 14

# 计算 RSI 指标
def calc_rsi(series: pd.Series) -> pd.Series:
    delta = series.diff().dropna()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(RSI_WIN).mean()
    roll_down = down.rolling(RSI_WIN).mean()
    rs = roll_up / roll_down
    rsi = 100 - 100 / (1 + rs)
    rsi = rsi.reindex(series.index, method='pad')
    return rsi

# 计算 ATR 指标
def calc_atr(df: pd.DataFrame) -> pd.Series:
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(ATR_WIN).mean()
    return atr

# 添加基础指标

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['MA5'] = df['Close'].rolling(MA_WIN_SHORT).mean()
    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA20'] = df['Close'].rolling(MA_WIN_LONG).mean()
    df['RSI'] = calc_rsi(df['Close'])
    df['ATR'] = calc_atr(df)
    return df

# 添加 MACD、布林带和 KDJ 指标
def add_macd_boll_kdj(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # MACD
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # 布林带（BOLL）
    df['BOLL_MID'] = df['Close'].rolling(window=20).mean()
    df['BOLL_UP'] = df['BOLL_MID'] + 2 * df['Close'].rolling(window=20).std()
    df['BOLL_DOWN'] = df['BOLL_MID'] - 2 * df['Close'].rolling(window=20).std()

    # KDJ 指标
    low_min = df['Low'].rolling(window=9).min()
    high_max = df['High'].rolling(window=9).max()
    rsv = (df['Close'] - low_min) / (high_max - low_min) * 100
    df['K'] = rsv.ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']

    return df
