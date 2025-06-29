import pandas as pd
import yfinance as yf
from datetime import datetime, timezone

from core.indicators import add_basic_indicators
from core.signal      import make_signal
from core.risk        import calc_position_size, ATR_MULT_SL, ATR_MULT_TP

PAIR = "ETH-USD"

INTERVALS = {
    "1h":  {"interval": "60m",  "period": "4d"},
    "4h":  {"interval": "240m", "period": "30d"},
    "15m": {"interval": "15m",  "period": "2d"},
}

def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    df.columns = [str(c).capitalize() for c in df.columns]
    return df

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(PAIR, interval=interval, period=period, progress=False)
    df = _flatten_columns(df)
    df.index = df.index.tz_localize("UTC").tz_convert("Asia/Shanghai")
    return add_basic_indicators(df).dropna()

def get_eth_analysis() -> dict:
    dfs = {k: _download_tf(**cfg) for k, cfg in INTERVALS.items()}
    df_1h, df_4h, df_15m = dfs["1h"], dfs["4h"], dfs["15m"]

    last  = df_1h.iloc[-1]
    price = float(last["Close"])
    atr   = float(last["Atr"])

    signal, trend_up = make_signal(df_1h, df_15m, df_4h)

    risk_usd, qty = calc_position_size(price, atr)
    stop = round(price - ATR_MULT_SL * atr, 2) if trend_up else round(price + ATR_MULT_SL * atr, 2)
    tp   = round(price + ATR_MULT_TP * atr, 2) if trend_up else round(price - ATR_MULT_TP * atr, 2)

    return {
        "price":    price,
        "ma20":     float(last["Ma20"]),
        "rsi":      float(last["Rsi"]),
        "signal":   signal,
        "entry":    price,
        "stop":     stop,
        "target":   tp,
        "risk_usd": risk_usd,
        "position": qty,
        "atr":      atr,
    }
