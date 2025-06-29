# generate_data.py

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from datetime import datetime


def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
    macro = get_macro_event_summary()
    page_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        # BTC
        "btc_price": btc["price"],
        "btc_ma20": btc["ma20"],
        "btc_rsi": btc["rsi"],
        "btc_atr": btc["atr"],
        "btc_signal": btc["signal"],
        "btc_sl": btc["sl"],
        "btc_tp": btc["tp"],
        "btc_qty": btc["qty"],
        "btc_risk": btc["risk_usd"],
        "btc_update_time": btc["update_time"],

        # ETH
        "eth_price": eth["price"],
        "eth_ma20": eth["ma20"],
        "eth_rsi": eth["rsi"],
        "eth_atr": eth["atr"],
        "eth_signal": eth["signal"],
        "eth_sl": eth["sl"],
        "eth_tp": eth["tp"],
        "eth_qty": eth["qty"],
        "eth_risk": eth["risk_usd"],
        "eth_update_time": eth["update_time"],

        # 恐惧与贪婪
        "fg_idx": fg_idx,
        "fg_txt": fg_txt,
        "fg_emoji": fg_emoji,
        "fg_ts": fg_ts,

        # 宏观事件
        "macro_events": macro,

        # 页面更新时间（北京时间）
        "page_update": page_update,
    }


if __name__ == "__main__":
    import pprint
    import json
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
