from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_sentiment import get_sentiment_summary  # 确保这个函数返回包含 value、level、date

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_events()
    sentiment = get_sentiment_summary()

    data = {
        # BTC
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),
        "btc_risk": btc.get("max_loss", "N/A"),
        "btc_position": btc.get("per_trade_position", "N/A"),
        "btc_entry": btc.get("entry_price", "N/A"),
        "btc_stop": btc.get("stop_loss", "N/A"),
        "btc_target": btc.get("take_profit", "N/A"),

        # ETH
        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # 宏观事件
        "macro_events": macro,

        # 情绪指标
        "fear_index": sentiment.get("value", "N/A"),
        "fear_level": sentiment.get("level", "N/A"),
        "fear_date": sentiment.get("date", "N/A"),
    }

    return data
