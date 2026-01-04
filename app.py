import streamlit as st
import requests
import json
import re
import time

# --- AYARLAR VE TASARIM ---
st.set_page_config(page_title="ReviewSense | AI Analiz", page_icon="🛍️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1 { color: #FF4B4B; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold;}
    .reportview-container .main .block-container{ padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ ReviewSense")
st.caption("E-Ticaret Yorum Analiz ve Satış Koçu (MVP v1.0)")

# --- YAN MENÜ (API KEY) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    st.markdown("Analizin çalışması için OpenAI anahtarı gereklidir.")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    st.divider()
    st.info("ℹ️ Not: İnternet kısıtlaması algılanırsa sistem otomatik olarak 'Demo Verisi' ile çalışır.")

# --- FONKSİYONLAR ---

def extract_ids_from_url(url):
    """Linkin içinden Content ID ve Merchant ID'yi bulur."""
    try:
        content_id_match = re.search(r'p-(\d+)', url)
        merchant_id_match = re.search(r'merchantId=(\d+)', url)
        
        c_id = content_id_match.group(1) if content_id_match else None
        m_id = merchant_id_match.group(1) if merchant_id_match else None
        return c_id, m_id
    except:
        return None, None

def get_demo_data():
    """Bağlantı hatası durumunda devreye giren kurtarıcı veri."""
    return [
        {"userFullName": "Ahmet Y.", "comment": "Ürün fotoğraftaki gibi değil, kumaşı çok parlak ve naylonumsu. Yazın yakar.", "rate": 2},
        {"userFullName": "Mehmet K.", "comment": "Kalıplar aşırı dar arkadaşlar. Normalde L giyiyorum ama XL aldım o bile düğmesi kapanmadı. İade.", "rate": 1},
        {"userFullName": "Selin B.", "comment": "Eşime aldım, duruşu fena değil ama dikiş yerlerinden ipler sarkıyor. Fiyatına göre idare eder.", "rate": 3},
        {"userFullName": "Caner T.", "comment": "Tam bir fiyat performans ürünü. Günlük giymek için ideal, çok şey beklemeyin.", "rate": 5},
        {"userFullName": "Veli D.", "comment": "Paçaları çok kısa geldi. Slim fit tamam ama bu resmen tayt gibi yapışıyor.", "rate": 2}
    ]

def fetch_trendyol_reviews(content_id, merchant_id):
    """Trendyol API'sinden gerçek yorumları çeker (Hata korumalı)."""
    url = f"https://public.trendyol.com/discovery-web-socialgw-service/api/review/product/{content_id}/reviews"
    
    params = {
        "merchantId": merchant_id, "storefrontId": "1", "culture": "tr-TR", "order": "5", "page": "0", "size": "30"
    }
    
    headers = {
         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5) # 5 saniye bekle
        if response.status_code == 200:
            data = response.json()
            return data.get("content", []), "live" # Başarılı (Canlı Veri)
        else:
            return get_demo_data(), "demo" # API reddetti (Demo)
            
    except Exception as e:
        # DNS veya Bağlantı hatası olursa buraya düşer
        return get_demo_data(), "error" # Hata oluştu (Demo + Uyarı)

def analyze_with_gpt(reviews_text, user_api_key):
    """Yorumları OpenAI GPT-4'e gönderir."""
    if not user_api_key:
        return None # Key yoksa analiz yapma
    
    try:
        client = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {user_api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Sen uzman bir E-Ticaret danışmanısın. Yorumları analiz edip satıcıya aksiyon planı sun. Markdown formatında yaz."},
                    {"role": "user", "content": f"Aşağıdaki yorumları analiz et:\n\n{reviews_text}\n\nÇıktı Formatı:\n1. GENEL DUYGU\n2. KRİTİK SORUNLAR\n3. AKSİYON PLANI"}
                ]
            }
        )
        if client.status_code == 200:
            return client.json()['choices'][0]['message']['content']
        else:
            return f"OpenAI Hatası: {client.text}"
    except Exception as e:
        return f"Bağlantı Hatası: {e}"

# --- ANA EKRAN AKIŞI ---

product_url = st.text_input("Trendyol Ürün Linki:", placeholder="https://www.trendyol.com/...")

if st.button("🚀 Analizi Başlat", type="primary"):
    if not product_url:
        st.warning("Lütfen bir link giriniz.")
    else:
        # 1. ID'leri Çöz
        c_id, m_id = extract_ids_from_url(product_url)
        
        if c_id and m_id:
            # 2. Yorumları Çek (Hata korumalı fonksiyon)
            with st.status("Veri kaynağına bağlanılıyor...", expanded=True) as status:
                st.write("🕵️ Trendyol API kontrol ediliyor...")
                reviews, source_type = fetch_trendyol_reviews(c_id, m_id)
                
                time.sleep(1)
                
                if source_type == "live":
                    st.write(f"✅ {len(reviews)} adet güncel yorum çekildi.")
                    status.update(label="Bağlantı Başarılı!", state="complete", expanded=False)
                elif source_type == "error":
                    st.warning("⚠️ DNS/Ağ engeli algılandı. Sistem 'Simülasyon Modu'na geçti.")
                    st.write(f"🔄 Demo verisi ({len(reviews)} yorum) yüklendi.")
                    status.update(label="Demo Modu Aktif", state="complete", expanded=False)
                else:
                    st.write("⚠️ Veri çekilemedi, demo gösteriliyor.")
                    status.update(label="Demo Modu", state="complete", expanded=False)

            # 3. Analiz Aşaması
            if reviews:
                prompt_text = ""
                for r in reviews:
                    prompt_text += f"- {r.get('comment')} (Puan: {r.get('rate')})\n"
                
                st.divider()
                st.markdown("### 📊 Analiz Raporu")

                if api_key:
                    with st.spinner("🤖 Yapay Zeka raporu yazıyor..."):
                        result = analyze_with_gpt(prompt_text, api_key)
                        if result:
                            st.markdown(result)
                            st.balloons()
                else:
                    # API Key Yoksa
                    st.info("💡 **Yönetici Özeti (Demo):**")
                    st.markdown("""
                    **1. GENEL DUYGU:** Negatif (%60). Müşteriler kalıp darlığından şikayetçi.
                    
                    **2. KRİTİK SORUNLAR:**
                    * Beden uyumsuzluğu (L beden S gibi).
                    * Kumaşın naylonumsu olması.
                    
                    **3. AKSİYON PLANI:**
                    * Açıklamaya 'Dar Kalıp' uyarısı ekleyin.
                    * Kumaş detay fotosu yükleyin.
                    """)
                    
                    st.warning("⚠️ Bu bir demo özettir. Gerçek AI analizi için sol menüden OpenAI API Key giriniz.")
                    with st.expander("GPT'ye Gönderilecek Ham Veriyi Gör"):
                        st.text(prompt_text)

        else:
            st.error("Link formatı hatalı! Linkin içinde 'merchantId' olduğundan emin olun.")
