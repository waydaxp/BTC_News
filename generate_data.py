from utils.fetch_btc_data import get_btc_analysis, get_btc_raw
from utils.fetch_eth_data import get_eth_analysis, get_eth_raw
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index

def get_all_analysis():
    btc_raw = get_btc_raw()
    eth_raw = get_eth_raw()
    macro_events = get_macro_event_summary()
    fear_data = get_fear_and_greed_index()

    data = {
        # BTC
        "btc_price": btc_raw.get("price"),
        "btc_ma20": btc_raw.get("ma20"),
        "btc_rsi": btc_raw.get("rsi"),
        "btc_signal": btc_raw.get("signal"),
        "btc_risk": btc_raw.get("risk"),
        "btc_position": btc_raw.get("position"),
        "btc_entry": btc_raw.get("entry"),
        "btc_stop": btc_raw.get("stop_loss"),
        "btc_target": btc_raw.get("take_profit"),

        # ETH
        "eth_price": eth_raw.get("price"),
        "eth_ma20": eth_raw.get("ma20"),
        "eth_rsi": eth_raw.get("rsi"),
        "eth_signal": eth_raw.get("signal"),

        # 宏观事件
        "macro_events": macro_events,

        # 恐惧与贪婪指数
        "fear_index": fear_data.get("index"),
        "fear_level": fear_data.get("level"),
        "fear_date": fear_data.get("date"),
    }

    return data
