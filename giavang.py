import requests
import os
import re

# 1. Lấy thông tin từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    r = requests.post(url, data=data)
    print(f"Telegram status: {r.status_code}")

def kiem_tra_gia_vang():
    # Nguồn dự phòng rất nhẹ và dễ lấy
    url = "https://sjc.com.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        text = response.text
        
        # Tìm tất cả các số có dạng xx,xx (ví dụ 85,50 hoặc 89,00)
        # Đây là định dạng giá vàng trên trang SJC
        prices = re.findall(r'\d{2},\d{2}', text)
        
        if prices:
            # Lấy con số đầu tiên tìm thấy
            gia_str = prices[0]
            gia_so = float(gia_str.replace(',', '.'))
            
            print(f"--- DA TIM THAY GIA: {gia_so} ---")

            # Ngưỡng test: luôn báo tin
            GIA_BAO_DONG = 200.0 

            if gia_so < GIA_BAO_DONG:
                msg = f"💰 GIÁ VÀNG SJC\nBán ra: {gia_so} triệu/lượng\nNguồn: SJC"
                gui_telegram(msg)
        else:
            # Nếu vẫn không thấy số, gửi tin nhắn báo kết nối thông suốt
            print("Không tìm thấy số giá vàng, gửi tin test kết nối...")
            gui_telegram("Bot đã kết nối được GitHub nhưng chưa lấy được số từ Web SJC.")
            
    except Exception as e:
        print(f"Loi: {e}")
        gui_telegram(f"Bot gặp lỗi hệ thống: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
