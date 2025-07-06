import yfinance as yf
import pandas as pd
from datetime import datetime
from pytz import timezone
from core.indicators import add_basic_indicators, add_macd_boll_kdj, backtest_signals
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "BTC-USD"

def _download_tf(interval: str, period: str) -> pd.DataFrame:
    df = yf.download(PAIR, interval=interval, period=period, progress=False, auto_adjust=False)
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(PAIR, level=1, axis=1)
    df = df.rename(columns=str.title)
    df.index = df.index.tz_localize(None)
    df = add_basic_indicators(df)
    df = add_macd_boll_kdj(df)
    return df.dropna()

def _judge_signal(df: pd.DataFrame, interval_label="") -> tuple:
    last = df.iloc[-1]
    close = last['Close']
    rsi = last['RSI']
    ma20 = last['MA20']
    ma5_val = df['MA5'].iloc[-1]
    prev_candle = df.iloc[-2]

    signal, reason = "⏸ 中性信号", "未检测到显著信号"

    if rsi < 35 and df['RSI'].iloc[-2] < 30 and close > ma20:
        signal = "🟢 底部反转（可尝试做多）"
        reason = "RSI 超跌 + 回升至 MA20 上方"
    elif rsi > 65 and df['RSI'].iloc[-2] > 70 and close < ma20:
        signal = "🔻 顶部反转（可尝试做空）"
        reason = "RSI 高位回落 + 跌破 MA20"
    elif close > ma20 and rsi > 50 and close > ma5_val:
        signal = "🟢 做多信号"
        reason = "价格站上 MA20 且 RSI 强"
    elif close < ma20 and rsi < 50 and close < ma5_val:
        signal = "🔻 做空信号"
        reason = "价格低于 MA20 且 RSI 弱"
    elif abs(close - ma20) / ma20 < 0.005:
        signal = "⏸ 震荡中性"
        reason = "价格围绕 MA20 波动"

    print(f"[DEBUG] {PAIR}-{interval_label}: Signal={signal}, Reason={reason}, RSI={rsi:.2f}, Close={close:.2f}")
    return signal, reason

def _calc_trade(entry: float, atr: float, signal: str) -> tuple:
    if "多" in signal:
        sl = entry - ATR_MULT_SL * atr
        tp = entry + ATR_MULT_TP * atr
        qty = calc_position_size(entry, RISK_USD, ATR_MULT_SL, atr, "long")
    elif "空" in signal:
        sl = entry + ATR_MULT_SL * atr
        tp = entry - ATR_MULT_TP * atr
        qty = calc_position_size(entry, RISK_USD, ATR_MULT_SL, atr, "short")
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

    win_rate = backtest_signals(df1h, "BTC-1h")

    last15, last1h, last4h = df15.iloc[-1], df1h.iloc[-1], df4h.iloc[-1]
    atr1h = float(last1h['ATR'])

    # 预测建仓价 = MA20（趋势中枢）
    predicted_entry = float(last1h['MA20'])
    sl1h, tp1h, qty1h = _calc_trade(predicted_entry, atr1h, s1h)

    update_time = datetime.now(timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": predicted_entry,
        "ma20": float(last1h['MA20']),
        "rsi": float(last1h['RSI']),
        "atr": atr1h,
        "signal": f"{s4h} ({l4h}, 4h) / {s1h} ({l1h}, 1h) / {s15} ({l15}, 15m)",
        "entry_1h":  predicted_entry,
        "sl_1h":  sl1h,
        "tp_1h":  tp1h,
        "qty_1h":  qty1h,
        "risk_usd": RISK_USD,
        "update_time": update_time,
        "reason_15m": l15,
        "reason_1h": l1h,
        "reason_4h": l4h,
        "signal_15m": s15,
        "signal_1h": s1h,
        "signal_4h": s4h,
        "win_rate": win_rate,
    }
