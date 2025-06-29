# utils/fetch_btc_data.py
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_TP, ATR_MULT_SL

PAIR = "BTC-USD"        # yfinance 标准写法
INTERVALS = {
    "1h":  {"interval": "60m", "period": "90d"},
    "4h":  {"interval": "240m", "period": "360d"},
    "1d":  {"interval": "1d",  "period": "720d"},
    "15m": {"interval": "15m", "period": "30d"},
}
TREND_LEN = 5           # 连续 N 根确认
N15_CONF = 12           # 15m N 根二次确认

# ---------------------------------------------------------
def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(
        PAIR, interval=interval, period=period, progress=False
    )

    # -------- 扁平化去掉 ticker 这一层列名 --------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)

    df.index = df.index.tz_localize(None)
    return add_basic_indicators(df)


def get_btc_analysis() -> dict:
    dfs = {k: _download_tf(**v) for k, v in INTERVALS.items()}

    df_1h, df_4h, df_1d, df_15m = (
        dfs["1h"], dfs["4h"], dfs["1d"], dfs["15m"]
    )

    last_1h = df_1h.iloc[-1]
    price   = float(last_1h["Close"])
    ma20    = float(last_1h["MA20"])
    rsi     = float(last_1h["RSI"])
    atr     = float(last_1h["ATR"])

    # --- 趋势方向判定 ---
    trend_up = (
        (df_1h["Close"].tail(TREND_LEN) > df_1h["MA20"].tail(TREND_LEN)).all()
        and (df_4h["Close"].iloc[-1] > df_4h["MA20"].iloc[-1])
        and (df_1d["Close"].iloc[-1] > df_1d["MA20"].iloc[-1])
        and (df_15m["Close"].tail(N15_CONF) > df_15m["MA20"].tail(N15_CONF)).all()
        and (df_1h["Close"].diff().tail(3).abs().sum() <= 2 * atr)
        and rsi > 50
    )
    trend_down = (
        (df_1h["Close"].tail(TREND_LEN) < df_1h["MA20"].tail(TREND_LEN)).all()
        and (df_4h["Close"].iloc[-1] < df_4h["MA20"].iloc[-1])
        and (df_1d["Close"].iloc[-1] < df_1d["MA20"].iloc[-1])
        and (df_15m["Close"].tail(N15_CONF) < df_15m["MA20"].tail(N15_CONF)).all()
        and (df_1h["Close"].diff().tail(3).abs().sum() <= 2 * atr)
        and rsi < 50
    )

    direction = "long" if trend_up else "short" if trend_down else "neutral"

    # --- 下单参数 ---
    if direction in ("long", "short"):
        sl  = price - ATR_MULT_SL * atr if direction == "long" else price + ATR_MULT_SL * atr
        tp  = price + ATR_MULT_TP * atr if direction == "long" else price - ATR_MULT_TP * atr
        pos = calc_position_size(price)
    else:
        sl = tp = pos = None

    return {
        "price":          price,
        "ma20":           ma20,
        "rsi":            rsi,
        "atr":            atr,
        "direction":      direction,          # long / short / neutral
        "entry":          price if direction in ("long", "short") else None,
        "sl":             sl,
        "tp":             tp,
        "quantity_after_leverage": pos,
        "risk_usd":       calc_position_size.risk_usd,
        "timestamp":      datetime.utcnow(),
    }
