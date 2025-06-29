# utils/fetch_btc_data.py (完整版 - 含增强的日内短线信号逻辑)

import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"


def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0].title() for col in df.columns]
    else:
        df.columns = df.columns.str.title()

    expected = ["Open", "High", "Low", "Close", "Volume"]
    if not all(col in df.columns for col in expected):
        raise KeyError(f"[BTC] 缺少必要列：期望 {expected}，实际为 {list(df.columns)}，interval={interval}, period={period}")

    df.index = df.index.tz_localize(None)
    df = df[expected]
    df = add_basic_indicators(df)
    return df.dropna()


def get_btc_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")

    df4h = df1h.resample("4h", label="right", closed="right").agg({
        'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'
    }).dropna()
    df4h = add_basic_indicators(df4h).dropna()

    last15 = df15.iloc[-1]
    last4 = df4h.iloc[-1]
    rsi = float(last15['RSI'])
    price = float(last15['Close'])
    atr = float(last15['ATR'])
    ma20 = float(last15['MA20'])

    # ===================== 短线日内逻辑 =====================
    recent = df15.tail(5)
    above_ma20_count = (recent['Close'] > recent['MA20']).sum()
    below_ma20_count = (recent['Close'] < recent['MA20']).sum()

    if (
        (last15['Close'] > last15['MA20']) and
        above_ma20_count >= 4 and
        45 < rsi < 65 and
        last15['Close'] > last15['MA5']
    ):
        signal = "✅ 短线做多信号"
        sl = price - ATR_MULT_SL * atr
        tp = price + ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "long")

    elif (
        (last15['Close'] < last15['MA20']) and
        below_ma20_count >= 4 and
        35 < rsi < 55 and
        last15['Close'] < last15['MA5']
    ):
        signal = "🔻 短线做空信号"
        sl = price + ATR_MULT_SL * atr
        tp = price - ATR_MULT_TP * atr
        qty = calc_position_size(price, RISK_USD, ATR_MULT_SL, atr, "short")

    else:
        signal = "⏸ 中性信号：观望"
        sl = None
        tp = None
        qty = 0.0

    # 时间格式统一为北京时间
    update_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "ma20": ma20,
        "rsi": rsi,
        "atr": atr,
        "signal": signal,
        "sl": sl,
        "tp": tp,
        "qty": qty,
        "risk_usd": RISK_USD,
        "update_time": update_time,
    }
