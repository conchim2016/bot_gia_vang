import requests
from bs4 import BeautifulSoup
import os

# 1. Lấy thông tin từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    try:
        r = requests.post(url, data=data)
        print(f"Telegram status: {r.status_code}")
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

def kiem_tra_gia_vang():
    # Sử dụng nguồn tygia.vn vì nó rất nhẹ
    url = "https://tygia.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm giá bán ra
        gia_element = soup.find("td", class_="price-sale")
        
        if gia_element:
            gia_so = gia_element.get_text(strip=True)
            msg = f"✅ KẾT NỐI THÀNH CÔNG!\n💰 Giá vàng SJC: {gia_so} triệu\n📍 Nguồn: tygia.vn"
            gui_telegram(msg)
            print(f"Đã tìm thấy giá {gia_so} và gửi tin nhắn.")
        else:
            # NẾU KHÔNG TÌM THẤY GIÁ, VẪN GỬI TIN NHẮN BÁO LỖI ĐỂ KIỂM TRA KẾT NỐI
            print("Không tìm thấy dữ liệu trên web.")
            gui_telegram("🔔 THÔNG BÁO: Bot đã chạy thành công trên GitHub nhưng chưa lấy được số giá vàng. Đường truyền Telegram đã CHUẨN 100% rồi nhé Cường!")
            
    except Exception as e:
        error_msg = f"Lỗi hệ thống: {e}"
        print(error_msg)
        gui_telegram(f"Bot gặp lỗi: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
