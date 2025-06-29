# generate_data.py
"""
汇总 BTC 与 ETH 的行情解析，再补充恐惧贪婪指数、宏观事件等信息，
最终返回一个**扁平化 dict**，直接用于 index_template.html 的占位符替换。
"""

from __future__ import annotations

# === 行情相关 ===
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis

# === 额外信息 ===
from utils.fear_greed       import get_fear_and_greed   # (idx, text, emoji, ts_bj)
from utils.fetch_macro_events import get_macro_events   # List[str]

# === 其他 ===
from datetime import datetime
from zoneinfo import ZoneInfo


# --------------------------------------------------------------------------- #
# 内部工具：拼接附加字段
# --------------------------------------------------------------------------- #
def _extra_fields() -> dict[str, str]:
    """恐惧指数 / 宏观日历等附加信息，返回键值均为字符串。"""
    # 1) Fear & Greed Index
    fg_idx, fg_txt, fg_emoji, fg_time = get_fear_and_greed()

    # 2) 宏观事件（取最近 5 条）
    macro_events_html = "<br>".join(get_macro_events()[:5])

    # 3) 页面更新时间（北京时间）
    bj_now = datetime.now(tz=ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M")

    return {
        "fg_idx"   : str(fg_idx),
        "fg_text"  : fg_txt,
        "fg_emoji" : fg_emoji,
        "fg_time"  : fg_time,
        "macro_ev" : macro_events_html,
        "update_ts": bj_now,
    }


# --------------------------------------------------------------------------- #
# 对外主函数
# --------------------------------------------------------------------------- #
def get_all_analysis() -> dict[str, str]:
    """综合 BTC、ETH + 其它信息，返回扁平 dict."""
    # === 技术面 ===
    btc = get_btc_analysis()   # utils/fetch_btc_data.py 输出字段
    eth = get_eth_analysis()   # utils/fetch_eth_data.py 输出字段

    base: dict[str, str] = {
        # ----- BTC -----
        "btc_price" : str(btc["price"]),
        "btc_signal": btc["signal"],
        "btc_ma20"  : str(btc["ma20"]),
        "btc_rsi"   : str(btc["rsi"]),
        "btc_atr"   : str(btc["atr"]),
        "btc_sl"    : str(btc["sl"]),
        "btc_tp"    : str(btc["tp"]),
        "btc_qty"   : str(btc["qty"]),
        "btc_risk"  : str(btc["risk_usd"]),

        # ----- ETH -----
        "eth_price" : str(eth["price"]),
        "eth_signal": eth["signal"],
        "eth_ma20"  : str(eth["ma20"]),
        "eth_rsi"   : str(eth["rsi"]),
        "eth_atr"   : str(eth["atr"]),
        "eth_sl"    : str(eth["sl"]),
        "eth_tp"    : str(eth["tp"]),
        "eth_qty"   : str(eth["qty"]),
        "eth_risk"  : str(eth["risk_usd"]),
    }

    # 合并附加字段（恐惧指数 / 宏观日历 / 更新时间）
    base.update(_extra_fields())
    return base


# --------------------------------------------------------------------------- #
# CLI 自测
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
