import pandas as pd

TREND_LEN = 3   # 连续 K 线确认
ADX_TH     = 20 # 趋势强度阈值

def make_signal(df_1h: pd.DataFrame, df_4h: pd.DataFrame) -> str:
    """
    传入 1h、4h 两个周期的带指标数据 → 返回 'long' / 'short' / 'neutral'
    """
    last_1h  = df_1h.iloc[-1]
    last_4h  = df_4h.iloc[-1]

    # 1) 连续 N 根 K 线方向（靠滚动求和判断）
    df_1h["above_ma20"] = (df_1h["Close"] > df_1h["MA20"]).astype(int)
    df_1h["below_ma20"] = (df_1h["Close"] < df_1h["MA20"]).astype(int)
    up_cnt   = df_1h["above_ma20"].rolling(TREND_LEN).sum().iloc[-1]
    down_cnt = df_1h["below_ma20"].rolling(TREND_LEN).sum().iloc[-1]

    # 2) ADX 过滤
    has_trend = last_1h["ADX"] > ADX_TH

    # 3) 多均线共振：MA20 与 MA50 方向一致
    long_bias  = last_1h["Close"] > last_1h["MA20"] > last_1h["MA50"]
    short_bias = last_1h["Close"] < last_1h["MA20"] < last_1h["MA50"]

    # 4) 高周期（4h）方向和 1h 一致
    long_4h  = last_4h["Close"] > last_4h["MA20"]
    short_4h = last_4h["Close"] < last_4h["MA20"]

    # === 组合判断 ===
    if (up_cnt == TREND_LEN and long_bias and long_4h
            and last_1h["RSI"].between(30,70) and has_trend):
        return "long"
    if (down_cnt == TREND_LEN and short_bias and short_4h
            and last_1h["RSI"].between(30,70) and has_trend):
        return "short"
    return "neutral"
