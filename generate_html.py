# generate_html.py

import os
from datetime import datetime
import pytz
from generate_data import get_all_analysis

TEMPLATE = open("index_template.html", encoding="utf-8").read()

def main():
    ctx = get_all_analysis()
    ctx["page_update_time"] = datetime.now(pytz.timezone("Asia/Shanghai")) \
        .strftime("%Y-%m-%d %H:%M")
    html = TEMPLATE.format(**ctx)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html generated")

if __name__ == "__main__":
    main()
