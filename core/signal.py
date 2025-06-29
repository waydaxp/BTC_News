from __future__ import annotations
import pandas as pd

TREND_LEN = 3         # 连续 3 根确认
RSI_LOW   = 30
RSI_HIGH  = 70

def make_signal(df_1h: pd.DataFrame,
                df_4h: pd.DataFrame,
                df_15m: pd.DataFrame) -> tuple[str, bool]:
    """返回 (信号字符串, 是否大级别上涨趋势)"""

    # 4H 趋势判断
    trend_up = (df_4h["Close"].tail(TREND_LEN) > df_4h["MA20"].tail(TREND_LEN)).all()

    # 15m 短线动量
    momo_up  = (df_15m["Close"].tail(TREND_LEN) > df_15m["MA20"].tail(TREND_LEN)).all()
    momo_dn  = (df_15m["Close"].tail(TREND_LEN) < df_15m["MA20"].tail(TREND_LEN)).all()

    last = df_1h.iloc[-1]
    price_above_ma = last["Close"] > last["MA20"]
    rsi = last["RSI"]

    if trend_up and momo_up and price_above_ma and rsi < RSI_HIGH:
        return "✅ 做多信号：多级别共振", trend_up
    elif (not trend_up) and momo_dn and (not price_above_ma) and rsi > RSI_LOW:
        return "🔻 做空信号：下行共振", trend_up
    else:
        return "⏸ 中性信号：观望为主", trend_up
