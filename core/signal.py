# core/signal.py
"""
决定做多 / 做空 / 观望 的信号生成器
-------------------------------------------------
思路：
1. 读取 1H 与 4H DataFrame
2. 依据 MA20、MA50、RSI 等条件给出方向
   - long  : 多头
   - short : 空头
   - neutral / None : 观望
"""

def make_signal(df_1h, df_4h):
    """
    Parameters
    ----------
    df_1h : pandas.DataFrame
        必须包含列 ["Close", "MA20", "RSI"]
    df_4h : pandas.DataFrame
        必须包含列 ["Close", "MA50"]

    Returns
    -------
    str  'long' | 'short' | 'neutral'
    """
    # 最近一根 1H、4H K 线
    last_1h = df_1h.iloc[-1]
    last_4h = df_4h.iloc[-1]

    close_1h = float(last_1h["Close"])
    ma20_1h  = float(last_1h["MA20"])
    rsi_1h   = float(last_1h["RSI"])

    close_4h = float(last_4h["Close"])
    ma50_4h  = float(last_4h["MA50"])

    # ────────── 条件拆分 ──────────
    above_ma20  = close_1h > ma20_1h
    below_ma20  = close_1h < ma20_1h
    rsi_ok      = 30 < rsi_1h < 70
    trend_up_4h = close_4h > ma50_4h
    trend_dn_4h = close_4h < ma50_4h

    # ────────── 决策树 ──────────
    if above_ma20 and rsi_ok and trend_up_4h:
        return "long"

    if below_ma20 and rsi_ok and trend_dn_4h:
        return "short"

    # 其它情况：观望
    return "neutral"
