import { useState } from 'react';
import axios from 'axios';

const Step1 = ({ onNext }) => {
  const [formData, setFormData] = useState({
    title: '',
    general_requirements: ''
  });
  const [loading, setLoading] = useState(false);
  const [warning, setWarning] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setWarning(null);
    
    try {
      const requestData = {
        title: formData.title || 'Sözleşmeli Bilişim Personeli Alımı',
        content: 'İlan içeriği (otomatik oluşturuldu)',
        general_requirements: formData.general_requirements
      };
      
      const response = await axios.post('http://localhost:8000/api/step1/save-contract', requestData);
      
      if (response.data.success === false && response.data.warning) {
        // Uyarı göster
        setWarning(response.data);
      } else if (response.data.success === true) {
        // Başarılı - sonraki adıma geç
        onNext(response.data.contract.id);
      } else {
        // Beklenmeyen durum
        console.error('Unexpected response:', response.data);
        alert('Beklenmeyen bir yanıt alındı');
      }
    } catch (error) {
      console.error('Error saving contract:', error);
      
      // Detaylı hata mesajı
      if (error.response) {
        console.error('Response error:', error.response.data);
        alert(`Hata: ${error.response.data.detail || error.response.data.message || 'Bilinmeyen hata'}`);
      } else if (error.request) {
        console.error('Request error:', error.request);
        alert('Sunucuya erişim sağlanamadı. Backend çalışıyor mu?');
      } else {
        console.error('Generic error:', error.message);
        alert('Beklenmeyen bir hata oluştu');
      }
    } finally {
      setLoading(false);
    }
  };



  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="step-container">
      <h2>Adım 1: İlan Bilgilerini Girin</h2>
      
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label htmlFor="title">İlan Başlığı:</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Örn: Sözleşmeli Bilişim Personeli Alımı"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="general_requirements">Genel Şartlar:</label>
          <textarea
            id="general_requirements"
            name="general_requirements"
            value={formData.general_requirements}
            onChange={handleChange}
            placeholder="Genel şartları buraya yazın..."
            rows="10"
            required
          />
        </div>

        {warning && (
          <div className="warning-message">
            <div className="warning-content">
              <h4>⚠️ Aynı İlan Adı Bulundu</h4>
              <p>'{warning.existing_contract.title}' adında bir ilan zaten mevcut.</p>
              <p><strong>Mevcut İlan ID:</strong> {warning.existing_contract.id}</p>
              <p><strong>Oluşturulma:</strong> {new Date(warning.existing_contract.created_at).toLocaleString('tr-TR')}</p>
              <p><strong>Lütfen farklı bir ilan adı girin.</strong></p>
              
              <div className="warning-actions">
                <button 
                  type="button" 
                  onClick={() => setWarning(null)}
                  className="btn-primary"
                >
                  Tamam
                </button>
              </div>
            </div>
          </div>
        )}

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Kaydediliyor...' : 'Kaydet ve Devam Et'}
        </button>
      </form>
    </div>
  );
};

export default Step1; 