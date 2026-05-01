import requests
import os

# Lấy thông tin từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_tin_nhan():
    # Mình viết thẳng api.telegram.org vào đây để tránh lỗi parse
    url = f"https://telegram.org{TOKEN}/sendMessage"
    
    data = {
        "chat_id": CHAT_ID,
        "text": "🎉 THÔNG MẠCH RỒI CƯỜNG ƠI!\nTin nhắn này gửi từ GitHub Actions."
    }

    try:
        r = requests.post(url, data=data)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Loi: {e}")

if __name__ == "__main__":
    gui_tin_nhan()
