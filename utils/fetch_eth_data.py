"""
ETH 数据抓取 + 技术分析
--------------------------------
输出字段与 fetch_btc_data.py 相同，方便前端统一渲染
"""

import yfinance as yf
import pandas  as pd

from core.signal import make_signal, TREND_LEN


# ────────────────── 工具函数 ──────────────────
def _fetch_ohlc(interval: str, lookback: str) -> pd.DataFrame:
    """从 yfinance 拉 ETH-USD K 线并全部转小写列名"""
    df = yf.Ticker("ETH-USD").history(period=lookback, interval=interval)
    df.rename(columns=str.lower, inplace=True)
    return df


def _ensure_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """如缺 MA20 / RSI 即现场计算，保证后续列访问安全"""
    if "ma20" not in df:
        df["ma20"] = df["close"].rolling(20, min_periods=20).mean()

    if "rsi" not in df:
        delta = df["close"].diff()
        up    = delta.clip(lower=0).rolling(14).mean()
        down  = -delta.clip(upper=0).rolling(14).mean()
        rs    = up / down
        df["rsi"] = 100 - 100 / (1 + rs)

    return df
# ─────────────────────────────────────────────


def get_eth_analysis() -> dict:
    """统一入口，返回 dict 供 generate_data.py 调用"""

    # 🔹 ETH 波动略小，look-back 周期适当更长
    df_1h = _fetch_ohlc("1h", "14d")
    df_4h = _fetch_ohlc("4h", "60d")

    if df_1h.empty or df_4h.empty:
        return {"signal": "⚠️ 数据不足"}

    df_1h = _ensure_indicators(df_1h)
    df_4h = _ensure_indicators(df_4h)

    # === 方向判断（复用核心算法） ===
    direction = make_signal(df_1h, df_4h)

    last  = df_1h.iloc[-1]
    price = float(last["close"])
    ma20  = float(last["ma20"])
    rsi   = float(last["rsi"])

    # === 统一风控参数 ===
    account_usd = 1000
    leverage    = 20
    max_loss    = round(account_usd * 0.02, 2)
    pos_size    = round(max_loss * leverage, 2)

    entry = price
    if direction == "long":
        stop = round(price * 0.985, 2)
        tp   = round(price * 1.03, 2)
        sig  = f"✅ 做多信号：连续{TREND_LEN}根站上 MA20"
    elif direction == "short":
        stop = round(price * 1.015, 2)
        tp   = round(price * 0.97, 2)
        sig  = f"🔻 做空信号：连续{TREND_LEN}根跌破 MA20"
    else:
        stop = tp = "N/A"
        sig  = "⏸ 中性信号：观望为主"

    return {
        "price":  price,
        "ma20":   ma20,
        "rsi":    rsi,
        "signal": sig,

        "entry_price":         entry,
        "stop_loss":           stop,
        "take_profit":         tp,
        "max_loss":            max_loss,
        "per_trade_position":  pos_size,
    }
