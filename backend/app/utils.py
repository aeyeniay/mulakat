"""
Utility functions for the backend application.
"""
from openai import OpenAI
import json
import logging
from typing import Dict, Any, List
import subprocess
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 4o mini API configuration
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
    timeout=60.0,
    max_retries=3
)

# GPU kontrol fonksiyonu

def is_gpu_available():
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

def get_gpu_memory_usage():
    """GPU memory kullanımını kontrol et"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            memory_info = []
            for line in lines:
                if ',' in line:
                    used, total = line.split(',')
                    memory_info.append({
                        "used_mb": int(used.strip()),
                        "total_mb": int(total.strip()),
                        "usage_percent": round((int(used.strip()) / int(total.strip())) * 100, 2)
                    })
            return memory_info
        return None
    except Exception:
        return None

def check_gpu_usage():
    """GPU kullanımını kontrol et"""
    gpu_available = is_gpu_available()
    memory_info = get_gpu_memory_usage()
    
    return {
        "gpu_available": gpu_available,
        "memory_info": memory_info,
        "gpu_using": memory_info and any(m["used_mb"] > 0 for m in memory_info) if memory_info else False
    }


def check_gpu_availability():
    """Check GPU availability and return system information."""
    try:
        # Sadece NVIDIA SMI ile GPU kontrolü (torch olmadan)
        import subprocess
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            gpus = []
            for line in lines:
                name, memory = line.split(',')
                gpus.append({
                    "device_name": name.strip(),
                    "gpu_memory_gb": float(memory.strip().split()[0]) / 1024
                })
            return {
                "cuda_available": True,
                "gpu_count": len(gpus),
                "gpus": gpus
            }
        else:
            return {
                "cuda_available": False,
                "error": result.stderr.strip()
            }
    except Exception as e:
        logger.error(f"Error checking GPU availability: {str(e)}")
        return {
            "cuda_available": False,
            "error": str(e)
        }


def check_4o_mini_status():
    """Check if 4o mini API is available."""
    try:
        # Test API connection
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10
        )
        
        return {
            "api_available": True,
            "model": "4o-mini",
            "status": "connected",
            "test_response": response.choices[0].message.content
        }
    except Exception as e:
        logger.error(f"Error connecting to 4o mini API: {str(e)}")
        return {
            "api_available": False,
            "error": str(e),
            "details": "API bağlantı hatası - timeout veya network sorunu"
        }


def get_available_4o_mini_models():
    """4o mini API modellerini al"""
    try:
        return [
            {
                "name": "4o-mini",
                "display_name": "4o-mini - OpenAI API",
                "size_gb": 0,
                "size_bytes": 0,
                "speed_category": "🚀 API Hızlı",
                "color": "#28a745",
                "recommended": True
            }
        ]
    except Exception as e:
        logger.error(f"Error getting 4o mini models: {str(e)}")
        return [
            {
                "name": "4o-mini",
                "display_name": "4o-mini - OpenAI API",
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
    Generate questions using 4o mini API - tek tek soru üretimi.
    """
    logger.info("4o mini API ile soru üretimi başlatılıyor.")
    
    try:
        # Her soru tipi için ayrı ayrı soru üret
        all_questions = {
            "professional_experience": [],
            "theoretical_knowledge": [],
            "practical_application": []
        }
        
        # Soru tipleri ve sayıları
        question_types = [
            ("professional_experience", "Mesleki Deneyim", question_config.get('professional_experience', 5)),
            ("theoretical_knowledge", "Teorik Bilgi", question_config.get('theoretical_knowledge', 5)),
            ("practical_application", "Pratik Uygulama", question_config.get('practical_application', 5))
        ]
        
        for question_type, type_name, count in question_types:
            logger.info(f"{type_name} soruları üretiliyor: {count} adet")
            
            for i in range(count):
                # Her soru için özel prompt
                prompt = f"""
Sen bir İnsan Kaynakları uzmanısın ve sözleşmeli bilişim personeli alımı için {type_name} kategorisinde KALİTELİ bir mülakat sorusu hazırlıyorsun.

İŞ POSTING BİLGİLERİ:
{job_context}

SORU TİPİ: {type_name}
ZORLUK SEVİYESİ: {question_config.get('difficulty_level', 'Orta')}
SORU NUMARASI: {i+1}/{count}

ÖNEMLI TALİMATLAR:
1. İlanın genel şartlarını ve özel şartlarını DİKKATLİCE analiz et
2. Özel şartlarda geçen teknolojiler, mimariler, araçlar ve yapıları soruya dahil et
3. Rolün maaş katsayısına göre zorluk seviyesini ayarla
4. Sadece JSON formatında cevap ver
5. Soru kaliteli, detaylı ve rolün gereksinimlerine uygun olsun

Lütfen aşağıdaki JSON formatında TEK BİR SORU hazırla:

{{
    "question": "Detaylı ve kaliteli soru metni",
    "type": "{question_type}",
    "difficulty": "kolay|orta|zor"
}}

ÖRNEK SORU YAPISI:
- Mesleki Deneyim: "React Native ile geliştirdiğiniz en karmaşık mobil uygulamanızı anlatın. Hangi teknolojileri kullandınız ve karşılaştığınız zorlukları nasıl çözdünüz?"
- Teorik Bilgi: "Mikroservis mimarisinin avantajları ve dezavantajları nelerdir? Hangi durumlarda tercih edilmelidir?"
- Pratik Uygulama: "Verilen bir API endpoint'ini test etmek için Postman'de nasıl bir test suite oluşturursunuz?"
"""

                        # Generate single question using 4o mini API
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
                    logger.info(f"4o mini API response received for {type_name} sorusu {i+1}")
                except Exception as api_error:
                    logger.error(f"4o mini API error for {type_name} sorusu {i+1}: {str(api_error)}")
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
                    # Find JSON content in the response
                    json_start = generated_text.find('{')
                    json_end = generated_text.rfind('}') + 1
                    
                    if json_start != -1 and json_end != -1:
                        json_content = generated_text[json_start:json_end]
                        
                        # Try to fix common JSON issues
                        json_content = json_content.replace('\n', ' ').replace('\r', ' ')
                        json_content = json_content.replace('},}', '}}').replace(',}', '}')
                        json_content = json_content.replace('},]', '}]').replace(',]', ']')
                        
                        # Try to parse
                        try:
                            question_data = json.loads(json_content)
                            
                            # Soruyu ilgili kategoriye ekle
                            if "question" in question_data and "type" in question_data:
                                all_questions[question_data["type"]].append({
                                    "question": question_data["question"],
                                    "difficulty": question_data.get("difficulty", "orta")
                                })
                                logger.info(f"{type_name} sorusu {i+1} başarıyla üretildi")
                            else:
                                logger.warning(f"{type_name} sorusu {i+1} için geçersiz JSON")
                                
                        except json.JSONDecodeError:
                            logger.warning(f"{type_name} sorusu {i+1} için JSON parsing hatası")
                            # Basit soru oluştur
                            all_questions[question_type].append({
                                "question": f"{type_name} sorusu {i+1} - JSON hatası nedeniyle basit soru",
                                "difficulty": "orta"
                            })
                    else:
                        logger.warning(f"{type_name} sorusu {i+1} için JSON bulunamadı")
                        # Basit soru oluştur
                        all_questions[question_type].append({
                            "question": f"{type_name} sorusu {i+1} - JSON bulunamadı",
                            "difficulty": "orta"
                        })
                        
                except Exception as e:
                    logger.error(f"{type_name} sorusu {i+1} için hata: {str(e)}")
                    # Basit soru oluştur
                    all_questions[question_type].append({
                        "question": f"{type_name} sorusu {i+1} - Hata nedeniyle basit soru",
                        "difficulty": "orta"
                    })
        
        # Tüm sorular üretildi
        logger.info("Tüm sorular üretildi")
        return {
            "success": True,
            "questions": all_questions,
            "model_used": model_name,
            "api_used": "4o_mini"
        }
            
    except Exception as e:
        logger.error(f"Error generating questions with 4o mini API: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "api_used": "4o_mini"
        }


def format_system_info():
    """Get formatted system information."""
    gpu_info = check_gpu_availability()
    api_info = check_4o_mini_status()
    
    return {
        "system": {
            "python_version": sys.version,
            "platform": sys.platform
        },
        "gpu": gpu_info,
        "api": api_info
    } 