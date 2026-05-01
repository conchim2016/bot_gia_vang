import requests
import os

def gui_tin_nhan():
    # Lấy thông tin từ GitHub Secrets
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # ĐỊA CHỈ NÀY LÀ CỐ ĐỊNH, KHÔNG ĐƯỢC THAY ĐỔI
    url = f"https://telegram.org{token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": "🔥 CHÚC MỪNG! Bot đã thực sự thông mạch rồi nhé Cường Trần!"
    }

    try:
        # Gửi tin nhắn
        r = requests.post(url, data=data)
        print(f"Status: {r.status_code}")
        print(f"Ket qua: {r.text}")
    except Exception as e:
        print(f"Loi: {e}")

if __name__ == "__main__":
    gui_tin_nhan()
