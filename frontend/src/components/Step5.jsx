import React, { useState } from 'react';
import axios from 'axios';

function Step5({ contractId, onPrevious }) {
    const [downloading, setDownloading] = useState(false);
    const [error, setError] = useState(null);
    const [completed, setCompleted] = useState(false);

    const downloadWordDocument = async () => {
        setDownloading(true);
        setError(null);
        
        try {
            const response = await axios.post('/api/step5/generate-word', {
                contract_id: contractId
            }, {
                responseType: 'blob' // Dosya indirme için gerekli
            });
            
            // Dosyayı indir
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            
            // Dosya adını response header'dan al veya default kullan
            const contentDisposition = response.headers['content-disposition'];
            let filename = 'mulakat_sorulari.docx';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="(.+)"/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }
            
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
            
            // Başarılı indirme sonrası tamamlandı mesajını göster
            setCompleted(true);
            
        } catch (error) {
            console.error('Word dosyası indirme hatası:', error);
            setError('Word dosyası indirilirken bir hata oluştu. Lütfen tekrar deneyin.');
        } finally {
            setDownloading(false);
        }
    };

    return (
        <div className="step-container">
            <h2>Adım 5: Final Seti</h2>
            
            <div className="step5-description">
                <p>Tebrikler! Mülakat sorularınız başarıyla üretildi. Şimdi bu soruları Word dosyası olarak indirebilirsiniz.</p>
            </div>
            
            <div className="download-section">
                <h3>Word Dosyası İndirme</h3>
                <p>Üretilen soruları profesyonel bir Word dosyası formatında indirin. Dosya şunları içerecek:</p>
                
                <ul className="features-list">
                    <li>✓ İlan bilgileri ve kurum detayları</li>
                    <li>✓ Her pozisyon için ayrı bölüm</li>
                    <li>✓ Soru kategorileri (Mesleki Deneyim, Teorik Bilgi, Pratik Uygulama)</li>
                    <li>✓ Numaralandırılmış sorular</li>
                    <li>✓ Zorluk seviyeleri</li>
                    <li>✓ Profesyonel format ve düzen</li>
                </ul>
                
                <button 
                    onClick={downloadWordDocument} 
                    disabled={downloading}
                    className="download-btn"
                >
                    {downloading ? 'Dosya Hazırlanıyor...' : 'Word Dosyasını İndir'}
                </button>
                
                {error && (
                    <div className="error-message">
                        <p>❌ {error}</p>
                    </div>
                )}
                
                {downloading && (
                    <div className="processing-info">
                        <p>⏳ Word dosyası hazırlanıyor, lütfen bekleyin...</p>
                    </div>
                )}
            </div>
            
            {completed && (
                <div className="completion-message">
                    <h3>🎉 İşlem Tamamlandı!</h3>
                    <p>Mülakat sorularınız başarıyla oluşturuldu ve Word dosyası olarak indirildi. Bu dosyayı mülakat sürecinizde kullanabilirsiniz.</p>
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
            </div>
        </div>
    );
}

export default Step5; 