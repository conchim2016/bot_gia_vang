import requests
import os

def check():
    # Lấy thông tin từ Secrets
    t = os.getenv('TELEGRAM_TOKEN')
    c = os.getenv('TELEGRAM_CHAT_ID')
    
    # Địa chỉ URL viết liền, không dùng f-string phức tạp để tránh lỗi parse
    url = "https://telegram.org" + str(t) + "/sendMessage"
    
    data = {"chat_id": c, "text": "Test lan cuoi: Neu thay tin nay la thanh cong 100%!"}
    
    try:
        r = requests.post(url, data=data)
        print("Status:", r.status_code)
        print("Phan hoi:", r.text)
    except Exception as e:
        print("Loi:", e)

if __name__ == "__main__":
    check()
