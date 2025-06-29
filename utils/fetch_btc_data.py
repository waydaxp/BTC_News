"""
拉取 BTC-USDT K 线（15 m / 1 h / 4 h），计算技术指标 + 交易信号
"""
from __future__ import annotations

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone
from core.indicators import add_basic_indicators
from core.signal      import make_signal                       # already provided
from core.risk        import calc_position_size, ATR_MULT_TP, ATR_MULT_SL

PAIR       = "BTC-USD"        # yfinance 符号
ACCOUNT_USD = 1000            # 账户本金，用于头寸计算

# 需要拉的周期
INTERVALS = {
    "15m": dict(interval="15m", period="3d"),   # 192 根
    "1h":  dict(interval="60m", period="14d"),  # 336 根
    "4h":  dict(interval="240m", period="90d"), # 540 根
}

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """
    ◆ 拉取指定周期 K 线 → 统一列名 → tz 转 UTC → 计算指标
    ◆ 如返回空表或缺少必要列则直接抛错
    """
    df: pd.DataFrame = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=False,
        threads=False,
    )

    if df.empty:
        raise RuntimeError(f"Yahoo 返回空 K 线 ({interval}/{period})")

    # 统一列名大小写
    df.columns = [c.capitalize() for c in df.columns]

    required = {"Open", "High", "Low", "Close", "Volume"}
    if not required.issubset(df.columns):
        raise RuntimeError(f"缺少必要列 {required - set(df.columns)} ({interval})")

    # 索引时区处理
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")

    return add_basic_indicators(df)

# --------------------------------------------------------------------------- #

def get_btc_analysis() -> dict[str, object]:
    """主入口：返回包含价格 & 信号 & 风控信息的字典"""
    # === 1. 数据拉取 & 指标计算 ===
    dfs = {k: _download_tf(**kw) for k, kw in INTERVALS.items()}
    df_15m, df_1h, df_4h = dfs["15m"], dfs["1h"], dfs["4h"]

    last_1h = df_1h.iloc[-1]
    price   = float(last_1h["Close"])
    atr     = float(last_1h["ATR"])

    # === 2. 交易信号 ===
    signal = make_signal(df_15m, df_1h, df_4h)

    # === 3. 风控参数 ===
    pos_qty, risk_usd = calc_position_size(
        balance_usd=ACCOUNT_USD,
        price=price,
        atr=atr,
        atr_mult_sl=ATR_MULT_SL,
    )

    stop   = round(price - ATR_MULT_SL * atr, 2)  # 默认多头；空头在 signal 里反转
    target = round(price + ATR_MULT_TP * atr, 2)

    return {
        "symbol": "BTC",
        "last_price": price,
        "atr": atr,
        "signal": signal.text,        # e.g. "✅ 做多信号"
        "side": signal.side,          # "long" / "short" / "flat"
        "risk_usd": risk_usd,
        "position_qty": pos_qty,
        "entry": price,
        "stop": stop if signal.side != "flat" else "N/A",
        "target": target if signal.side != "flat" else "N/A",
        "updated": datetime.now(timezone.utc).astimezone(
            timezone(timedelta(hours=8))
        ).strftime("%Y-%m-%d %H:%M"),
    }
