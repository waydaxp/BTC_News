# -*- coding: utf-8 -*-
"""
ETH 多周期数据抓取 + 技术信号
"""
from __future__ import annotations
import yfinance as yf
import pandas as pd
from core.indicators import add_basic_indicators

PAIR = "ETH-USD"
CFG  = {
    "15m": {"interval": "15m", "period": "5d"},
    "1h":  {"interval": "1h",  "period": "45d"},
    "4h":  {"interval": "4h",  "period": "180d"},
}

ACCOUNT_USD      = 1_000
RISK_PER_TRADE   = 0.02
ATR_SL_MULT      = 1
TARGET_R_MULT    = 1.5

to_float = lambda x: float(x.iloc[0] if hasattr(x, "iloc") else x)


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.index = (df.index.tz_localize("UTC") if df.index.tz is None
                else df.index.tz_convert("UTC"))
    return add_basic_indicators(df)


def _series_gt(a: pd.Series, b: pd.Series) -> bool:
    s1, s2 = a.dropna(), b.dropna()
    common = s1.index.intersection(s2.index)
    if len(common) < 1:
        return False
    return (s1.loc[common].to_numpy() > s2.loc[common].to_numpy()).all()


def get_eth_analysis() -> dict:
    dfs = {k: _download_tf(**v) for k, v in CFG.items()}
    df_15m, df_1h, df_4h = dfs["15m"], dfs["1h"], dfs["4h"]

    last_1h, last_4h = df_1h.iloc[-1], df_4h.iloc[-1]

    price = to_float(last_1h["Close"])
    ma20  = to_float(last_1h["MA20"])
    rsi   = to_float(last_1h["RSI"])
    atr   = to_float(last_1h["ATR"])

    trend_up = (
        to_float(last_4h["Close"]) > to_float(last_4h["MA20"])
        and _series_gt(df_15m["Close"].tail(12), df_15m["MA20"].tail(12))
    )
    trend_dn = (
        to_float(last_4h["Close"]) < to_float(last_4h["MA20"])
        and _series_gt(df_15m["MA20"].tail(12), df_15m["Close"].tail(12))
    )

    if trend_up and (30 < rsi < 70):
        signal = "✅ 做多信号：多周期均线共振"
        entry  = price
        stop   = round(price - ATR_SL_MULT * atr, 2)
        target = round(price + TARGET_R_MULT * (price - stop), 2)
        strat  = (
            f"✅ 做多\n建仓≈{entry:.2f}\n"
            f"止损 = 现价 - {ATR_SL_MULT}×ATR ≈ {stop:.2f}\n"
            f"止盈 = 现价 + {TARGET_R_MULT}×R ≈ {target:.2f}"
        )
    elif trend_dn and (30 < rsi < 70):
        signal = "🔻 做空信号：多周期均线共振"
        entry  = price
        stop   = round(price + ATR_SL_MULT * atr, 2)
        target = round(price - TARGET_R_MULT * (stop - price), 2)
        strat  = (
            f"🔻 做空\n建仓≈{entry:.2f}\n"
            f"止损 = 现价 + {ATR_SL_MULT}×ATR ≈ {stop:.2f}\n"
            f"止盈 = 现价 - {TARGET_R_MULT}×R ≈ {target:.2f}"
        )
    else:
        signal = "⏸ 中性信号：观望"
        entry = stop = target = strat = "N/A"

    max_loss = round(ACCOUNT_USD * RISK_PER_TRADE, 2)
    position = (
        round(max_loss / max(1e-9, abs(price - stop)), 6) if stop != "N/A" else "N/A"
    )

    return dict(
        price=price,
        ma20=ma20,
        rsi=rsi,
        atr=atr,
        signal=signal,
        entry_price=entry,
        stop_loss=stop,
        take_profit=target,
        max_loss=max_loss,
        per_trade_position=position,
        strategy_text=strat,
    )
