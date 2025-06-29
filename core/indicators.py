# core/indicators.py
# --------------------------------------------------
# 统一为 K 线 DataFrame 追加常用指标：MA20 / RSI14 / ATR14
# 依赖 pandas + pandas_ta（纯 Python，无需 TA-Lib）
# --------------------------------------------------
import pandas as pd
import pandas_ta as ta


def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    在传入的 OHLCV DataFrame 上附加
    - MA20  : 20-period Simple Moving Average
    - RSI14 : 14-period Relative Strength Index
    - ATR14 : 14-period Average True Range
    要求 df 至少含有列: High、Low、Close
    """
    out = df.copy()

    # 1️⃣ MA20
    out["MA20"] = out["Close"].rolling(20, min_periods=1).mean()

    # 2️⃣ RSI14
    out["RSI"] = ta.rsi(out["Close"], length=14)

    # 3️⃣ ATR14
    out["ATR"] = ta.atr(out["High"], out["Low"], out["Close"], length=14)

    return out
