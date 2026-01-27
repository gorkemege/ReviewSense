# 🛍️ ReviewSense: AI-Powered E-Commerce Assistant

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**ReviewSense** is a SaaS (Software as a Service) MVP designed to help e-commerce sellers understand their customers without reading thousands of comments. It uses **OpenAI (GPT-4o)** to analyze product reviews and generates actionable business insights to reduce return rates and increase sales.

---

## 🚀 Key Features

* **🧠 AI-Driven Analysis:** Automatically summarizes hundreds of reviews into a clear executive report.
* **📊 Sentiment Analysis:** Determines the overall emotional tone of the customers (Positive/Negative/Neutral).
* **💡 Actionable Insights:** Provides a concrete "Action Plan" for sellers (e.g., *"Update size chart," "Improve packaging"*).
* **🛡️ Hybrid Data Mode:**
    * **Manual Mode (Guaranteed):** Paste reviews directly to get instant analysis (Bypasses all WAF/Firewalls).
    * **Auto-Link Mode (Beta):** Attempts to scrape data directly from product links (Includes Demo Mode for restricted networks).
* **⚡ Real-time Processing:** Built with Streamlit for a fast and interactive web interface.

---

## 📸 Screenshots

<img width="1465" height="758" alt="Ekran Resmi 2026-01-27 05 58 21" src="https://github.com/user-attachments/assets/fb4fbafa-26d3-494d-958b-3ae184cba0fb" />

<img width="1171" height="751" alt="Ekran Resmi 2026-01-27 06 00 00" src="https://github.com/user-attachments/assets/63c892f8-6477-4ca9-9e87-d2c0858bbe9d" />

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Backend Logic:** Python 3.9+
* **AI Engine:** OpenAI API (GPT-4o / GPT-3.5)
* **Data Collection:** `BeautifulSoup4` & `CloudScraper` (for WAF bypassing)

---

## 📦 Installation & Local Setup

Clone the repository and run the application on your local machine.

### 1. Clone the Repo

git clone [https://github.com/YOUR_USERNAME/ReviewSense.git](https://github.com/YOUR_USERNAME/ReviewSense.git)
cd ReviewSense

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Run the App

streamlit run app.py

### 4. Enter API Key

The application requires an OpenAI API Key to perform the analysis. You can enter this securely in the sidebar of the application.

### 📖 How to Use

1. ### Launch the App: Open the link provided by Streamlit (or localhost).

2. ### Select Mode:
   
  - Manual Paste: Copy reviews from any marketplace (Trendyol, Amazon, etc.) and paste them into the text area.
  - Link Mode: Paste a product URL (Currently supports Trendyol).

3. ### Analyze: Click the "Analyze" button.

4. ### Get Results: Read the AI-generated report containing:
  - General Sentiment Score
  - Top 3 Critical Issues (Pain Points)
  - Seller Action Plan

### 🗺️ Roadmap
[x] MVP Release (Streamlit Web App)

[x] OpenAI Integration

[x] Manual Input Mode (Fail-safe)

[ ] Pro: Export Reports as PDF/Excel

[ ] Pro: Competitor Comparison Analysis

[ ] Enterprise: Shopify & WooCommerce Plugins

### 👨‍💻 Developer
Developed by [Görkem Ege Zor]
