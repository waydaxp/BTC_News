# -*- coding: utf-8 -*-
"""
generate_data.py
================
汇总:
  • BTC 技术面 + 策略
  • ETH 技术面 + 策略
  • 宏观事件（可选）
  • 恐惧与贪婪指数（可选）

返回一个 dict，方便 HTML / Telegram 渲染。
"""

from datetime import datetime, timezone, timedelta

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis

# 这两个模块如果暂时没有，可以先写 stub，让函数直接返回 "N/A"
try:
    from utils.fetch_macro_events import get_macro_event_summary
except ImportError:
    def get_macro_event_summary() -> str:   # type: ignore
        return "N/A"

try:
    from utils.fetch_fear_greed import get_fear_and_greed_index
except ImportError:
    def get_fear_and_greed_index() -> dict:   # type: ignore
        return {"index": "N/A", "level": "N/A", "date": "N/A"}


def pretty(val):
    """统一把浮点数格式化成 2 位小数，其余保持原样"""
    return f"{val:.2f}" if isinstance(val, (int, float)) else val


def get_all_analysis() -> dict:
    """主入口：拉全部数据 → 组装 ctx 字典"""

    # ── 1. 各品种技术面 ───────────────────────────────────────────────────
    btc = get_btc_analysis()       # dict
    eth = get_eth_analysis()       # dict

    # ── 2. 宏观数据 & 情绪指标（可选）─────────────────────────────────────
    macro = get_macro_event_summary()
    fear  = get_fear_and_greed_index()

    # ── 3. 更新时间（转为北京时间 UTC+8）─────────────────────────────────
    cn_time = datetime.now(timezone.utc) + timedelta(hours=8)
    update_time = cn_time.strftime("%Y-%m-%d %H:%M（北京时间）")

    # ── 4. 组装上下文 ────────────────────────────────────────────────────
    ctx = {
        # ===== BTC =====
        "btc_price":          pretty(btc["price"]),
        "btc_direction":      btc["direction"],          # long / short / neutral
        "btc_strategy_text":  btc["strategy_text"],
        "btc_sl":             pretty(btc["sl"]),
        "btc_tp":             pretty(btc["tp"]),

        # ===== ETH =====
        "eth_price":          pretty(eth["price"]),
        "eth_direction":      eth["direction"],
        "eth_strategy_text":  eth["strategy_text"],
        "eth_sl":             pretty(eth["sl"]),
        "eth_tp":             pretty(eth["tp"]),

        # ===== 宏观 & 情绪 =====
        "macro_events":       macro,
        "fear_index":         fear.get("index"),
        "fear_level":         fear.get("level"),
        "fear_date":          fear.get("date"),

        # ===== 其他 =====
        "update_time":        update_time,
    }

    return ctx


# ────────────────────── 本地调试用 ──────────────────────
if __name__ == "__main__":
    import pprint
    pprint.pp(get_all_analysis())  # noqa: F821
