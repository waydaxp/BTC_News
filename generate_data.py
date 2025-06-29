# generate_data.py
"""
集中汇总 BTC / ETH 行情与装饰信息，供 generate_html.py 调用。
---------------------------------------------------------------
依赖：
    utils.fetch_btc_data.get_btc_analysis
    utils.fetch_eth_data.get_eth_analysis
    utils.fear_greed.get_fear_and_greed
    utils.fetch_macro_events.get_macro_events
"""

from __future__ import annotations

import inspect
from datetime import datetime, timezone

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_events


# ------------------------------------------------------------------
# 额外装饰字段：宏观事件、恐惧贪婪、更新时间（统一在此处容错）
# ------------------------------------------------------------------
def _extra_fields() -> dict[str, str]:
    """保证第三方函数格式变化时不崩溃。"""

    # ---------- ① 宏观事件 ----------
    sig = inspect.signature(get_macro_events)
    macro_lines = (
        get_macro_events(limit=5)
        if "limit" in sig.parameters
        else get_macro_events()[:5]
    )
    macro_events_html = "<br>".join(macro_lines)

    # ---------- ② 恐惧 / 贪婪 ----------
    fg_raw = get_fear_and_greed()

    # 1) 元组 (idx, text)
    if isinstance(fg_raw, tuple) and len(fg_raw) >= 2:
        fg_idx, fg_text = fg_raw[:2]

    # 2) 单值（int/float/str）
    elif isinstance(fg_raw, (int, float, str)):
        fg_idx = int(float(fg_raw))
        fg_text = (
            "极度恐惧" if fg_idx < 20 else
            "恐惧"     if fg_idx < 40 else
            "中性"     if fg_idx < 60 else
            "贪婪"     if fg_idx < 80 else
            "极度贪婪"
        )

    # 3) 字典 {"value": .., "text": ..}
    elif isinstance(fg_raw, dict):
        fg_idx  = int(float(fg_raw.get("value", 0)))
        fg_text = fg_raw.get("text", "")

    # 4) 其它未知格式
    else:
        fg_idx, fg_text = "-", "N/A"

    # ---------- ③ 更新时间 ----------
    update_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return {
        "macro_events": macro_events_html,
        "fg_index"    : fg_idx,
        "fg_text"     : fg_text,
        "update_time" : update_time,
    }


# ------------------------------------------------------------------
# 主接口：给 HTML 模板使用
# ------------------------------------------------------------------
def get_all_analysis() -> dict:
    """返回一个扁平 dict，对应 index_template.html 的占位符。"""
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base: dict[str, str | float] = {
        # ===== BTC =====
        "btc_price" : btc["price"],
        "btc_signal": btc["signal"],
        "btc_ma20"  : btc["ma20"],
        "btc_rsi"   : btc["rsi"],
        "btc_atr"   : btc["atr"],
        "btc_sl"    : btc["sl"],
        "btc_tp"    : btc["tp"],
        "btc_qty"   : btc["qty"],
        "btc_risk"  : btc["risk_usd"],

        # ===== ETH =====
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

    # 装饰字段
    base.update(_extra_fields())
    return base


# ------------------------------------------------------------------
# 自测入口
# ------------------------------------------------------------------
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
