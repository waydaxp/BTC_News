import pandas as pd
import talib as ta

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    在 DataFrame 内就地新增：
    MA20, MA50, RSI14, ADX14
    """
    df = df.copy()
    df["MA20"] = ta.SMA(df["Close"], 20)
    df["MA50"] = ta.SMA(df["Close"], 50)
    df["RSI"]  = ta.RSI(df["Close"], 14)
    df["ADX"]  = ta.ADX(df["High"], df["Low"], df["Close"], 14)
    return df
