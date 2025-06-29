# generate_data.py
"""
集中汇总 BTC 与 ETH 行情 + 辅助信息，供 generate_html.py 调用
"""

from datetime import datetime, timezone, timedelta
from typing import Dict

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro   import get_macro_events       # 你已有或自行实现
from utils.fear_greed    import get_fear_and_greed     # 你已有或自行实现


TZ = timezone(timedelta(hours=8))      # 上海时区 UTC+8


def _extra_fields() -> Dict[str, str]:
    """宏观事件、恐惧与贪婪、更新时间等附加字段"""
    # ① 宏观事件：直接返回 <br> 拼好的多行字符串
    macro_events: str = "<br>".join(get_macro_events(limit=5))

    # ② 恐惧与贪婪
    fg_id, fg_val = get_fear_and_greed()

    # ③ 更新时间
    updated = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")

    return {
        "macro_events"   : macro_events or "无重要事件",
        "fear_greed_id"  : fg_id,
        "fear_greed_val" : fg_val,
        "updated"        : updated,
    }


def get_all_analysis() -> Dict[str, str]:
    """返回一个扁平字典 ↔ index_template.html 占位符"""
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base = {
        # ========= BTC =========
        "btc_price" : btc["price"],
        "btc_signal": btc["signal"],
        "btc_ma20"  : btc["ma20"],
        "btc_rsi"   : btc["rsi"],
        "btc_atr"   : btc["atr"],
        "btc_sl"    : btc["sl"],
        "btc_tp"    : btc["tp"],
        "btc_qty"   : btc["qty"],
        "btc_risk"  : btc["risk_usd"],

        # ========= ETH =========
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

    # 合并附加字段
    base.update(_extra_fields())
    return base


if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
