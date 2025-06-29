# generate_data.py
"""
集中汇总 BTC 与 ETH 的行情解析，供 generate_html.py 调用
"""
from datetime import datetime, timezone, timedelta

from utils.fetch_btc_data  import get_btc_analysis
from utils.fetch_eth_data  import get_eth_analysis
from utils.fear_greed      import get_fear_and_greed
from utils.fetch_macro_events import get_macro_events   # ⇽ 已在 utils 里

TZ = timezone(timedelta(hours=8))              # 北京时间


def _extra_fields() -> dict:
    """宏观事件 / 恐惧贪婪 / 页面时间"""
    # ---- 宏观事件（列表 → html <li>） ----
    events = get_macro_events(n_future=5)      # List[str]
    ev_html = "<ul style='margin:0;padding-left:18px'>" + "".join(
        f"<li>{e}</li>" for e in events
    ) + "</ul>"

    # ---- 恐惧贪婪 ----
    fg_idx, fg_txt, fg_emoji, fg_utc = get_fear_and_greed()  # 68, "Greed", "😊", "2025-06-30 00:00"
    fg_time_cst = (
        datetime.fromisoformat(fg_utc).replace(tzinfo=timezone.utc)
        .astimezone(TZ).strftime("%Y-%m-%d %H:%M")
    )

    # ---- 页脚时间 ----
    page_time = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")

    return {
        "macro_events" : ev_html,
        "fear_greed"   : f"{fg_idx}（{fg_txt}） {fg_emoji}",
        "fg_time"      : fg_time_cst,
        "page_time"    : page_time,
    }


def get_all_analysis() -> dict:
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base = {
        # === BTC ===
        "btc_price" : btc["price"],  "btc_signal": btc["signal"],
        "btc_ma20"  : btc["ma20"],   "btc_rsi"   : btc["rsi"],
        "btc_atr"   : btc["atr"],    "btc_sl"    : btc["sl"],
        "btc_tp"    : btc["tp"],     "btc_qty"   : btc["qty"],
        "btc_risk"  : btc["risk_usd"],
        "btc_update_time": btc["update_time"],

        # === ETH ===
        "eth_price" : eth["price"],  "eth_signal": eth["signal"],
        "eth_ma20"  : eth["ma20"],   "eth_rsi"   : eth["rsi"],
        "eth_atr"   : eth["atr"],    "eth_sl"    : eth["sl"],
        "eth_tp"    : eth["tp"],     "eth_qty"   : eth["qty"],
        "eth_risk"  : eth["risk_usd"],
        "eth_update_time": eth["update_time"],
    }
    base.update(_extra_fields())
    return base


if __name__ == "__main__":
    import pprint, json
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
