# utils/fetch_btc_data.py
"""
下载 BTC 多周期 K 线 → 计算指标 → 输出一个 dict
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Literal

import yfinance as yf
import pandas as pd

from core.indicators import add_basic_indicators
from core.signal      import make_signal          # 技术方向
from core.risk        import (
    calc_position_size,
    ATR_MULT_SL,
    ATR_MULT_TP,
    RISK_USD,
)

PAIR       = "BTC-USD"
TZ         = timezone(timedelta(hours=8))   # 北京时间
TREND_LEN  = 4                              # 1h 连续 N 根
INTERVALS: dict[str, dict[str, str]] = {
    "1h" : dict(interval="1h",  period="90d"),
    "4h" : dict(interval="1h",  period="180d"),   # 先 1h 拉长，再 resample
    "15m": dict(interval="15m", period="30d"),
}

# --------------------------------------------------------------------------- #
# 内部工具
# --------------------------------------------------------------------------- #
def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """拉指定周期，并附加指标"""
    df: pd.DataFrame = yf.download(PAIR, interval=interval, period=period, progress=False)
    df.index = df.index.tz_localize(None).tz_localize(TZ)   # 统一成北京时间
    df.columns = [c.capitalize() for c in df.columns]       # 兼容 Pandas OHLC 列名
    return add_basic_indicators(df).dropna()


# --------------------------------------------------------------------------- #
# 核心接口
# --------------------------------------------------------------------------- #
def get_btc_analysis() -> dict:
    # --- 1. 拉取多周期 K 线 -------------------------------------------------- #
    dfs = {k: _download_tf(**cfg) for k, cfg in INTERVALS.items()}

    # 4h 由 1h resample 而来（聚合 OHLC）
    df_1h = dfs["1h"]
    ohlc  = {
        "Open":  "first",
        "High":  "max",
        "Low":   "min",
        "Close": "last",
        "Volume":"sum",
        "MA20":  "last",
        "RSI":   "last",
        "ATR":   "last",
    }
    dfs["4h"] = df_1h.resample("4H", label="right", closed="right").agg(ohlc).dropna()

    df_4h  = dfs["4h"]
    df_15m = dfs["15m"]

    # --- 2. 最近行情快照 ------------------------------------------------------ #
    last_1h  = df_1h.iloc[-1]
    price    = float(last_1h["Close"])
    ma20     = float(last_1h["MA20"])
    rsi      = float(last_1h["RSI"])
    atr      = float(last_1h["ATR"])

    # --- 3. 技术方向 & 建仓区 --------------------------------------------------- #
    signal, trend_up = make_signal(df_1h, df_4h, df_15m, trend_len=TREND_LEN)

    # --- 4. 风控计算 ---------------------------------------------------------- #
    if signal in ("多", "空"):
        side: Literal["long", "short"] = "long" if signal == "多" else "short"
        qty   = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, side)
        entry = price
        sl    = price - ATR_MULT_SL * atr if side == "long" else price + ATR_MULT_SL * atr
        tp    = price + ATR_MULT_TP * atr if side == "long" else price - ATR_MULT_TP * atr
    else:  # 观望
        qty = entry = sl = tp = None

    # --- 5. 打包输出 ---------------------------------------------------------- #
    return dict(
        price        = round(price, 2),
        ma20         = round(ma20, 2),
        rsi          = round(rsi, 2),
        atr          = round(atr, 2),
        signal       = ("✅ 做多信号" if signal == "多"
                        else "🔻 做空信号" if signal == "空"
                        else "⏸ 中性信号：观望为主"),
        qty          = round(qty,   3) if qty   else "N/A",
        entry        = round(entry, 2) if entry else "N/A",
        sl           = round(sl,    2) if sl    else "N/A",
        tp           = round(tp,    2) if tp    else "N/A",
        risk_usd     = RISK_USD,
        update_time  = datetime.now(TZ).strftime("%Y-%m-%d %H:%M"),  # ★ 北京时间
    )
