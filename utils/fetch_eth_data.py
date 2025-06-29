import yfinance as yf
import pandas as pd
from datetime import datetime
from pytz import timezone
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False, auto_adjust=False)
    print("[DEBUG] Columns:", df.columns)

    if isinstance(df.columns, pd.MultiIndex):
        if "Ticker" in df.columns.names and "Price" in df.columns.names:
            try:
                df = df.xs(PAIR, level="Ticker", axis=1)
            except KeyError:
                raise ValueError(f"[错误] MultiIndex 中未找到: {PAIR}")
        else:
            raise ValueError("[错误] 未识别的 MultiIndex 结构")

    df = df.rename(columns=str.title)

    expected_cols = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(f"[错误] 缺失所需列: {missing}, 当前列为: {df.columns.tolist()}")

    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    return df.dropna()

def _judge_signal(df: pd.DataFrame, interval_label="") -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()
    recent = df['Close'].tail(5) > df['MA20'].tail(5)
    above_ma20 = recent.sum() >= 4
    below_ma20 = (df['Close'].tail(5) < df['MA20'].tail(5)).sum() >= 4

    signal = "⏸ 中性信号"

    if last['RSI'] < 40 or last['RSI'] > 70:
        signal = "⚠ 背离信号"
    elif abs(last['Close'] - last['MA20']) / last['MA20'] < 0.005:
        signal = "⏸ 震荡中性"
    elif last['Close'] > last['MA20'] and above_ma20 and 45 < last['RSI'] < 65 and last['Close'] > ma5.iloc[-1]:
        signal = "🟢 做多信号"
    elif last['Close'] < last['MA20'] and below_ma20 and 35 < last['RSI'] < 55 and last['Close'] < ma5.iloc[-1]:
        signal = "🔻 做空信号"
    elif last['Close'] > last['MA20'] * 1.02 and last['RSI'] > 60:
        signal = "🟢 趋势偏强"
    elif last['Close'] < last['MA20'] * 0.98 and last['RSI'] < 40:
        signal = "🔻 趋势偏弱"

    print(f"[DEBUG] ETH-{interval_label}: Signal={signal}, RSI={last['RSI']:.2f}, Close={last['Close']:.2f}, MA20={last['MA20']:.2f}")
    return signal

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

def get_eth_analysis() -> dict:
    df15 = _download_tf("15m", "3d")
    df1h = _download_tf("1h", "7d")
    df4h = _download_tf("4h", "30d")

    signal15 = _judge_signal(df15, "15m")
    signal1h = _judge_signal(df1h, "1h")
    signal4h = _judge_signal(df4h, "4h")

    last15, last1h, last4h = df15.iloc[-1], df1h.iloc[-1], df4h.iloc[-1]
    price15, price1h, price4h = float(last15['Close']), float(last1h['Close']), float(last4h['Close'])
    atr15, atr1h, atr4h = float(last15['ATR']), float(last1h['ATR']), float(last4h['ATR'])

    sl15, tp15, qty15 = _calc_trade(price15, atr15, signal15)
    sl1h, tp1h, qty1h = _calc_trade(price1h, atr1h, signal1h)
    sl4h, tp4h, qty4h = _calc_trade(price4h, atr4h, signal4h)

    update_time = datetime.now(timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price1h,
        "ma20": float(last1h['MA20']),
        "rsi": float(last1h['RSI']),
        "atr": atr1h,
        "signal": f"{signal4h} (4h) / {signal1h} (1h) / {signal15} (15m)",

        "entry_15m": price15, "sl_15m": sl15, "tp_15m": tp15, "qty_15m": qty15,
        "entry_1h":  price1h, "sl_1h":  sl1h, "tp_1h":  tp1h,  "qty_1h":  qty1h,
        "entry_4h":  price4h, "sl_4h":  sl4h, "tp_4h":  tp4h,  "qty_4h":  qty4h,

        "risk_usd": RISK_USD,
        "update_time": update_time
    }
