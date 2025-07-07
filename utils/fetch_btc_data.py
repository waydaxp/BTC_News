from datetime import datetime
import yfinance as yf

def get_btc_analysis():
    symbol = "BTC-USD"
    df = yf.download(tickers=symbol, interval="1h", period="1d", progress=False)

    if df.empty or len(df) < 20:
        return {"error": "数据不足"}

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    price = round(close.iloc[-1], 2)
    ma20 = round(close.rolling(window=20).mean().iloc[-1], 2)
    rsi = round(compute_rsi(close), 2)
    atr = round(compute_atr(high, low, close), 2)

    support = round(min(low[-6:]), 2)
    resistance = round(max(high[-6:]), 2)
    entry = round((support + resistance) / 2, 2)
    tp = round(resistance * 1.02, 2)
    sl = round(support * 0.99, 2)

    return {
        "price": price,
        "ma20": ma20,
        "rsi": rsi,
        "atr": atr,
        "support_4h": support,
        "resistance_4h": resistance,
        "entry_4h": entry,
        "tp_4h": tp,
        "sl_4h": sl,
        "volume_4h": int(volume.iloc[-1]),
        "funding_rate": 0.0018,  # 示例值，可动态集成
        "signal_4h": judge_signal(rsi, price, ma20),
        "reason_4h": generate_reason(rsi, price, ma20),
        "update_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

def compute_rsi(close, period=14):
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(period).mean()
    ma_down = down.rolling(period).mean()
    rs = ma_up / ma_down
    return 100 - (100 / (1 + rs)).iloc[-1]

def compute_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = tr1.combine(tr2, max).combine(tr3, max)
    return tr.rolling(period).mean().iloc[-1]

def judge_signal(rsi, price, ma):
    if rsi > 60 and price > ma:
        return "看涨偏多"
    elif rsi < 40 and price < ma:
        return "看跌偏空"
    else:
        return "震荡中性"

def generate_reason(rsi, price, ma):
    parts = []
    if rsi > 60:
        parts.append("RSI 强势")
    elif rsi < 40:
        parts.append("RSI 弱势")
    else:
        parts.append("RSI 中性")

    if price > ma:
        parts.append("价格在 MA20 上方")
    elif price < ma:
        parts.append("价格在 MA20 下方")
    else:
        parts.append("价格贴近 MA20")

    return " + ".join(parts)
