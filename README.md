# Mülakat Soru Üretim Sistemi

Bu proje, sözleşmeli bilişim personeli alımı için otomatik mülakat soruları üreten bir web uygulamasıdır. İlan analizi yaparak, pozisyon gereksinimlerine uygun kaliteli sorular üretir.

## 🚀 Özellikler

- **İlan Analizi**: İlan metnini analiz ederek genel ve özel şartları çıkarır
- **Rol Bazlı Soru Üretimi**: Her pozisyon için özelleştirilmiş sorular
- **AI Destekli**: OpenAI GPT-4o-mini ile kaliteli soru üretimi
- **Çok Adımlı Süreç**: 5 adımlı wizard ile kolay kullanım
- **Dinamik Konfigürasyon**: Soru sayısı ve zorluk seviyesi ayarlanabilir

## 🛠️ Teknolojiler

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM ve veritabanı yönetimi
- **SQLite**: Hafif veritabanı
- **OpenAI API**: GPT-4o-mini ile soru üretimi

### Frontend
- **React**: Modern UI framework
- **Vite**: Hızlı build tool
- **Axios**: HTTP client
- **Tailwind CSS**: Styling

## 📋 Kurulum

### Gereksinimler
- Python 3.8+
- Node.js 16+
- OpenAI API Key

### Backend Kurulumu

```bash
cd backend

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Environment variable ayarla
export OPENAI_API_KEY="your-openai-api-key-here"

# Uygulamayı başlat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Kurulumu

```bash
cd frontend

# Bağımlılıkları yükle
npm install

# Uygulamayı başlat
npm run dev
```

## 🎯 Kullanım

1. **İlan Girişi**: İlan metnini yapıştırın
2. **Rol Tanımlama**: Pozisyonları ve gereksinimleri belirleyin
3. **Konfigürasyon**: Soru sayısı ve dağılımını ayarlayın
4. **Soru Üretimi**: AI ile soruları üretin
5. **Sonuçlar**: Üretilen soruları görüntüleyin

## 📁 Proje Yapısı

```
mulakat_soru/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI uygulaması
│   │   ├── models.py        # Veritabanı modelleri
│   │   ├── database.py      # Veritabanı bağlantısı
│   │   └── utils.py         # Yardımcı fonksiyonlar
│   ├── requirements.txt     # Python bağımlılıkları
│   └── mulakat.db          # SQLite veritabanı
├── frontend/
│   ├── src/
│   │   ├── components/      # React bileşenleri
│   │   ├── App.jsx         # Ana uygulama
│   │   └── main.jsx        # Giriş noktası
│   ├── package.json        # Node.js bağımlılıkları
│   └── vite.config.js      # Vite konfigürasyonu
└── README.md
```

## 🔧 API Endpoints

### İlan Yönetimi
- `GET /api/step1/contract/{contract_id}` - İlan detayları
- `POST /api/step1/save-contract` - İlan kaydetme

### Rol Yönetimi
- `GET /api/step2/roles/{contract_id}` - Rolleri listele
- `POST /api/step2/add-role` - Rol ekleme
- `PUT /api/step2/roles/{role_id}` - Rol güncelleme
- `DELETE /api/step2/roles/{role_id}` - Rol silme

### Konfigürasyon
- `GET /api/step3/global-config/{contract_id}` - Global konfigürasyon
- `POST /api/step3/save-global-config` - Global konfigürasyon kaydetme
- `GET /api/step3/role-question-configs/{contract_id}` - Rol konfigürasyonları

### Soru Üretimi
- `POST /api/step4/generate-questions` - Soru üretimi
- `GET /api/step4/questions/{contract_id}` - Üretilen sorular

## 🔒 Güvenlik

- API anahtarları environment variable olarak saklanır
- Veritabanı dosyası .gitignore'da
- Hassas bilgiler kodda hardcode edilmez

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Sorularınız için issue açabilirsiniz. 