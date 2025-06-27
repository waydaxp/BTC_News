from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_event_summary()
    fear = get_fear_and_greed_index()

    return {
        # BTC 技术数据
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),

        # BTC 操作建议
        "btc_entry": btc.get("entry", "N/A"),
        "btc_stop": btc.get("stop", "N/A"),
        "btc_target": btc.get("target", "N/A"),
        "btc_risk": btc.get("risk", "N/A"),
        "btc_position": btc.get("position", "N/A"),

        # ETH 技术数据
        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # 宏观事件
        "macro_events": macro or "暂无重要宏观事件",

        # 恐惧贪婪指数
        "fear_date": fear.get("date", "N/A"),
        "fear_index": fear.get("index", "N/A"),
        "fear_level": fear.get("level", "N/A"),
    }
