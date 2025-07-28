import { useState, useEffect } from 'react';
import axios from 'axios';

const Step5 = ({ contractId, onNext, onPrevious }) => {
  const [loading, setLoading] = useState(false);
  const [contractData, setContractData] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [selectedQuestions, setSelectedQuestions] = useState([]);
  const [completed, setCompleted] = useState(false);

  // Contract bilgilerini yükle
  useEffect(() => {
    const fetchContractData = async () => {
      try {
        setLoading(true);
        
        // Contract bilgilerini al
        const contractResponse = await axios.get(`http://localhost:8000/api/step1/contract/${contractId}`);
        if (contractResponse.data.success) {
          setContractData(contractResponse.data.contract);
        }
        
        // Üretilen soruları al
        const questionsResponse = await axios.get(`http://localhost:8000/api/step4/questions/${contractId}`);
        if (questionsResponse.data.success) {
          setQuestions(questionsResponse.data.questions_by_role);
        }
        
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (contractId) {
      fetchContractData();
    }
  }, [contractId]);

  // Soru seçimi
  const handleQuestionSelect = (questionId, isSelected) => {
    if (isSelected) {
      setSelectedQuestions(prev => [...prev, questionId]);
    } else {
      setSelectedQuestions(prev => prev.filter(id => id !== questionId));
    }
  };

  // Final soru setini oluştur
  const createFinalQuestionSet = async () => {
    if (selectedQuestions.length === 0) {
      alert('Lütfen en az bir soru seçin');
      return;
    }

    setCompleted(true);
    // Burada final soru seti oluşturma işlemi yapılabilir
  };

  return (
    <div className="step-container">
      <h2>Adım 5: Final Soru Seti Oluşturma</h2>
      
      <div className="step5-description">
        <p>Üretilen sorulardan final mülakat setini oluşturun.</p>
      </div>

      {loading ? (
        <div className="loading-message">
          <p>Veriler yükleniyor...</p>
        </div>
      ) : (
        <>
          {/* Contract Bilgisi */}
          {contractData && (
            <div className="contract-info">
              <h3>İlan Bilgileri</h3>
              <p><strong>Başlık:</strong> {contractData.title}</p>
            </div>
          )}

          {/* Soru Seçimi */}
          <div className="question-selection">
            <h3>Soru Seçimi</h3>
            <p>Final mülakat seti için soruları seçin:</p>
            
            {questions.map((roleData, roleIndex) => (
              <div key={roleIndex} className="role-questions-section">
                <h4>{roleData.role_name}</h4>
                
                {Object.entries(roleData.questions || {}).map(([type, questions]) => (
                  <div key={type} className="question-type-section">
                    <h5>{type === 'professional_experience' ? 'Mesleki Deneyim' : 
                         type === 'theoretical_knowledge' ? 'Teorik Bilgi' : 
                         'Pratik Uygulama'} Soruları</h5>
                    
                    {questions.map((question, qIndex) => (
                      <div key={qIndex} className="question-item-selectable">
                        <label className="question-checkbox">
                          <input
                            type="checkbox"
                            checked={selectedQuestions.includes(question.id)}
                            onChange={(e) => handleQuestionSelect(question.id, e.target.checked)}
                          />
                          <span className="question-text">{question.question}</span>
                        </label>
                        <div className="question-details">
                          <span className="difficulty-badge">{question.difficulty}</span>
                          {question.expected_answer && (
                            <span className="has-answer">Beklenen Cevap Var</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            ))}
          </div>

          {/* Seçim Özeti */}
          <div className="selection-summary">
            <h3>Seçim Özeti</h3>
            <p>Seçilen soru sayısı: <strong>{selectedQuestions.length}</strong></p>
          </div>

          {/* Navigation */}
          <div className="step-navigation">
            <button onClick={onPrevious} className="nav-button">
              ← Önceki Adım
            </button>
            <button 
              onClick={createFinalQuestionSet} 
              className="nav-button primary"
              disabled={selectedQuestions.length === 0}
            >
              Final Seti Oluştur
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Step5; 