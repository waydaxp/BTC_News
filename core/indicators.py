import pandas as pd

# === 参数配置 ===
MA_WIN_SHORT = 5
MA_WIN_LONG = 20
RSI_WIN = 14
ATR_WIN = 14

# === RSI ===
def calc_rsi(series: pd.Series) -> pd.Series:
    delta = series.diff().dropna()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(RSI_WIN).mean()
    roll_down = down.rolling(RSI_WIN).mean()
    rs = roll_up / roll_down
    rsi = 100 - 100 / (1 + rs)
    return rsi.reindex(series.index, method='pad')

# === ATR ===
def calc_atr(df: pd.DataFrame) -> pd.Series:
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(ATR_WIN).mean()

# === 基础指标 ===
def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['MA5'] = df['Close'].rolling(MA_WIN_SHORT).mean()
    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA20'] = df['Close'].rolling(MA_WIN_LONG).mean()
    df['RSI'] = calc_rsi(df['Close'])
    df['ATR'] = calc_atr(df)
    return df

# === MACD、BOLL、KDJ 指标 ===
def add_macd_boll_kdj(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # 布林带
    df['BOLL_MID'] = df['Close'].rolling(window=20).mean()
    df['BOLL_UP'] = df['BOLL_MID'] + 2 * df['Close'].rolling(window=20).std()
    df['BOLL_DOWN'] = df['BOLL_MID'] - 2 * df['Close'].rolling(window=20).std()

    # KDJ
    low_min = df['Low'].rolling(window=9).min()
    high_max = df['High'].rolling(window=9).max()
    rsv = (df['Close'] - low_min) / (high_max - low_min) * 100
    df['K'] = rsv.ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']

    return df

# === 简单历史胜率回测 ===
def backtest_signals(df: pd.DataFrame, label="") -> float:
    trades = []
    for i in range(10, len(df) - 10):
        rsi = df['RSI'].iloc[i]
        ma20 = df['MA20'].iloc[i]
        close = df['Close'].iloc[i]
        ma5 = df['Close'].rolling(5).mean().iloc[i]
        entry = close
        exit_price = df['Close'].iloc[i + 8]

        if close > ma20 and 40 < rsi < 75 and close > ma5:
            trades.append(1 if exit_price > entry else 0)
        elif close < ma20 and 25 < rsi < 60 and close < ma5:
            trades.append(1 if exit_price < entry else 0)

    win_rate = round(sum(trades) / len(trades) * 100, 1) if trades else 0.0
    print(f"[回测] {label} 胜率: {win_rate}% ，共 {len(trades)} 笔")
    return win_rate
