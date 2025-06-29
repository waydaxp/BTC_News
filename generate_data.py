"""
聚合 BTC / ETH 行情分析，供 generate_html.py 渲染
------------------------------------------------------------------
依赖：
    utils.fetch_btc_data.get_btc_analysis
    utils.fetch_eth_data.get_eth_analysis
    utils.fear_greed.get_fear_and_greed        -> (idx:int, txt:str, ts:str)
    utils.fetch_macro_events.get_macro_events  -> List[str]
------------------------------------------------------------------
返回:
    dict ─── 键名 100 % 对应 HTML 模板的 {{ 占位符 }}
"""

from utils.fetch_btc_data   import get_btc_analysis
from utils.fetch_eth_data   import get_eth_analysis
from utils.fear_greed       import get_fear_and_greed
from utils.fetch_macro_events import get_macro_events


# ――― 私有：附加信息（恐惧/贪婪 + 宏观事件 + 更新时间） ─―― #
def _extra_fields() -> dict:
    """统一打包附加字段，避免主逻辑膨胀"""
    fg_idx, fg_txt, fg_ts = get_fear_and_greed()      # 68, "Greed", "2025-06-30 01:45"

    macro_events = "<br>".join(get_macro_events()[:5])   # 取前 5 条，用 <br> 分行

    return {
        "fg_index"   : fg_idx,
        "fg_text"    : fg_txt,
        "update_time": fg_ts,
        "macro_events": macro_events,
    }


# ――― 对外主接口 ─―― #
def get_all_analysis() -> dict:
    """扁平化字段，方便 HTML .format(**ctx) 直接替换"""
    btc = get_btc_analysis()
    eth = get_eth_analysis()

    base = {
        # ╭─────────  BTC  ─────────╮
        "btc_price" : btc["price"],
        "btc_signal": btc["signal"],
        "btc_ma20"  : btc["ma20"],
        "btc_rsi"   : btc["rsi"],
        "btc_sl"    : btc["sl"],
        "btc_tp"    : btc["tp"],
        "btc_qty"   : btc["qty"],
        "btc_risk"  : btc["risk_usd"],

        # ╭─────────  ETH  ─────────╮
        "eth_price" : eth["price"],
        "eth_signal": eth["signal"],
        "eth_ma20"  : eth["ma20"],
        "eth_rsi"   : eth["rsi"],
        "eth_sl"    : eth["sl"],
        "eth_tp"    : eth["tp"],
        "eth_qty"   : eth["qty"],
        "eth_risk"  : eth["risk_usd"],
    }

    # 插入附加信息（恐惧 & 宏观 & 更新时间）
    base.update(_extra_fields())
    return base


# ――― CLI 快速预览 ─―― #
if __name__ == "__main__":
    import json, pprint
    pprint.pp(json.dumps(get_all_analysis(), indent=2, ensure_ascii=False))
