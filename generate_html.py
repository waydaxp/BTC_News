Below are **all three updated files** ready to paste into your project.

---

## 1️⃣ utils/generate\_data.py

```python
"""Return one‑direction strategy (long / short / neutral) + common data."""
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
        "stop":    round(price * 0.985, 2),      # ‑1.5 %
        "target":  round(price * 1.03,  2),      # +3 %
        "risk":    max_loss,
        "position":position,
        "strategy": "✅ 做多策略：买入 → 涨\n跌 1.5% 止损\n涨 3% 止盈"
    }
    short_params = {
        "entry":   round(price, 2),
        "stop":    round(price * 1.015, 2),      # +1.5 %
        "target":  round(price * 0.97,  2),      # ‑3 %
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
```

---

## 2️⃣ generate\_html.py

```python
"""Render index.html from template with single‑direction suggestion."""
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
    eth_price=data["eth_price"], eth_ma20=data["eth_ma20"], eth_rsi=data["eth_rsi"], eth_signal=data["eth_signal"],
    macro_events=data["macro_events"], fear_index=data["fear_index"], fear_level=data["fear_level"],
    fear_date=data["fear_date"], updated_time=data["updated_time"]
)

# === 条件块处理 ===
if data["direction"] == "long":
    # 保留做多块，注释做空块
    tpl_rendered = tpl_rendered.replace("{long_block_start}", "").replace("{long_block_end}", "")
    tpl_rendered = tpl_rendered.replace("{short_block_start}", "<!--").replace("{short_block_end}", "-->")
elif data["direction"] == "short":
    tpl_rendered = tpl_rendered.replace("{short_block_start}", "").replace("{short_block_end}", "")
    tpl_rendered = tpl_rendered.replace("{long_block_start}", "<!--").replace("{long_block_end}", "-->")
else:  # neutral
    tpl_rendered = tpl_rendered.replace("{long_block_start}", "<!--")\
                                 .replace("{long_block_end}", "-->")\
                                 .replace("{short_block_start}", "<!--")\
                                 .replace("{short_block_end}", "-->")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(tpl_rendered)

print("✅ index.html 已生成")
```

---

## 3️⃣ index\_template.html

> 已将 CSS 大括号全部替换为 `{{` 和 `}}`，并加入条件块标记

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>BTC 技术分析报告</title>
  <style>
    body {{ font-family:"Helvetica Neue",sans-serif;background:#f7f7f7;padding:20px;line-height:1.6; }}
    h2  {{ background:#fff;padding:10px;border-left:5px solid #4CAF50;font-size:20px; }}
    .section {{ background:#fff;margin-bottom:20px;padding:15px;border-left:3px solid #4CAF50; }}
    .footer  {{ font-size:14px;color:gray;text-align:right; }}
  </style>
</head>
<body>

<h2>📉【BTC 技术分析】</h2>
<div class="section">
  当前价格: {btc_price}<br>
  MA20: {btc_ma20}<br>
  RSI: {btc_rsi}<br>
  技术信号: {btc_signal}
</div>

{long_block_start}
<h2>📈 做多操作建议</h2>
<div class="section">
  - 💰 风险金额: {risk}<br>
  - 🛠 杠杆后下单量: {position}<br>
  - 📌 建仓价: {entry}<br>
  - 🛑 止损: {stop}<br>
  - 🎯 止盈: {target}
</div>
{long_block_end}

{short_block_start}
<h2>📉 做空操作建议</h2>
<div class="section">
  - 💰 风险金额: {risk}<br>
  - 🛠 杠杆后下单量: {position}<br>
  - 📌 建仓价: {entry}<br>
  - 🛑 止损: {stop}<br>
  - 🎯 止盈: {target}
</div>
{short_block_end}

<h2>📌 策略说明</h2>
<div class="section">{strategy.replace('\n','<br>')}</div>

<h2>📉【ETH 技术分析】</h2>
<div class="section">
  当前价格: {eth_price}<br>
  MA20: {eth_ma20}<br>
  RSI: {eth_rsi}<br>
  技术信号: {eth_signal}
</div>

<h2>📅【宏观事件提醒】</h2>
<div class="section">{macro_events}</div>

<h2>📊 恐惧与贪婪指数（{fear_date}）</h2>
<div class="section">当前值: {fear_index}（{fear_level}）</div>

<hr>
<div class="footer">
  最后更新时间: {updated_time}
</div>

</body>
</html>
```

---

💡 这样：

* 仅在 **做多信号** 时显示做多板块；做空同理。
* “中性/超买/超卖” 情况下，两个板块都会被注释掉，仅展示技术信号和说明。

复制到项目 → Commit → Actions 运行即可。
