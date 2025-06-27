from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index
from datetime import datetime, timedelta

def get_all_analysis():
    # 获取各类分析数据
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_event_summary()
    fear_data = get_fear_and_greed_index()

    # 构建双向策略说明（多/空均展示）
    btc_long_strategy = (
        "✅ 做多策略说明：买入 → 涨\n"
        "止损：跌 1.5%\n"
        "止盈：涨 3%"
    )
    btc_short_strategy = (
        "🔻 做空策略说明：卖出 → 跌\n"
        "止损：涨 1.5%\n"
        "止盈：跌 3%"
    )

    # 更新时间（北京时间）
    now_bj = datetime.utcnow() + timedelta(hours=8)
    updated_time = now_bj.strftime("%Y-%m-%d %H:%M（北京时间）")

    # 组装返回数据
    data = {
        # BTC 数据
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),
        "btc_entry": btc.get("entry_price", "N/A"),
        "btc_stop": btc.get("stop_loss", "N/A"),
        "btc_target": btc.get("take_profit", "N/A"),
        "btc_risk": btc.get("max_loss", "N/A"),
        "btc_position": btc.get("per_trade_position", "N/A"),
        "btc_long_strategy": btc_long_strategy,
        "btc_short_strategy": btc_short_strategy,

        # ETH 数据
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
