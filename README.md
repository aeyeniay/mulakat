# Mülakat Soru Hazırlama Sistemi

Coğrafi Bilgi Sistemleri Genel Müdürlüğü için geliştirilmiş, yapay zeka destekli mülakat soru hazırlama sistemi.

## 🚀 Özellikler

- **5 Adımlı Wizard Arayüzü**: Kullanıcı dostu, adım adım soru hazırlama süreci
- **Yapay Zeka Destekli Soru Üretimi**: OpenAI GPT-4o-mini API ile kaliteli sorular
- **Profesyonel Rubrik Modeli**: 5 katmanlı zorluk seviyesi sistemi (K1-K5)
- **Word Dosyası İndirme**: Profesyonel formatlı mülakat soruları
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu arayüz

## 📋 Sistem Gereksinimleri

- Python 3.8+
- Node.js 16+
- PostgreSQL (opsiyonel, SQLite varsayılan)
- OpenAI API Key

## 🛠️ Kurulum

### Backend Kurulumu

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Kurulumu

```bash
cd frontend
npm install
npm run dev
```

## 🔧 Konfigürasyon

### OpenAI API Key

`backend/app/utils.py` dosyasında API key'i güncelleyin:

```python
client = OpenAI(
    api_key="your-openai-api-key-here",
    timeout=60.0,
    max_retries=3
)
```

## 📖 Kullanım

### 1. İlan Bilgileri
- İlan başlığı ve içeriğini girin
- Genel şartları belirtin

### 2. Rol Tanımları
- Pozisyon adlarını ekleyin
- Maaş katsayılarını belirleyin (2x, 3x, 4x)
- Özel gereksinimleri tanımlayın

### 3. Soru Konfigürasyonu
- Her rol için soru sayılarını ayarlayın
- Soru kategorilerini yapılandırın

### 4. Soru Üretimi
- Yapay zeka ile soruları üretin
- Sonuçları önizleyin

### 5. Final Seti
- Word dosyası olarak indirin
- Mülakat sürecinde kullanın

## 🎯 Zorluk Seviyeleri

### 2x - Orta Düzey Uygulayıcı
- **Deneyim**: 2-4 yıl
- **Odak**: Günlük operasyon, temel optimizasyon
- **Katman Dağılımı**: K1: 30%, K2: 40%, K3: 25%, K4: 5%, K5: 0%

### 3x - Kıdemli Uzman
- **Deneyim**: 5-8 yıl
- **Odak**: Çapraz disiplin, mentorluk, kritik problem çözümü
- **Katman Dağılımı**: K1: 15%, K2: 25%, K3: 35%, K4: 20%, K5: 5%

### 4x - Mimar/Teknik Lider
- **Deneyim**: ≥10 yıl
- **Odak**: Strateji, büyük ölçekli mimari, ekip yönetimi
- **Katman Dağılımı**: K1: 5%, K2: 15%, K3: 25%, K4: 35%, K5: 20%

## 🏗️ Teknik Mimari

### Backend (FastAPI)
- **Framework**: FastAPI
- **Veritabanı**: SQLAlchemy + SQLite
- **AI**: OpenAI GPT-4o-mini
- **Dosya İşleme**: python-docx

### Frontend (React)
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: CSS3
- **HTTP Client**: Axios

## 📁 Proje Yapısı

```
mulakat_soru/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI uygulaması
│   │   ├── models.py        # Veritabanı modelleri
│   │   ├── utils.py         # AI ve yardımcı fonksiyonlar
│   │   └── database.py      # Veritabanı bağlantısı
│   ├── requirements.txt     # Python bağımlılıkları
│   └── venv/               # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/      # React bileşenleri
│   │   ├── assets/         # Resimler ve statik dosyalar
│   │   ├── App.jsx         # Ana uygulama
│   │   └── App.css         # Stiller
│   ├── public/             # Statik dosyalar
│   ├── package.json        # Node.js bağımlılıkları
│   └── vite.config.js      # Vite konfigürasyonu
└── README.md
```

## 🔒 Güvenlik

- API key'ler environment variable olarak saklanmalı
- CORS ayarları production için yapılandırılmalı
- Rate limiting eklenebilir

## 🚀 Deployment

### Backend (Production)
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (Production)
```bash
npm run build
# dist/ klasörünü web sunucusuna deploy edin
```

## 📝 Lisans

Bu proje Coğrafi Bilgi Sistemleri Genel Müdürlüğü için geliştirilmiştir.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Proje Sahibi: [İletişim Bilgileri]

---

**Not**: Bu sistem mülakat süreçlerini standardize etmek ve kaliteli sorular üretmek amacıyla geliştirilmiştir. 