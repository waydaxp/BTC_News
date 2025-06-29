import yfinance as yf
from core.datasource import pull_ohlc
from core.indicators import add_basic_indicators
from core.signal import make_signal

def get_btc_analysis() -> dict:
    # ------- 获取多周期 OHLC -------
    df_1h  = pull_ohlc("BTC-USD", "7d", "1h")   # 最近 7 天 1h
    df_4h  = pull_ohlc("BTC-USD", "60d", "4h")  # 作为趋势过滤
    if df_1h.empty or len(df_1h) < 60:
        return {k: "N/A" for k in (
            "price","ma20","rsi","signal",
            "entry_price","stop_loss","take_profit",
            "max_loss","per_trade_position","strategy_text"
        )}

    df_1h = add_basic_indicators(df_1h)
    df_4h = add_basic_indicators(df_4h)

    # ------- 生成方向信号 -------
    direction = make_signal(df_1h, df_4h)
    last      = df_1h.iloc[-1]

    # ------- 输出建议价位 -------
    price = round(float(last["Close"]), 2)
    if direction == "long":
        stop   = round(price * 0.985, 2)
        target = round(price * 1.03,  2)
        sig    = "✅ 做多信号：连续{}根站上 MA20".format(TREND_LEN)
        strat  = "✅ 做多：买入→涨\n跌1.5%止损\n涨3%止盈"
    elif direction == "short":
        stop   = round(price * 1.015, 2)
        target = round(price * 0.97,  2)
        sig    = "🔻 做空信号：连续{}根跌破 MA20".format(TREND_LEN)
        strat  = "🔻 做空：卖出→跌\n涨1.5%止损\n跌3%止盈"
    else:
        stop = target = "N/A"
        sig  = "⏸ 观望"
        strat= "暂无有效趋势"

    # ------- 风控 -------
    acc_usd, lev, risk_pct = 1000, 20, 0.02
    max_loss  = round(acc_usd * risk_pct, 2)
    position  = round(max_loss * lev, 2)

    return {
        "price": price, "ma20": round(last["MA20"],2), "rsi": round(last["RSI"],2),
        "signal": sig, "entry_price": price, "stop_loss": stop,
        "take_profit": target, "max_loss": max_loss, "per_trade_position": position,
        "strategy_text": strat
    }
