import pandas as pd

def calc_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)

def calc_atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window).mean()

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # 1) 统一列名（防止大小写或MultiIndex）
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    df = df.rename(columns=lambda c: str(c).capitalize())

    # 2) 丢弃多余列，只保留：Open, High, Low, Close, Volume
    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"缺少必要列 {missing}，当前 columns={list(df.columns)}")
    df = df[required]

    # 3) 计算指标
    df["Ma20"] = df["Close"].rolling(20).mean()
    df["Rsi"]  = calc_rsi(df["Close"])
    df["Atr"]  = calc_atr(df)

    return df
