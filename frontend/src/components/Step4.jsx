import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Step4({ contractId, onNext, onPrevious }) {
    const [questions, setQuestions] = useState([]);
    const [processing, setProcessing] = useState({});  // Her rol için ayrı processing durumu
    const [selectedModel] = useState("gpt-4o-mini");  // OpenAI GPT-4o-mini model
    const [completed, setCompleted] = useState(false);
    const [roles, setRoles] = useState([]);  // Rolleri saklamak için

    useEffect(() => {
        // Rolleri ve mevcut soruları yükle
        if (contractId) {
            loadRoles();
            loadExistingQuestions();
        }
    }, [contractId]);

    const loadRoles = async () => {
        try {
            const response = await axios.get(`/api/step2/roles/${contractId}`);
            if (response.data.success) {
                setRoles(response.data.roles);
            }
        } catch (error) {
            console.error('Error loading roles:', error);
        }
    };

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

    const generateQuestionsForRole = async (roleId, roleName) => {
        setProcessing(prev => ({ ...prev, [roleId]: true }));
        try {
            const response = await axios.post('/api/step4/generate-questions', {
                contract_id: contractId,
                model_name: selectedModel,
                role_id: roleId  // Sadece bu rol için soru üret
            });

            if (response.data.success) {
                // Mevcut soruları koru, yeni soruları ekle/güncelle
                const backendQuestions = response.data.questions;
                if (Array.isArray(backendQuestions) && backendQuestions.length > 0) {
                    setQuestions(prevQuestions => {
                        // Mevcut soruları filtrele (bu rolün eski sorularını çıkar)
                        const filteredQuestions = prevQuestions.filter(q => q.role_id !== roleId);
                        // Yeni soruları ekle
                        return [...filteredQuestions, ...backendQuestions];
                    });
                }
                setCompleted(true);
            } else {
                alert(`${roleName} için soru üretimi başarısız: ` + response.data.error);
            }
        } catch (error) {
            console.error('Error generating questions:', error);
            alert(`${roleName} için soru üretimi sırasında hata oluştu: ` + error.message);
        } finally {
            setProcessing(prev => ({ ...prev, [roleId]: false }));
        }
    };

    const regenerateQuestionsForRole = async (roleId, roleName) => {
        if (window.confirm(`${roleName} için soruları yeniden üretmek istediğinizden emin misiniz?`)) {
            await generateQuestionsForRole(roleId, roleName);
        }
    };

    const handleNext = () => {
        if (!completed) {
            const confirmLeave = window.confirm('Sorular henüz üretilmedi. Devam etmek istiyor musunuz?');
            if (!confirmLeave) return;
        }
        onNext(contractId);
    };

    const renderQuestionsForRole = (roleId) => {
        const roleQuestions = questions.find(q => q.role_id === roleId);
        if (!roleQuestions) {
            return <p>Bu rol için henüz soru üretilmedi.</p>;
        }

        return (
            <div className="role-questions-section">
                {roleQuestions.questions && Object.entries(roleQuestions.questions).map(([type, questionList]) => (
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
        );
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

            <div className="roles-section">
                <h3>İlanlar ve Soru Üretimi</h3>
                <div className="roles-list">
                    {roles.map((role) => {
                        const hasQuestions = questions.some(q => q.role_id === role.id);
                        const isProcessing = processing[role.id];
                        
                        return (
                            <div key={role.id} className="role-item">
                                <div className="role-card">
                                    <div className="role-header">
                                        <h4>{role.name}</h4>
                                        <div className="role-info">
                                            <span className="multiplier-badge" data-multiplier={role.salary_multiplier}>
                                                {role.salary_multiplier}x
                                            </span>
                                            <span className="position-count">
                                                {role.position_count} pozisyon
                                            </span>
                                        </div>
                                    </div>
                                    
                                    <div className="role-actions">
                                        {!hasQuestions ? (
                                            <button 
                                                onClick={() => generateQuestionsForRole(role.id, role.name)}
                                                disabled={isProcessing}
                                                className="generate-btn"
                                            >
                                                {isProcessing ? 'Üretiliyor...' : 'Soruları Üret'}
                                            </button>
                                        ) : (
                                            <div className="action-buttons">
                                                <button 
                                                    onClick={() => regenerateQuestionsForRole(role.id, role.name)}
                                                    disabled={isProcessing}
                                                    className="regenerate-btn"
                                                >
                                                    {isProcessing ? 'Yeniden Üretiliyor...' : 'Yeniden Üret'}
                                                </button>
                                                <span className="status-badge success">✓ Üretildi</span>
                                            </div>
                                        )}
                                    </div>
                                    
                                    {isProcessing && (
                                        <div className="processing-info">
                                            <p>⏳ {role.name} için sorular üretiliyor...</p>
                                        </div>
                                    )}
                                </div>
                                
                                {/* Bu rol için üretilen soruları göster */}
                                {hasQuestions && (
                                    <div className="role-questions">
                                        {renderQuestionsForRole(role.id)}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>

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