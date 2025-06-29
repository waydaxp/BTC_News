# core/indicators.py
import pandas as pd

# ============= 基础指标 ============= #
def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    给 DataFrame 补充：
        MA20 / RSI14 / ATR14
    df 必须包含列：High Low Close
    """
    # --- MA20
    df["MA20"] = df["Close"].rolling(window=20, min_periods=1).mean()

    # --- RSI14
    delta = df["Close"].diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)

    rs = gain.rolling(14, min_periods=1).mean() / loss.rolling(14, min_periods=1).mean()
    df["RSI"] = 100 - 100 / (1 + rs)

    # --- ATR14
    tr = pd.concat(
        [
            (df["High"] - df["Low"]),
            (df["High"] - df["Close"].shift()).abs(),
            (df["Low"]  - df["Close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    df["ATR"] = tr.rolling(14, min_periods=1).mean()

    return df

# 可以额外暴露快捷函数，便于其他模块直接调用
calc_rsi = lambda s: add_basic_indicators(s.to_frame(name="Close"))["RSI"]
calc_atr = lambda s_hlcv: add_basic_indicators(s_hlcv)["ATR"]
