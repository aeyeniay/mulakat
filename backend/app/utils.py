"""
Utility functions for the backend application.
"""
from openai import OpenAI
import json
import logging
from typing import Dict, Any, List
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            
            # Her soru tipi için soruları üret
            for question_type, type_name in [
                ("professional_experience", "Mesleki Deneyim"),
                ("theoretical_knowledge", "Teorik Bilgi"),
                ("practical_application", "Pratik Uygulama")
            ]:
                # question_config bir dict değilse default değer kullan
                if isinstance(question_config, dict):
                    question_count = question_config.get(question_type, 5)
                else:
                    question_count = 5
                
                if question_count > 0:
                    logger.info(f"{type_name} soruları üretiliyor: {question_count} adet")
                    
                    for i in range(question_count):
                        # Her soru için ayrı prompt oluştur - Profesyonel Rubrik Modeli
                        prompt = f"""
İlan Başlığı: {job_context}

Pozisyon: {role_name}
Pozisyon Sayısı: {position_count}
Maaş Katsayısı: {salary_coefficient}x
Zorluk Seviyesi: {difficulty}

Özel Şartlar: {special_requirements}

Görev: {type_name} kategorisinde {i+1}. soruyu ve beklenen cevabını üret.

PROFESYONEL RUBRİK MODELİ - Zorluk Katmanları:
K1: Temel Bilgi - Tanım, sözdizimi, kavram (Remember/Novice)
K2: Uygulamalı - Küçük kod-konfig yazma, CLI komutu, basit hesap (Apply/Advanced Beginner)
K3: Hata Çözümleme - Gerçek log/kod verip sorun bulma (Analyze/Competent)
K4: Tasarım - Komponent diyagramı, ölçeklenir mimari, best-practice seçimi (Evaluate/Proficient)
K5: Stratejik & Liderlik - Trade-off analizi, roadmap, takım-proses optimizasyonu (Create/Expert)

Soru ve Cevap gereksinimleri:
- {type_name} alanında spesifik ve detaylı bir soru olmalı
- Zorluk seviyesi: {difficulty} ({salary_coefficient}x seviyesine uygun katmanlarda)
- Pozisyonun özel şartlarına uygun olmalı
- Beklenen cevap jüriyi bilgilendirici tonda yazılmalı (adayın ağzından değil)
- Beklenen cevap şu yapıda olmalı: "Adayın [konu] hakkında [beklenen bilgi/deneyim] göstermesi beklenir. [Detaylı açıklama ve örnekler]"
- Kod örnekleri varsa markdown kod bloğu formatında yazılmalı: ```yaml veya ```bash gibi
- JSON formatında döndür: {{"question": "soru metni", "expected_answer": "beklenen cevap"}}

Soru ve Beklenen Cevap:"""

                        try:
                            response = client.chat.completions.create(
                                model=model_name,
                                messages=[
                                    {"role": "system", "content": "Sen bir İnsan Kaynakları uzmanısın ve sözleşmeli bilişim personeli alımı için kaliteli mülakat soruları hazırlıyorsun."},
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
                        
                        # Try to extract JSON from the response
                        try:
                            # Markdown code block'ları temizle
                            cleaned_text = generated_text.strip()
                            if cleaned_text.startswith('```json'):
                                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
                            elif cleaned_text.startswith('```'):
                                cleaned_text = cleaned_text.replace('```', '').strip()
                            
                            # Eğer JSON formatında geldiyse parse et
                            if cleaned_text.startswith('{'):
                                question_data = json.loads(cleaned_text)
                                question_text = question_data.get('question', cleaned_text)
                                expected_answer = question_data.get('expected_answer', '')
                            else:
                                # Düz metin olarak gelirse direkt kullan
                                question_text = cleaned_text
                                expected_answer = ''
                            
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
        # Tür isimlerini belirle
        type_names = {
            'professional_experience': 'Mesleki Deneyim',
            'theoretical_knowledge': 'Teorik Bilgi',
            'practical_application': 'Pratik Uygulama'
        }
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

Soru ve Cevap gereksinimleri:
- {type_name} alanında spesifik ve detaylı bir soru olmalı
- Beklenen cevap jüriyi bilgilendirici tonda yazılmalı (adayın ağzından değil)
- Beklenen cevap şu yapıda olmalı: "Adayın [konu] hakkında [beklenen bilgi/deneyim] göstermesi beklenir. [Detaylı açıklama ve örnekler]"
- Kod örnekleri varsa markdown kod bloğu formatında yazılmalı: ```yaml veya ```bash gibi
- JSON formatında döndür: {{"question": "yeni soru", "expected_answer": "yeni cevap"}}

Düzeltilmiş Soru ve Cevap:"""

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Sen bir İnsan Kaynakları uzmanısın ve sözleşmeli bilişim personeli alımı için kaliteli mülakat soruları hazırlıyorsun."},
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
        
        # Try to extract JSON from the response
        try:
            # Markdown code block'ları temizle
            cleaned_text = generated_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
            elif cleaned_text.startswith('```'):
                cleaned_text = cleaned_text.replace('```', '').strip()
            
            # Eğer JSON formatında geldiyse parse et
            if cleaned_text.startswith('{'):
                question_data = json.loads(cleaned_text)
                question_text = question_data.get('question', cleaned_text)
                expected_answer = question_data.get('expected_answer', '')
            else:
                # Düz metin olarak gelirse direkt kullan
                question_text = cleaned_text
                expected_answer = ''
            
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
