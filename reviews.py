import requests
import json

# Hedef Ürün Bilgileri
content_id = "1019187502"
merchant_id = "319129"

# DÜZELTME: "public-mdc" yerine "public" kullanıyoruz.
api_url = f"https://public.trendyol.com/discovery-web-socialgw-service/api/review/product/{content_id}/reviews"

# Parametreler
params = {
    "merchantId": merchant_id,
    "storefrontId": "1",
    "culture": "tr-TR",
    "order": "5",
    "page": "0",
    "size": "20"
}

# Header kısmını biraz daha güçlendirdim (Browser gibi görünmek için)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://www.trendyol.com",
    "Referer": "https://www.trendyol.com/"
}

def get_reviews():
    print(f"🚀 API'ye bağlanılıyor: public.trendyol.com...")
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # JSON yapısı bazen değişebilir, güvenli çekelim
            reviews = data.get("content", [])
            
            if not reviews:
                print("⚠️ API cevap verdi ama yorum listesi boş döndü.")
                print("Tam Cevap:", data)
                return

            print(f"✅ HEDEF VURULDU! Toplam {len(reviews)} adet yorum çekildi.\n")
            print("-" * 50)
            
            for review in reviews:
                # Verileri ayıklayalım
                user = review.get("userFullName", "Gizli Kullanıcı")
                comment = review.get("comment", "Yorum metni yok")
                rating = review.get("rate", 0)
                
                # Yıldızları görselleştirelim
                stars = "★" * rating + "☆" * (5 - rating)
                
                print(f"👤 {user}")
                print(f"Puan: {stars} ({rating}/5)")
                print(f"💬 {comment}")
                print("-" * 50)
                
        else:
            print(f"⛔ Hata! Status Code: {response.status_code}")
            print("Mesaj:", response.text)

    except Exception as e:
        print(f"💥 Bağlantı Hatası: {e}")

if __name__ == "__main__":
    get_reviews()
