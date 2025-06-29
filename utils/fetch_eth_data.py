import pandas as pd
import yfinance as yf
from datetime import datetime, timezone
from core.indicators import add_basic_indicators
from core.signal      import make_signal
from core.risk        import calc_position_size, ATR_MULT_SL, ATR_MULT_TP

PAIR = "ETH-USD"

INTERVALS = {
    "1h":  {"interval": "60m", "period": "4d"},
    "4h":  {"interval": "240m", "period": "30d"},
    "15m": {"interval": "15m", "period": "2d"},
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(
        PAIR, interval=interval, period=period, progress=False
    )
    df.columns = [c.capitalize() for c in df.columns]
    df.index   = df.index.tz_localize("UTC").tz_convert("Asia/Shanghai")
    df         = add_basic_indicators(df)
    return df.dropna()

def get_eth_analysis() -> dict:
    dfs      = {k: _download_tf(**cfg) for k, cfg in INTERVALS.items()}
    df_1h, df_4h, df_15m = dfs["1h"], dfs["4h"], dfs["15m"]

    last_1h = df_1h.iloc[-1]
    price   = float(last_1h["Close"])
    atr     = float(last_1h["ATR"])

    signal, trend_up = make_signal(df_1h, df_15m, df_4h)  # ★ 修正顺序

    risk_usd, qty   = calc_position_size(price, atr)
    stop_loss       = round(price - ATR_MULT_SL * atr, 2) if trend_up else round(price + ATR_MULT_SL * atr, 2)
    take_profit     = round(price + ATR_MULT_TP * atr, 2) if trend_up else round(price - ATR_MULT_TP * atr, 2)

    return {
        "price":    price,
        "ma20":     float(last_1h["MA20"]),
        "rsi":      float(last_1h["RSI"]),
        "signal":   signal,
        "entry":    price,
        "stop":     stop_loss,
        "target":   take_profit,
        "risk_usd": risk_usd,
        "position": qty,
        "atr":      atr,
    }
