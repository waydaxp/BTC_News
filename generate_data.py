# generate_data.py
"""
集中汇总 BTC 与 ETH 的行情解析，供 generate_html.py 调用。
"""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

# 业务层 ------------------------------------------------------------------
from utils.fetch_btc_data import get_btc_analysis   # 返回 dict，字段里含 "update_time" (UTC)
from utils.fetch_eth_data import get_eth_analysis
from utils.fear_greed    import get_fear_and_greed  # idx, txt, emoji, ts_utc
from utils.fetch_macro   import get_macro_events    # List[str]

BJ = ZoneInfo("Asia/Shanghai")  # 北京时区 ↓ 统一用它


# ------------------------------------------------------------------------
# 额外信息（恐惧 & 贪婪、宏观事件、页面生成时间）
# ------------------------------------------------------------------------
def _extra_fields() -> dict[str, str]:
    idx, txt, emoji, ts_utc = get_fear_and_greed()

    fg_full = f"{idx} {emoji}（{txt}）"

    fg_time = (
        datetime.fromisoformat(ts_utc)
        .astimezone(BJ)
        .strftime("%Y-%m-%d %H:%M")
    )

    macro_events_html = "<br>".join(get_macro_events())  # 已经是 list[str]

    page_time = (
        datetime.now(tz=ZoneInfo("UTC"))
        .astimezone(BJ)
        .strftime("%Y-%m-%d %H:%M")
    )

    return {
        "fear_greed": fg_full,
        "fg_time": fg_time,
        "macro_events": macro_events_html,
        "page_time": page_time,
    }


# ------------------------------------------------------------------------
# 主入口
# ------------------------------------------------------------------------
def get_all_analysis() -> dict[str, str | float]:
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    # —— 把 fetch_* 返回的 update_time(UTC) → 北京时间  ——
    btc_time_bj = (
        datetime.fromisoformat(btc["update_time"])
        .astimezone(BJ)
        .strftime("%Y-%m-%d %H:%M")
    )
    eth_time_bj = (
        datetime.fromisoformat(eth["update_time"])
        .astimezone(BJ)
        .strftime("%Y-%m-%d %H:%M")
    )

    base: dict[str, str | float] = {
        # ===== BTC =====
        "btc_price": btc["price"],
        "btc_signal": btc["signal"],
        "btc_ma20": btc["ma20"],
        "btc_rsi": btc["rsi"],
        "btc_atr": btc["atr"],
        "btc_sl": btc["sl"],
        "btc_tp": btc["tp"],
        "btc_qty": btc["qty"],
        "btc_risk": btc["risk_usd"],
        "btc_update_time": btc_time_bj,          # ★ 顶部用

        # ===== ETH =====
        "eth_price": eth["price"],
        "eth_signal": eth["signal"],
        "eth_ma20": eth["ma20"],
        "eth_rsi": eth["rsi"],
        "eth_atr": eth["atr"],
        "eth_sl": eth["sl"],
        "eth_tp": eth["tp"],
        "eth_qty": eth["qty"],
        "eth_risk": eth["risk_usd"],
        "eth_update_time": eth_time_bj,          # 如模板需要
    }

    # 额外公共字段
    base.update(_extra_fields())
    return base


# 本地调试 ---------------------------------------------------------------
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
