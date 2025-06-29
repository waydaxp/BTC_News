# generate_data.py
"""
集中汇总 BTC 与 ETH 的行情解析，供 generate_html.py 调用。
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

# === 业务层 ===
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fear_greed   import get_fear_and_greed          # (idx, txt, emoji, ts)
from utils.fetch_macro  import get_macro_events            # str 列表


# ----------------------------------------------------------------------
# 辅助：额外字段（恐惧&贪婪、宏观事件、更新时间）
# ----------------------------------------------------------------------
def _extra_fields() -> dict[str, str]:
    idx, txt, emoji, ts_utc = get_fear_and_greed()

    # 1) 恐惧与贪婪
    fg_full = f"{idx} {emoji}（{txt}）"
    fg_time = (
        datetime.fromisoformat(ts_utc)           # 原始 UTC ISO8601
                .astimezone(ZoneInfo("Asia/Shanghai"))
                .strftime("%Y-%m-%d %H:%M")
    )

    # 2) 未来宏观事件（最多 5 条）
    macro_events = "<br>".join(get_macro_events())

    # 3) 当前页面生成时间（北京时间）
    bj_now = (
        datetime.now(tz=ZoneInfo("UTC"))  # ① always reliable UTC
                .astimezone(ZoneInfo("Asia/Shanghai"))  # ② convert to BJ
                .strftime("%Y-%m-%d %H:%M")
    )

    return {
        "fear_greed":   fg_full,
        "fg_time":      fg_time,
        "macro_events": macro_events,
        "page_time":    bj_now,
    }


# ----------------------------------------------------------------------
# 对外主函数
# ----------------------------------------------------------------------
def get_all_analysis() -> dict[str, str | float]:
    """返回一个扁平化 dict，键名直接对接 index_template.html 的占位符。"""
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base: dict[str, str | float] = {
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

    # 合并额外字段
    base.update(_extra_fields())
    return base


# ----------------------------------------------------------------------
# 快速本地调试
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
