# utils/fetch_btc_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)

    # 如果是 MultiIndex（通常出现在多个 ticker），取对应 PAIR 的数据
    if isinstance(df.columns, pd.MultiIndex):
        if PAIR in df.columns.levels[0]:
            df = df.xs(PAIR, axis=1, level=0)
        else:
            raise ValueError(f"MultiIndex 数据中未找到: {PAIR}")

    # 确保必要列存在
    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"缺失所需列: {missing}")

    df = df[required].copy()
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()

def _judge_signal(df: pd.DataFrame) -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()

    recent = df['Close'].tail(5) > df['MA20'].tail(5)
    above_ma20 = recent.sum() >= 4
    below_ma20 = (df['Close'].tail(5) < df['MA20'].tail(5)).sum() >= 4

    if last['Close'] > last['MA20'] and above_ma20 and 45 < last['RSI'] < 65 and last['Close'] > ma5.iloc[-1]:
        return "🟢 做多信号"
    elif last['Close'] < last['MA20'] and below_ma20 and 35 < last['RSI'] < 55 and last['Close'] < ma5.iloc[-1]:
        return "🔻 做空信号"
    elif abs(last['RSI'] - 50) < 3:
        return "⏸ 震荡中性"
    else:
        return "⏸ 中性信号"

def _calc_trade(price: float, atr: float, signal: str) -> tuple:
    if "多" in signal:
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "空" in signal:
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")
    else:
        sl, tp, qty = None, None, 0.0
    return sl, tp, qty

def get_btc_analysis() -> dict:
    df15 = _download_tf("15m", "3d")   # 短线
    df1h = _download_tf("1h", "7d")     # 中期
    df4h = _download_tf("4h", "30d")    # 长期

    signal15 = _judge_signal(df15)
    signal1h = _judge_signal(df1h)
    signal4h = _judge_signal(df4h)

    last15, last1h, last4h = df15.iloc[-1], df1h.iloc[-1], df4h.iloc[-1]
    price15, price1h, price4h = float(last15['Close']), float(last1h['Close']), float(last4h['Close'])
    atr15, atr1h, atr4h = float(last15['ATR']), float(last1h['ATR']), float(last4h['ATR'])

    sl15, tp15, qty15 = _calc_trade(price15, atr15, signal15)
    sl1h, tp1h, qty1h = _calc_trade(price1h, atr1h, signal1h)
    sl4h, tp4h, qty4h = _calc_trade(price4h, atr4h, signal4h)

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price1h,
        "ma20": float(last1h['MA20']),
        "rsi": float(last1h['RSI']),
        "atr": atr1h,
        "signal": f"{signal4h} (4h) / {signal1h} (1h) / {signal15} (15m)",

        "sl_15m": sl15, "tp_15m": tp15, "qty_15m": qty15,
        "sl_1h": sl1h, "tp_1h": tp1h, "qty_1h": qty1h,
        "sl_4h": sl4h, "tp_4h": tp4h, "qty_4h": qty4h,

        "risk_usd": RISK_USD,
        "update_time": update_time
    }
