"""
拉取 ETH-USDT K 线（同 BTC 逻辑）
"""
from __future__ import annotations

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone
from core.indicators import add_basic_indicators
from core.signal      import make_signal
from core.risk        import calc_position_size, ATR_MULT_TP, ATR_MULT_SL

PAIR        = "ETH-USD"
ACCOUNT_USD = 1000

INTERVALS = {
    "15m": dict(interval="15m", period="3d"),
    "1h":  dict(interval="60m", period="14d"),
    "4h":  dict(interval="240m", period="90d"),
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df: pd.DataFrame = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=False,
        threads=False,
    )
    if df.empty:
        raise RuntimeError(f"Yahoo 返回空 K线 ({interval}/{period})")

    df.columns = [c.capitalize() for c in df.columns]
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")

    return add_basic_indicators(df)

# --------------------------------------------------------------------------- #

def get_eth_analysis() -> dict[str, object]:
    dfs = {k: _download_tf(**kw) for k, kw in INTERVALS.items()}
    df_15m, df_1h, df_4h = dfs["15m"], dfs["1h"], dfs["4h"]

    last_1h = df_1h.iloc[-1]
    price   = float(last_1h["Close"])
    atr     = float(last_1h["ATR"])

    signal = make_signal(df_15m, df_1h, df_4h)

    pos_qty, risk_usd = calc_position_size(
        balance_usd=ACCOUNT_USD,
        price=price,
        atr=atr,
        atr_mult_sl=ATR_MULT_SL,
    )

    stop   = round(price - ATR_MULT_SL * atr, 2)
    target = round(price + ATR_MULT_TP * atr, 2)

    return {
        "symbol": "ETH",
        "last_price": price,
        "atr": atr,
        "signal": signal.text,
        "side": signal.side,
        "risk_usd": risk_usd,
        "position_qty": pos_qty,
        "entry": price,
        "stop": stop if signal.side != "flat" else "N/A",
        "target": target if signal.side != "flat" else "N/A",
        "updated": datetime.now(timezone.utc).astimezone(
            timezone(timedelta(hours=8))
        ).strftime("%Y-%m-%d %H:%M"),
    }
