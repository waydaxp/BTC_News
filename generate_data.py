# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro import get_macro_events
from utils.fetch_fg_index import get_fg_index

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_events()
    fg_data = get_fg_index()

    return {
        # BTC 信息
        "btc_price": round(btc["price"], 2),
        "btc_ma20": round(btc["ma20"], 2),
        "btc_rsi": round(btc["rsi"], 2),
        "btc_atr": round(btc["atr"], 2),
        "btc_signal": btc["signal"],
        "btc_risk": btc["risk_usd"],
        "btc_qty": round(btc["qty"], 6),
        "btc_sl": round(btc["sl"], 2) if btc["sl"] else "None",
        "btc_tp": round(btc["tp"], 2) if btc["tp"] else "None",

        # ETH 信息
        "eth_price": round(eth["price"], 2),
        "eth_ma20": round(eth["ma20"], 2),
        "eth_rsi": round(eth["rsi"], 2),
        "eth_atr": round(eth["atr"], 2),
        "eth_signal": eth["signal"],
        "eth_risk": eth["risk_usd"],
        "eth_qty": round(eth["qty"], 6),
        "eth_sl": round(eth["sl"], 2) if eth["sl"] else "None",
        "eth_tp": round(eth["tp"], 2) if eth["tp"] else "None",

        # 宏观与贪婪指数
        "macro_events": macro,
        "fg_idx": fg_data["value"],
        "fg_txt": fg_data["text"],
        "fg_emoji": fg_data["emoji"],
        "page_update": btc["update_time"]  # 页面统一用 BTC 更新时间
    }
