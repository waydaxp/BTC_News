# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index
from datetime import datetime, timedelta

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_event_summary()
    fear_data = get_fear_and_greed_index()

    # 通用仓位与风险参数
    account_usd = 1000
    leverage = 20
    risk_per_trade = 0.02
    risk = round(account_usd * risk_per_trade, 2)
    position = round(risk * leverage, 2)

    # 获取当前价格
    price = btc.get("price", 0)

    # 做多参数
    long_entry = round(price, 2)
    long_stop = round(long_entry * 0.985, 2)
    long_target = round(long_entry * 1.03, 2)
    long_strategy = "✅ 做多策略：买入 → 涨\n跌 1.5% 止损\n涨 3% 止盈"

    # 做空参数
    short_entry = round(price, 2)
    short_stop = round(short_entry * 1.015, 2)
    short_target = round(short_entry * 0.97, 2)
    short_strategy = "🔻 做空策略：卖出 → 跌\n涨 1.5% 止损\n跌 3% 止盈"

    # 判断是否显示做多或做空建议
    signal_text = btc.get("signal", "")
    show_long = "✅" in signal_text or "做多" in signal_text
    show_short = "🔻" in signal_text or "做空" in signal_text

    # 更新时间（北京时间）
    updated_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M（北京时间）")

    data = {
        # BTC 指标
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),

        # 做多策略
        "btc_long_entry": long_entry,
        "btc_long_stop": long_stop,
        "btc_long_target": long_target,
        "btc_long_risk": risk,
        "btc_long_position": position,
        "btc_long_strategy": long_strategy,

        # 做空策略
        "btc_short_entry": short_entry,
        "btc_short_stop": short_stop,
        "btc_short_target": short_target,
        "btc_short_risk": risk,
        "btc_short_position": position,
        "btc_short_strategy": short_strategy,

        # 控制显示
        "show_long": show_long,
        "show_short": show_short,

        # ETH 指标
        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # 宏观事件
        "macro_events": macro,

        # 恐惧贪婪指数
        "fear_index": fear_data.get("index", "N/A"),
        "fear_level": fear_data.get("level", "N/A"),
        "fear_date": fear_data.get("date", "N/A"),

        # 更新时间
        "updated_time": updated_time
    }

    return data
