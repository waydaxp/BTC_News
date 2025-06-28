# generate_data.py
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index
from datetime import datetime, timedelta

def get_all_analysis():
    btc   = get_btc_analysis()
    eth   = get_eth_analysis()
    macro = get_macro_event_summary()
    fear  = get_fear_and_greed_index()

    now_bj = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")

    data = {
        # === BTC ===
        "btc_price" : btc["price"],  "btc_ma20": btc["ma20"], "btc_rsi": btc["rsi"],
        "btc_signal": btc["signal"],
        "btc_entry" : btc["entry_price"],   "btc_stop": btc["stop_loss"],
        "btc_target": btc["take_profit"],   "btc_risk": btc["max_loss"],
        "btc_position": btc["per_trade_position"],
        "btc_strategy_text": btc["strategy_text"],

        # === ETH ===
        "eth_price" : eth["price"],  "eth_ma20": eth["ma20"], "eth_rsi": eth["rsi"],
        "eth_signal": eth["signal"],
        "eth_entry" : eth["entry_price"],   "eth_stop": eth["stop_loss"],
        "eth_target": eth["take_profit"],   "eth_risk": eth["max_loss"],
        "eth_position": eth["per_trade_position"],
        "eth_strategy_text": eth["strategy_text"],

        # === 宏观 & 情绪 ===
        "macro_events": macro,
        "fear_index": fear["index"], "fear_level": fear["level"], "fear_date": fear["date"],
        "update_time": now_bj
    }
    return data
