import { useState, useEffect } from 'react';
import axios from 'axios';

const Step3 = ({ contractId, onNext, onPrevious }) => {
  const [globalConfig, setGlobalConfig] = useState({
    candidate_multiplier: 10,
    questions_per_candidate: 5,
    question_type_distribution: {}
  });
  const [roleConfigs, setRoleConfigs] = useState([]);
  const [availableQuestionTypes, setAvailableQuestionTypes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [globalConfigSaved, setGlobalConfigSaved] = useState(false);

  // Global konfigürasyonu yükle
  useEffect(() => {
    const fetchGlobalConfig = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/step3/global-config/${contractId}`);
        if (response.data.success) {
          setGlobalConfig(response.data.global_config);
          setAvailableQuestionTypes(response.data.available_question_types);
          setGlobalConfigSaved(true);
        }
      } catch (error) {
        console.error('Error fetching global config:', error);
      }
    };

    if (contractId) {
      fetchGlobalConfig();
    }
  }, [contractId]);

  // Soru tiplerini yükle - artık global config ile birlikte geliyor

  // Rol konfigürasyonlarını yükle (sadece global config kaydedildikten sonra)
  useEffect(() => {
    const fetchRoleConfigs = async () => {
      if (!globalConfigSaved) return;
      
      try {
        const response = await axios.get(`http://localhost:8000/api/step3/role-question-configs/${contractId}`);
        if (response.data.success) {
          setRoleConfigs(response.data.role_configs);
          setHasUnsavedChanges(false);
        }
      } catch (error) {
        console.error('Error fetching role configs:', error);
      }
    };

    if (contractId && globalConfigSaved) {
      fetchRoleConfigs();
    }
  }, [contractId, globalConfigSaved]);

  // Global konfigürasyon değişikliği
  const handleGlobalConfigChange = (field, value) => {
    setGlobalConfig(prev => ({
      ...prev,
      [field]: parseInt(value)
    }));
    setHasUnsavedChanges(true);
  };

  // Soru türü dağılımı değişikliği
  const handleQuestionTypeDistributionChange = (questionTypeCode, value) => {
    setGlobalConfig(prev => ({
      ...prev,
      question_type_distribution: {
        ...prev.question_type_distribution,
        [questionTypeCode]: parseInt(value)
      }
    }));
    setHasUnsavedChanges(true);
  };

  // Global konfigürasyonu kaydet
  const saveGlobalConfig = async () => {
    setLoading(true);
    
    try {
      const response = await axios.post('http://localhost:8000/api/step3/save-global-config', {
        contract_id: contractId,
        ...globalConfig
      });
      
      if (response.data.success) {
        setSaveStatus('Global sınav ayarları kaydedildi!');
        setGlobalConfigSaved(true);
        setHasUnsavedChanges(false);
        
        // Rol konfigürasyonlarını yeniden yükle
        const roleResponse = await axios.get(`http://localhost:8000/api/step3/role-question-configs/${contractId}`);
        if (roleResponse.data.success) {
          setRoleConfigs(roleResponse.data.role_configs);
        }
        
        setTimeout(() => setSaveStatus(''), 3000);
      }
    } catch (error) {
      console.error('Error saving global config:', error);
      setSaveStatus('Ayarlar kaydedilirken hata oluştu!');
      setTimeout(() => setSaveStatus(''), 3000);
    } finally {
      setLoading(false);
    }
  };

  // Soru sayısını değiştir
  const changeQuestionCount = (roleIndex, questionTypeIndex, newCount) => {
    setRoleConfigs(prevConfigs => {
      const newConfigs = [...prevConfigs];
      newConfigs[roleIndex].question_types[questionTypeIndex].question_count = parseInt(newCount);
      return newConfigs;
    });
    setHasUnsavedChanges(true);
  };

  // Rol konfigürasyonlarını kaydet
  const saveRoleConfigs = async () => {
    setLoading(true);
    
    try {
      for (const roleConfig of roleConfigs) {
        for (const questionType of roleConfig.question_types) {
          await axios.post('http://localhost:8000/api/step3/save-role-question-config', {
            role_id: roleConfig.role_id,
            question_type_id: questionType.question_type_id,
            question_count: questionType.question_count
          });
        }
      }
      
      setSaveStatus('Soru konfigürasyonları kaydedildi!');
      setHasUnsavedChanges(false);
      setTimeout(() => setSaveStatus(''), 3000);
    } catch (error) {
      console.error('Error saving role configs:', error);
      setSaveStatus('Konfigürasyonlar kaydedilirken hata oluştu!');
      setTimeout(() => setSaveStatus(''), 3000);
    } finally {
      setLoading(false);
    }
  };

  // Sonraki adıma geç
  const handleNext = async () => {
    if (hasUnsavedChanges) {
      const confirmLeave = window.confirm('Değişiklikler kaydedilmedi. Kaydetmeden devam etmek istiyor musunuz?');
      if (!confirmLeave) return;
    }
    
    onNext(contractId);
  };

  // Formülün açıklaması
  const calculateTotalQuestions = () => {
    return roleConfigs.reduce((total, role) => {
      return total + role.question_types.reduce((roleTotal, qt) => roleTotal + qt.question_count, 0);
    }, 0);
  };

  // Toplam soru türü dağılımını hesapla
  const getTotalDistribution = () => {
    return Object.values(globalConfig.question_type_distribution || {}).reduce((sum, count) => sum + count, 0);
  };

  return (
    <div className="step-container">
      <h2>Adım 3: Sınav ve Soru Konfigürasyonu</h2>
      
      {/* Global Sınav Ayarları */}
      <div className="global-config-section">
        <h3>🎯 Genel Sınav Ayarları</h3>
        <p className="config-description">
          Bu ayarlar tüm roller için geçerli olacak temel sınav parametrelerini belirler.
        </p>
        
        <div className="global-config-form">
          <div className="config-row">
            <div className="config-group">
              <label>Her pozisyon için kaç aday çağırılacak?</label>
              <input
                type="number"
                min="1"
                max="20"
                value={globalConfig.candidate_multiplier}
                onChange={(e) => handleGlobalConfigChange('candidate_multiplier', e.target.value)}
                className="config-input"
              />
              <small>Örn: 10 → Her 1 pozisyon için 10 aday</small>
            </div>
            
            <div className="config-group">
              <label>Her adaya toplam kaç soru sorulacak?</label>
              <input
                type="number"
                min="3"
                max="10"
                value={globalConfig.questions_per_candidate}
                onChange={(e) => handleGlobalConfigChange('questions_per_candidate', e.target.value)}
                className="config-input"
              />
              <small>Mülakata girecek her aday için</small>
            </div>
          </div>
          
          {availableQuestionTypes.length > 0 && (
            <div className="question-distribution">
              <h4>📋 Soru Türü Dağılımı (Her aday için)</h4>
              <div className="distribution-row">
                {availableQuestionTypes.map((questionType) => (
                  <div key={questionType.id} className="distribution-group">
                    <label>{questionType.name}:</label>
                    <input
                      type="number"
                      min="0"
                      max={globalConfig.questions_per_candidate}
                      value={globalConfig.question_type_distribution?.[questionType.code] || 0}
                      onChange={(e) => handleQuestionTypeDistributionChange(questionType.code, e.target.value)}
                      className="distribution-input"
                    />
                    <small>{questionType.description}</small>
                  </div>
                ))}
              </div>
              
              <div className="distribution-check">
                <strong>Toplam: </strong>
                {getTotalDistribution()} / {globalConfig.questions_per_candidate}
                {getTotalDistribution() !== globalConfig.questions_per_candidate && (
                  <span className="distribution-warning"> ⚠️ Toplam eşleşmiyor!</span>
                )}
              </div>
            </div>
          )}
          
          <button 
            onClick={saveGlobalConfig}
            className="btn-save-global"
            disabled={loading}
          >
            {loading ? 'Kaydediliyor...' : 'Ayarları Kaydet ve Hesapla'}
          </button>
        </div>
      </div>
      
      {/* Rol Bazlı Soru Hesaplaması */}
      {globalConfigSaved && roleConfigs.length > 0 && (
        <div className="role-configs-section">
          <h3>📊 Rol Bazlı Soru Hesaplaması</h3>
          <p className="calculation-description">
            Global ayarlara göre her rol için otomatik hesaplanmış soru sayıları. İsterseniz manuel olarak düzenleyebilirsiniz.
          </p>
          
          <div className="roles-grid">
            {roleConfigs.map((roleConfig, roleIndex) => (
              <div key={roleConfig.role_id} className="role-config-card">
                <div className="role-config-header">
                  <div className="role-title-section">
                    <h4>{roleConfig.role_name}</h4>
                    <span className="position-calculation">
                      {roleConfig.position_count} pozisyon × {globalConfig.candidate_multiplier} = {roleConfig.candidate_count} aday
                    </span>
                  </div>
                  <span className="multiplier-badge" data-multiplier={roleConfig.salary_multiplier}>
                    {roleConfig.salary_multiplier}x
                  </span>
                </div>
                
                <div className="question-types-grid">
                  {roleConfig.question_types.map((questionType, questionTypeIndex) => (
                    <div key={questionType.question_type_id} className="question-type-card">
                      <div className="question-type-header">
                        <h5>{questionType.question_type_name}</h5>
                        <div className="calculation-formula">
                          {roleConfig.candidate_count} aday × {
                            globalConfig.question_type_distribution?.[questionType.question_type_code] || 1
                          } soru
                        </div>
                      </div>
                      
                      <div className="question-count-section">
                        <label>Üretilecek Soru Sayısı:</label>
                        <input
                          type="number"
                          min="1"
                          max="200"
                          value={questionType.question_count}
                          onChange={(e) => changeQuestionCount(roleIndex, questionTypeIndex, e.target.value)}
                          className="question-count-input"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          
          {/* Özet Bilgileri */}
          <div className="summary-section">
            <h4>📈 Özet</h4>
            <div className="summary-stats">
              <div className="stat-item">
                <span className="stat-label">Toplam Rol:</span>
                <span className="stat-value">{roleConfigs.length}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Toplam Pozisyon:</span>
                <span className="stat-value">
                  {roleConfigs.reduce((total, role) => total + role.position_count, 0)}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Toplam Aday:</span>
                <span className="stat-value">
                  {roleConfigs.reduce((total, role) => total + role.candidate_count, 0)}
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Üretilecek Soru:</span>
                <span className="stat-value">{calculateTotalQuestions()}</span>
              </div>
            </div>
          </div>
          
          <button 
            onClick={saveRoleConfigs}
            className="btn-save-roles"
            disabled={loading}
          >
            {loading ? 'Kaydediliyor...' : 'Soru Konfigürasyonlarını Kaydet'}
          </button>
        </div>
      )}
      
      {/* Durum Mesajları */}
      {saveStatus && (
        <div className={`status-message ${saveStatus.includes('hata') ? 'error' : 'success'}`}>
          {saveStatus}
        </div>
      )}

      {/* Adım Aksiyonları */}
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
          disabled={!globalConfigSaved || roleConfigs.length === 0}
        >
          Sonraki Adıma Geç
        </button>
      </div>
    </div>
  );
};

export default Step3; 