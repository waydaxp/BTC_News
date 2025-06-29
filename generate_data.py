# generate_data.py
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis


def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    return {
        # BTC
        "btc_price": btc["price"],
        "btc_ma20":  btc["ma20"],
        "btc_rsi":   btc["rsi"],
        "btc_signal": btc["signal"],
        "btc_entry":  btc["entry_price"],
        "btc_stop":   btc["stop_loss"] or "N/A",
        "btc_target": btc["take_profit"] or "N/A",
        "btc_risk":   btc["risk_usd"],
        "btc_position": btc["position"],
        "btc_strategy": f"{btc['direction']} @ {btc['entry_price']}",

        # ETH
        "eth_price": eth["price"],
        "eth_ma20":  eth["ma20"],
        "eth_rsi":   eth["rsi"],
        "eth_signal": eth["signal"],

        # 更新时间
        "updated_time": btc["updated_time"],
    }
