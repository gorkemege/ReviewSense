import requests
from bs4 import BeautifulSoup
import time
import random

# Hedef Ürün (Senin attığın link)
url = "https://www.trendyol.com/hello7/slim-fit-kumas-gunluk-erkek-pantolon-tarz-sahibi-rahat-kesim-p-1019187502?boutiqueId=61&merchantId=319129"

def fetch_product_data(target_url):
    print("🕵️  Trendyol'a bağlanılıyor...")
    
    # Kendimizi gerçek bir tarayıcı gibi tanıtıyoruz (User-Agent Spoofing)
    # Bunu yapmazsak Trendyol bizi bot sanıp engeller.
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        response = requests.get(target_url, headers=headers)
        
        if response.status_code == 200:
            print("✅ Bağlantı Başarılı! (Status: 200)")
            
            # HTML içeriğini ayrıştır
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Ürün Başlığını Bulmaya Çalışalım (Genelde h1 etiketindedir)
            product_name = soup.find("h1", class_="pr-new-br")
            
            if product_name:
                 print(f"🎯 Ürün Bulundu: {product_name.get_text(strip=True)}")
            else:
                 # Trendyol bazen class isimlerini değiştirir veya h1 kullanır.
                 # Alternatif bir yakalama deneyelim
                 alternative_name = soup.find("h1")
                 if alternative_name:
                     print(f"🎯 Ürün Bulundu: {alternative_name.get_text(strip=True)}")
                 else:
                     print("⚠️ Ürün başlığı çekilemedi (HTML yapısı değişmiş olabilir).")
            
            # Burası kritik: Yorumlar genellikle JavaScript ile sonradan yüklenir.
            # İlk aşamada sadece sayfanın HTML'ini alabildik mi ona bakıyoruz.
            print(f"📄 İndirilen Sayfa Boyutu: {len(response.content)} byte")
            
        else:
            print(f"⛔ Erişim Reddedildi! Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Bir hata oluştu: {e}")

# Kodu Çalıştır
if __name__ == "__main__":
    fetch_product_data(url)
