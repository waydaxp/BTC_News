# utils/fetch_eth_data.py
"""
获取 ETH-USD 1h / 4h K 线，叠加：
1) 连续 TREND_LEN 根 K 线同向
2) ADX>20 趋势过滤
3) MA20-MA50 共振
4) 4h 高周期方向一致

输出与 fetch_btc_data.py 完全相同的字段，便于 generate_data.py 汇总。
"""

from core.datasource   import pull_ohlc
from core.indicators   import add_basic_indicators
from core.signal       import make_signal, TREND_LEN


def get_eth_analysis() -> dict:
    # ===== 1. 拉数据 =====
    df_1h = pull_ohlc("ETH-USD", period="7d",  interval="1h")
    df_4h = pull_ohlc("ETH-USD", period="60d", interval="4h")

    if df_1h.empty or len(df_1h) < 60:
        # 返回占位，避免 KeyError
        keys = ("price","ma20","rsi","signal",
                "entry_price","stop_loss","take_profit",
                "max_loss","per_trade_position","strategy_text")
        return {k: "N/A" for k in keys}

    df_1h = add_basic_indicators(df_1h)
    df_4h = add_basic_indicators(df_4h)

    # ===== 2. 生成方向 =====
    direction = make_signal(df_1h, df_4h)
    last = df_1h.iloc[-1]

    price = round(float(last["Close"]), 2)

    if direction == "long":
        stop   = round(price * 0.985, 2)
        target = round(price * 1.03,  2)
        signal = f"✅ 做多信号：连续{TREND_LEN}根站上 MA20"
        strat  = "✅ 做多：买入→涨\n跌1.5%止损\n涨3%止盈"
    elif direction == "short":
        stop   = round(price * 1.015, 2)
        target = round(price * 0.97,   2)
        signal = f"🔻 做空信号：连续{TREND_LEN}根跌破 MA20"
        strat  = "🔻 做空：卖出→跌\n涨1.5%止损\n跌3%止盈"
    else:
        stop = target = "N/A"
        signal = "⏸ 观望"
        strat  = "暂无有效趋势"

    # ===== 3. 统一风控 =====
    account_usd, leverage, risk_pct = 1000, 20, 0.02
    max_loss  = round(account_usd * risk_pct, 2)
    position  = round(max_loss * leverage,   2)

    # ===== 4. 返回结构 =====
    return {
        "price"              : price,
        "ma20"               : round(last["MA20"], 2),
        "rsi"                : round(last["RSI"],  2),
        "signal"             : signal,
        "entry_price"        : price,
        "stop_loss"          : stop,
        "take_profit"        : target,
        "max_loss"           : max_loss,
        "per_trade_position" : position,
        "strategy_text"      : strat
    }
