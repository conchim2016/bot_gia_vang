import requests
from bs4 import BeautifulSoup
import os

# Lấy thông tin từ GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mess}
    requests.post(url, data=data)

def kiem_tra_gia_vang():
    # Nguồn tygia.vn (SJC) - Nguồn này cực kỳ ổn định cho bot
    url = "https://tygia.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm giá bán ra của SJC
        gia_element = soup.find("td", class_="price-sale")
        
        if gia_element:
            gia_str = gia_element.get_text(strip=True)
            # Chuyển đổi "85.500" -> 85.5
            gia_so = float(gia_str.replace('.', '').replace(',', '.'))
            
            print(f"--- ĐÃ TÌM THẤY GIÁ: {gia_so} triệu ---")

            # NGƯỠNG BÁO: Bạn đặt 200 để nó luôn báo về khi test nhé
            GIA_BAO_DONG = 200.0 

            if gia_so < GIA_BAO_DONG:
                msg = f"💰 CẬP NHẬT GIÁ VÀNG SJC\n-------------------\n👉 Bán ra: {gia_so} triệu/lượng\n📍 Nguồn: tygia.vn"
                gui_telegram(msg)
                print("Gửi Telegram thành công!")
        else:
            print("Lỗi: Không tìm thấy thẻ giá vàng trên web.")
            gui_telegram("Bot kết nối tốt nhưng web đổi giao diện, không lấy được giá!")
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    kiem_tra_gia_vang()
