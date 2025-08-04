# Mülakat Soru Hazırlama Sistemi

## Proje Hakkında

Bu sistem, kamu kurumlarında sözleşmeli bilişim personeli alımı süreçlerinde kullanılmak üzere geliştirilmiş bir mülakat sorusu hazırlama uygulamasıdır. Yapay zeka teknolojisi kullanarak pozisyon, seviye ve uzmanlık alanı kriterlerine göre özelleştirilmiş mülakat soruları üretir ve Word dosyası formatında çıktı alır.

## Özellikler

- Beş aşamalı soru üretim süreci
- Rol bazlı soru konfigürasyonu
- Otomatik soru üretimi (OpenAI GPT-4o-mini)
- Beklenen cevap anahtarları
- Düzenlenebilir sorular
- Word formatında aday ve jüri kitapçıkları
- Zorluk seviyesi yönetimi (2x, 3x, 4x katsayıları)

## Kullanılan Teknolojiler

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite + SQLAlchemy ORM 2.0.23
- **AI Integration**: OpenAI GPT-4o-mini API
- **Document Processing**: python-docx 1.1.0
- **Server**: Uvicorn 0.24.0

### Frontend
- **Framework**: React.js + Vite
- **HTTP Client**: Axios
- **Styling**: CSS3 + Bootstrap benzeri responsive tasarım

## Sistem Gereksinimleri

- Python 3.8 veya üzeri
- Node.js 16 veya üzeri
- NPM paket yöneticisi
- OpenAI API anahtarı

## Kurulum

### Backend Kurulumu

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Kurulumu

```bash
cd frontend
npm install
npm run dev
```

## Konfigürasyon

OpenAI API anahtarınızı `backend/app/utils.py` dosyasında güncelleyin:

```python
client = OpenAI(
    api_key="your-api-key-here",
    timeout=60.0,
    max_retries=3
)
```

## Kullanım

### 1. İlan Bilgileri
İlan başlığı ve genel şartları girin. Sistem otomatik olarak benzersiz bir ID oluşturur.

### 2. Rol Tanımları
- Pozisyon adı ve açıklaması
- Maaş katsayısı (2x, 3x, 4x)
- Pozisyon sayısı
- Özel gereksinimler

### 3. Soru Konfigürasyonu
Her rol için soru tiplerini ve sayılarını belirleyin:
- Mesleki Deneyim Soruları
- Teorik Bilgi Soruları
- Pratik Uygulama Soruları

### 4. Soru Üretimi
"Soruları Üret" butonuna tıklayarak AI destekli soru üretim sürecini başlatın. Üretilen soruları tek tek düzenleyebilirsiniz.

### 5. Dosya İndirme
Her rol için ayrı ayrı Word formatında aday kitapçığı (S1, S2...) ve jüri kitapçığı (C1, C2...) indirebilirsiniz.

## Proje Yapısı

```
mulakat_soru/
├── backend/
│   ├── app/
│   │   ├── main.py          # Ana API endpoint'leri
│   │   ├── models.py        # Veritabanı modelleri
│   │   ├── utils.py         # AI entegrasyonu ve yardımcı fonksiyonlar
│   │   └── database.py      # Veritabanı bağlantı yönetimi
│   └── requirements.txt     # Python bağımlılıkları
├── frontend/
│   ├── src/
│   │   ├── components/      # React bileşenleri
│   │   ├── App.jsx         # Ana uygulama
│   │   └── App.css         # Stil dosyaları
│   └── package.json        # Node.js bağımlılıkları
└── README.md
```

## API Endpoint'leri

- `/api/step1/` - İlan yönetimi
- `/api/step2/` - Rol yönetimi
- `/api/step3/` - Soru konfigürasyonu
- `/api/step4/` - Soru üretimi
- `/api/step5/` - Word dosyası üretimi
- `/api/system/` - Sistem bilgileri

## Veritabanı

Sistem SQLite veritabanı kullanır ve şu ana tabloları içerir:
- contracts (ilanlar)
- roles (roller)
- question_types (soru tipleri)
- role_question_configs (rol soru konfigürasyonları)
- questions (üretilen sorular)

## Geliştirme

Detaylı teknik dokümantasyon için her dosyanın başında bulunan açıklamaları inceleyiniz. DOCUMENTATION.md dosyası sistem mimarisi hakkında kapsamlı bilgi içermektedir.

## İletişim

Ahmet Erdem Yeniay  
Coğrafi Bilgi Sistemleri Genel Müdürlüğü  
Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı  
Yapay Zeka Teknolojileri Şube Müdürlüğü  
ahmeterdem.yeniay@csb.gov.tr

## Lisans

Bu proje Coğrafi Bilgi Sistemleri Genel Müdürlüğü - Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı için geliştirilmiştir.

---

**Geliştirme Tarihi**: 2025  
**Versiyon**: 1.0.0 