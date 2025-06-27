# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_sentiment import get_sentiment_summary

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro_events = get_macro_event_summary()
    fear = get_sentiment_summary()

    return {
        # BTC 部分
        "btc_price": btc.get("price"),
        "btc_ma20": btc.get("ma20"),
        "btc_rsi": btc.get("rsi"),
        "btc_signal": btc.get("signal"),
        "btc_risk": btc.get("risk"),
        "btc_position": btc.get("position"),
        "btc_entry": btc.get("entry"),
        "btc_stop": btc.get("stop"),
        "btc_target": btc.get("target"),

        # ETH 部分
        "eth_price": eth.get("price"),
        "eth_ma20": eth.get("ma20"),
        "eth_rsi": eth.get("rsi"),
        "eth_signal": eth.get("signal"),

        # 宏观事件
        "macro_events": macro_events,

        # 恐惧贪婪
        "fear_index": fear.get("index"),
        "fear_level": fear.get("level"),
        "fear_date": fear.get("date"),
    }
