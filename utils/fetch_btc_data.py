from __future__ import annotations
import yfinance as yf
import pandas as pd
from core.indicators import add_basic_indicators
from core.signal      import make_signal
from core.risk        import build_risk
from datetime         import datetime, timezone

PAIR = "BTC-USD"
TZ   = "Asia/Shanghai"

# ⚠️ 只能用 1h → 再重采样成 4h（或 90m）
INTERVALS = {
    "1h" : dict(interval="60m", period="120d"),   # 120 天够用
    "15m": dict(interval="15m", period="30d"),
}

def _flatten(df: pd.DataFrame) -> pd.DataFrame:
    names = [c.capitalize() if isinstance(c, str) else str(c[0]).capitalize()
             for c in df.columns]
    df.columns = names
    return df

def _download(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten(df)
    # 处理时区
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC").tz_convert(TZ)
    else:
        df.index = df.index.tz_convert(TZ)
    return add_basic_indicators(df).dropna()

def _resample_4h(df_1h: pd.DataFrame) -> pd.DataFrame:
    """把 1h K 线转成 4h（开高低收 + 指标全部重算）"""
    ohlc = {
        "Open" : "first",
        "High" : "max",
        "Low"  : "min",
        "Close": "last",
        "Volume": "sum",
    }
    df = df_1h.resample("4H", label="right", closed="right").agg(ohlc).dropna()
    return add_basic_indicators(df).dropna()

# ---------- 主函数 ----------
def get_btc_analysis(balance_usd: float = 1_000.0) -> dict:
    df_1h  = _download(**INTERVALS["1h"])
    df_4h  = _resample_4h(df_1h)
    df_15m = _download(**INTERVALS["15m"])

    signal, trend_up = make_signal(df_1h, df_4h, df_15m)

    last = df_1h.iloc[-1]
    price = float(last["Close"])
    atr   = float(last["ATR"])

    risk  = build_risk(price, atr, balance_usd)

    return {
        "pair"         : "BTC/USDT",
        "price"        : price,
        "ma20"         : float(last["MA20"]),
        "rsi"          : float(last["RSI"]),
        "atr"          : atr,
        "signal"       : signal,          # ✅ 改名
        "trend_up"     : trend_up,
        **risk,
        "update_time"  : datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M"),
    }
