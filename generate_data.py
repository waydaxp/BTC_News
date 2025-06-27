# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index


def get_all_analysis():
    try:
        btc = get_btc_analysis() or {}
    except Exception as e:
        print(f"[Error] BTC 数据获取失败: {e}")
        btc = {}

    try:
        eth = get_eth_analysis() or {}
    except Exception as e:
        print(f"[Error] ETH 数据获取失败: {e}")
        eth = {}

    try:
        macro = get_macro_event_summary() or []
    except Exception as e:
        print(f"[Error] 宏观事件获取失败: {e}")
        macro = []

    try:
        fear_data = get_fear_and_greed_index() or {}
    except Exception as e:
        print(f"[Error] 恐惧贪婪指数获取失败: {e}")
        fear_data = {}

    data = {
        # ✅ BTC 数据
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),
        "btc_entry": btc.get("entry_price", "N/A"),
        "btc_stop": btc.get("stop_loss", "N/A"),
        "btc_target": btc.get("take_profit", "N/A"),
        "btc_risk": btc.get("max_loss", "N/A"),
        "btc_position": btc.get("per_trade_position", "N/A"),

        # ✅ ETH 数据
        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # ✅ 宏观事件
        "macro_events": macro,

        # ✅ 恐惧贪婪指数
        "fear_index": fear_data.get("index", "N/A"),
        "fear_level": fear_data.get("level", "N/A"),
        "fear_date": fear_data.get("date", "N/A"),
    }

    return data
