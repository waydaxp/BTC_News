# -*- coding: utf-8 -*-
"""
BTC 多周期数据抓取 + 技术信号生成
"""
from __future__ import annotations

import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
from core.indicators import add_basic_indicators

PAIR = "BTC-USD"

# —— 配置 —— #
CFG: dict[str, dict[str, str]] = {
    "15m": {"interval": "15m", "period": "5d"},    # 最近 ~480 根
    "1h":  {"interval": "1h",  "period": "45d"},
    "4h":  {"interval": "4h",  "period": "180d"},
}

RISK_PER_TRADE = 0.02       # 账户 2 %
ACCOUNT_USD     = 1_000
TARGET_R_MULT   = 1.5       # TP = 1.5 × R(isk)
ATR_SL_MULT     = 1         # SL = 1 × ATR

# —— 工具 —— #
to_float = lambda x: float(x.iloc[0] if hasattr(x, "iloc") else x)

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """下载并加指标，输出索引 tz-aware(UTC) 的 DataFrame"""
    df = yf.download(PAIR, interval=interval, period=period, progress=False)

    # 某些频率自带 tz，需要统一
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")

    return add_basic_indicators(df)

# —— 主函数 —— #
def get_btc_analysis() -> dict:
    # 1) 下载 15m / 1h / 4h
    dfs = {k: _download_tf(**v) for k, v in CFG.items()}
    df_15m, df_1h, df_4h = dfs["15m"], dfs["1h"], dfs["4h"]

    # 2) 取最新一根
    last_15m = df_15m.iloc[-1]
    last_1h  = df_1h.iloc[-1]
    last_4h  = df_4h.iloc[-1]

    price = to_float(last_1h["Close"])
    ma20  = to_float(last_1h["MA20"])
    rsi   = to_float(last_1h["RSI"])
    atr   = to_float(last_1h["ATR"])

    # 3) 趋势过滤：4h + 15m 同向才给信号
    trend_up = (
        (to_float(last_4h["Close"]) > to_float(last_4h["MA20"])) and
        (df_15m["Close"].tail(12) > df_15m["MA20"].tail(12)).all()
    )
    trend_dn = (
        (to_float(last_4h["Close"]) < to_float(last_4h["MA20"])) and
        (df_15m["Close"].tail(12) < df_15m["MA20"].tail(12)).all()
    )

    # 4) 组合信号
    if trend_up and (30 < rsi < 70):
        signal = "✅ 做多信号：多周期均线共振"
        entry  = price
        stop   = round(price - ATR_SL_MULT * atr, 2)
        target = round(price + TARGET_R_MULT * (price - stop), 2)
        strat  = (
            "✅ 做多\n"
            f"建仓价≈{entry:.2f}\n"
            f"止损 = 现价 - {ATR_SL_MULT}×ATR ≈ {stop:.2f}\n"
            f"止盈 = 现价 + {TARGET_R_MULT}×R ≈ {target:.2f}"
        )
    elif trend_dn and (30 < rsi < 70):
        signal = "🔻 做空信号：多周期均线共振"
        entry  = price
        stop   = round(price + ATR_SL_MULT * atr, 2)
        target = round(price - TARGET_R_MULT * (stop - price), 2)
        strat  = (
            "🔻 做空\n"
            f"建仓价≈{entry:.2f}\n"
            f"止损 = 现价 + {ATR_SL_MULT}×ATR ≈ {stop:.2f}\n"
            f"止盈 = 现价 - {TARGET_R_MULT}×R ≈ {target:.2f}"
        )
    else:
        signal = "⏸ 中性信号：观望"
        entry = stop = target = strat = "N/A"

    # 5) 风控 & 返回
    max_loss = round(ACCOUNT_USD * RISK_PER_TRADE, 2)
    position = round(max_loss / max(1e-9, abs(price - stop)), 6) if stop != "N/A" else "N/A"

    return {
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "atr":   atr,
        "signal": signal,
        "entry_price": entry,
        "stop_loss":   stop,
        "take_profit": target,
        "max_loss":    max_loss,
        "per_trade_position": position,
        "strategy_text": strat,
    }
