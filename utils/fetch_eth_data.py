# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime

from core.indicators import add_basic_indicators
from core.risk       import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    """
    下载指定周期和时间段的原始 K 线，
    保留 Open/High/Low/Close/Volume 五列，
    去掉时区信息，添加指标并剔除 NaN。
    """
    df = yf.download(PAIR, interval=interval, period=period, progress=False, auto_adjust=True)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    # 去掉 tz-aware，后续统一按本地时间处理
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()

def get_eth_analysis() -> dict:
    """
    返回 ETH 最新的技术分析与交易建议：
      - 15 分钟、1 小时、4 小时 三个周期同时用 MA20/R SI/ATR 判断趋势
      - 确认做多信号时，计算止损、止盈、仓位
      - 否则返回中性观望
    """
    # 各时间周期数据
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h",  "7d")

    # 从 1h 数据重采样到 4h OHLCV
    df4h = (
        df1h
        .resample("4H", label="right", closed="right")
        .agg({
            'Open'  :'first',
            'High'  :'max',
            'Low'   :'min',
            'Close' :'last',
            'Volume':'sum'
        })
        .dropna()
    )
    # 给 4h 周期也加上 MA20/RSI/ATR
    df4h = add_basic_indicators(df4h).dropna()

    # 取各周期最后一根
    last15 = df15.iloc[-1]
    last1  = df1h.iloc[-1]
    last4  = df4h.iloc[-1]

    price = float(last1['Close'])
    ma20  = float(last1['MA20'])
    rsi   = float(last1['RSI'])
    atr   = float(last1['ATR'])

    # 趋势确认：4h 与 15m 同时在 MA20 之上，且 RSI 在 [30,70] 之间
    trend_up = (
        (last4['Close'] > last4['MA20'])
        and
        (df15['Close'].tail(12) > df15['MA20'].tail(12)).all()
    )

    if trend_up and 30 < rsi < 70:
        signal = "✅ ETH 做多信号"
        sl     = price - ATR_MULT_SL * atr
        tp     = price + ATR_MULT_TP * atr
        qty    = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    else:
        signal = "⏸ 中性信号：观望"
        sl     = None
        tp     = None
        qty    = 0.0

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price":       price,
        "ma20":        ma20,
        "rsi":         rsi,
        "atr":         atr,
        "signal":      signal,
        "sl":          sl,
        "tp":          tp,
        "qty":         qty,
        "risk_usd":    RISK_USD,
        "update_time": update_time,
    }
