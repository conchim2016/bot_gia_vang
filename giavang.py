import requests
from bs4 import BeautifulSoup
import os

# 1. Lấy thông tin từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    # ĐỊA CHỈ PHẢI CÓ CHỮ "api." Ở ĐẦU
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    try:
        r = requests.post(url, data=data)
        print(f"Telegram status: {r.status_code}")
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

def kiem_tra_gia_vang():
    url = "https://sjc.com.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các ô giá trên SJC
        items = soup.find_all('td', class_='txt_center')
        
        if items and len(items) >= 3:
            # Lấy giá bán ra
            gia_str = items[2].get_text(strip=True)
            # Chuyển "85,50" -> 85.5
            gia_so = float(gia_str.replace(',', '.'))
            
            print(f"--- DA TIM THAY GIA: {gia_so} trieu ---")

            # NGƯỠNG BÁO: Đặt 200 để luôn báo về khi test
            GIA_BAO_DONG = 200.0 

            if gia_so < GIA_BAO_DONG:
                msg = f"💰 GIÁ VÀNG SJC HÔM NAY\n-------------------\n👉 Bán ra: {gia_so} triệu/lượng\n📍 Nguồn: SJC.com.vn"
                gui_telegram(msg)
                print("Da gui tin thanh cong!")
        else:
            # Nếu không lấy được giá, gửi tin test để biết đường truyền đã thông
            gui_telegram("✅ Bot đã thông mạch! Nhưng chưa lấy được số giá vàng từ web SJC.")
            
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
