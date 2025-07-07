from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_event_summary
from utils.strategy_helper import generate_strategy_text_dynamic
from datetime import datetime, timedelta, timezone

def wrap_asset(asset: dict) -> dict:
    """
    提取 4h 数据并附加策略分析，返回精简上下文
    """
    print("[wrap_asset] 输入数据:", asset)

    try:
        tf_data = asset.get("4h", {})  # 默认以 4h 数据为主
        price = float(tf_data.get("price", 0))
        ma20 = float(tf_data.get("ma20", 0))
        rsi = float(tf_data.get("rsi", 0))
        atr = float(tf_data.get("atr", 0))
        volume = float(tf_data.get("volume", 0))
        funding = float(tf_data.get("funding", 0)) if tf_data.get("funding") not in [None, "-"] else "-"

        support = float(tf_data.get("support", 0))
        resistance = float(tf_data.get("resistance", 0))
        sl = float(tf_data.get("sl", 0)) if tf_data.get("sl") else "-"
        tp = float(tf_data.get("tp", 0)) if tf_data.get("tp") else "-"

        # 自动生成策略说明文本
        strategy_note = generate_strategy_text_dynamic(
            price=price,
            support=support,
            resistance=resistance,
            atr=atr,
            volume_up=volume > 0,
            timeframe="4h",
            funding_rate=None if funding == "-" else funding
        )

        return {
            "price": price,
            "ma20": ma20,
            "rsi": rsi,
            "atr": atr,
            "volume": volume,
            "funding": funding,
            "entry_4h": price,
            "sl_4h": sl,
            "tp_4h": tp,
            "support_4h": support,
            "resistance_4h": resistance,
            "strategy_4h": strategy_note
        }

    except Exception as e:
        print(f"[wrap_asset] Error: {e}")
        return {}

def get_all_analysis() -> dict:
    """
    获取 BTC/ETH 技术分析、市场情绪、宏观事件并整合为模板上下文
    """
    btc, eth = {}, {}
    fg_idx, fg_txt, fg_emoji, fg_ts = 0, "未知", "❓", "N/A"
    macro = "-"

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

    print("[最终上下文 ctx]:", ctx)
    return ctx
