"""
拉取 BTC 多周期 K 线 → 计算指标 → 生成交易信号 & 风控建议
"""
from __future__ import annotations

import pandas as pd
import yfinance as yf
from datetime import datetime
from zoneinfo import ZoneInfo

from core.indicators import add_basic_indicators      # MA20 / ATR / RSI…
from core.signal      import make_signal              # 给出 “做多 / 做空 / 观望”
from core.risk        import calc_position_size, ATR_MULT_SL, ATR_MULT_TP

PAIR       = "BTC-USD"          # yfinance 的币种写法
TZ         = ZoneInfo("Asia/Shanghai")

# --------- 下载配置 ----------
INTERVALS = {
    "1h" : dict(interval="60m", period="90d"),   # 保证至少 60 根
    "4h" : dict(interval="240m", period="360d"),
    "15m": dict(interval="15m", period="30d"),
}
# -----------------------------

# ---------- 工具函数 ----------
def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """兼容 yfinance 新版列名（可能带 'Adj Close'）"""
    # (1) 多层列转平面
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)

    # (2) 统一首字母大写
    df.columns = [str(c).capitalize() for c in df.columns]

    # (3) Adj Close → Close
    if "Adj close" in df.columns and "Close" not in df.columns:
        df = df.rename(columns={"Adj close": "Close"})
    elif "Adj close" in df.columns:          # 两列都在则删掉冗余列
        df = df.drop(columns=["Adj close"])

    return df


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """下载单一时间框架并打标指标"""
    df: pd.DataFrame = yf.download(
        PAIR, interval=interval, period=period, progress=False
    )
    df = _flatten_columns(df)
    df.index = df.index.tz_localize("UTC").tz_convert(TZ)

    return add_basic_indicators(df).dropna()


# -----------------------------


def get_btc_analysis() -> dict:
    """主函数：返回 BTC 分析 + 风控建议"""
    dfs = {k: _download_tf(**cfg) for k, cfg in INTERVALS.items()}

    df_1h, df_4h, df_15m = dfs["1h"], dfs["4h"], dfs["15m"]

    # === 技术信号 ===
    signal, trend_up = make_signal(df_1h, df_4h, df_15m)

    # === 价格与指标最新值 ===
    last_1h = df_1h.iloc[-1]
    price   = float(last_1h["Close"])
    atr     = float(last_1h["ATR"])

    # === 风控 ===
    risk_usd, pos_qty = calc_position_size(price, atr)

    if signal == "long":      # 多
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
    elif signal == "short":   # 空
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
    else:                     # 观望
        sl = tp = None

    return {
        "pair":          "BTC/USDT",
        "update_time":   datetime.now(TZ).strftime("%Y-%m-%d %H:%M"),
        "price":         round(price, 2),
        "atr":           round(atr, 2),
        "signal":        signal,          # 'long' / 'short' / 'neutral'
        "trend_up":      trend_up,        # bool
        "risk_usd":      risk_usd,
        "position_qty":  pos_qty,
        "sl":            round(sl, 2) if sl else "N/A",
        "tp":            round(tp, 2) if tp else "N/A",
    }
