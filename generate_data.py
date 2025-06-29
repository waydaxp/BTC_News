"""
集中汇总 BTC 与 ETH 的行情、风控 & 辅助指标，供 generate_html.py 调用
"""

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fear_greed     import get_fear_and_greed
from utils.fetch_macro_events import get_macro_events


# ──────────────────────────────────────────────────────────────
def _extra_fields() -> dict:
    """
    附加信息：恐惧/贪婪 + 宏观事件 + 更新时间
    返回一个 dict，键名直接映射到 HTML 模板占位符
    """
    # utils/fear_greed.get_fear_and_greed() → (指数, 文本, emoji, 更新时间)
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()

    macro_events = "<br>".join(get_macro_events()[:5])  # 取最近 5 条，<br> 换行

    return {
        "fg_index"     : fg_idx,       # 68
        "fg_text"      : fg_txt,       # Greed
        "fg_emoji"     : fg_emoji,     # 😨/😊
        "update_time"  : fg_ts,        # 2025-06-30 01:45
        "macro_events" : macro_events,
    }


# ──────────────────────────────────────────────────────────────
def get_all_analysis() -> dict:
    """
    将 BTC / ETH 的信号和附加信息打平到一个大 dict，
    方便 generate_html.py 一次 format()
    """
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base = {
        # -------- BTC --------
        "btc_price" : btc["price"],
        "btc_signal": btc["signal"],
        "btc_ma20"  : btc["ma20"],
        "btc_rsi"   : btc["rsi"],
        "btc_atr"   : btc["atr"],
        "btc_sl"    : btc["sl"],
        "btc_tp"    : btc["tp"],
        "btc_qty"   : btc["qty"],
        "btc_risk"  : btc["risk_usd"],
        # -------- ETH --------
        "eth_price" : eth["price"],
        "eth_signal": eth["signal"],
        "eth_ma20"  : eth["ma20"],
        "eth_rsi"   : eth["rsi"],
        "eth_atr"   : eth["atr"],
        "eth_sl"    : eth["sl"],
        "eth_tp"    : eth["tp"],
        "eth_qty"   : eth["qty"],
        "eth_risk"  : eth["risk_usd"],
    }

    # 合并扩展字段（恐惧/贪婪 & 宏观事件 & 更新时间）
    base.update(_extra_fields())
    return base


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
