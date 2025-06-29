import yfinance as yf
import pandas as pd
from datetime import datetime
from pytz import timezone
from core.indicators import add_basic_indicators, add_macd_boll_kdj
from core.risk import calc_position_size, ATR_MULT_SL, ATR_MULT_TP, RISK_USD

PAIR = "ETH-USD"

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

def backtest_signals(df: pd.DataFrame, label: str = "") -> float:
    trades = []
    for i in range(10, len(df)-5):
        rsi = df['RSI'].iloc[i]
        ma5_val = df['Close'].rolling(5).mean().iloc[i]
        close = df['Close'].iloc[i]
        ma20 = df['MA20'].iloc[i]
        atr = df['ATR'].iloc[i]

        if close > ma20 and 45 < rsi < 70 and close > ma5_val:
            entry = close
            exit_price = df['Close'].iloc[i+5]
            trades.append(1 if exit_price > entry else 0)
        elif close < ma20 and 30 < rsi < 55 and close < ma5_val:
            entry = close
            exit_price = df['Close'].iloc[i+5]
            trades.append(1 if exit_price < entry else 0)
    win_rate = round(sum(trades) / len(trades) * 100, 1) if trades else 0.0
    print(f"[回测] {label} 准确率: {win_rate}%")
    return win_rate

def _judge_signal(df: pd.DataFrame, interval_label="") -> str:
    last = df.iloc[-1]
    ma5 = df['Close'].rolling(5).mean()
    rsi = last['RSI']
    close = last['Close']
    ma20 = last['MA20']
    ma5_val = ma5.iloc[-1]
    vol = last['Volume']
    avg_vol = df['Volume'].rolling(10).mean().iloc[-1]

    recent = df['Close'].tail(3) > df['MA20'].tail(3)
    above_ma20 = recent.sum() >= 2
    below_ma20 = (df['Close'].tail(3) < df['MA20'].tail(3)).sum() >= 2

    prev_candle = df.iloc[-2]
    signal = "⏸ 中性信号"
    grade = "观望"

    if rsi < 35 and df['RSI'].iloc[-2] < 30 and close > ma20:
        signal, grade = "🟢 底部反转", "强烈建议"
    elif rsi > 65 and df['RSI'].iloc[-2] > 70 and close < ma20:
        signal, grade = "🔻 顶部反转", "强烈建议"
    elif close > ma20 and above_ma20 and 40 < rsi < 72 and close > ma5_val:
        signal, grade = "🟢 做多信号", "建议"
    elif close < ma20 and below_ma20 and 30 < rsi < 55 and close < ma5_val:
        signal, grade = "🔻 做空信号", "建议"
    elif close > ma20 * 1.02 and rsi > 60:
        signal, grade = "🟢 趋势偏强", "谨慎"
    elif close < ma20 * 0.98 and rsi < 40:
        signal, grade = "🔻 趋势偏弱", "谨慎"
    elif rsi < 40 or rsi > 70:
        signal, grade = "⚠ 背离信号", "谨慎"
    elif abs(close - ma20) / ma20 < 0.005:
        signal, grade = "⏸ 震荡中性", "观望"

    print(f"[DEBUG] ETH-{interval_label}: Signal={signal}, Grade={grade}, RSI={rsi:.2f}, MA20={ma20:.2f}, Close={close:.2f}, Vol={vol:.2f}, AvgVol={avg_vol:.2f}")
    return f"{signal}（{grade}）"

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

    backtest_1h = backtest_signals(df1h, "ETH 1h")

    return {
        "price": price1h,
        "ma20": float(last1h['MA20']),
        "rsi": float(last1h['RSI']),
        "atr": atr1h,
        "signal": f"{signal4h} / {signal1h} / {signal15}",
        "entry_15m": price15, "sl_15m": sl15, "tp_15m": tp15, "qty_15m": qty15,
        "entry_1h":  price1h, "sl_1h":  sl1h, "tp_1h":  tp1h,  "qty_1h":  qty1h,
        "entry_4h":  price4h, "sl_4h":  sl4h, "tp_4h":  tp4h,  "qty_4h":  qty4h,
        "risk_usd": RISK_USD,
        "update_time": update_time,
        "win_rate": backtest_1h
    }
