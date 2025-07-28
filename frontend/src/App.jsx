import { useState } from 'react';
import Step1 from './components/Step1';
import Step2 from './components/Step2';
import Step3 from './components/Step3';
import Step4 from './components/Step4';
import Step5 from './components/Step5';
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
        <h1>Mülakat Sorusu Hazırlama Sistemi</h1>
        <div className="step-indicator">
          <div className="steps">
            {[1, 2, 3, 4, 5].map(step => (
              <div 
                key={step}
                className={`step ${currentStep === step ? 'active' : currentStep > step ? 'completed' : ''}`}
              >
                {step}
              </div>
            ))}
          </div>
        </div>
      </header>

      <main className="app-main">
        {renderStep()}
      </main>

      <footer className="app-footer">
        <p>Contract ID: {contractId || 'Henüz oluşturulmadı'}</p>
      </footer>
    </div>
  );
}

export default App;
