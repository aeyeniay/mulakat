"""
Veritabanı modelleri
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
        """Maaş katsayısına göre zorluk seviyesi belirle - 5 Katmanlı Model"""
        if self.salary_multiplier <= 2:
            return {
                "level": "temel",
                "name": "🟢 ORTA DÜZEY UZMAN (2x)",
                "description": "2-4 yıl tecrübe - Günlük operasyonu eksiksiz yürütme, temel optimizasyon",
                "experience_years": "2-4 yıl",
                "focus": "İşe hazır teknik beceri, temel araçlar ve çerçevelerde yetkinlik",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 30,      # Tanım, sözdizimi, kavram
                    "K2_Uygulamali": 40,        # Küçük kod-konfig yazma, CLI komutu
                    "K3_Hata_Cozumleme": 25,    # Gerçek log/kod verip sorun bulma
                    "K4_Tasarim": 5,            # Komponent diyagramı, basit mimari
                    "K5_Stratejik": 0           # Trade-off analizi, roadmap
                },
                "bloom_seviyesi": "Remember/Apply",
                "dreyfus_seviyesi": "Novice/Advanced Beginner"
            }
        elif self.salary_multiplier <= 3:
            return {
                "level": "orta", 
                "name": "🟡 KIDEMLI UZMAN (3x)",
                "description": "5-8 yıl tecrübe - Çapraz disiplinde hâkimiyet, mentorluk, kritik problem çözümü",
                "experience_years": "5-8 yıl",
                "focus": "Tasarım kalıpları, mimari kararlar, performans optimizasyonu, mentorluk",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 15,      # Temel kavramlar
                    "K2_Uygulamali": 25,        # Gelişmiş uygulama
                    "K3_Hata_Cozumleme": 35,    # Kritik problem çözümü
                    "K4_Tasarim": 20,           # Mimari tasarım, best-practice
                    "K5_Stratejik": 5           # Stratejik kararlar
                },
                "bloom_seviyesi": "Analyze/Evaluate",
                "dreyfus_seviyesi": "Competent/Proficient"
            }
        elif self.salary_multiplier <= 4:
            return {
                "level": "ileri",
                "name": "🟠 MİMAR/TEKNİK LİDER (4x)", 
                "description": "8-10 yıl tecrübe - Strateji, büyük ölçekli mimari, metodoloji, ekip & süreç yönetimi",
                "experience_years": "8-10 yıl", 
                "focus": "Sistem mimarisi, scalability, güvenlik, team leadership, stratejik planlama",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 5,       # Minimal temel
                    "K2_Uygulamali": 15,        # İleri uygulama
                    "K3_Hata_Cozumleme": 25,    # Kompleks problem çözümü
                    "K4_Tasarim": 35,           # Büyük ölçekli mimari tasarım
                    "K5_Stratejik": 20          # Stratejik kararlar, roadmap
                },
                "bloom_seviyesi": "Evaluate/Create",
                "dreyfus_seviyesi": "Proficient/Expert"
            }
        else:  # 5x ve üzeri
            return {
                "level": "uzman",
                "name": "🔴 ENTERPRISE UZMAN (5x+)",
                "description": "10+ yıl tecrübe - Enterprise mimari, strategik kararlar, teknoloji liderliği, global ölçek",
                "experience_years": "10+ yıl",
                "focus": "Enterprise architecture, strategic decisions, innovation, global governance",
                "katman_dagilimi": {
                    "K1_Temel_Bilgi": 0,       # Minimal
                    "K2_Uygulamali": 10,        # Stratejik uygulama
                    "K3_Hata_Cozumleme": 20,    # Enterprise problem çözümü
                    "K4_Tasarim": 30,           # Enterprise mimari tasarım
                    "K5_Stratejik": 40          # Stratejik liderlik, roadmap
                },
                "bloom_seviyesi": "Create",
                "dreyfus_seviyesi": "Expert"
            }

    @property 
    def question_difficulty_distribution(self):
        """Zorluk seviyesine göre soru dağılımı - 5 Katmanlı Model"""
        difficulty = self.difficulty_level
        
        if difficulty["level"] == "temel":  # 2x
            return {
                "K1_Temel_Bilgi": 30,      # Tanım, sözdizimi, kavram
                "K2_Uygulamali": 40,        # Küçük kod-konfig yazma, CLI komutu
                "K3_Hata_Cozumleme": 25,    # Gerçek log/kod verip sorun bulma
                "K4_Tasarim": 5,            # Komponent diyagramı, basit mimari
                "K5_Stratejik": 0           # Trade-off analizi, roadmap
            }
        elif difficulty["level"] == "orta":  # 3x
            return {
                "K1_Temel_Bilgi": 15,      # Temel kavramlar
                "K2_Uygulamali": 25,        # Gelişmiş uygulama
                "K3_Hata_Cozumleme": 35,    # Kritik problem çözümü
                "K4_Tasarim": 20,           # Mimari tasarım, best-practice
                "K5_Stratejik": 5           # Stratejik kararlar
            }
        elif difficulty["level"] == "ileri":  # 4x
            return {
                "K1_Temel_Bilgi": 5,       # Minimal temel
                "K2_Uygulamali": 15,        # İleri uygulama
                "K3_Hata_Cozumleme": 25,    # Kompleks problem çözümü
                "K4_Tasarim": 35,           # Büyük ölçekli mimari tasarım
                "K5_Stratejik": 20          # Stratejik kararlar, roadmap
            }
        else:  # uzman (5x+)
            return {
                "K1_Temel_Bilgi": 0,       # Minimal
                "K2_Uygulamali": 10,        # Stratejik uygulama
                "K3_Hata_Cozumleme": 20,    # Enterprise problem çözümü
                "K4_Tasarim": 30,           # Enterprise mimari tasarım
                "K5_Stratejik": 40          # Stratejik liderlik, roadmap
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