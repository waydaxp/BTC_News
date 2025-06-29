from __future__ import annotations

import yfinance as yf
import pandas as pd
from core.indicators import add_basic_indicators
from core.signal      import make_signal
from core.risk        import build_risk
from datetime import datetime

PAIR = "BTC-USD"
TZ   = "Asia/Shanghai"

INTERVALS = {
    "1h" : dict(interval="60m", period="60d"),
    "4h" : dict(interval="240m", period="720d"),
    "15m": dict(interval="15m", period="7d"),
}

def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """yfinance 多层列 → 扁平首字母大写（Open High …）"""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c.capitalize() for c, _ in df.columns]
    else:
        df.columns = [str(c).capitalize() for c in df.columns]
    return df

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten_columns(df)

    # 统一时区 —— 根据是否已有 tz 选择 localize / convert
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(TZ)
    else:
        df.index = df.index.tz_convert(TZ)

    return add_basic_indicators(df).dropna()

def get_btc_analysis(balance_usd: float = 1_000.0) -> dict:
    dfs = {k: _download_tf(**cfg) for k, cfg in INTERVALS.items()}
    df_1h, df_4h, df_15m = dfs["1h"], dfs["4h"], dfs["15m"]

    signal, trend_up = make_signal(df_1h, df_4h, df_15m)

    last   = df_1h.iloc[-1]
    price  = float(last["Close"])
    atr    = float(last["ATR"])

    risk   = build_risk(price, atr, balance_usd)

    now    = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "pair"          : "BTC/USDT",
        "price"         : price,
        "ma20"          : float(last["MA20"]),
        "rsi"           : float(last["RSI"]),
        "atr"           : atr,
        "signal"        : signal,
        "trend_up"      : trend_up,
        **risk,
        "update_time"   : now,
    }
