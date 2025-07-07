from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from utils.strategy_helper import generate_strategy_text_dynamic
from datetime import datetime, timedelta, timezone

def wrap_asset(asset: dict) -> dict:
    try:
        return {
            "price": asset.get("price"),
            "ma20": asset.get("ma20"),
            "rsi": asset.get("rsi"),
            "atr": asset.get("atr"),
            "volume": asset.get("volume"),
            "funding": asset.get("funding"),

            "entry_4h": asset.get("entry_4h"),
            "sl_4h": asset.get("sl_4h"),
            "tp_4h": asset.get("tp_4h"),
            "support_4h": asset.get("support_4h"),
            "resistance_4h": asset.get("resistance_4h"),

            "strategy_4h": generate_strategy_text_dynamic(
                price=asset.get("price"),
                support=asset.get("support_4h"),
                resistance=asset.get("resistance_4h"),
                atr=asset.get("atr"),
                volume_up=asset.get("volume_up", False)
            )
        }
    except Exception as e:
        print(f"[wrap_asset] Error: {e}")
        return {}

def get_all_analysis() -> dict:
    # 初始化各项数据
    btc, eth = {}, {}
    fg_idx, fg_txt, fg_emoji, fg_ts = 0, "未知", "❓", "N/A"
    macro = []

    try:
        btc = get_btc_analysis()
        print("[分析] BTC 获取成功")
    except Exception as e:
        print(f"[分析] BTC 获取失败: {e}")

    try:
        eth = get_eth_analysis()
        print("[分析] ETH 获取成功")
    except Exception as e:
        print(f"[分析] ETH 获取失败: {e}")

    try:
        fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()
        print("[分析] 恐惧贪婪指数获取成功")
    except Exception as e:
        print(f"[分析] 恐惧贪婪指数失败: {e}")

    try:
        macro = get_macro_event_summary()
        print("[分析] 宏观事件获取成功")
    except Exception as e:
        print(f"[分析] 宏观事件失败: {e}")

    # 获取北京时间
    beijing_tz = timezone(timedelta(hours=8))
    page_update = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

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
