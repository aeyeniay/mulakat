import { useState } from 'react';
import Step1 from './components/Step1';
import Step2 from './components/Step2';
import Step3 from './components/Step3';
import Step4 from './components/Step4';
import Step5 from './components/Step5';
import logoImage from './assets/logo.png';
import './App.css';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [contractId, setContractId] = useState(null);

  const handleStep1Complete = (id) => {
    setContractId(id);
    setCurrentStep(2);
  };

  const handleStep2Complete = (id) => {
    setCurrentStep(3);
  };
                                            
  const handleStep3Complete = (id) => {
    setCurrentStep(4);
  };

  const handleStep4Complete = (id) => {
    setCurrentStep(5);
  };

  const handleStep5Complete = (id) => {
    // Step 5 tamamlandı, işlem bitti
    alert('Mülakat soru seti başarıyla oluşturuldu!');
  };

  // Önceki adıma geçiş fonksiyonu
  const goToPreviousStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  // Step'e tıklama fonksiyonu
  const handleStepClick = (stepNumber) => {
    if (stepNumber === currentStep) return; // Aynı step'e tıklanırsa hiçbir şey yapma
    
    // Eğer geriye gidiyorsa (daha küçük step'e) direkt geç
    if (stepNumber < currentStep) {
      setCurrentStep(stepNumber);
      return;
    }
    
    // İleriye gidiyorsa (daha büyük step'e) onay iste
    const confirmed = window.confirm(
      `Adım ${stepNumber}'e geçmek istediğinizden emin misiniz? ` +
      'Bu adıma geçmek için önceki adımları tamamlamanız gerekebilir.'
    );
    
    if (confirmed) {
      setCurrentStep(stepNumber);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return <Step1 onNext={handleStep1Complete} />;
      case 2:
        return <Step2 contractId={contractId} onNext={handleStep2Complete} onPrevious={goToPreviousStep} />;
      case 3:
        return <Step3 contractId={contractId} onNext={handleStep3Complete} onPrevious={goToPreviousStep} />;
      case 4:
        return <Step4 contractId={contractId} onNext={handleStep4Complete} onPrevious={goToPreviousStep} />;
      case 5:
        return <Step5 contractId={contractId} onNext={handleStep5Complete} onPrevious={goToPreviousStep} />;
      default:
        return <Step1 onNext={handleStep1Complete} />;
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <img src={logoImage} alt="Logo" className="logo" />
            <div className="institution-name">Coğrafi Bilgi Sistemleri Genel Müdürlüğü</div>
            <div className="department-name">Yapay Zeka ve Yenilikçi Teknolojiler Daire Başkanlığı</div>
          </div>
          <h1>Sözleşmeli Personel Alımı – Mülakat Sorusu Hazırlama Arayüzü</h1>
          <div className="step-indicator">
            <div className="steps">
              {[
                { number: 1, title: 'İlan Bilgileri' },
                { number: 2, title: 'Rol Tanımları' },
                { number: 3, title: 'Soru Konfigürasyonu' },
                { number: 4, title: 'Soru Üretimi' },
                { number: 5, title: 'Final Seti' }
              ].map(step => (
                <div 
                  key={step.number}
                  className={`step ${currentStep === step.number ? 'active' : currentStep > step.number ? 'completed' : ''}`}
                  onClick={() => handleStepClick(step.number)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="step-number">{step.number}</div>
                  <div className="step-title">{step.title}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main className="app-main">
        {renderStep()}
      </main>

      <footer className="app-footer">
        <p>İlan ID: {contractId || 'Henüz oluşturulmadı'}</p>
      </footer>
    </div>
  );
}

export default App;
