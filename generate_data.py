from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from utils.strategy_helper import generate_strategy_text_dynamic
from datetime import datetime, timedelta, timezone

def get_all_analysis() -> dict:
    # 获取分析数据
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
    macro = get_macro_event_summary()

    beijing_tz = timezone(timedelta(hours=8))
    page_update = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

    def wrap_asset(asset):
        return {
            "price": asset["price"],
            "ma20": asset["ma20"],
            "rsi": asset["rsi"],
            "atr": asset["atr"],
            "volume": asset.get("volume"),
            "funding": asset.get("funding"),

            "entry_4h": asset["entry_4h"],
            "sl_4h": asset["sl_4h"],
            "tp_4h": asset["tp_4h"],
            "support_4h": asset.get("support_4h"),
            "resistance_4h": asset.get("resistance_4h"),

            "strategy_4h": generate_strategy_text_dynamic(
                price=asset["price"],
                support=asset.get("support_4h"),
                resistance=asset.get("resistance_4h"),
                atr=asset.get("atr"),
                volume_up=asset.get("volume_up", False)
            )
        }

    return {
        "btc": wrap_asset(btc),
        "eth": wrap_asset(eth),
        "fg_idx": fg_idx,
        "fg_txt": fg_txt,
        "fg_emoji": fg_emoji,
        "fg_ts": fg_ts,
        "macro_events": macro,
        "page_update": page_update
    }
    def get_eth_analysis():
    return fetch_eth_data()
