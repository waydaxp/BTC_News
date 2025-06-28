# generate_html.py
from generate_data import get_all_analysis
from datetime import datetime, timedelta

data = get_all_analysis()

with open("index_template.html", encoding="utf-8") as f:
    tpl = f.read()

html = tpl.format(**data)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html 已生成 ——", data["update_time"])
