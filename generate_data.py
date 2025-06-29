# generate_data.py
"""
汇总 BTC / ETH 行情 + 装饰信息，供 generate_html.py 调用
---------------------------------------------------------------
依赖：
    utils.fetch_btc_data.get_btc_analysis
    utils.fetch_eth_data.get_eth_analysis
    utils.fear_greed.get_fear_and_greed
    utils.fetch_macro_events.get_macro_events
"""

from __future__ import annotations

import inspect, re
from datetime import datetime, timezone
from typing import Tuple

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fear_greed import get_fear_and_greed
from utils.fetch_macro_events import get_macro_events


# ------------------------------------------------------------------
# 工具：将任何混合字符串 -> (index:int, text:str)
# ------------------------------------------------------------------
_DIGIT_RE = re.compile(r"\d+")


def _parse_fg(raw) -> Tuple[str, str]:
    """把 get_fear_and_greed() 的返回值解析成 (指数, 文本)。"""
    # ① 已是 (idx, text) 元组
    if isinstance(raw, tuple) and len(raw) >= 2:
        return str(raw[0]), str(raw[1])

    # ② 字典
    if isinstance(raw, dict):
        return str(raw.get("value", "-")), str(raw.get("text", "N/A"))

    # ③ 单值（数字 or 字符串）
    raw_str = str(raw)
    m = _DIGIT_RE.search(raw_str)
    idx = m.group(0) if m else "-"
    txt = (
        raw_str.replace(idx, "").strip(" ()：:") or  # 去掉数字后剩余字符
        ("极度恐惧" if idx != "-" and int(idx) < 20 else
         "恐惧"     if idx != "-" and int(idx) < 40 else
         "中性"     if idx != "-" and int(idx) < 60 else
         "贪婪"     if idx != "-" and int(idx) < 80 else
         "极度贪婪")
    )
    return idx, txt


# ------------------------------------------------------------------
def _extra_fields() -> dict[str, str]:
    """宏观事件 / 恐惧贪婪 / 更新时间 —— 均带健壮容错。"""
    # ---------- 宏观事件 ----------
    sig = inspect.signature(get_macro_events)
    events = get_macro_events(limit=5) if "limit" in sig.parameters else get_macro_events()[:5]
    macro_events_html = "<br>".join(events)

    # ---------- 恐惧贪婪 ----------
    fg_index, fg_text = _parse_fg(get_fear_and_greed())

    # ---------- 更新时间 ----------
    update_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return {
        "macro_events": macro_events_html,
        "fg_index"    : fg_index,
        "fg_text"     : fg_text,
        "update_time" : update_time,
    }


# ------------------------------------------------------------------
def get_all_analysis() -> dict:
    """返回扁平化字典，对应 HTML 占位符。"""
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base = {
        # ===== BTC =====
        "btc_price": btc["price"], "btc_signal": btc["signal"],
        "btc_ma20": btc["ma20"],   "btc_rsi": btc["rsi"], "btc_atr": btc["atr"],
        "btc_sl": btc["sl"],       "btc_tp": btc["tp"],   "btc_qty": btc["qty"],
        "btc_risk": btc["risk_usd"],

        # ===== ETH =====
        "eth_price": eth["price"], "eth_signal": eth["signal"],
        "eth_ma20": eth["ma20"],   "eth_rsi": eth["rsi"], "eth_atr": eth["atr"],
        "eth_sl": eth["sl"],       "eth_tp": eth["tp"],   "eth_qty": eth["qty"],
        "eth_risk": eth["risk_usd"],
    }

    base.update(_extra_fields())
    return base


# ------------------------------------------------------------------
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
