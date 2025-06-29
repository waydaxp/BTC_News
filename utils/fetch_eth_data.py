# utils/fetch_eth_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.columns = df.columns.str.title()
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    df['MA5'] = df['Close'].rolling(5).mean()
    return df.dropna()

def _judge_trend(df: pd.DataFrame, tf_name: str) -> (str, float, float, float):
    last = df.iloc[-1]
    price = float(last['Close'])
    ma20 = float(last['MA20'])
    ma5 = float(last['MA5'])
    rsi = float(last['RSI'])
    atr = float(last['ATR'])

    recent = df['Close'].tail(5)
    recent_ma20 = df['MA20'].tail(5)

    above_ma20_count = (recent > recent_ma20).sum()
    below_ma20_count = (recent < recent_ma20).sum()

    signal = "⏸ 中性信号：观望"
    sl = tp = qty = None

    if price > ma20 and above_ma20_count >= 4 and 45 < rsi < 65 and price > ma5:
        signal = f"✅ {tf_name}短线做多信号"
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif price < ma20 and below_ma20_count >= 4 and 35 < rsi < 55 and price < ma5:
        signal = f"🔻 {tf_name}短线做空信号"
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")

    return signal, sl, tp, qty

def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")   # 短线
    df1h = _download_tf("1h", "7d")    # 中期
    df4h = _download_tf("4h", "30d")   # 长期

    last_price = float(df1h.iloc[-1]['Close'])
    last_ma20 = float(df1h.iloc[-1]['MA20'])
    last_rsi = float(df1h.iloc[-1]['RSI'])
    last_atr = float(df1h.iloc[-1]['ATR'])

    sig15, sl15, tp15, qty15 = _judge_trend(df15, "短线")
    sig1h, sl1h, tp1h, qty1h = _judge_trend(df1h, "中期")
    sig4h, sl4h, tp4h, qty4h = _judge_trend(df4h, "长期")

    # 综合判断：以中期为主，长短线辅助
    signal = "⏸ 中性信号：观望"
    sl = tp = qty = None
    if "做多" in sig1h and "做多" in sig4h and "做多" in sig15:
        signal = "🟢 中期做多信号"
        sl, tp, qty = sl1h, tp1h, qty1h
    elif "做空" in sig1h and "做空" in sig4h and "做空" in sig15:
        signal = "🔴 中期做空信号"
        sl, tp, qty = sl1h, tp1h, qty1h
    elif "做多" in sig4h:
        signal = "🟢 长期做多信号"
        sl, tp, qty = sl4h, tp4h, qty4h
    elif "做空" in sig4h:
        signal = "🔴 长期做空信号"
        sl, tp, qty = sl4h, tp4h, qty4h
    elif "做多" in sig15:
        signal = "🟢 短线做多信号"
        sl, tp, qty = sl15, tp15, qty15
    elif "做空" in sig15:
        signal = "🔴 短线做空信号"
        sl, tp, qty = sl15, tp15, qty15

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price":        last_price,
        "ma20":         last_ma20,
        "rsi":          last_rsi,
        "atr":          last_atr,
        "signal":       signal,
        "sl":           sl,
        "tp":           tp,
        "qty":          qty if qty else 0.0,
        "risk_usd":     RISK_USD,
        "update_time":  update_time,
    }
