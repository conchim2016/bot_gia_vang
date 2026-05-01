import requests
import os

# Lấy Token và ID từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def test_bot():
    # ĐỊA CHỈ URL PHẢI CÓ CHỮ "api." Ở ĐẦU
    url = f"https://telegram.org{TOKEN}/sendMessage"
    
    msg = "🚀 CHÚC MỪNG CƯỜNG TRẦN!\nBot đã thông mạch và gửi tin nhắn thành công rồi nhé!"
    
    data = {"chat_id": CHAT_ID, "text": msg}
    
    try:
        r = requests.post(url, data=data)
        # In ra để kiểm tra trong Log
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    test_bot()
