import requests
from bs4 import BeautifulSoup
import os

# 1. Lấy thông tin từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    requests.post(url, data=data)

def kiem_tra_gia_vang():
    # Nguồn này dữ liệu rất sạch, khó lỗi
    url = "https://sjc.com.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm bảng giá SJC
        # Chúng ta sẽ tìm tất cả các thẻ <td> có class là 'txt_center'
        items = soup.find_all('td', class_='txt_center')
        
        if len(items) >= 3:
            # Vị trí số 3 (index 2) thường là giá Bán ra của SJC TP.HCM
            gia_str = items[2].get_text(strip=True) 
            
            # Chuyển đổi "85,50" -> 85.5
            gia_so = float(gia_str.replace(',', '.'))
            
            print(f"--- DA TIM THAY GIA SJC: {gia_so} ---")

            # Đặt ngưỡng 200 để chắc chắn nó sẽ gửi tin nhắn báo về máy bạn ngay
            GIA_BAO_DONG = 200.0 

            if gia_so < GIA_BAO_DONG:
                msg = f"🔔 SJC CẬP NHẬT: {gia_so} triệu/lượng\nNguồn: SJC.com.vn"
                gui_telegram(msg)
                print("Da gui tin nhan thanh cong!")
        else:
            print("Lỗi: Cấu trúc bảng giá đã thay đổi.")
            
    except Exception as e:
        print(f"Loi: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
