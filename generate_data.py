"""
Generate one–direction strategy (long / short / neutral) and common market data.
"""

from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index
from datetime import datetime, timedelta

ACCOUNT_USD = 1000      # 本金
LEVERAGE    = 20        # 杠杆
RISK_PCT    = 0.02      # 单笔风险 2%

def get_all_analysis() -> dict:
    # === 拉取数据 ===
    btc   = get_btc_analysis()
    eth   = get_eth_analysis()
    macro = get_macro_event_summary()
    fear  = get_fear_and_greed_index()

    # === 统一仓位 / 风险 ===
    max_loss = round(ACCOUNT_USD * RISK_PCT, 2)
    position = round(max_loss * LEVERAGE, 2)

    price = btc.get("price", 0) or 0

    # === 做多参数 ===
    long_entry   = round(price, 2)
    long_stop    = round(long_entry * 0.985, 2)   # -1.5 %
    long_target  = round(long_entry * 1.03,  2)   # +3 %
    long_strategy = (
        "✅ 做多策略：买入 → 涨\n"
        "跌 1.5% 止损\n"
        "涨 3%  止盈"
    )

    # === 做空参数 ===
    short_entry   = round(price, 2)
    short_stop    = round(short_entry * 1.015, 2)  # +1.5 %
    short_target  = round(short_entry * 0.97,  2)  # -3 %
    short_strategy = (
        "🔻 做空策略：卖出 → 跌\n"
        "涨 1.5% 止损\n"
        "跌 3%  止盈"
    )

    # === 根据信号选方向 ===
    signal_txt = btc.get("signal", "")
    if "做多" in signal_txt:
        direction = "long"
        entry, stop, target, strategy = long_entry, long_stop, long_target, long_strategy
    elif "做空" in signal_txt:
        direction = "short"
        entry, stop, target, strategy = short_entry, short_stop, short_target, short_strategy
    else:
        direction = "neutral"
        entry = stop = target = strategy = "N/A"

    updated_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M（北京时间）")

    return {
        # --- BTC ---
        "btc_price"  : btc.get("price", "N/A"),
        "btc_ma20"   : btc.get("ma20",  "N/A"),
        "btc_rsi"    : btc.get("rsi",   "N/A"),
        "btc_signal" : signal_txt,

        # --- 选定方向参数 ---
        "direction"  : direction,          # long / short / neutral
        "entry"      : entry,
        "stop"       : stop,
        "target"     : target,
        "risk"       : max_loss,
        "position"   : position,
        "strategy"   : strategy,

        # --- ETH ---
        "eth_price"  : eth.get("price", "N/A"),
        "eth_ma20"   : eth.get("ma20",  "N/A"),
        "eth_rsi"    : eth.get("rsi",   "N/A"),
        "eth_signal" : eth.get("signal","N/A"),

        # --- 宏观 & 情绪 ---
        "macro_events": macro,
        "fear_index"  : fear.get("index", "N/A"),
        "fear_level"  : fear.get("level", "N/A"),
        "fear_date"   : fear.get("date",  "N/A"),

        # 更新时间
        "updated_time": updated_time
    }
