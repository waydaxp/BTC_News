# ✅ utils/generate_data.py
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary

def get_all_analysis():
    btc_data = get_btc_analysis()
    eth_data = get_eth_analysis()
    macro_data = get_macro_events()
    sentiment_data = get_sentiment_summary()

    return {
        "btc": btc_data,
        "eth": eth_data,
        "macro": macro_data,
        "sentiment": sentiment_data
    }
