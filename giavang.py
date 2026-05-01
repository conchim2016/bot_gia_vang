import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def test_bot():
    msg = "🚀 THÀNH CÔNG RỒI! Script đã kết nối được với Telegram của Cường Trần!"
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    r = requests.post(url, data=data)
    print(f"Status: {r.status_code}, Response: {r.text}")

if __name__ == "__main__":
    test_bot()
