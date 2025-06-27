import requests
import os

# ✅ 你自己的 Telegram 配置（已硬编码）
BOT_TOKEN = "8149475252:AAEkYJRGJSQje6w1i57gjPOFhXRiZ2Ghf-0"
CHAT_ID = "5264947511"

def send_telegram_message(message: str, image_path: str = None):
    """
    向 Telegram 发送消息，支持文本和图片
    :param message: 要发送的文本消息
    :param image_path: 可选的本地图片路径（如图表）
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Telegram 配置缺失，无法发送")
        return

    # 发送文本消息
    text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(text_url, data=payload)
        if response.status_code != 200:
            print("❌ 消息发送失败:", response.text)
        else:
            print("✅ 消息已成功发送")
    except Exception as e:
        print("❌ 发送 Telegram 消息出错:", e)

    # 发送图片（如图表）
    if image_path and os.path.exists(image_path):
        photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as image_file:
            files = {"photo": image_file}
            data = {"chat_id": CHAT_ID}
            try:
                photo_response = requests.post(photo_url, data=data, files=files)
                if photo_response.status_code != 200:
                    print("❌ 图片发送失败:", photo_response.text)
                else:
                    print("📷 图像已成功发送")
            except Exception as e:
                print("❌ 发送 Telegram 图片出错:", e)
