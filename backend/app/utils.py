"""
MÜLAKAT SORU HAZIRLAMASI SİSTEMİ - YARDIMCI FONKSİYONLAR
=========================================================

📋 DOSYA AMACI:
Bu dosya, mülakat soru hazırlama sisteminin temel yardımcı fonksiyonlarını içerir.
OpenAI API entegrasyonu, soru üretimi algoritmaları, zorluk seviyesi hesaplamaları
ve JSON parse işlemleri bu dosyada gerçekleştirilir.

🎯 KAPSAM:
1. 🤖 AI ENTEGRASYONU:
   - OpenAI GPT-4o-mini API bağlantısı
   - Soru üretimi prompt'ları
   - AI yanıt işleme ve parse etme

2. 📊 ZORLUK SİSTEMİ:
   - Maaş katsayısına göre zorluk seviyesi (2x, 3x, 4x)
   - K1-K5 rubrik modeli katsayıları
   - Bilişsel seviye dağılımları

3. 🔍 SORU ÜRETİMİ:
   - Dinamik soru tipi yönetimi
   - Konu çeşitliliği algoritması
   - JSON format düzeltme mekanizmaları

4. 🗄️ VERİTABANI ENTEGRASYONU:
   - Aktif soru tiplerini çekme
   - Soru kaydetme işlemleri

📊 VERİ AKIŞI:
GİRİŞ: İlan bilgileri, rol verileri, soru konfigürasyonları
İŞLEM: AI prompt oluşturma, API çağrısı, yanıt parse, veritabanı kayıt
ÇIKIŞ: Üretilmiş sorular ve beklenen cevaplar (JSON formatı)

🔧 TEMEL FONKSİYONLAR:
- get_difficulty_distribution_by_multiplier() → Zorluk katsayı hesaplama
- get_active_question_types() → Aktif soru tiplerini getirme
- generate_questions_with_4o_mini() → AI ile soru üretimi
- generate_corrected_question_with_4o_mini() → Tekil soru düzeltme
- check_4o_mini_status() → API durum kontrolü

⚙️ TEKNİK ÖZELLİKLER:
- OpenAI API timeout: 60 saniye
- Maksimum retry: 3 defa
- JSON parse gelişmiş hata düzeltme
- Regex tabanlı format temizleme
- Logging sistemi entegrasyonu

🚫 KURAL SİSTEMİ:
- KESİNLİKLE kod yazdırma sorusu üretilmez
- Aynı konudan birden fazla soru sorulmaz
- Konu çeşitliliği zorunlu
- Anahtar kelimeler expected_answer içinde

👨‍💻 GELIŞTIREN: AI Destekli Geliştirme
📅 TARİH: 2025
🔄 VERSİYON: 1.0.0
"""
from openai import OpenAI
import json
import logging
import re
from typing import Dict, Any, List
import sys
import os
from sqlalchemy.orm import Session
from .models import QuestionType
from .database import SessionLocal

def get_difficulty_distribution_by_multiplier(salary_multiplier):
    """Maaş katsayısına göre güncellenmiş zorluk dağılımı hesapla"""
    if salary_multiplier <= 2:  # 2x – Uzman
        return {
            "K1_Temel_Bilgi": 45,      # Tanım, kavram (yüksek)
            "K2_Uygulamali": 40,       # Uygulama örneği (yüksek)
            "K3_Hata_Cozumleme": 10,   # Az hata tespiti
            "K4_Tasarim": 5,           # Sınırlı mimari
            "K5_Stratejik": 0          # YOK
        }
    elif salary_multiplier <= 3:  # 3x – Kıdemli Uzman
        return {
            "K1_Temel_Bilgi": 20,      # Kavramlar
            "K2_Uygulamali": 25,       # Uygulama mantığı
            "K3_Hata_Cozumleme": 35,   # Log analizi, hata çözümü
            "K4_Tasarim": 20,          # Mimarî karşılaştırma
            "K5_Stratejik": 0          # Henüz yok
        }
    elif salary_multiplier <= 4:  # 4x – Takım Lideri
        return {
            "K1_Temel_Bilgi": 5,       # Temel bilgi çok az
            "K2_Uygulamali": 15,       # Stratejik uygulama
            "K3_Hata_Cozumleme": 25,   # Derinlemesine analiz
            "K4_Tasarim": 35,          # Mimarî kararlar
            "K5_Stratejik": 20         # Liderlik, süreç kararı
        }
    else:  # 5x+ – Stratejik Liderlik
        return {
            "K1_Temel_Bilgi": 5,       # Minimal
            "K2_Uygulamali": 10,       # Üst seviye uygulama
            "K3_Hata_Cozumleme": 20,   # Enterprise düzey hata çözüm
            "K4_Tasarim": 30,          # Büyük ölçekli mimari
            "K5_Stratejik": 35         # Roadmap, stratejik kararlar
        }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_active_question_types():
    """Aktif soru tiplerini veri tabanından çek"""
    db = SessionLocal()
    try:
        question_types = db.query(QuestionType).filter(
            QuestionType.is_active == True
        ).order_by(QuestionType.order_index).all()
        
        return [(qt.code, qt.name) for qt in question_types]
    except Exception as e:
        logger.error(f"Soru tipleri alınırken hata: {str(e)}")
        # Fallback: hardcoded values
        return [
            ("professional_experience", "Mesleki Deneyim Soruları"),
            ("theoretical_knowledge", "Teorik Bilgi Soruları"),
            ("practical_application", "Pratik Uygulama Soruları")
        ]
    finally:
        db.close()

# OpenAI API configuration
client = OpenAI(
    api_key="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",
    timeout=60.0,
    max_retries=3
)

def check_4o_mini_status():
    """Check if OpenAI API is available."""
    try:
        # Test API connection
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10
        )
        
        return {
            "api_available": True,
            "model": "gpt-4o-mini",
            "status": "connected",
            "test_response": response.choices[0].message.content
        }
        
    except Exception as e:
        logger.error(f"Error connecting to OpenAI API: {str(e)}")
        return {
            "api_available": False,
            "error": str(e),
            "details": "API bağlantı hatası - timeout veya network sorunu"
        }


def get_available_4o_mini_models():
    """OpenAI API modellerini al"""
    try:
        return [
            {
                "name": "gpt-4o-mini",
                "display_name": "gpt-4o-mini - OpenAI API",
                "size_gb": 0,
                "size_bytes": 0,
                "speed_category": "🚀 API Hızlı",
                "color": "#28a745",
                "recommended": True
            }
        ]
    except Exception as e:
        logger.error(f"Error getting OpenAI models: {str(e)}")
        return [
            {
                "name": "gpt-4o-mini",
                "display_name": "gpt-4o-mini - OpenAI API",
                "size_gb": 0,
                "size_bytes": 0,
                "speed_category": "🚀 API Hızlı",
                "color": "#28a745",
                "recommended": True
            }
        ]


def generate_questions_with_4o_mini(
    model_name: str,
    job_context: str,
    roles: List[Dict[str, Any]],
    question_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate questions using OpenAI API - tek tek soru üretimi.
    """
    logger.info("OpenAI API ile soru üretimi başlatılıyor.")
    
    try:
        # Her soru tipi için ayrı ayrı soru üret
        all_questions = {
            "professional_experience": [],
            "theoretical_knowledge": [],
            "practical_application": []
        }
        
        # Her rol için soruları üret
        for role in roles:
            role_name = role.get("name", "Unknown Role")
            position_count = role.get("position_count", 1)
            salary_coefficient = role.get("salary_coefficient", 2)
            special_requirements = role.get("special_requirements", "")
            
            # Zorluk seviyesini question_config'den al
            difficulty = question_config.get("difficulty_level", "orta")
            
            # Dinamik soru tiplerini veri tabanından al
            active_question_types = get_active_question_types()
            
            # Her soru tipi için soruları üret  
            for question_type, type_name in active_question_types:
                # question_config bir dict değilse default değer kullan
                if isinstance(question_config, dict):
                    question_count = question_config.get(question_type, 5)
                else:
                    question_count = 5
                
                if question_count > 0:
                    logger.info(f"{type_name} soruları üretiliyor: {question_count} adet")
                    
                    for i in range(question_count):
                        # Zorluk dağılımını hesapla
                        difficulty_distribution = get_difficulty_distribution_by_multiplier(salary_coefficient)
                        
                        # Her soru için ayrı prompt oluştur - AKTİF KATSAYILARLA (KOD SORUSU YOK!)
                        prompt = f"""
İlan Başlığı: {job_context}
Pozisyon: {role_name}
Pozisyon Sayısı: {position_count}
Maaş Katsayısı: {salary_coefficient}x
Zorluk Seviyesi: {difficulty}
Özel Şartlar: {special_requirements}

Bu pozisyona ait {type_name} kategorisinde {i+1}. soruyu ve beklenen cevabını üret.

Kod yazdırmak kesinlikle yasaktır. Soru içerisinde herhangi bir kod, algoritma, script, fonksiyon isteme ya da kod tamamlama ifadesi olmamalıdır. Adaydan sadece açıklama, analiz, yorum, yaklaşım veya deneyim paylaşımı beklenmelidir.

Her soru özel şartlarda belirtilen farklı bir konuya odaklanmalıdır. Aynı konu başlığından birden fazla soru oluşturulmamalı, her soru pozisyonun farklı bir teknolojik alanına değinmelidir. Örneğin; bir soru React Native, bir diğeri Git, bir diğeri SOAP/REST üzerine olabilir.

Soru zorluk seviyesi, maaş katsayısına göre belirlenen bilgi derinliğine uygun olmalıdır. {salary_coefficient}x seviyesi, {difficulty} düzeyini temsil eder. Aşağıdaki ağırlık dağılımına göre soru uygun katmandan seçilmelidir:

- Temel Bilgi (%{difficulty_distribution['K1_Temel_Bilgi']}): Tanım, kavram açıklama (kod içermez)
- Uygulamalı Bilgi (%{difficulty_distribution['K2_Uygulamali']}): Konfigürasyon, yöntem, kullanım önerisi (kod içermez)
- Hata Çözümleme (%{difficulty_distribution['K3_Hata_Cozumleme']}): Log analizi, hata tespiti ve değerlendirme (kod içermez)
- Tasarım (%{difficulty_distribution['K4_Tasarim']}): Mimari yapı, teknoloji karşılaştırması, ölçeklenebilirlik gibi konular
- Stratejik (%{difficulty_distribution['K5_Stratejik']}): Süreç iyileştirme, teknoloji seçimi, karar gerekçesi gibi liderlik odaklı sorular

Soru doğrudan, açık ve konuya odaklı olmalı; içinde ayrıca 'adayın bilgi vermesi beklenir' gibi tekrar eden ifadeler olmamalıdır. Bu açıklama beklenen cevap kısmında yapılacaktır.

Beklenen cevap jüri için bilgilendirici tonda yazılmalı, adayın ağzından değil, gözlemleyen veya değerlendiren kişi diliyle ifade edilmelidir. Şu yapıda olmalıdır:

"Adayın [seçilen konu] hakkında [beklenen bilgi/deneyim] göstermesi beklenir. [Detaylı açıklama ve örnekler]."

Cevabın sonunda bir satır boşluk bırakılarak 4–5 anahtar kelime verilmelidir.

Sonuç kesinlikle şu formatta JSON olarak döndürülmelidir (başka format kabul edilmez):

{{
  "question": "soru metni burada",
  "expected_answer": "beklenen cevap burada\\n\\nAnahtar kelimeler: kelime1, kelime2, kelime3, kelime4"
}}

DİKKAT: Anahtar kelimeler expected_answer içinde olmalı, ayrı bir alan olmamalı!
"""


                        try:
                            response = client.chat.completions.create(
                                model=model_name,
                                messages=[
                                    {"role": "system", "content": (
                                        "Sen bir İnsan Kaynakları uzmanısın. Görevin, kamu kurumunda sözleşmeli bilişim personeli alımı için mülakat sürecine uygun, "
                                        "değerlendirilebilir ve yapılandırılmış sorular üretmektir. Hazırlayacağın her soru, belirli bir pozisyona, belirli bir kategoriye "
                                        "(örn. Teorik Bilgi, Pratik Uygulama, Mesleki Deneyim) ve belirlenmiş zorluk seviyesine göre şekillenmelidir. "
                                        
                                        "Sorular sadece açıklama, yorum, analiz veya deneyim temelli olmalıdır. Kod yazdırmak, algoritma istemek, fonksiyon yazımı, script talebi gibi "
                                        "uygulamalı programlama içeren hiçbir içerik sorulmamalıdır. Bu tür sorular kesinlikle yasaktır ve üretmeyeceksin. "
                                        
                                        "Mülakat soruları, adayların ilgili pozisyonla ilişkili teknolojiler hakkında bilgi düzeyini, analitik becerilerini ve deneyimlerini anlamaya yönelik olmalıdır. "
                                        "Soru konuları, pozisyonun özel şartlarında belirtilen teknolojiler veya araçlar arasından rastgele seçilmelidir. Aynı konudan birden fazla soru üretilmemelidir. "
                                        
                                        "Ayrıca, her sorunun zorluk seviyesi pozisyonun maaş katsayısına (örn. 2x, 3x, 4x) göre değişir. Bu katsayılar, adayın kıdem düzeyine göre "
                                        "sorunun bilgi derinliği ve analitik gereksinimini belirler. Örneğin; 2x adaydan temel kavramsal açıklama beklenirken, 4x adaydan mimari tasarım "
                                        "veya stratejik karar analizleri beklenebilir. Bu seviye dağılımı önceden sana verilecektir. "

                                        "Hazırlayacağın her soru, tek bir teknolojiye odaklanmalı ve net bir başlık/konu içermelidir. Sorunun sonunda ise, jüriye yönelik açıklayıcı bir 'beklenen cevap' "
                                        "vermelisin. Bu cevap, adayın ne tür bilgi, beceri ya da yaklaşımı göstermesinin beklendiğini açıklar. Cevap adayın ağzından değil, değerlendirme "
                                        "perspektifinden yazılmalı, öğretici ve açıklayıcı olmalıdır. Son olarak da anahtar kavramlar listelenmelidir."

                                        "Tüm çıktı, sana verilen formata uygun olarak, JSON yapısında döndürülmelidir. Görevin, bu yapıya tam uyarak açık, anlaşılır ve kurum ciddiyetine uygun "
                                        "mülakat soruları üretmektir."
                                    )},
                                    {"role": "user", "content": prompt}
                                ],
                                temperature=0.8,
                                max_tokens=1000
                            )
                            logger.info(f"OpenAI API response received for {type_name} sorusu {i+1}")
                        except Exception as api_error:
                            logger.error(f"OpenAI API error for {type_name} sorusu {i+1}: {str(api_error)}")
                            # Fallback: basit soru oluştur
                            all_questions[question_type].append({
                                "question": f"{type_name} sorusu {i+1} - API hatası nedeniyle basit soru",
                                "difficulty": "orta"
                            })
                            continue
                        
                        # Parse the response
                        generated_text = response.choices[0].message.content
                        
                        # Try to extract JSON from the response - IMPROVED
                        try:
                            # Markdown code block'ları ve diğer formatları temizle
                            cleaned_text = generated_text.strip()
                            
                            # Farklı JSON başlangıçlarını temizle - REGEX ile güçlendirildi
                            
                            # ```json { ... } ``` formatını temizle
                            if '```json' in cleaned_text and '```' in cleaned_text:
                                # Regex ile ```json ile ``` arasındaki kısmı çıkar
                                json_match = re.search(r'```json\s*(\{.*?\})\s*```', cleaned_text, re.DOTALL)
                                if json_match:
                                    cleaned_text = json_match.group(1).strip()
                            elif cleaned_text.startswith('```json'):
                                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
                            elif cleaned_text.startswith('```'):
                                cleaned_text = cleaned_text.replace('```', '').strip()
                            elif cleaned_text.startswith('json ('):
                                cleaned_text = cleaned_text.replace('json (', '{', 1).strip()
                            elif cleaned_text.startswith('"json ('):
                                cleaned_text = cleaned_text.replace('"json (', '{', 1).strip()
                            
                            # JSON içinde başlangıç/bitiş karakterlerini düzelt
                            if not cleaned_text.startswith('{') and '{' in cleaned_text:
                                # İlk { karakterinden başla
                                start_idx = cleaned_text.find('{')
                                cleaned_text = cleaned_text[start_idx:]
                            
                            if not cleaned_text.endswith('}') and '}' in cleaned_text:
                                # Son } karakterinde bitir
                                end_idx = cleaned_text.rfind('}')
                                cleaned_text = cleaned_text[:end_idx+1]
                            
                            # JSON içindeki yanlış anahtar kelimeler formatını düzelt - SÜPER GÜÇLENDİRİLDİ
                            # AI'ın ürettiği en yaygın hatalı formatları yakala ve düzelt:
                            
                            # Format 1: "expected_answer": "text", "\n\nAnahtar kelimeler: words" }
                            pattern1 = r'("expected_answer":\s*"[^"]*"),\s*"(\\n\\nAnahtar kelimeler:[^"]*)"(\s*\})'
                            if re.search(pattern1, cleaned_text):
                                cleaned_text = re.sub(pattern1, r'\1\2"\3', cleaned_text)
                                logger.info("JSON Format 1 düzeltildi")
                            
                            # Format 2: "text", "\n\nAnahtar kelimeler: words" 
                            pattern2 = r'",\s*"(\\n\\nAnahtar kelimeler:[^"]*)"'
                            if re.search(pattern2, cleaned_text):
                                cleaned_text = re.sub(pattern2, r'\1"', cleaned_text)
                                logger.info("JSON Format 2 düzeltildi")
                                
                            # Format 3: Çift quotes düzeltme
                            cleaned_text = cleaned_text.replace('""', '"')
                            
                            # Eğer JSON formatında geldiyse parse et
                            if cleaned_text.startswith('{') and cleaned_text.endswith('}'):
                                question_data = json.loads(cleaned_text)
                                question_text = question_data.get('question', cleaned_text)
                                expected_answer = question_data.get('expected_answer', '')
                            else:
                                # Düz metin olarak gelirse direkt kullan
                                question_text = cleaned_text
                                expected_answer = ''
                                logger.warning(f"JSON parse edilemedi, düz metin kullanılıyor: {cleaned_text[:100]}...")
                            
                            # Soruyu ekle
                            all_questions[question_type].append({
                                "question": question_text,
                                "expected_answer": expected_answer,
                                "difficulty": difficulty,
                                "role": role_name
                            })
                            
                            logger.info(f"{type_name} sorusu {i+1} ve cevabı başarıyla üretildi")
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON parse hatası: {e}")
                            # JSON parse hatası durumunda düz metin olarak kullan
                            all_questions[question_type].append({
                                "question": generated_text.strip(),
                                "expected_answer": '',
                                "difficulty": difficulty,
                                "role": role_name
                            })
                            logger.info(f"{type_name} sorusu {i+1} başarıyla üretildi (düz metin)")
        
        logger.info("Tüm sorular üretildi")
        return {
            "success": True,
            "questions": all_questions,
            "api_used": "openai"
        }
        
    except Exception as e:
        logger.error(f"Error generating questions with OpenAI API: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "api_used": "openai"
        }


def generate_corrected_question_with_4o_mini(
    model_name: str,
    original_question: str,
    correction_instruction: str,
    job_context: str,
    question_type: str
) -> Dict[str, Any]:
    """
    Tek bir soruyu düzeltme talimatına göre yeniden üret
    """
    logger.info("Tekil soru düzeltme başlatılıyor.")
    
    try:
        # Dinamik soru tiplerini veri tabanından al ve tür isimlerini belirle
        active_question_types = get_active_question_types()
        type_names = {code: name for code, name in active_question_types}
        type_name = type_names.get(question_type, question_type)
        
        # Düzeltme prompt'u oluştur
        prompt = f"""
{job_context}

ÖNCEKİ SORU:
{original_question}

DÜZELTME TALİMATI:
{correction_instruction}

Lütfen yukarıdaki soruyu düzeltme talimatına göre yeniden üret.
Aynı format ve kalitede, sadece istenen değişiklikleri yap.
Kod soruları 2 tipte olsun. 1. tip kodun ne işe yaradığı olabilir. 2. tip ise kodda ki hatayı bulma sorusu olabilir. 


Soru ve Cevap gereksinimleri:
- Özel şartlardan BİR TEK KONU seçerek {type_name} alanında spesifik soru sor
- Eğer düzeltme talimatında konu belirtilmişse o konuya odaklan
- Beklenen cevap jüriyi bilgilendirici tonda yazılmalı (adayın ağzından değil)
- Beklenen cevap şu yapıda olmalı: "Adayın [seçilen konu] hakkında [beklenen bilgi/deneyim] göstermesi beklenir. [Detaylı açıklama ve örnekler]"
- Beklenen cevabın sonuna bir satır boşluk bırakarak anahtar kelimeleri ekle
- Kesinlikle şu JSON formatında döndür (başka format kabul edilmez):

{{"question": "yeni soru", "expected_answer": "yeni cevap\\n\\nAnahtar kelimeler: kelime1, kelime2, kelime3, kelime4"}}

DİKKAT: Anahtar kelimeler expected_answer içinde olmalı, ayrı alan olmamalı!

Düzeltilmiş Soru ve Cevap:"""

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Sen bir İnsan Kaynakları uzmanısın ve sözleşmeli bilişim personeli alımı için kaliteli mülakat soruları hazırlıyorsun. Kavramsal, deneyimsel ve teorik sorular sor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            logger.info("OpenAI API response received for corrected question")
        except Exception as api_error:
            logger.error(f"OpenAI API error for corrected question: {str(api_error)}")
            return {
                "success": False,
                "error": f"API hatası: {str(api_error)}",
                "api_used": "openai"
            }
        
        # Parse the response
        generated_text = response.choices[0].message.content
        
        # Try to extract JSON from the response - IMPROVED
        try:
            # Markdown code block'ları ve diğer formatları temizle
            cleaned_text = generated_text.strip()
            
            # Farklı JSON başlangıçlarını temizle - REGEX ile güçlendirildi
            
            # ```json { ... } ``` formatını temizle
            if '```json' in cleaned_text and '```' in cleaned_text:
                # Regex ile ```json ile ``` arasındaki kısmı çıkar
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', cleaned_text, re.DOTALL)
                if json_match:
                    cleaned_text = json_match.group(1).strip()
            elif cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
            elif cleaned_text.startswith('```'):
                cleaned_text = cleaned_text.replace('```', '').strip()
            elif cleaned_text.startswith('json ('):
                cleaned_text = cleaned_text.replace('json (', '{', 1).strip()
            elif cleaned_text.startswith('"json ('):
                cleaned_text = cleaned_text.replace('"json (', '{', 1).strip()
            
            # JSON içinde başlangıç/bitiş karakterlerini düzelt
            if not cleaned_text.startswith('{') and '{' in cleaned_text:
                # İlk { karakterinden başla
                start_idx = cleaned_text.find('{')
                cleaned_text = cleaned_text[start_idx:]
            
            if not cleaned_text.endswith('}') and '}' in cleaned_text:
                # Son } karakterinde bitir
                end_idx = cleaned_text.rfind('}')
                cleaned_text = cleaned_text[:end_idx+1]
            
            # JSON içindeki yanlış anahtar kelimeler formatını düzelt - SÜPER GÜÇLENDİRİLDİ
            # AI'ın ürettiği en yaygın hatalı formatları yakala ve düzelt:
            
            # Format 1: "expected_answer": "text", "\n\nAnahtar kelimeler: words" }
            pattern1 = r'("expected_answer":\s*"[^"]*"),\s*"(\\n\\nAnahtar kelimeler:[^"]*)"(\s*\})'
            if re.search(pattern1, cleaned_text):
                cleaned_text = re.sub(pattern1, r'\1\2"\3', cleaned_text)
                logger.info("JSON Format 1 düzeltildi (corrected question)")
            
            # Format 2: "text", "\n\nAnahtar kelimeler: words" 
            pattern2 = r'",\s*"(\\n\\nAnahtar kelimeler:[^"]*)"'
            if re.search(pattern2, cleaned_text):
                cleaned_text = re.sub(pattern2, r'\1"', cleaned_text)
                logger.info("JSON Format 2 düzeltildi (corrected question)")
                
            # Format 3: Çift quotes düzeltme
            cleaned_text = cleaned_text.replace('""', '"')
            
            # Eğer JSON formatında geldiyse parse et
            if cleaned_text.startswith('{') and cleaned_text.endswith('}'):
                question_data = json.loads(cleaned_text)
                question_text = question_data.get('question', cleaned_text)
                expected_answer = question_data.get('expected_answer', '')
            else:
                # Düz metin olarak gelirse direkt kullan
                question_text = cleaned_text
                expected_answer = ''
                logger.warning(f"JSON parse edilemedi, düz metin kullanılıyor: {cleaned_text[:100]}...")
            
            logger.info("Tekil soru düzeltme başarıyla tamamlandı")
            
            return {
                "success": True,
                "question": question_text,
                "expected_answer": expected_answer,
                "api_used": "openai"
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse hatası: {e}")
            # JSON parse hatası durumunda düz metin olarak kullan
            return {
                "success": True,
                "question": generated_text.strip(),
                "expected_answer": '',
                "api_used": "openai"
            }
    
    except Exception as e:
        logger.error(f"Error generating corrected question with OpenAI API: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "api_used": "openai"
        }





def format_system_info():
    """Get formatted system information."""
    api_info = check_4o_mini_status()
    
    return {
        "system": {
            "python_version": sys.version,
            "platform": sys.platform
        },
        "api": api_info
    } 
