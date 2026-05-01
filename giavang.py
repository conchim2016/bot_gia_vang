import requests
from bs4 import BeautifulSoup
import os
import sys

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
    # Nguồn tygia.vn rất ổn định và dễ lấy số
    url = "https://tygia.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm giá SJC bán ra (thường nằm trong thẻ td có class 'price-sale')
        gia_element = soup.find("td", class_="price-sale")
        
        if gia_element:
            gia_str = gia_element.get_text(strip=True)
            # Chuyển đổi định dạng "85.500" -> 85.5
            gia_so = float(gia_str.replace('.', '').replace(',', '.'))
            
            print(f"--- TIM THAY GIA: {gia_so} trieu ---")

            # NGƯỠNG BÁO: Đặt số cao để test nổ tin nhắn ngay lập tức
            GIA_BAO_DONG = 200.0 

            if gia_so < GIA_BAO_DONG:
                msg = f"🔔 CẬP NHẬT GIÁ VÀNG\n💰 Giá bán: {gia_so} triệu/lượng\n📍 Nguồn: tygia.vn"
                gui_telegram(msg)
                print("Đã gửi tin thành công!")
        else:
            print("Lỗi: Không tìm thấy thẻ chứa giá vàng trên web.")
            
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
