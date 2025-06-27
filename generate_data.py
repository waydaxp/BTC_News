Below are all three updated files ready to paste into your project.

⸻

1️⃣ utils/generate_data.py

"""Return one-direction strategy (long / short / neutral) + common data."""
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index
from datetime import datetime, timedelta

ACCOUNT_USD = 1000           # 账户本金
LEVERAGE    = 20             # 杠杆倍数
RISK_PCT    = 0.02           # 单笔风险 2 %


def get_all_analysis():
    # === 拉取各模块数据 ===
    btc   = get_btc_analysis()
    eth   = get_eth_analysis()
    macro = get_macro_event_summary()
    fear  = get_fear_and_greed_index()

    price = btc.get("price", 0)

    # === 统一仓位 / 风险计算 ===
    max_loss = round(ACCOUNT_USD * RISK_PCT, 2)
    position = round(max_loss * LEVERAGE, 2)

    # === 生成双向参数（先算好，一会儿按方向选用） ===
    long_params  = {
        "entry":   round(price, 2),
        "stop":    round(price * 0.985, 2),      # -1.5 %
        "target":  round(price * 1.03,  2),      # +3 %
        "risk":    max_loss,
        "position":position,
        "strategy": "✅ 做多策略：买入 → 涨\n跌 1.5% 止损\n涨 3% 止盈"
    }
    short_params = {
        "entry":   round(price, 2),
        "stop":    round(price * 1.015, 2),      # +1.5 %
        "target":  round(price * 0.97,  2),      # -3 %
        "risk":    max_loss,
        "position":position,
        "strategy": "🔻 做空策略：卖出 → 跌\n涨 1.5% 止损\n跌 3% 止盈"
    }

    # === 根据信号决定最终方向 ===
    signal_txt = btc.get("signal", "")
    if "做多" in signal_txt:
        dir_flag  = "long"
        params    = long_params
    elif "做空" in signal_txt:
        dir_flag  = "short"
        params    = short_params
    else:
        dir_flag  = "neutral"
        params    = {k: "N/A" for k in long_params}

    # === 更新时间（北京时间） ===
    updated_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M（北京时间）")

    # === 汇总返回 ===
    data = {
        # BTC technical
        "btc_price" : btc.get("price", "N/A"),
        "btc_ma20"  : btc.get("ma20",  "N/A"),
        "btc_rsi"   : btc.get("rsi",   "N/A"),
        "btc_signal": signal_txt,

        # 统一策略字段（根据方向填充）
        "entry"     : params["entry"],
        "stop"      : params["stop"],
        "target"    : params["target"],
        "risk"      : params["risk"],
        "position"  : params["position"],
        "strategy"  : params["strategy"],
        "direction" : dir_flag,               # long / short / neutral

        # ETH 部分
        "eth_price" : eth.get("price", "N/A"),
        "eth_ma20"  : eth.get("ma20",  "N/A"),
        "eth_rsi"   : eth.get("rsi",   "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        # 宏观 & 情绪
        "macro_events": macro,
        "fear_index"  : fear.get("index", "N/A"),
        "fear_level"  : fear.get("level", "N/A"),
        "fear_date"   : fear.get("date",  "N/A"),

        "updated_time": updated_time
    }
    return data


⸻

2️⃣ generate_html.py

"""Render index.html from template with single-direction suggestion."""
from generate_data import get_all_analysis
from datetime import datetime, timedelta

data = get_all_analysis()

# 读取模板
with open("index_template.html", "r", encoding="utf-8") as f:
    tpl = f.read()

# 先填充通用占位符
tpl_rendered = tpl.format(
    btc_price=data["btc_price"], btc_ma20=data["btc_ma20"], btc_rsi=data["btc_rsi"], btc_signal=data["btc_signal"],
    entry=data["entry"], stop=data["stop"], target=data["target"],
    risk=data["risk"], position=data["position"], strategy=data["strategy"],
    eth_price=data["eth_price"], eth_ma20=data
