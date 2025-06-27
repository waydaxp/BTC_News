# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index
from datetime import datetime

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro_events = get_macro_event_summary()
    fear_data = get_fear_and_greed_index()

    # 解析时间戳为可读格式
    try:
        fear_date = datetime.utcfromtimestamp(int(fear_data['time'])).strftime('%Y-%m-%d')
    except Exception:
        fear_date = "N/A"

    return {
        # BTC
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),
        "btc_risk": btc.get("risk", "N/A"),
        "btc_position": btc.get("position", "N/A"),
        "btc_entry": btc.get("entry", "N/A"),
        "btc_stop": btc.get("stop", "N/A"),
        "btc_target": btc.get("target", "N/A"),

        # ETH
        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # 宏观
        "macro_events": macro_events,

        # 恐惧与贪婪
        "fear_index": fear_data.get("value", "N/A"),
        "fear_level": fear_data.get("value_classification", "N/A"),
        "fear_date": fear_date,
    }
