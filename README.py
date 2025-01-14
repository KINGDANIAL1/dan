import os
import requests
from flask import Flask, request
from threading import Thread

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # عنوان الويب هوك
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)

def send_message(chat_id, text):
    """إرسال رسالة إلى مستخدم Telegram."""
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def increase_views(video_url, views_count):
    """محاكاة زيادة المشاهدات على فيديو YouTube."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        for i in range(views_count):
            response = requests.get(video_url, headers=headers)
            if response.status_code == 200:
                print(f"تمت مشاهدة الفيديو ({i + 1}/{views_count})")
            else:
                print(f"فشل تحميل الفيديو. رمز الحالة: {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ أثناء زيادة المشاهدات: {e}")

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    """معالجة الرسائل الواردة من Telegram."""
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if text.startswith("/start"):
        send_message(chat_id, "مرحبًا! أرسل رابط الفيديو وعدد المشاهدات المطلوبة بصيغة:\n`رابط الفيديو عدد_المشاهدات`")
    elif "youtube.com" in text or "youtu.be" in text:
        try:
            video_url, views_count = text.split()
            views_count = int(views_count)
            
            send_message(chat_id, f"تم بدء زيادة المشاهدات على الفيديو: {video_url}\nالعدد المطلوب: {views_count}")

            # تشغيل العملية في Thread
            Thread(target=increase_views, args=(video_url, views_count)).start()
        except Exception as e:
            send_message(chat_id, f"حدث خطأ: {e}")
    else:
        send_message(chat_id, "صيغة غير صحيحة! أرسل رابط الفيديو وعدد المشاهدات المطلوبة.")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
