# generate_data.py
"""
集中汇总 BTC 与 ETH 的行情解析，供 generate_html.py 使用。
---------------------------------------------------------------
- 把所有需要渲染到模板的字段“拍扁”成一个 dict
- 兼容旧版 / 新版 get_macro_events()（有没有 limit 形参都能跑）
"""

from __future__ import annotations

import inspect
from datetime import datetime, timezone

from utils.fetch_btc_data  import get_btc_analysis
from utils.fetch_eth_data  import get_eth_analysis
from utils.fear_greed      import get_fear_and_greed        # 返回 (指数, 文本)
from utils.fetch_macro_events import get_macro_events       # 可能有 / 没有 limit 参数


# ------------------------------------------------------------------
# 额外装饰字段：宏观事件、恐惧贪婪、更新时间
# ------------------------------------------------------------------
def _extra_fields() -> dict[str, str]:
    """返回 dict，可并入最终汇总。"""

    # ---- ① 宏观事件 ----
    sig = inspect.signature(get_macro_events)
    if "limit" in sig.parameters:                # 新版
        macro_lines = get_macro_events(limit=5)
    else:                                        # 旧版 fallback
        macro_lines = get_macro_events()[:5]

    macro_events_html = "<br>".join(macro_lines)

    # ---- ② 恐惧 & 贪婪 ----
    fg_idx, fg_text = get_fear_and_greed()       # 例如 (38, "恐惧")

    # ---- ③ 更新时间（UTC→东八区可自行调整）----
    update_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return {
        "macro_events" : macro_events_html,
        "fg_index"     : fg_idx,
        "fg_text"      : fg_text,
        "update_time"  : update_time,
    }


# ------------------------------------------------------------------
# 主接口：供 generate_html.py 调用
# ------------------------------------------------------------------
def get_all_analysis() -> dict[str, str | float]:
    """返回一个扁平化 dict，键名直接对应 HTML 模板占位符。"""
    btc = get_btc_analysis()    # utils/fetch_btc_data.py 里定义的字段
    eth = get_eth_analysis()    # utils/fetch_eth_data.py 里定义的字段

    base = {
        # ===== BTC =====
        "btc_price"  : btc["price"],
        "btc_signal" : btc["signal"],
        "btc_ma20"   : btc["ma20"],
        "btc_rsi"    : btc["rsi"],
        "btc_atr"    : btc["atr"],
        "btc_sl"     : btc["sl"],
        "btc_tp"     : btc["tp"],
        "btc_qty"    : btc["qty"],
        "btc_risk"   : btc["risk_usd"],

        # ===== ETH =====
        "eth_price"  : eth["price"],
        "eth_signal" : eth["signal"],
        "eth_ma20"   : eth["ma20"],
        "eth_rsi"    : eth["rsi"],
        "eth_atr"    : eth["atr"],
        "eth_sl"     : eth["sl"],
        "eth_tp"     : eth["tp"],
        "eth_qty"    : eth["qty"],
        "eth_risk"   : eth["risk_usd"],
    }

    # 合并额外字段（宏观事件 / 恐惧贪婪 / 更新时间）
    base.update(_extra_fields())
    return base


# ------------------------------------------------------------------
# CLI 自测
# ------------------------------------------------------------------
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
