"""
BTC 数据抓取 & 技术分析
------------------------------------------------------------
依赖:
    - yfinance               (行情下载)
    - core.indicators        (add_basic_indicators / calc_atr / calc_rsi)
    - core.signal            (make_signal)
    - core.risk              (calc_position_size / ATR_MULT_SL / ATR_MULT_TP)

输出:
    dict -> generate_data.py 统一汇总
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf
from datetime import datetime, timezone

from core.indicators import add_basic_indicators, calc_atr
from core.signal      import make_signal
from core.risk        import calc_position_size, ATR_MULT_SL, ATR_MULT_TP

PAIR        = "BTC-USD"
ACCOUNT_USD = 1_000               # 账户规模
RISK_PCT    = 0.02                # 每笔亏损上限 2%

# 下载 15 m / 1 h / 4 h 三个时间框的行情
INTERVALS = {
    "15m": dict(interval="15m", period="3d"),
    "1h" : dict(interval="60m", period="7d"),
    "4h" : dict(interval="4h",  period="60d"),
}


# ---------- 工具函数 -------------------------------------------------- #
def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """
    统一下载一个时间框, 并附加 MA / RSI / ATR 等基础指标
    * 修复: 处理 yfinance 返回二级列索引 ('Close', 'BTC-USD') 的情况
    """
    # --- 下载 ---
    df: pd.DataFrame = yf.download(
        PAIR,
        interval=interval,
        period=period,
        progress=False,
    )

    # --- 列名清洗 (tuple -> str) ---
    clean_cols: list[str] = []
    for c in df.columns:
        if isinstance(c, tuple):           # MultiIndex => 取第 0 级
            c = c[0]
        clean_cols.append(str(c).capitalize())
    df.columns = clean_cols

    # --- 技术指标 ---
    df = add_basic_indicators(df)
    return df.dropna().copy()


# ---------- 主入口 ---------------------------------------------------- #
def get_btc_analysis() -> dict:
    # ① 批量拉取/加工
    dfs = {k: _download_tf(**kw) for k, kw in INTERVALS.items()}
    df_15m, df_1h, df_4h = dfs["15m"], dfs["1h"], dfs["4h"]

    # ② 生成信号 (示例: 连续 3 根 K 线站上 / 跌破 MA20)
    signal, trend_up = make_signal(df_1h, df_4h, df_15m)

    # ③ 最新价 & 指标
    last = df_1h.iloc[-1]
    price   = float(last["Close"])
    ma20    = float(last["Ma20"])
    rsi     = float(last["Rsi"])
    atr     = float(last["Atr"])

    # ④ 风控 / 仓位
    risk_usd      = round(ACCOUNT_USD * RISK_PCT, 2)
    entry_price   = price
    stop_loss     = round(price - ATR_MULT_SL * atr, 2)
    take_profit   = round(price + ATR_MULT_TP * atr, 2)
    qty           = calc_position_size(risk_usd, entry_price, stop_loss)

    # ⑤ 结果打包
    return {
        "price"       : price,
        "ma20"        : ma20,
        "rsi"         : rsi,
        "atr"         : atr,
        "signal"      : signal,
        "trend_up"    : trend_up,
        "entry_price" : entry_price,
        "stop_loss"   : stop_loss,
        "take_profit" : take_profit,
        "risk_usd"    : risk_usd,
        "position_qty": qty,
        "update_time" : datetime.now(timezone.utc).strftime("%F %T UTC"),
    }
