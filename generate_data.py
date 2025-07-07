from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from utils.strategy_helper import generate_strategy_text_dynamic
from datetime import datetime, timedelta, timezone

def wrap_asset(asset: dict) -> dict:
    print("[wrap_asset] 输入数据:", asset)  # 调试日志

    try:
        price = asset.get("price") or "-"
        ma20 = asset.get("ma20") or "-"
        rsi = asset.get("rsi") or "-"
        atr = asset.get("atr") or "-"
        volume = asset.get("volume") or "-"
        funding = asset.get("funding") or "-"

        support_4h = asset.get("support_4h") or "-"
        resistance_4h = asset.get("resistance_4h") or "-"

        return {
            "price": price,
            "ma20": ma20,
            "rsi": rsi,
            "atr": atr,
            "volume": volume,
            "funding": funding,

            "entry_4h": asset.get("entry_4h") or "-",
            "sl_4h": asset.get("sl_4h") or "-",
            "tp_4h": asset.get("tp_4h") or "-",
            "support_4h": support_4h,
            "resistance_4h": resistance_4h,

            "strategy_4h": generate_strategy_text_dynamic(
                price=price if isinstance(price, (int, float)) else 0,
                support=support_4h,
                resistance=resistance_4h,
                atr=atr if isinstance(atr, (int, float)) else 0,
                volume_up=asset.get("volume_up", False)
            )
        }
    except Exception as e:
        print(f"[wrap_asset] Error: {e}")
        return {}

def get_all_analysis() -> dict:
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

    beijing_tz = timezone(timedelta(hours=8))
    page_update = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")

    ctx = {
        "btc": wrap_asset(btc),
        "eth": wrap_asset(eth),
        "fg_idx": fg_idx,
        "fg_txt": fg_txt,
        "fg_emoji": fg_emoji,
        "fg_ts": fg_ts,
        "macro_events": macro,
        "page_update": page_update
    }

    print("[最终上下文 ctx]:", ctx)  # 可选调试

    return ctx
