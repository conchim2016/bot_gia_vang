import requests
from bs4 import BeautifulSoup
import os
import re

# 1. Lấy thông tin bảo mật từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    requests.post(url, data=data)

def kiem_tra_gia_vang():
    url = "https://giavang.org/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8' # Đảm bảo đọc đúng tiếng Việt
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lấy toàn bộ chữ trên trang web
        full_text = soup.get_text()
        
        # Dùng Regex để tìm cụm "Bán ra" kèm con số phía sau
        # Nó sẽ tìm dạng: "Bán ra 85.500" hoặc "Bán ra 165.500"
        match = re.search(r'Bán\s+ra\s*([\d\.,]+)', full_text)
        
        if match:
            gia_chu = match.group(1)
            # Làm sạch số: bỏ dấu chấm/phẩy thừa
            gia_sach = gia_chu.replace('.', '').replace(',', '')
            # Chuyển về đơn vị triệu (VD: 165500 -> 165.5 triệu)
            gia_so = float(gia_sach) / 1000
            
            print(f"--- DA TIM THAY GIA: {gia_so} trieu ---")

            # NGƯỠNG BÁO ĐỘNG (Bạn sửa 2 số này theo ý mình)
            GIA_BAO_DONG_TEST = 200.0 

            if gia_so < GIA_BAO_DONG_TEST:
                msg = f"🔔 Cập nhật giá vàng: {gia_so} triệu\nNguồn: {url}"
                gui_telegram(msg)
                print("Da gui tin nhan!")
        else:
            print("LỖI: Khong tìm thay chu 'Ban ra' tren trang web.")
            
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
