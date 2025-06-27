# generate_data.py
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_macro_events import get_macro_event_summary
from utils.fetch_fear_greed import get_fear_and_greed_index

def get_all_analysis():
    btc = get_btc_analysis()
    eth = get_eth_analysis()
    macro = get_macro_event_summary()
    fear = get_fear_and_greed_index()

    return {
        "btc_price": btc.get("price", "N/A"),
        "btc_ma20": btc.get("ma20", "N/A"),
        "btc_rsi": btc.get("rsi", "N/A"),
        "btc_signal": btc.get("signal", "N/A"),
        "btc_risk": btc.get("risk", "N/A"),
        "btc_position": btc.get("position", "N/A"),
        "btc_entry": btc.get("entry", "N/A"),
        "btc_stop": btc.get("stop", "N/A"),
        "btc_target": btc.get("target", "N/A"),

        "eth_price": eth.get("price", "N/A"),
        "eth_ma20": eth.get("ma20", "N/A"),
        "eth_rsi": eth.get("rsi", "N/A"),
        "eth_signal": eth.get("signal", "N/A"),

        "macro_events": macro,

        "fear_index": fear.get("index", "N/A"),
        "fear_level": fear.get("level", "N/A"),
        "fear_date": fear.get("date", "N/A")
    }


# generate_html.py
from jinja2 import Environment, FileSystemLoader
from generate_data import get_all_analysis

def generate_html():
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("index_template.html")

    context = get_all_analysis()
    print("[DEBUG] HTML 渲染数据:", context)

    rendered_html = template.render(context)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

if __name__ == "__main__":
    generate_html()
