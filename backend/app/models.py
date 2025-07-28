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
        """Maaş katsayısına göre zorluk seviyesi belirle"""
        if self.salary_multiplier <= 2:
            return {
                "level": "temel",
                "name": "🟢 TEMEL",
                "description": "3 yıl tecrübe - Syntax, temel kavramlar, basit uygulamalar",
                "experience_years": "3 yıl",
                "focus": "Temel syntax, framework kullanımı, basit algoritma"
            }
        elif self.salary_multiplier <= 3:
            return {
                "level": "orta", 
                "name": "🟡 ORTA",
                "description": "5-7 yıl tecrübe - Mimari yaklaşımlar, best practices, problem çözme",
                "experience_years": "5-7 yıl",
                "focus": "Tasarım kalıpları, mimari kararlar, performans optimizasyonu"
            }
        elif self.salary_multiplier <= 4:
            return {
                "level": "ileri",
                "name": "🟠 İLERİ", 
                "description": "8-10 yıl tecrübe - Sistem tasarımı, performans tuning, kompleks problemler",
                "experience_years": "8-10 yıl", 
                "focus": "Sistem mimarisi, scalability, güvenlik, team leadership"
            }
        else:
            return {
                "level": "uzman",
                "name": "🔴 UZMAN",
                "description": "10+ yıl tecrübe - Enterprise mimari, strategik kararlar, teknoloji liderliği", 
                "experience_years": "10+ yıl",
                "focus": "Enterprise architecture, strategic decisions, innovation"
            }

    @property 
    def question_difficulty_distribution(self):
        """Zorluk seviyesine göre soru dağılımı"""
        difficulty = self.difficulty_level
        
        if difficulty["level"] == "temel":
            return {
                "kolay": 70,    # %70 kolay soru
                "orta": 25,     # %25 orta soru  
                "zor": 5        # %5 zor soru
            }
        elif difficulty["level"] == "orta":
            return {
                "kolay": 40,    # %40 kolay
                "orta": 45,     # %45 orta
                "zor": 15       # %15 zor
            }
        elif difficulty["level"] == "ileri":
            return {
                "kolay": 20,    # %20 kolay
                "orta": 50,     # %50 orta  
                "zor": 30       # %30 zor
            }
        else:  # uzman
            return {
                "kolay": 10,    # %10 kolay
                "orta": 40,     # %40 orta
                "zor": 50       # %50 zor
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