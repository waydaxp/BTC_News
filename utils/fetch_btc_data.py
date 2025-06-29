import yfinance as yf
import pandas as pd
from datetime import datetime
from pytz import timezone
from core.indicators import add_basic_indicators
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"

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
    rsi = last['RSI']
    close = last['Close']
    ma20 = last['MA20']
    ma5_val = ma5.iloc[-1]
    vol = last['Volume']
    avg_vol = df['Volume'].rolling(10).mean().iloc[-1]

    recent = df['Close'].tail(5) > df['MA20'].tail(5)
    above_ma20 = recent.sum() >= 3
    below_ma20 = (df['Close'].tail(5) < df['MA20'].tail(5)).sum() >= 3

    prev_candle = df.iloc[-2]

    signal = "⏸ 中性信号"

    # 强趋势多头
    if close > ma20 and above_ma20 and 45 < rsi < 70 and close > ma5_val:
        signal = "🟢 做多信号"

    # 趋势偏强
    elif close > ma20 * 1.02 and rsi > 60:
        signal = "🟢 趋势偏强"

    # 超跌反弹
    elif rsi < 35 and close > prev_candle['Open'] and close > ma5_val and close > ma20:
        signal = "🟢 超跌反弹"

    # 底部反转结构 + 放量
    elif (
        rsi > 40 and rsi - df['RSI'].iloc[-5] > 10 and
        close > ma5_val and
        last['Close'] > last['Open'] and
        prev_candle['Low'] < prev_candle['Close'] and
        vol > avg_vol
    ):
        signal = "🟢 反转信号"

    # 做空信号
    elif close < ma20 and below_ma20 and 30 < rsi < 55 and close < ma5_val:
        signal = "🔻 做空信号"

    # 趋势偏弱
    elif close < ma20 * 0.98 and rsi < 40:
        signal = "🔻 趋势偏弱"

    # 背离信号
    elif rsi < 40 or rsi > 70:
        signal = "⚠ 背离信号"

    # MA20 附近震荡
    elif abs(close - ma20) / ma20 < 0.005:
        signal = "⏸ 震荡中性"

    print(f"[DEBUG] ETH-{interval_label}: Signal={signal}, RSI={rsi:.2f}, Close={close:.2f}, MA20={ma20:.2f}, Vol={vol:.2f}, AvgVol={avg_vol:.2f}")
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

def get_btc_analysis() -> dict:
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

        "sl_15m": sl15, "tp_15m": tp15, "qty_15m": qty15, "entry_15m": price15,
        "sl_1h": sl1h, "tp_1h": tp1h, "qty_1h": qty1h, "entry_1h": price1h,
        "sl_4h": sl4h, "tp_4h": tp4h, "qty_4h": qty4h, "entry_4h": price4h,

        "risk_usd": RISK_USD,
        "update_time": update_time
    }
