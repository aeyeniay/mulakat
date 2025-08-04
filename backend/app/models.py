"""
MÜLAKAT SORU HAZIRLAMASI SİSTEMİ - VERİTABANI MODELLERİ
========================================================

📋 DOSYA AMACI:
Bu dosya, mülakat soru hazırlama sisteminin tüm veritabanı modellerini içerir.
SQLAlchemy ORM kullanarak ilişkisel veritabanı yapısını tanımlar ve
iş mantığı property'lerini sağlar.

🎯 KAPSAM:
1. 📄 İLAN YÖNETİMİ:
   - Contract: İlan bilgileri ve genel şartlar
   - ContractData: Ayrıştırılmış JSON verileri

2. 👥 ROL YÖNETİMİ:  
   - Role: Pozisyon tanımları ve maaş katsayıları
   - Difficulty level hesaplamaları (2x, 3x, 4x)

3. ❓ SORU SİSTEMİ:
   - QuestionType: Dinamik soru tipi tanımları
   - RoleQuestionConfig: Rol bazlı soru konfigürasyonları
   - Question: Üretilmiş sorular ve cevap anahtarları

4. ⚙️ SİSTEM YÖNETİMİ:
   - QuestionConfig: Global sınav ayarları
   - SystemInfo: GPU/API durum bilgileri
   - GenerationLog: Soru üretim logları

📊 VERİ İLİŞKİLERİ:
Contract (1) ←→ (N) Role ←→ (N) RoleQuestionConfig ←→ (1) QuestionType
Contract (1) ←→ (N) Question
Role (1) ←→ (N) Question

🔧 ÖZELLİKLER:
1. 📈 DİNAMİK ZORLUK SİSTEMİ:
   - Maaş katsayısına göre otomatik zorluk seviyesi
   - K1-K5 rubrik dağılımı property'leri
   - Bloom/Dreyfus taxonomy entegrasyonu

2. 🎯 SORU TİPİ YÖNETİMİ:
   - Aktif/pasif soru tipi kontrolü
   - Sıralama sistemi (order_index)
   - Dinamik kategori ekleme/çıkarma

3. 📊 METRİK TAKİBİ:
   - Soru üretim süreleri
   - API kullanım istatistikleri
   - Sistem performans logları

⚙️ TEKNİK BİLGİLER:
- ORM: SQLAlchemy 2.0.23
- Veritabanı: SQLite (geliştirme), PostgreSQL uyumlu
- Encoding: UTF-8 (Türkçe karakter desteği)
- Timestamp: UTC timezone
- JSON fields: PostgreSQL JSON/SQLite TEXT

🏗️ TABLO YAPISI:
- contracts (ilanlar)
- roles (roller/pozisyonlar)  
- question_types (soru tipleri)
- role_question_configs (rol-soru konfigürasyonları)
- questions (üretilmiş sorular)
- question_configs (global ayarlar)
- contract_data (ayrıştırılmış veriler)
- system_info (sistem bilgileri)
- generation_logs (üretim logları)

👨‍💻 GELIŞTIREN: AI Destekli Geliştirme
📅 TARİH: 2025
🔄 VERSİYON: 1.0.0
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Contract(Base):
    """İlan bilgileri - 1. Adım"""
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)  # İlan metni
    general_requirements = Column(Text)  # Genel şartlar
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    roles = relationship("Role", back_populates="contract")

class Role(Base):
    """Roller ve gereksinimler - 2. Adım"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    name = Column(String, index=True)
    salary_multiplier = Column(Float)
    position_count = Column(Integer)
    requirements = Column(Text)
    
    contract = relationship("Contract", back_populates="roles")
    question_configs = relationship("RoleQuestionConfig", back_populates="role")

    @property
    def difficulty_level(self):
        """Maaş katsayısına göre zorluk seviyesi belirle - Güncellenmiş Model (KOD SORUSU YOK!)"""
        if self.salary_multiplier <= 2:
            return {
                "level": "2x",
                "name": "🟢 UZMAN DÜZEYİ (2x - Orta Seviye)",
                "description": "3 Yıl Deneyim - Temel kavramsal bilgi, yaygın teknolojilerin kullanımı ve bilinen problemlere çözüm yolları. KOD SORUSU SORULMAZ!",
                "experience_years": "3 yıl",
                "focus": "Tanım yapma, açıklama, basit konfigürasyon veya kullanım örnekleri. Kod yazdırma kesinlikle yasak!",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 40,      # Tanım, kavram, açıklama
                    "K2_Uygulamali": 35,        # Konfigürasyon, kullanım (KOD DEĞİL!)
                    "K3_Hata_Cozumleme": 20,    # Log analizi, sorun tespiti (KOD DEĞİL!)
                    "K4_Tasarim": 5,            # Basit yaklaşım önerileri
                    "K5_Stratejik": 0           # Yok
                },
                "bloom_seviyesi": "Remember/Understand/Apply",
                "dreyfus_seviyesi": "Advanced Beginner/Competent",
                "no_code_rule": "KESİNLİKLE KOD YAZDIRMA SORULARI SORULMASUN!"
            }
        elif self.salary_multiplier <= 3:
            return {
                "level": "3x", 
                "name": "🟡 KIDEMLİ UZMAN DÜZEYİ (3x - İleri Seviye)",
                "description": "5 Yıl Deneyim - İleri seviye teknik bilgi, sistemler arası ilişkileri anlama ve problem çözme yetkinliği. KOD SORUSU SORULMAZ!",
                "experience_years": "5 yıl",
                "focus": "Log inceleme, sistem yapılandırma hatalarını analiz etme, farklı çözümler arasında tercih yapma. Kod yazdırma kesinlikle yasak!",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 25,      # İleri kavramlar
                    "K2_Uygulamali": 30,        # Gelişmiş konfigürasyon (KOD DEĞİL!)
                    "K3_Hata_Cozumleme": 30,    # Sistem hatası analizi (KOD DEĞİL!)
                    "K4_Tasarim": 15,           # Çözüm karşılaştırması
                    "K5_Stratejik": 0           # Tasarım ve stratejik sorular YOK!
                },
                "bloom_seviyesi": "Analyze/Evaluate",
                "dreyfus_seviyesi": "Competent/Proficient",
                "no_code_rule": "KESİNLİKLE KOD YAZDIRMA SORULARI SORULMASUN!"
            }
        elif self.salary_multiplier <= 4:
            return {
                "level": "4x",
                "name": "🟠 TAKIM LİDERİ / STRATEJİK UZMAN DÜZEYİ (4x - Yüksek Seviye)", 
                "description": "7+ Yıl Deneyim - Yüksek seviye teknik liderlik, stratejik karar alma ve mimari tasarım yetkinlikleri. KOD SORUSU SORULMAZ!",
                "experience_years": "7+ yıl", 
                "focus": "Sistem mimarisi tasarımı, teknoloji alternatiflerinin karşılaştırılması, ekip süreçlerinin iyileştirilmesi. Kod yazdırma kesinlikle yasak!",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 10,       # Minimal temel
                    "K2_Uygulamali": 20,        # Stratejik uygulama yaklaşımları (KOD DEĞİL!)
                    "K3_Hata_Cozumleme": 25,    # Kompleks sistem problemleri (KOD DEĞİL!)
                    "K4_Tasarim": 30,           # Mimari tasarım, teknoloji seçimi
                    "K5_Stratejik": 15          # Karar gerekçeleri, süreç iyileştirme
                },
                "bloom_seviyesi": "Evaluate/Create",
                "dreyfus_seviyesi": "Proficient/Expert",
                "no_code_rule": "KESİNLİKLE KOD YAZDIRMA SORULARI SORULMASUN!"
            }
        else:  # 5x ve üzeri (eski sistem için koruma)
            return {
                "level": "5x+",
                "name": "🔴 ENTERPRISE UZMAN (5x+)",
                "description": "10+ yıl tecrübe - Enterprise mimari, strategik kararlar, teknoloji liderliği. KOD SORUSU SORULMAZ!",
                "experience_years": "10+ yıl",
                "focus": "Enterprise architecture, strategic decisions, innovation. Kod yazdırma kesinlikle yasak!",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 5,       # Minimal
                    "K2_Uygulamali": 15,        # Stratejik uygulama
                    "K3_Hata_Cozumleme": 20,    # Enterprise problem çözümü
                    "K4_Tasarim": 30,           # Enterprise mimari tasarım
                    "K5_Stratejik": 30          # Stratejik liderlik, roadmap
                },
                "bloom_seviyesi": "Create",
                "dreyfus_seviyesi": "Expert",
                "no_code_rule": "KESİNLİKLE KOD YAZDIRMA SORULARI SORULMASUN!"
            }

    @property 
    def question_difficulty_distribution(self):
        """Zorluk seviyesine göre soru dağılımı - Güncellenmiş Model (KOD SORUSU YOK!)"""
        difficulty = self.difficulty_level
        
        if difficulty["level"] == "2x":  # Uzman Düzeyi
            return {
                "K1_Temel_Bilgi": 40,      # Tanım, kavram, açıklama (KOD YOK!)
                "K2_Uygulamali": 35,        # Konfigürasyon, kullanım (KOD YOK!)
                "K3_Hata_Cozumleme": 20,    # Log analizi, sorun tespiti (KOD YOK!)
                "K4_Tasarim": 5,            # Basit yaklaşım önerileri
                "K5_Stratejik": 0           # YOK
            }
        elif difficulty["level"] == "3x":  # Kıdemli Uzman Düzeyi
            return {
                "K1_Temel_Bilgi": 25,      # İleri kavramlar
                "K2_Uygulamali": 30,        # Gelişmiş konfigürasyon (KOD YOK!)
                "K3_Hata_Cozumleme": 30,    # Sistem hatası analizi (KOD YOK!)
                "K4_Tasarim": 15,           # Çözüm karşılaştırması
                "K5_Stratejik": 0           # Tasarım ve stratejik sorular YOK!
            }
        elif difficulty["level"] == "4x":  # Takım Lideri / Stratejik Uzman
            return {
                "K1_Temel_Bilgi": 10,       # Minimal temel
                "K2_Uygulamali": 20,        # Stratejik uygulama yaklaşımları (KOD YOK!)
                "K3_Hata_Cozumleme": 25,    # Kompleks sistem problemleri (KOD YOK!)
                "K4_Tasarim": 30,           # Mimari tasarım, teknoloji seçimi
                "K5_Stratejik": 15          # Karar gerekçeleri, süreç iyileştirme
            }
        else:  # 5x+ (eski sistem için koruma)
            return {
                "K1_Temel_Bilgi": 5,       # Minimal
                "K2_Uygulamali": 15,        # Stratejik uygulama (KOD YOK!)
                "K3_Hata_Cozumleme": 20,    # Enterprise problem çözümü (KOD YOK!)
                "K4_Tasarim": 30,           # Enterprise mimari tasarım
                "K5_Stratejik": 30          # Stratejik liderlik, roadmap
            }

class QuestionType(Base):
    """Soru tipleri (dinamik) - 3. Adım"""
    __tablename__ = "question_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # "Mesleki Tecrübe Soruları"
    description = Column(Text)  # "Adayın deneyim ve projelerini değerlendiren sorular"
    code = Column(String(50), unique=True, nullable=False)  # "professional_experience"
    order_index = Column(Integer, default=0)  # Gösterim sırası
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    question_configs = relationship("RoleQuestionConfig", back_populates="question_type")

class RoleQuestionConfig(Base):
    """Her rol için soru tipleri ve sayıları - 3. Adım (Rolle bazlı)"""
    __tablename__ = "role_question_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    question_type_id = Column(Integer, ForeignKey("question_types.id"))
    
    # Soru sayısı (her rol + soru tipi kombinasyonu için)
    question_count = Column(Integer, default=5)
    
    # Role özgü zorluk seviyesi
    difficulty_level = Column(String(50), default="Orta")  # Kolay, Orta, Zor
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    role = relationship("Role", back_populates="question_configs")
    question_type = relationship("QuestionType", back_populates="question_configs")

class QuestionConfig(Base):
    """Global sınav ve soru konfigürasyonu - 3. ve 4. Adım"""
    __tablename__ = "question_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    
    # Global sınav ayarları - 3. Adım
    candidate_multiplier = Column(Integer, default=10)  # Her pozisyon için kaç aday çağırılacak
    questions_per_candidate = Column(Integer, default=5)  # Her adaya kaç soru sorulacak
    
    # Soru türü dağılımı (JSON formatında - dinamik)
    question_type_distribution = Column(JSON, default=lambda: {
        "professional_experience": 1,
        "theoretical_knowledge": 2, 
        "practical_application": 2
    })  # Her soru tipi için aday başına soru sayısı
    
    # LLM ayarları - 4. Adım
    llm_model = Column(String(100), default="gpt-4o-mini")  # OpenAI GPT-4o-mini model
    generation_status = Column(String(50), default="pending")  # pending, generating, completed, failed
    
    # Sistem bilgileri
    focus_areas = Column(Text)  # JSON formatında odak alanları
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContractData(Base):
    """İlan verilerinin JSON formatında saklanması - 4. Adım"""
    __tablename__ = "contract_data"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    parsed_data = Column(Text, nullable=False)  # JSON formatında ayrıştırılmış veri
    created_at = Column(DateTime, default=datetime.utcnow)

class Question(Base):
    """Oluşturulan sorular - 5. Adım (Güncellenmiş)"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))  # Hangi role ait
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    
    # Soru bilgileri
    question_text = Column(Text, nullable=False)
    question_type = Column(String(100), nullable=False)  # professional_experience, theoretical_knowledge, practical_application
    difficulty = Column(String(50))  # kolay, orta, zor
    
    # API'den gelen ek bilgiler
    expected_answer = Column(Text)  # Beklenen cevap rehberi
    scoring_criteria = Column(Text)  # Değerlendirme kriterleri
    
    # Metadata
    llm_model = Column(String(100))  # Kullanılan LLM modeli
    generation_metadata = Column(JSON)  # Üretim metadata'sı
    
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemInfo(Base):
    """Sistem bilgileri ve GPU durumu"""
    __tablename__ = "system_info"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # GPU bilgileri
    cuda_available = Column(Boolean, default=False)
    gpu_count = Column(Integer, default=0)
    gpu_name = Column(String(255))
    gpu_memory_gb = Column(Float)
    allocated_memory_gb = Column(Float)
    
    # API bilgileri
    api_available = Column(Boolean, default=False)
    available_models = Column(JSON)  # Mevcut modeller
    
    # Sistem bilgileri
    python_version = Column(String(100))
    platform = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GenerationLog(Base):
    """Soru üretim logları"""
    __tablename__ = "generation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))  # Hangi role ait
    
    # Üretim bilgileri
    model_name = Column(String(100))
    prompt_length = Column(Integer)
    response_length = Column(Integer)
    generation_time = Column(Float)  # Saniye
    
    # Durum
    status = Column(String(50))  # success, failed, partial
    error_message = Column(Text)
    
    # Raw data
    raw_prompt = Column(Text)
    raw_response = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow) 