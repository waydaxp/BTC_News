"""
集中汇总 BTC 与 ETH 的行情解析，供 generate_html.py 调用。
"""

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fear_greed     import get_fear_and_greed
from utils.fetch_macro_events import get_macro_events


def _extra_fields() -> dict:
    """恐惧贪婪、宏观事件、更新时间等杂项"""
    fg_idx, fg_txt, fg_emoji, fg_ts = get_fear_and_greed()

    macro_events = "<br>".join(get_macro_events()[:5])

    return {
        "fg_idx" : fg_idx,
        "fg_txt" : fg_txt,
        "fg_emoji": fg_emoji,
        "fg_time": fg_ts,
        "macro_events": macro_events,
        "update_time": fg_ts,   # 全局更新时间可复用
    }


def get_all_analysis() -> dict:
    """返回一个扁平化 dict，键名直接对接 index_template.html 内的占位符。"""
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base = {
        # ===== BTC =====
        "btc_price" : btc["price"],
        "btc_signal": btc["signal"],
        "btc_ma20"  : btc["ma20"],
        "btc_rsi"   : btc["rsi"],
        "btc_sl"    : btc["sl"],
        "btc_tp"    : btc["tp"],
        "btc_qty"   : btc["qty"],
        "btc_risk"  : btc["risk_usd"],

        # ===== ETH =====
        "eth_price" : eth["price"],
        "eth_signal": eth["signal"],
        "eth_ma20"  : eth["ma20"],
        "eth_rsi"   : eth["rsi"],
        "eth_sl"    : eth["sl"],
        "eth_tp"    : eth["tp"],
        "eth_qty"   : eth["qty"],
        "eth_risk"  : eth["risk_usd"],
    }

    base.update(_extra_fields())
    return base


if __name__ == "__main__":
    import pprint, json
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
