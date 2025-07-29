import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Step4({ contractId, onNext, onPrevious }) {
    const [questions, setQuestions] = useState([]);
    const [processing, setProcessing] = useState(false);
    const [selectedModel] = useState("gpt-4o-mini");  // OpenAI GPT-4o-mini model
    const [completed, setCompleted] = useState(false);

    useEffect(() => {
        // Eğer daha önce sorular üretilmişse onları yükle
        if (contractId) {
            loadExistingQuestions();
        }
    }, [contractId]);

    const loadExistingQuestions = async () => {
        try {
            const response = await axios.get(`/api/step4/questions/${contractId}`);
            if (response.data.success && response.data.questions) {
                setQuestions(response.data.questions);
                setCompleted(true);
            }
        } catch (error) {
            console.error('Error loading existing questions:', error);
        }
    };

    const generateQuestions = async () => {
        setProcessing(true);
        try {
            const response = await axios.post('/api/step4/generate-questions', {
                contract_id: contractId,
                model_name: selectedModel
            });

            if (response.data.success) {
                // Backend'den gelen veriyi düzgün formata çevir
                const backendQuestions = response.data.questions;
                if (Array.isArray(backendQuestions) && backendQuestions.length > 0) {
                    // Tüm rolleri ve sorularını sakla
                    setQuestions(backendQuestions);
                } else {
                    setQuestions([]);
                }
                setCompleted(true);
            } else {
                alert('Soru üretimi başarısız: ' + response.data.error);
            }
        } catch (error) {
            console.error('Error generating questions:', error);
            alert('Soru üretimi sırasında hata oluştu: ' + error.message);
        } finally {
            setProcessing(false);
        }
    };

    const handleNext = () => {
        if (!completed) {
            const confirmLeave = window.confirm('Sorular henüz üretilmedi. Devam etmek istiyor musunuz?');
            if (!confirmLeave) return;
        }
        onNext(contractId);
    };

    const renderQuestions = () => {
        if (!questions || !Array.isArray(questions) || questions.length === 0) {
            return <p>Henüz soru üretilmedi.</p>;
        }

        return questions.map((role, roleIndex) => (
            <div key={roleIndex} className="role-questions-section">
                <div className="role-header">
                    <h3>{role.role_name}</h3>
                    <div className="role-info">
                        <span className="multiplier-badge" data-multiplier={role.salary_multiplier}>
                            {role.salary_multiplier}x
                        </span>
                    </div>
                </div>
                
                {role.questions && Object.entries(role.questions).map(([type, questionList]) => (
                    <div key={type} className="question-type">
                        <h4>{type === 'professional_experience' ? 'Mesleki Deneyim' : 
                             type === 'theoretical_knowledge' ? 'Teorik Bilgi' : 
                             'Pratik Uygulama'} Soruları</h4>
                        {Array.isArray(questionList) && questionList.map((q, qIndex) => (
                            <div key={qIndex} className="question-item">
                                <p className="question-text">
                                    <span className="question-number">{qIndex + 1}.</span> {q.question}
                                </p>
                                {q.expected_answer && (
                                    <div className="expected-answer">
                                        <h5>Beklenen Cevap:</h5>
                                        <div 
                                            className="answer-content"
                                            dangerouslySetInnerHTML={{ __html: q.expected_answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                                        />
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        ));
    };

    return (
        <div className="step-container">
            <h2>Adım 4: Soru Üretimi</h2>
            
            <div className="step4-description">
                <p>Bu adımda, daha önce belirlenen pozisyon, seviye ve uzmanlık alanı kriterlerine göre mülakat soruları yapay zekâ destekli olarak üretilecektir.</p>
            </div>
            
            <div className="model-info">
                <h4>Kullanılan Model: <span className="model-badge">GPT-4o-mini</span> (OpenAI API – Yüksek Doğruluk)</h4>
                <p>Sorular; belirlenen konfigürasyona göre, yüksek kaliteli doğal dil üretimi sağlayan OpenAI altyapısı üzerinden otomatik olarak oluşturulacaktır.</p>
            </div>

            {!completed ? (
                <div className="generate-section">
                    <button 
                        onClick={generateQuestions} 
                        disabled={processing}
                        className="generate-btn"
                    >
                        {processing ? 'Sorular ve Cevaplar Üretiliyor...' : 'Soruları ve Cevapları Üret'}
                    </button>
                    
                    {processing && (
                        <div className="processing-info">
                            <p>⏳ Sorular üretiliyor, lütfen bekleyin...</p>
                            <p>Bu işlem birkaç dakika sürebilir.</p>
                        </div>
                    )}
                </div>
            ) : (
                <div className="results-section">
                    <h3>Üretilen Sorular</h3>
                    {renderQuestions()}
                </div>
            )}

            {/* Adım Aksiyonları - Her zaman görünür */}
            <div className="step-actions">
                <button 
                    onClick={onPrevious}
                    className="btn-secondary"
                >
                    Önceki Adım
                </button>
                <button 
                    onClick={handleNext}
                    className="btn-primary"
                >
                    Sonraki Adım
                </button>
            </div>
        </div>
    );
}

export default Step4;