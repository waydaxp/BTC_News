from generate_data import get_all_analysis
from jinja2 import Template

def main():
    ctx = get_all_analysis()
    tpl = open("index_template.html", "r", encoding="utf-8").read()
    template = Template(tpl)
    html = template.render(ctx=ctx)  # 将 ctx 作为整体传入模板中
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 已更新")

if __name__ == "__main__":
    main()
