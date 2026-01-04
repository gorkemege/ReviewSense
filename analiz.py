import json

def generate_master_prompt():
    try:
        with open("veri.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        reviews = data.get("content", [])
        
        # 1. Giriş: AI'ya Rol Veriyoruz
        prompt = "Sen uzman bir E-Ticaret Danışmanısın. Aşağıda bir ürün hakkında yapılmış müşteri yorumları var.\n"
        prompt += "Bu yorumları analiz et ve satıcıya cirosunu artırması için net, maddeler halinde, profesyonel bir rapor sun.\n\n"
        
        # 2. Gelişme: Verileri Ekliyoruz
        prompt += "--- MÜŞTERİ YORUMLARI ---\n"
        for r in reviews:
            comment = r.get("comment", "")
            rate = r.get("rate", 0)
            prompt += f"- (Puan: {rate}/5) {comment}\n"
            
        # 3. Sonuç: İstenen Çıktı Formatı
        prompt += "\n--- İSTENEN RAPOR FORMATI ---\n"
        prompt += "1. GENEL DUYGU: (Yüzdesel tahmin ve özet)\n"
        prompt += "2. KRİTİK SORUNLAR: (En çok şikayet edilen 3 konu)\n"
        prompt += "3. AKSİYON PLANI: (Satıcının hemen yapması gereken 3 değişiklik)\n"
        prompt += "4. PAZARLAMA FIRSATI: (Müşterilerin sevdiği ve öne çıkarılması gereken özellik)\n"
        
        print(prompt)
        print("\n" + "="*50)
        print("✅ PROMPT HAZIR! Yukarıdaki metni kopyala ve ChatGPT'ye yapıştır.")
        print("="*50)

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    generate_master_prompt()
