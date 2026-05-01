import requests
from bs4 import BeautifulSoup
import os

# 1. Lấy thông tin bảo mật từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def kiem_tra_gia_vang():
    url = "https://giavang.org"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tìm giá vàng SJC bán ra trên giavang.org
        # Lưu ý: Script đang tìm thẻ <td> có class là "ban-ra"
        gia_element = soup.find("td", class_="ban-ra") 
        
        if gia_element:
            gia_str = gia_element.text.strip()
            # Chuyển đổi định dạng "85.500.000" thành số 85.5
            gia_so = float(gia_str.replace('.', '').replace(',', '.')) / 1000000
            
            # --- BẠN CÀI ĐẶT NGƯỠNG GIÁ MUỐN NHẬN THÔNG BÁO TẠI ĐÂY ---
            GIA_CAO_HON = 165.0  # Ví dụ: Báo khi giá vượt 165 triệu
            GIA_THAP_HON = 170.0  # Ví dụ: Báo khi giá dưới 170 triệu
            # -------------------------------------------------------

            if gia_so >= GIA_CAO_HON:
                thong_bao = f"🚀 GIÁ VÀNG TĂNG CAO: {gia_so} triệu\nLink xem: {url}"
                gui_telegram(thong_bao)
            elif gia_so <= GIA_THAP_HON:
                thong_bao = f"📉 GIÁ VÀNG GIẢM RẺ: {gia_so} triệu\nLink xem: {url}"
                gui_telegram(thong_bao)
            else:
                # Nếu giá nằm ở giữa, chỉ in ra màn hình Log để theo dõi
                print(f"Giá hiện tại là {gia_so} triệu. Chưa đạt ngưỡng báo động.")
        else:
            print("Không tìm thấy dữ liệu giá vàng trên trang web.")
            
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
