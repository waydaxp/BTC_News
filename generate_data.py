# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_event_summary()
    fear_data = get_fear_and_greed_index()

    # 如果 BTC 或 ETH 是字符串（代表错误信息），返回简化结果
    if isinstance(btc, str) or isinstance(eth, str):
        return {
            "btc_price": btc if isinstance(btc, str) else "⚠️ 数据异常",
            "eth_price": eth if isinstance(eth, str) else "⚠️ 数据异常",
            "macro_events": macro,
            "fear_index": fear_data.get("index", "N/A"),
            "fear_level": fear_data.get("level", "N/A"),
            "fear_date": fear_data.get("date", "N/A"),
        }

    return {
        **btc,
        **eth,
        "macro_events": macro,
        "fear_index": fear_data.get("index", "N/A"),
        "fear_level": fear_data.get("level", "N/A"),
        "fear_date": fear_data.get("date", "N/A"),
    }
