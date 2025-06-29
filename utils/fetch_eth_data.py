"""
ETH 数据抓取 + 技术分析
--------------------------------
返回字典字段与 fetch_btc_data.py 保持一致，方便
generate_data.py 统一调用。
"""

import yfinance as yf
import pandas  as pd

from core.signal import make_signal, TREND_LEN


# ========= 私有工具函数 ================================================= #
def _fetch_ohlc(interval: str, lookback: str) -> pd.DataFrame:
    eth = yf.Ticker("ETH-USD")
    df  = eth.history(period=lookback, interval=interval)
    df.rename(columns=str.lower, inplace=True)         # open/high/low/close
    return df
# ======================================================================== #


def get_eth_analysis() -> dict:
    """
    拉取 1h / 4h K 线 → 计算指标 → 生成做多/做空/观望 信号  
    返回字段与 BTC 保持一致，方便前端渲染。
    """

    df_1h = _fetch_ohlc("1h", "14d")   # ETH 波动略小，多拉几天
    df_4h = _fetch_ohlc("4h", "60d")

    if df_1h.empty or df_4h.empty:
        return {"signal": "⚠️ 数据不足"}

    # === 判断方向 ===
    direction = make_signal(df_1h, df_4h)

    last  = df_1h.iloc[-1]
    price = float(last["close"])
    ma20  = float(last["MA20"])
    rsi   = float(last["RSI"])

    # === 统一仓位&风控示例（可自行抽到 config.yaml） ===
    account_usd = 1000
    leverage    = 20
    max_loss    = round(account_usd * 0.02, 2)           # 2 % 账户风险
    pos_size    = round(max_loss * leverage, 2)

    entry = price
    if direction == "long":
        stop = round(price * 0.985, 2)
        tp   = round(price * 1.03, 2)
        sig_txt = f"✅ 做多信号：连续{TREND_LEN}根站上 MA20"
    elif direction == "short":
        stop = round(price * 1.015, 2)
        tp   = round(price * 0.97, 2)
        sig_txt = f"🔻 做空信号：连续{TREND_LEN}根跌破 MA20"
    else:
        stop = tp = "N/A"
        sig_txt = "⏸ 中性信号：观望为主"

    return {
        "price": price,
        "ma20":  ma20,
        "rsi":   rsi,
        "signal":       sig_txt,

        "entry_price":  entry,
        "stop_loss":    stop,
        "take_profit":  tp,
        "max_loss":     max_loss,
        "per_trade_position": pos_size,
    }
