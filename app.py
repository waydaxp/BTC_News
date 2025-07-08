#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, send_from_directory, jsonify
import os

# 如果你后面还有 API 需要保留，可以在这里 import
# from generate_data import get_all_analysis

app = Flask(
    __name__,
    static_folder='.',       # 静态文件根目录设为当前目录
    static_url_path=''       # 根路径 '' 对应 static_folder
)

# 首页：直接返回静态生成的 index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# 示例：如果你还想保留一个 /api/analysis 接口
# @app.route('/api/analysis')
# def api_analysis():
#     ctx = get_all_analysis()
#     return jsonify(ctx)

if __name__ == '__main__':
    # 本地调试时用
    app.run(debug=True, host='0.0.0.0', port=5000)
