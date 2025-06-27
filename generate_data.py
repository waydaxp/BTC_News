# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_events()
    sentiment = get_sentiment_summary()

    data = {
        # BTC
        "btc_price": btc.get("price"),
        "btc_ma20": btc.get("ma20"),
        "btc_rsi": btc.get("rsi"),
        "btc_signal": btc.get("signal"),
        "btc_risk": btc.get("risk"),
        "btc_position": btc.get("position_size"),
        "btc_entry": btc.get("entry_price"),
        "btc_stop": btc.get("stop_loss"),
        "btc_target": btc.get("take_profit"),

        # ETH
        "eth_price": eth.get("price"),
        "eth_ma20": eth.get("ma20"),
        "eth_rsi": eth.get("rsi"),
        "eth_signal": eth.get("signal"),

        # 宏观
        "macro_events": macro,

        # 情绪
        "fear_index": sentiment.get("value"),
        "fear_level": sentiment.get("level"),
        "fear_date": sentiment.get("date"),
    }

    return data
