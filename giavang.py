import requests
from bs4 import BeautifulSoup
import os

# 1. Lấy thông tin bảo mật từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    requests.post(url, data=data)

def kiem_tra_gia_vang():
    url = "https://giavang.org"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cách tìm mới: Tìm tất cả các ô có class 'ban-ra'
        gia_elements = soup.find_all("td", class_="ban-ra")
        
        if gia_elements:
            # Lấy ô đầu tiên (thường là giá SJC)
            gia_str = gia_elements[0].get_text(strip=True)
            
            # Xử lý chuỗi: xóa dấu chấm, đổi dấu phẩy thành chấm để chuyển sang số
            # Ví dụ: "85.000.000" -> "85000000" -> 85.0
            gia_so = float(gia_str.replace('.', '').replace(',', '.')) / 1000000
            
            print(f"--- DA TIM THAY GIA: {gia_so} trieu ---")

            # Cài đặt ngưỡng để test (Bạn có thể sửa lại sau)
            GIA_BAO_DONG = 100.0 # Để số cao hẳn để test gửi tin nhắn

            if gia_so < GIA_BAO_DONG:
                thong_bao = f"📉 Cập nhật giá vàng: {gia_so} triệu\nLink: {url}"
                gui_telegram(thong_bao)
                print("Da gui tin nhan qua Telegram!")
            else:
                print("Chua dat nguong bao dong.")
        else:
            print("LỖI: Khong tìm thay the <td class='ban-ra'>. Web có the da doi giao dien.")
            
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()

