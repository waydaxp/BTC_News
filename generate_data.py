from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index

def get_all_analysis():
    # 获取 BTC 技术数据（返回 dict）
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_event_summary()
    fear_data = get_fear_and_greed_index()

    data = {
        # BTC
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),
        "btc_entry": btc.get("entry_price", "N/A"),
        "btc_stop": btc.get("stop_loss", "N/A"),
        "btc_target": btc.get("take_profit", "N/A"),
        "btc_risk": btc.get("max_loss", "N/A"),
        "btc_position": btc.get("per_trade_position", "N/A"),

        # ETH
        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # 宏观事件
        "macro_events": macro,

        # 恐惧贪婪
        "fear_index": fear_data.get("index", "N/A"),
        "fear_level": fear_data.get("level", "N/A"),
        "fear_date": fear_data.get("date", "N/A"),
    }

    return data
