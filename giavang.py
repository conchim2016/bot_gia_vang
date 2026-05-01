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
    # Nguồn SJC chính thống
    url = "https://sjc.com.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm bảng giá, lấy ô giá bán đầu tiên
        gia_element = soup.find("td", class_="txt_center") 
        
        if gia_element:
            # Lấy toàn bộ danh sách các ô giá
            all_prices = soup.find_all("td", class_="txt_center")
            # Thông thường ô giá bán SJC TP.HCM nằm ở vị trí thứ 3 (index 2)
            gia_str = all_prices[2].get_text(strip=True)
            
            # Xử lý chuỗi "85,50" -> 85.5
            gia_so = float(gia_str.replace(',', '.'))
            
            print(f"--- DA TIM THAY GIA: {gia_so} trieu ---")

            # Đặt ngưỡng 200 để chắc chắn nổ tin nhắn ngay lập tức
            GIA_BAO_DONG = 200.0 

            if gia_so < GIA_BAO_DONG:
                msg = f"💰 GIÁ VÀNG SJC HÔM NAY\n-------------------\n👉 Bán ra: {gia_so} triệu/lượng\n📍 Nguồn: SJC.com.vn"
                gui_telegram(msg)
                print("Đã gửi tin thành công!")
        else:
            # Nếu không tìm thấy thẻ cụ thể, gửi tin báo lỗi để bạn biết
            print("Không tìm thấy thẻ giá, đang gửi tin báo lỗi về Telegram...")
            gui_telegram("Bot chạy được nhưng không tìm thấy dữ liệu trên web SJC. Cần kiểm tra lại code!")
            
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
