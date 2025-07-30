# Sözleşmeli Personel Alımı – Mülakat Sorusu Hazırlama Sistemi

Bu proje, Coğrafi Bilgi Sistemleri Genel Müdürlüğü bünyesinde sözleşmeli bilişim personeli alımı süreçlerinde kullanılmak üzere geliştirilmiş bir mülakat sorusu hazırlama sistemidir.

## 📋 Proje Hakkında

Sistem, yapay zeka destekli olarak mülakat soruları üretmekte ve bu soruları düzenlenebilir Word dosyaları halinde çıktı almaktadır. Pozisyon, seviye ve uzmanlık alanı kriterlerine göre özelleştirilmiş sorular üretilmektedir.

## 🚀 Özellikler

### **Ana Özellikler:**
- ✅ **Adım Adım Soru Üretimi**: 5 aşamalı süreç
- ✅ **Rol Bazlı Konfigürasyon**: Her pozisyon için özel ayarlar
- ✅ **Yapay Zeka Destekli**: OpenAI GPT-4o-mini entegrasyonu
- ✅ **Beklenen Cevaplar**: Her soru için jüri bilgilendirme metinleri
- ✅ **Tekil Soru Düzenleme**: Her soruyu ayrı ayrı düzenleme imkanı
- ✅ **Word Dosyası Üretimi**: Aday ve jüri için ayrı kitapçıklar
- ✅ **Markdown Kod Bloğu**: Teknik sorularda kod örnekleri

### **Teknik Özellikler:**
- **Frontend**: React + Vite
- **Backend**: FastAPI + SQLAlchemy
- **Veritabanı**: SQLite
- **AI Model**: OpenAI GPT-4o-mini
- **Dokümantasyon**: python-docx

## 📦 Kurulum

### **Gereksinimler:**
- Python 3.8+
- Node.js 16+
- npm veya yarn

### **Backend Kurulumu:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy openai python-docx
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend Kurulumu:**
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Kullanım

### **1. Adım: İlan Bilgileri**
- İlan başlığı ve genel şartları girin
- Sistem otomatik olarak contract ID oluşturur

### **2. Adım: Rol Tanımları**
- Pozisyon adı ve maaş katsayısı belirleyin
- Özel şartları ve pozisyon sayısını girin
- Her rol için ayrı konfigürasyon yapın

### **3. Adım: Soru Konfigürasyonu**
- Her rol için soru tiplerini seçin
- Soru sayılarını belirleyin
- Toplam soru sayısını kontrol edin

### **4. Adım: Soru Üretimi**
- "Soruları Üret" butonuna tıklayın
- Her soru için "Düzenle" butonu ile düzenleme yapın
- Beklenen cevaplar otomatik üretilir

### **5. Adım: Word Dosyası İndirme**
- Her rol için ayrı Word dosyaları indirin
- Aday kitapçıkları (S1, S2, S3...)
- Jüri kitapçıkları (C1, C2, C3...)

## 🔧 Teknik Mimari

### **Frontend (React):**
- **Ana Bileşen**: `App.jsx` - Step yönetimi
- **Step Bileşenleri**: `Step1.jsx`, `Step2.jsx`, `Step3.jsx`, `Step4.jsx`, `Step5.jsx`
- **Stil**: CSS modülleri ve responsive tasarım
- **State Yönetimi**: React hooks (useState, useEffect)

### **Backend (FastAPI):**
- **Ana Uygulama**: `main.py` - API endpoint'leri
- **Veritabanı**: `models.py` - SQLAlchemy modelleri
- **AI Entegrasyonu**: `utils.py` - OpenAI API
- **Dokümantasyon**: Word dosyası üretimi

### **Veritabanı Şeması:**
- **Contract**: İlan bilgileri
- **Role**: Pozisyon tanımları
- **RoleQuestionConfig**: Soru konfigürasyonları
- **Question**: Üretilen sorular

## 📁 Proje Yapısı

```
mulakat_soru/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Step1.jsx
│   │   │   ├── Step2.jsx
│   │   │   ├── Step3.jsx
│   │   │   ├── Step4.jsx
│   │   │   └── Step5.jsx
│   │   ├── App.jsx
│   │   └── App.css
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── utils.py
│   │   └── database.py
│   └── requirements.txt
└── README.md
```

## 🔐 API Key Konfigürasyonu

OpenAI API key'ini `backend/app/utils.py` dosyasında güncelleyin:

```python
client = OpenAI(
    api_key="your-api-key-here",
    timeout=60.0,
    max_retries=3
)
```

## 🚀 Deployment

### **Production Kurulumu:**
1. Backend'i gunicorn ile çalıştırın
2. Frontend'i build edin
3. Nginx ile reverse proxy yapın
4. SSL sertifikası ekleyin

### **Docker Kurulumu:**
```bash
docker-compose up -d
```

## 📞 İletişim

**Ahmet Erdem Yeniay**  
Coğrafi Bilgi Sistemleri Genel Müdürlüğü  
Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı  
Yapay Zeka Teknolojileri Şube Müdürlüğü  
ahmeterdem.yeniay@csb.gov.tr

## 📄 Lisans

Bu proje **Coğrafi Bilgi Sistemleri Genel Müdürlüğü - Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı** için geliştirilmiştir.

---

**Geliştirme Tarihi**: 2024  
**Versiyon**: 1.0.0  
**Durum**: Aktif Geliştirme 