"""
Veritabanı bağlantısı ve session yönetimi
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