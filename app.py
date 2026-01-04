import streamlit as st
import cloudscraper
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
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ ReviewSense")
st.caption("E-Ticaret Yorum Analiz ve Satış Koçu (Cloud v1.1)")

# --- YAN MENÜ ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.divider()
    st.info("ℹ️ Sistem, güvenlik duvarlarını aşmak için 'CloudScraper' kullanmaktadır.")

# --- FONKSİYONLAR ---

def extract_ids_from_url(url):
    try:
        content_id_match = re.search(r'p-(\d+)', url)
        merchant_id_match = re.search(r'merchantId=(\d+)', url)
        c_id = content_id_match.group(1) if content_id_match else None
        m_id = merchant_id_match.group(1) if merchant_id_match else None
        return c_id, m_id
    except:
        return None, None

def get_demo_data():
    return [
        {"userFullName": "Ahmet Y.", "comment": "Ürün fotoğraftaki gibi değil, kumaşı çok parlak ve naylonumsu. Yazın yakar.", "rate": 2},
        {"userFullName": "Mehmet K.", "comment": "Kalıplar aşırı dar arkadaşlar. Normalde L giyiyorum ama XL aldım o bile düğmesi kapanmadı. İade.", "rate": 1},
        {"userFullName": "Selin B.", "comment": "Eşime aldım, duruşu fena değil ama dikiş yerlerinden ipler sarkıyor. Fiyatına göre idare eder.", "rate": 3},
        {"userFullName": "Caner T.", "comment": "Tam bir fiyat performans ürünü. Günlük giymek için ideal, çok şey beklemeyin.", "rate": 5},
        {"userFullName": "Veli D.", "comment": "Paçaları çok kısa geldi. Slim fit tamam ama bu resmen tayt gibi yapışıyor.", "rate": 2}
    ]

def fetch_trendyol_reviews(content_id, merchant_id):
    """CloudScraper kullanarak Trendyol API'sinden veri çeker."""
    url = f"https://public.trendyol.com/discovery-web-socialgw-service/api/review/product/{content_id}/reviews"
    
    params = {
        "merchantId": merchant_id, "storefrontId": "1", "culture": "tr-TR", "order": "5", "page": "0", "size": "30"
    }
    
    # Cloudscraper: Kendini gerçek bir Chrome tarayıcısı gibi tanıtır
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
    
    try:
        response = scraper.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("content", []), "live"
        else:
            print(f"Status Code: {response.status_code}") # Loglara yaz
            return get_demo_data(), "blocked"
            
    except Exception as e:
        print(f"Hata: {e}")
        return get_demo_data(), "error"

def analyze_with_gpt(reviews_text, user_api_key):
    if not user_api_key: return None
    
    # OpenAI isteği için normal requests yeterli (API engellemez)
    import requests 
    try:
        client = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {user_api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Sen uzman bir E-Ticaret danışmanısın. Yorumları analiz et."},
                    {"role": "user", "content": f"Yorumlar:\n{reviews_text}\n\nFormat:\n1. GENEL DUYGU\n2. KRİTİK SORUNLAR\n3. AKSİYON PLANI"}
                ]
            }
        )
        if client.status_code == 200:
            return client.json()['choices'][0]['message']['content']
        else:
            return f"OpenAI Hatası: {client.text}"
    except Exception as e:
        return f"Bağlantı Hatası: {e}"

# --- ANA EKRAN ---

product_url = st.text_input("Trendyol Ürün Linki:", placeholder="https://www.trendyol.com/...")

if st.button("🚀 Analizi Başlat", type="primary"):
    if not product_url:
        st.warning("Lütfen bir link giriniz.")
    else:
        c_id, m_id = extract_ids_from_url(product_url)
        
        if c_id and m_id:
            with st.status("Veri kaynağına bağlanılıyor...", expanded=True) as status:
                st.write("🕵️ CloudScraper ile güvenlik duvarı aşılıyor...")
                reviews, source_type = fetch_trendyol_reviews(c_id, m_id)
                time.sleep(1)
                
                if source_type == "live":
                    st.success(f"✅ {len(reviews)} adet GERÇEK yorum çekildi!")
                    status.update(label="Başarılı!", state="complete", expanded=False)
                else:
                    st.warning(f"⚠️ Trendyol Güvenlik Duvarı çok sıkı! ({source_type})")
                    st.info("🔄 Demo verisi yüklendi (Yatırımcı sunumu modu).")
                    status.update(label="Demo Modu", state="complete", expanded=False)

            if reviews:
                prompt_text = "\n".join([f"- {r.get('comment')} ({r.get('rate')}/5)" for r in reviews])
                
                st.divider()
                st.markdown("### 📊 Analiz Raporu")

                if api_key:
                    with st.spinner("🤖 Yapay Zeka çalışıyor..."):
                        result = analyze_with_gpt(prompt_text, api_key)
                        if result: st.markdown(result)
                else:
                    st.info("💡 **Örnek Rapor (Demo):**")
                    st.markdown("""
                    **1. GENEL DUYGU:** Negatif (%60).
                    **2. KRİTİK SORUNLAR:** Kalıp darlığı, Kumaş kalitesi.
                    **3. AKSİYON PLANI:** 'Dar Kalıp' uyarısı ekleyin.
                    """)
                    with st.expander("GPT'ye gidecek veri"):
                        st.text(prompt_text)
        else:
            st.error("Hatalı Link! 'merchantId' parametresini kontrol edin.")
