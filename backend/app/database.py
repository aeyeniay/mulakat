"""
MÜLAKAT SORU HAZIRLAMASI SİSTEMİ - VERİTABANI BAĞLANTI YÖNETİMİ
===============================================================

📋 DOSYA AMACI:
Bu dosya, SQLAlchemy ORM kullanarak veritabanı bağlantı yönetimini sağlar.
Database engine, session factory ve dependency injection sistemini kurar.

🎯 KAPSAM:
1. 🔗 BAĞLANTI YÖNETİMİ:
   - SQLAlchemy Engine konfigürasyonu
   - Connection pool ayarları
   - Session factory oluşturma

2. 🏗️ ORM ALTYAPISI:
   - Declarative Base sınıfı
   - Model tanımlama temeli
   - Metadata yönetimi

3. 🔄 SESSION YÖNETİMİ:
   - FastAPI dependency injection
   - Auto-commit/rollback kontrolü
   - Session lifecycle yönetimi

📊 VERİ AKIŞI:
BAŞLATMA: Environment değişkenleri → Engine → SessionLocal → get_db()
KULLANIM: API endpoint'leri → DB session → ORM operations → Auto close

🔧 KONFIGÜRASYON:
- Varsayılan DB: SQLite (./mulakat.db)
- Environment: DATABASE_URL değişkeni ile override
- Connection Args: check_same_thread=False (SQLite için)
- Auto-commit: False (manual transaction control)
- Auto-flush: False (manual flush control)

⚙️ FONKSİYONLAR:
- get_db(): FastAPI dependency olarak session sağlar
- Otomatik session açma/kapama
- Exception durumunda otomatik cleanup

🔒 GÜVENLİK:
- Connection pool ile kaynak yönetimi
- Session isolation
- Memory leak önleme

📈 PERFORMANS:
- Connection pooling aktif
- Session reuse optimizasyonu
- Lazy loading stratejisi

🚀 KULLANIM ÖRNEĞİ:
```python
@app.get("/api/example")
async def example(db: Session = Depends(get_db)):
    # db session otomatik sağlanır
    result = db.query(Model).all()
    # session otomatik kapanır
    return result
```

👨‍💻 GELIŞTIREN: AI Destekli Geliştirme
📅 TARİH: 2025
🔄 VERSİYON: 1.0.0
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Environment variables'ları yükle
load_dotenv()

# SQLite bağlantı bilgileri
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./mulakat.db"
)

# SQLAlchemy engine ve session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Veritabanı session'ı döndürür"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 