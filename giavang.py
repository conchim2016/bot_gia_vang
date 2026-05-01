import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def gui_telegram(mess):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mess})

def kiem_tra():
    url = "https://tygia.vn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Tìm tất cả các thẻ <td> để lấy giá
        cells = soup.find_all('td')
        gia_so = 0
        
        for cell in cells:
            text = cell.get_text(strip=True)
            # Nếu thấy chuỗi có dạng "85.000" hoặc tương tự
            if "." in text and text.replace(".", "").isdigit():
                gia_so = float(text.replace(".", "")) / 1000
                break
        
        if gia_so > 0:
            print(f"Gia tim thay: {gia_so}")
            msg = f"💰 GIÁ VÀNG SJC: {gia_so} triệu/lượng\n📍 Nguồn: tygia.vn"
            gui_telegram(msg)
        else:
            gui_telegram("Bot chạy được nhưng không tìm thấy con số giá vàng.")
            
    except Exception as e:
        print(f"Loi: {e}")

if __name__ == "__main__":
    kiem_tra()
