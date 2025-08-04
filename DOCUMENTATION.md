# 📚 MÜLAKAT SORU HAZIRLAMASI SİSTEMİ - DOKÜMANTASYON REHBERİ

## 🎯 GENEL BAKIŞ

Bu dokümantasyon, sistemdeki her dosyanın amacını, kapsamını ve teknik detaylarını açıklamaktadır.

## 📁 DOSYA STRUKTüRÜ VE DOKÜMANTASYON

### 🖥️ BACKEND (Python/FastAPI)

#### 📄 `backend/app/main.py`
- **Amaç**: Ana API endpoint'leri ve iş mantığı
- **Kapsam**: 37 API endpoint, CORS konfigürasyonu, routing
- **Giriş**: HTTP istekleri, JSON veriler
- **Çıkış**: JSON yanıtları, Word/ZIP dosyaları
- **Satır Sayısı**: 1,370 satır

#### 🔧 `backend/app/utils.py`  
- **Amaç**: AI entegrasyonu ve yardımcı fonksiyonlar
- **Kapsam**: OpenAI API, soru üretimi, JSON parse, zorluk sistemi
- **Giriş**: İlan verileri, rol konfigürasyonları
- **Çıkış**: Üretilmiş sorular ve cevap anahtarları
- **Satır Sayısı**: 550 satır

#### 🗄️ `backend/app/models.py`
- **Amaç**: Veritabanı modelleri ve ilişkiler
- **Kapsam**: 9 SQLAlchemy modeli, property'ler, ilişkiler
- **Giriş**: ORM sorgular
- **Çıkış**: Database nesneleri
- **Satır Sayısı**: 294 satır

#### 🔗 `backend/app/database.py`
- **Amaç**: Veritabanı bağlantı yönetimi
- **Kapsam**: SQLAlchemy engine, session factory, dependency injection
- **Giriş**: Environment değişkenleri
- **Çıkış**: Database session'ları
- **Satır Sayısı**: 64 satır

#### 📦 `backend/requirements.txt`
- **Amaç**: Python paket bağımlılıkları
- **Kapsam**: 8 ana paket ve versiyonları
- **Kategoriler**: Web framework, AI, Database, Dosya işleme

### 🌐 FRONTEND (React.js)

#### ⚛️ `frontend/src/components/Step2.jsx`
- **Amaç**: Rol/pozisyon yönetimi arayüzü
- **Kapsam**: CRUD işlemleri, form validation, state yönetimi
- **Giriş**: Contract ID, user interactions
- **Çıkış**: Kaydedilmiş rol verileri
- **Satır Sayısı**: 409 satır

## 🔧 TEKNİK MİMARİ

### Backend Stack:
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite + SQLAlchemy ORM
- **AI**: OpenAI GPT-4o-mini
- **File Processing**: python-docx
- **Server**: Uvicorn ASGI

### Frontend Stack:
- **Framework**: React.js
- **State Management**: useState/useEffect hooks
- **HTTP Client**: Axios
- **UI**: Custom CSS + Bootstrap-like styling

## 📊 VERİ AKIŞ DİYAGRAMI

```
👤 USER INPUT → 🌐 FRONTEND → 📡 API CALLS → 🖥️ BACKEND → 🗄️ DATABASE
                                                ↓
🤖 OPENAI API ← 🔧 UTILS.PY ← 📊 BUSINESS LOGIC ← 📄 MAIN.PY
                                                ↓
📄 WORD FILES ← 📁 FILE GENERATION ← 💾 GENERATED QUESTIONS
```

## 🚀 KURULUM VE ÇALIŞTIRMA

### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m app.main
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 📝 DOKÜMANTASYON STANDARTları

Her dosyada aşağıdaki bölümler bulunur:
- 📋 **DOSYA AMACI**: Ne işe yarar?
- 🎯 **KAPSAM**: Hangi özellikler?
- 📊 **VERİ AKIŞI**: Girdi/çıktı nedir?
- 🔧 **TEKNİK BİLGİLER**: Kullanılan teknolojiler
- ⚙️ **FONKSİYONLAR**: Ana fonksiyon listesi
- 👨‍💻 **GELIŞTIREN**: Proje bilgileri

## 🔒 GÜVENLİK NOTALARI

- OpenAI API anahtarı environment değişkeninde saklanmalı
- Production'da CORS ayarları gözden geçirilmeli
- Database bağlantıları SSL ile korunmalı
- File upload boyut limitleri kontrol edilmeli

## 📞 DESTEK

Teknik sorularınız için dokümantasyonları inceleyiniz. Her dosyanın başında detaylı açıklamalar mevcuttur.

---
👨‍💻 **Geliştiren**: AI Destekli Geliştirme  
📅 **Tarih**: 2025  
🔄 **Versiyon**: 1.0.0