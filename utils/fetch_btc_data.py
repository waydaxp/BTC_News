import yfinance as yf
import pandas as pd
from datetime import datetime
from pytz import timezone
from core.indicators import add_basic_indicators, add_macd_boll_kdj
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False, auto_adjust=False)
    if isinstance(df.columns, pd.MultiIndex):
        if "Ticker" in df.columns.names and "Price" in df.columns.names:
            df = df.xs(PAIR, level="Ticker", axis=1)
        else:
            raise ValueError("[错误] 未识别的 MultiIndex 结构")
    df = df.rename(columns=str.title)
    expected_cols = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(f"[错误] 缺失所需列: {missing}, 当前列为: {df.columns.tolist()}")
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    df = add_macd_boll_kdj(df)
    return df.dropna()

def _judge_signal(df: pd.DataFrame, interval_label="") -> tuple:
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
    reason = "未检测到显著信号"
    signal = "⏸ 中性信号"

    if rsi < 35 and df['RSI'].iloc[-2] < 30 and close > ma20:
        signal = "🟢 底部反转（可尝试做多）"
        reason = "RSI 超跌连续低位 + 价格回升至 MA20 上方"
    elif rsi > 65 and df['RSI'].iloc[-2] > 70 and close < ma20:
        signal = "🔻 顶部反转（可尝试做空）"
        reason = "RSI 高位回落 + 收盘价跌破 MA20"
    elif close > ma20 and above_ma20 and 45 < rsi < 70 and close > ma5_val:
        signal = "🟢 做多信号"
        reason = "收盘价持续站上 MA20 且 RSI 处于多头区间"
    elif close < ma20 and below_ma20 and 30 < rsi < 55 and close < ma5_val:
        signal = "🔻 做空信号"
        reason = "收盘价持续低于 MA20 且 RSI 偏空"
    elif close > ma20 * 1.02 and rsi > 60:
        signal = "🟢 趋势偏强"
        reason = "价格突破 MA20 上方 2% 且 RSI 强势"
    elif close < ma20 * 0.98 and rsi < 40:
        signal = "🔻 趋势偏弱"
        reason = "价格低于 MA20 且 RSI 弱势"
    elif rsi < 35 and close > prev_candle['Open'] and close > ma5_val and close > ma20:
        signal = "🟢 超跌反弹"
        reason = "RSI 超跌 + 当前 K 线强势回升 + 均线突破"
    elif (
        rsi > 40 and rsi - df['RSI'].iloc[-5] > 10 and close > ma5_val and
        last['Close'] > last['Open'] and prev_candle['Low'] < prev_candle['Close'] and
        vol > avg_vol
    ):
        signal = "🟢 反转信号"
        reason = "RSI 回升 + 均线突破 + 成交量放大 + 多头 K 线形态"
    elif abs(close - ma20) / ma20 < 0.005:
        signal = "⏸ 震荡中性"
        reason = "价格围绕 MA20 波动"

    print(f"[DEBUG] {PAIR}-{interval_label}: Signal={signal}, Reason={reason}, RSI={rsi:.2f}, Close={close:.2f}")
    return signal, reason

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

    s15, l15 = _judge_signal(df15, "15m")
    s1h, l1h = _judge_signal(df1h, "1h")
    s4h, l4h = _judge_signal(df4h, "4h")

    last15, last1h, last4h = df15.iloc[-1], df1h.iloc[-1], df4h.iloc[-1]
    price15, price1h, price4h = float(last15['Close']), float(last1h['Close']), float(last4h['Close'])
    atr15, atr1h, atr4h = float(last15['ATR']), float(last1h['ATR']), float(last4h['ATR'])

    sl15, tp15, qty15 = _calc_trade(price15, atr15, s15)
    sl1h, tp1h, qty1h = _calc_trade(price1h, atr1h, s1h)
    sl4h, tp4h, qty4h = _calc_trade(price4h, atr4h, s4h)

    update_time = datetime.now(timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price1h,
        "ma20": float(last1h['MA20']),
        "rsi": float(last1h['RSI']),
        "atr": atr1h,
        "signal": f"{s4h} ({l4h}, 4h) / {s1h} ({l1h}, 1h) / {s15} ({l15}, 15m)",

        "entry_15m": price15, "sl_15m": sl15, "tp_15m": tp15, "qty_15m": qty15,
        "entry_1h":  price1h, "sl_1h":  sl1h, "tp_1h":  tp1h,  "qty_1h":  qty1h,
        "entry_4h":  price4h, "sl_4h":  sl4h, "tp_4h":  tp4h,  "qty_4h":  qty4h,

        "risk_usd": RISK_USD,
        "update_time": update_time,

        "reason_15m": l15,
        "reason_1h": l1h,
        "reason_4h": l4h,
    }
