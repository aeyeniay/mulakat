import { useState, useEffect } from 'react';
import axios from 'axios';

const Step4 = ({ contractId, onNext, onPrevious }) => {
  const [loading, setLoading] = useState(false);
  const [contractData, setContractData] = useState(null);
  const [roles, setRoles] = useState([]);
  const [configs, setConfigs] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [selectedModel] = useState("gpt-4o-mini");  // OpenAI GPT-4o-mini model
  const [completed, setCompleted] = useState(false);
  const [gpuUsed, setGpuUsed] = useState(false);

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
        
        // Role bilgilerini al
        const rolesResponse = await axios.get(`http://localhost:8000/api/step2/roles/${contractId}`);
        if (rolesResponse.data.success) {
          setRoles(rolesResponse.data.roles);
        }
        
        // Role config bilgilerini al
        const configsResponse = await axios.get(`http://localhost:8000/api/step3/role-question-configs/${contractId}`);
        if (configsResponse.data.success) {
          setConfigs(configsResponse.data.role_configs);
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

  // Direkt soru üretimi
  const generateQuestions = async () => {
    setProcessing(true);
    
    try {
      const response = await axios.post('http://localhost:8000/api/step4/generate-questions', {
        contract_id: contractId,
        model_name: selectedModel
      });
      
      if (response.data.success) {
        setQuestions(response.data.questions);
        setCompleted(true);
        // GPU kullanım bilgisini al
        const gpuUsed = response.data.questions.some(q => q.gpu_used);
        setGpuUsed(gpuUsed);
      } else {
        alert('Soru üretimi sırasında hata oluştu');
      }
      
    } catch (error) {
      console.error('Error generating questions:', error);
      alert('Soru üretimi sırasında hata oluştu');
    } finally {
      setProcessing(false);
    }
  };

  // Üretilen soruları görüntüle
  const viewGeneratedQuestions = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/step4/questions/${contractId}`);
      if (response.data.success) {
        setQuestions(response.data.questions_by_role);
        setCompleted(true);
      }
    } catch (error) {
      console.error('Error fetching questions:', error);
    }
  };

  // Sonraki adıma geç
  const handleNext = () => {
    if (!completed) {
      alert('Lütfen önce soruları üretin');
      return;
    }
    onNext(contractId);
  };

  return (
    <div className="step-container">
      <h2>Adım 4: Soru Üretimi</h2>
      
      <div className="step4-description">
        <p>Bu adımda AI modeliyle genel şartlar ve rol özel şartlarına dayanarak mülakat soruları üretilir.</p>
      </div>

      {loading ? (
        <div className="loading-message">
          <p>Veriler yükleniyor...</p>
        </div>
      ) : (
        <>
          {/* AI Model Bilgisi */}
          <div className="model-info-section">
            <h3>Kullanılan AI Modeli</h3>
            <div className="model-details">
              <input 
                type="text" 
                value={selectedModel} 
                readOnly 
                className="model-input"
              />
                             <div className="model-description">
                 GPU Destekli • 27B Parametre • Yüksek Kalite
               </div>
            </div>
          </div>

          {/* Soru Üretimi */}
          <div className="question-generation-section">
            <h3>Soru Üretimi Başlat</h3>
            <p>Bu işlem genel şartlar ve rol özel şartlarını analiz ederek, her rol için mülakat soruları üretecek.</p>
            
            <button 
              onClick={generateQuestions}
              disabled={processing}
              className="generate-button"
            >
              {processing ? 'Sorular Üretiliyor...' : '🚀 Soruları Üret'}
            </button>

            {completed && (
              <button 
                onClick={viewGeneratedQuestions}
                className="view-questions-button"
              >
                📋 Üretilen Soruları Görüntüle
              </button>
            )}
          </div>

          {/* GPU Kullanım Bilgisi */}
          {completed && (
            <div className="gpu-info">
              <p>
                {gpuUsed ? '✅ GPU ile çalıştırıldı' : '⚠️ CPU ile çalıştırıldı'}
              </p>
            </div>
          )}

          {/* Üretilen Sorular */}
          {questions.length > 0 && (
            <div className="questions-display">
              <h3>Üretilen Sorular</h3>
              {questions.map((roleData, index) => (
                <div key={index} className="role-questions">
                  <h4>{roleData.role_name}</h4>
                  
                  {roleData.error ? (
                    <div className="error-message">
                      <p>Hata: {roleData.error}</p>
                    </div>
                  ) : (
                    <div className="questions-by-type">
                      {Object.entries(roleData.questions || {}).map(([type, questions]) => (
                        <div key={type} className="question-type">
                          <h5>{type === 'professional_experience' ? 'Mesleki Deneyim' : 
                               type === 'theoretical_knowledge' ? 'Teorik Bilgi' : 
                               'Pratik Uygulama'} Soruları</h5>
                          {questions.map((q, qIndex) => (
                            <div key={qIndex} className="question-item">
                              <p><strong>Soru {qIndex + 1}:</strong> {q.question}</p>
                              <p><strong>Zorluk:</strong> {q.difficulty}</p>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Navigation */}
          <div className="step-navigation">
            <button onClick={onPrevious} className="nav-button">
              ← Önceki Adım
            </button>
            <button 
              onClick={handleNext} 
              className="nav-button primary"
              disabled={!completed}
            >
              Sonraki Adım →
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Step4; 