# 文件：generate_html.py
import json
from jinja2 import Template

TEMPLATE_FILE = "index_template.html"
OUTPUT_FILE = "index.html"

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template = Template(f.read())

html_output = template.render(
    btc=data.get("btc", "暂无数据"),
    eth=data.get("eth", "暂无数据"),
    events=data.get("events", "暂无数据"),
    sentiment=data.get("sentiment", {}).get("text", "暂无"),
    updated_at=data.get("updated_at", "未知时间")
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ HTML 页面已更新: {OUTPUT_FILE}")
