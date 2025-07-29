import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Step5({ contractId, onPrevious }) {
    const [downloading, setDownloading] = useState({});
    const [error, setError] = useState(null);
    const [completed, setCompleted] = useState({});
    const [roles, setRoles] = useState([]);

    useEffect(() => {
        if (contractId) {
            loadRoles();
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

    const downloadWordDocumentForRole = async (roleId, roleName) => {
        setDownloading(prev => ({ ...prev, [roleId]: true }));
        setError(null);
        
        try {
            const response = await axios.post('/api/step5/generate-word', {
                contract_id: contractId,
                role_id: roleId  // Sadece bu rol için Word dosyası oluştur
            }, {
                responseType: 'blob'
            });
            
            // Dosyayı indir
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            
            // Dosya adını response header'dan al veya default kullan
            const contentDisposition = response.headers['content-disposition'];
            let filename = `mulakat_sorulari_${roleName.replace(/\s+/g, '_')}.zip`;
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
            setCompleted(prev => ({ ...prev, [roleId]: true }));
            
        } catch (error) {
            console.error('Word dosyası indirme hatası:', error);
            setError(`${roleName} için Word dosyası indirilirken bir hata oluştu. Lütfen tekrar deneyin.`);
        } finally {
            setDownloading(prev => ({ ...prev, [roleId]: false }));
        }
    };

    return (
        <div className="step-container">
            <h2>Adım 5: Final Seti</h2>
            
            <div className="step5-description">
                <p>Tebrikler! Mülakat sorularınız başarıyla üretildi. Şimdi bu soruları ayrı Word dosyaları olarak indirebilirsiniz.</p>
            </div>
            
            <div className="download-section">
                <h3>Word Dosyaları İndirme</h3>
                <p>Üretilen soruları ayrı Word dosyaları formatında indirin. Her aday için ayrı soru kitapçığı ve jüri için cevap kitapçığı oluşturulacak:</p>
                
                <ul className="features-list">
                    <li>✓ Her aday için ayrı soru kitapçığı (S1, S2, S3...)</li>
                    <li>✓ Jüri için cevap kitapçıkları (C1, C2, C3...)</li>
                    <li>✓ Her pozisyon için ayrı dosyalar</li>
                    <li>✓ Soru kategorileri (Mesleki Deneyim, Teorik Bilgi, Pratik Uygulama)</li>
                    <li>✓ Numaralandırılmış sorular</li>
                    <li>✓ ZIP dosyası içinde düzenli organizasyon</li>
                </ul>
                
                <div className="roles-download-grid">
                    {roles.map((role) => {
                        const isDownloading = downloading[role.id];
                        const isCompleted = completed[role.id];
                        
                        return (
                            <div key={role.id} className="role-download-card">
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
                                
                                <div className="download-actions">
                                    <button 
                                        onClick={() => downloadWordDocumentForRole(role.id, role.name)}
                                        disabled={isDownloading}
                                        className="download-btn"
                                    >
                                        {isDownloading ? 'Hazırlanıyor...' : 'Word Dosyalarını İndir'}
                                    </button>
                                    
                                    {isCompleted && (
                                        <span className="status-badge success">✓ İndirildi</span>
                                    )}
                                </div>
                                
                                {isDownloading && (
                                    <div className="processing-info">
                                        <p>⏳ {role.name} için Word dosyaları hazırlanıyor...</p>
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
                
                {error && (
                    <div className="error-message">
                        <p>❌ {error}</p>
                    </div>
                )}
            </div>
            
            {Object.keys(completed).length > 0 && (
                <div className="completion-message">
                    <h3>🎉 İşlem Tamamlandı!</h3>
                    <p>Seçilen mülakat soruları başarıyla Word dosyaları olarak indirildi. ZIP dosyalarını açarak aday ve jüri kitapçıklarını kullanabilirsiniz.</p>
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