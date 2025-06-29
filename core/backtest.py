import pandas as pd

def backtest_signals(df: pd.DataFrame, label="") -> float:
    trades = []
    for i in range(10, len(df) - 10):
        rsi = df['RSI'].iloc[i]
        ma20 = df['MA20'].iloc[i]
        close = df['Close'].iloc[i]
        ma5 = df['Close'].rolling(5).mean().iloc[i]

        entry = close
        exit_price = df['Close'].iloc[i + 8]  # 持仓 8 根 K线
        if close > ma20 and 40 < rsi < 75 and close > ma5:
            trades.append(1 if exit_price > entry else 0)
        elif close < ma20 and 25 < rsi < 60 and close < ma5:
            trades.append(1 if exit_price < entry else 0)

    win_rate = round(sum(trades) / len(trades) * 100, 1) if trades else 0.0
    print(f"[回测] {label} 胜率: {win_rate}%，共 {len(trades)} 笔")
    return win_rate
