from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader
import os

def main():
    # 获取当前目录
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 设置模板目录
    template_dir = base_dir

    # 加载 Jinja2 模板环境
    env = Environment(
        loader=FileSystemLoader(template_dir),
        cache_size=0,
        auto_reload=True
    )

    # 加载模板文件（确保存在 index_template.html）
    template = env.get_template("index_template.html")

    # 获取分析上下文数据
    ctx = get_all_analysis()

    # 展开嵌套结构为扁平变量，用于模板渲染
    ctx_flat = {
        "btc_price": ctx["btc"].get("price"),
        "btc_ma20": ctx["btc"].get("ma20"),
        "btc_rsi": ctx["btc"].get("rsi"),
        "btc_atr": ctx["btc"].get("atr"),
        "btc_volume": ctx["btc"].get("volume"),
        "btc_support": ctx["btc"].get("support_4h"),
        "btc_resistance": ctx["btc"].get("resistance_4h"),
        "btc_funding_rate": ctx["btc"].get("funding"),
        "btc_tp": ctx["btc"].get("tp_4h"),
        "btc_sl": ctx["btc"].get("sl_4h"),
        "btc_signal": "多头" if ctx["btc"].get("entry_4h") else "观望",
        "btc_strategy_note": ctx["btc"].get("strategy_4h"),

        "eth_price": ctx["eth"].get("price"),
        "eth_ma20": ctx["eth"].get("ma20"),
        "eth_rsi": ctx["eth"].get("rsi"),
        "eth_atr": ctx["eth"].get("atr"),
        "eth_volume": ctx["eth"].get("volume"),
        "eth_support": ctx["eth"].get("support_4h"),
        "eth_resistance": ctx["eth"].get("resistance_4h"),
        "eth_funding_rate": ctx["eth"].get("funding"),
        "eth_tp": ctx["eth"].get("tp_4h"),
        "eth_sl": ctx["eth"].get("sl_4h"),
        "eth_signal": "多头" if ctx["eth"].get("entry_4h") else "观望",
        "eth_strategy_note": ctx["eth"].get("strategy_4h"),

        "fg_idx": ctx["fg_idx"],
        "fg_txt": ctx["fg_txt"],
        "fg_emoji": ctx["fg_emoji"],
        "fg_ts": ctx["fg_ts"],
        "macro_events": ctx["macro_events"],
        "page_update": ctx["page_update"],

        "predict_entry_comment": ctx["predict_entry_comment"],
        "risk_stats": ctx["risk_stats"]
    }

    # 渲染 HTML 内容
    html = template.render(**ctx_flat)

    # 输出路径
    output_path = "/var/www/html/index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已生成并部署到 /var/www/html ✅")

if __name__ == "__main__":
    main()
