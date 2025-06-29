# generate_data.py
# =============================================================
# 汇总各类分析数据（BTC / ETH / 宏观 / 情绪），
# 统一返回给 generate_html.py & 其它上层调用。
# =============================================================

from datetime import datetime, timedelta

# --- 技术面 ---
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis

# --- 情绪 / 宏观（如暂未实现，可先注释掉） ---
try:
    from utils.fetch_fear_greed import get_fear_and_greed_index
except ImportError:
    get_fear_and_greed_index = None     # 占位

try:
    from utils.fetch_macro_events import get_macro_event_summary
except ImportError:
    get_macro_event_summary = None      # 占位


def _safe_call(fn, default):
    """
    若某个模块不存在 / 网络失败，返回默认值而不中断整体流程。
    """
    if fn is None:
        return default
    try:
        return fn()
    except Exception as e:  # 线上可用 logging 记录
        return default


def get_all_analysis() -> dict:
    """
    拉取 BTC / ETH / 宏观 / 情绪 并统一为模板字段。
    若部分数据获取失败，字段会填充为 'N/A'，以避免 KeyError。
    """
    # ---------- 技术面 ----------
    btc = get_btc_analysis()            # dict
    eth = get_eth_analysis()            # dict

    # ---------- 基本面 / 情绪 ----------
    macro = _safe_call(get_macro_event_summary, "N/A")
    fear  = _safe_call(get_fear_and_greed_index, {
        "index": "N/A", "level": "N/A", "date": "N/A"
    })

    # ---------- 北京时间 ----------
    now_bj = datetime.utcnow() + timedelta(hours=8)
    updated_time = now_bj.strftime("%Y-%m-%d %H:%M")

    # ---------- 整合 ----------
    ctx = {
        # ===== BTC =====
        "btc_price":   btc.get("price", "N/A"),
        "btc_ma20":    btc.get("ma20",  "N/A"),
        "btc_rsi":     btc.get("rsi",   "N/A"),
        "btc_signal":  btc.get("signal","N/A"),

        "btc_entry":   btc.get("entry_price", "N/A"),
        "btc_stop":    btc.get("stop_loss",   "N/A"),
        "btc_target":  btc.get("take_profit", "N/A"),
        "btc_risk":    btc.get("max_loss",    "N/A"),     # 单笔风险 USD
        "btc_position":btc.get("per_trade_position", "N/A"),
        "btc_strategy_text": btc.get("strategy_text", ""),

        # ===== ETH =====
        "eth_price":   eth.get("price", "N/A"),
        "eth_ma20":    eth.get("ma20",  "N/A"),
        "eth_rsi":     eth.get("rsi",   "N/A"),
        "eth_signal":  eth.get("signal","N/A"),

        "eth_entry":   eth.get("entry_price", "N/A"),
        "eth_stop":    eth.get("stop_loss",   "N/A"),
        "eth_target":  eth.get("take_profit", "N/A"),
        "eth_risk":    eth.get("max_loss",    "N/A"),
        "eth_position":eth.get("per_trade_position", "N/A"),
        "eth_strategy_text": eth.get("strategy_text", ""),

        # ===== 宏观 & 情绪 =====
        "macro_events": macro,
        "fear_index":   fear.get("index"),
        "fear_level":   fear.get("level"),
        "fear_date":    fear.get("date"),

        # ===== 更新时间 =====
        "updated_time": updated_time
    }

    return ctx


# -----------------------------------------------------------------
# 调试：直接运行文件时打印结果
# -----------------------------------------------------------------
if __name__ == "__main__":
    import pprint
    pprint.pp(get_all_analysis())
