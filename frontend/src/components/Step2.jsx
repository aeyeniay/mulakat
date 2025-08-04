/**
 * MÜLAKAT SORU HAZIRLAMASI SİSTEMİ - ROL YÖNETİMİ COMPONENT'İ
 * =============================================================
 * 
 * 📋 COMPONENT AMACI:
 * Bu React component'i, mülakat sisteminde 2. adım olan rol/pozisyon tanımlama
 * işlemlerini yönetir. Kullanıcılar bu ekranda pozisyon bilgilerini girer,
 * maaş katsayılarını belirler ve özel gereksinimleri tanımlar.
 * 
 * 🎯 KAPSAM:
 * 1. 👥 ROL YÖNETİMİ:
 *    - Yeni rol ekleme (CRUD operations)
 *    - Mevcut rolleri düzenleme
 *    - Rol silme işlemleri
 *    - Real-time validation
 * 
 * 2. 📊 ZORLUK SİSTEMİ:
 *    - Maaş katsayısı seçimi (2x, 3x, 4x)
 *    - Pozisyon sayısı belirleme
 *    - Otomatik zorluk seviyesi gösterimi
 * 
 * 3. 📝 GEREKSİNİM YÖNETİMİ:
 *    - Özel şartlar text area
 *    - Teknoloji/beceri listesi
 *    - Form validation
 * 
 * 📊 VERİ AKIŞI:
 * GİRİŞ: contractId (parent'tan gelen ilan ID'si)
 * İŞLEM: API çağrıları, state yönetimi, form handling
 * ÇIKIŞ: Kaydedilmiş roller → Step 3'e geçiş
 * 
 * 🔧 STATE YÖNETİMİ:
 * - roles: Mevcut roller listesi
 * - newRole: Yeni rol form verileri
 * - editingRole: Düzenlenen rol ID'si
 * - editForm: Düzenleme form verileri
 * - loading: API çağrı durumu
 * 
 * 📡 API ENDPOİNTLERİ:
 * - GET /api/step2/roles/{contractId} → Rolleri getir
 * - POST /api/step2/roles → Yeni rol ekle
 * - PUT /api/step2/roles/{roleId} → Rol güncelle
 * - DELETE /api/step2/roles/{roleId} → Rol sil
 * 
 * 🎨 UI ÖZELLİKLERİ:
 * - Responsive card-based layout
 * - Real-time form validation
 * - Loading states ve error handling
 * - Inline editing interface
 * - Zorluk seviyesi renk kodlaması
 * 
 * 👨‍💻 GELIŞTIREN: AI Destekli Geliştirme
 * 📅 TARİH: 2025
 * 🔄 VERSİYON: 1.0.0
 */

import { useState, useEffect } from 'react';
import axios from 'axios';

const Step2 = ({ contractId, onNext, onPrevious }) => {
  const [roles, setRoles] = useState([]);
  const [newRole, setNewRole] = useState({
    name: '',
    salary_multiplier: 2,
    position_count: 1,
    special_requirements: ''
  });
  const [loading, setLoading] = useState(false);
  const [editingRole, setEditingRole] = useState(null); // Düzenlenen rol
  const [editForm, setEditForm] = useState({
    name: '',
    salary_multiplier: 2,
    position_count: 1,
    special_requirements: ''
  });

  // Özel şartları formatla
  const formatSpecialRequirements = (requirements) => {
    if (!requirements) return null;
    
    // Satırları ayır ve maddeleri tespit et
    const lines = requirements.split('\n');
    const formattedLines = [];
    
    for (let line of lines) {
      line = line.trim();
      if (line) {
        // Eğer satır numaralı madde ile başlıyorsa (örn: "2.1.", "1.2.")
        if (/^\d+\.\d+\./.test(line)) {
          formattedLines.push(
            <li key={line} className="requirement-item">
              {line}
            </li>
          );
        } else {
          // Diğer satırlar
          formattedLines.push(
            <li key={line} className="requirement-item">
              {line}
            </li>
          );
        }
      }
    }
    
    return (
      <ul className="requirements-list">
        {formattedLines}
      </ul>
    );
  };

  // Mevcut rolleri yükle
  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/step2/roles/${contractId}`);
        setRoles(response.data.roles);
      } catch (error) {
        console.error('Error fetching roles:', error);
      }
    };

    if (contractId) {
      fetchRoles();
    }
  }, [contractId]);

  // Yeni rol ekle
  const handleAddRole = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/step2/add-role', {
        contract_id: contractId,
        ...newRole
      });
      
      // Rolle listesini güncelle
      setRoles([...roles, response.data.role]);
      
      // Formu temizle
      setNewRole({
        name: '',
        salary_multiplier: 2,
        position_count: 1,
        special_requirements: ''
      });
      
      
    } catch (error) {
      console.error('Error adding role:', error);
      alert('Rol eklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  // Rolü sil
  const handleDeleteRole = async (roleId) => {
    try {
      await axios.delete(`http://localhost:8000/api/step2/roles/${roleId}`);
      setRoles(roles.filter(role => role.id !== roleId));
    } catch (error) {
      console.error('Error deleting role:', error);
      alert('Rol silinirken hata oluştu');
    }
  };

  // Rol düzenlemeye başla
  const handleEditRole = (role) => {
    setEditingRole(role.id);
    setEditForm({
      name: role.name,
      salary_multiplier: role.salary_multiplier,
      position_count: role.position_count,
      special_requirements: role.special_requirements
    });
  };

  // Düzenlemeyi iptal et
  const handleCancelEdit = () => {
    setEditingRole(null);
    setEditForm({
      name: '',
      salary_multiplier: 2,
      position_count: 1,
      special_requirements: ''
    });
  };

  // Rol düzenlemesini kaydet
  const handleSaveEdit = async (roleId) => {
    setLoading(true);

    try {
      const response = await axios.put(`http://localhost:8000/api/step2/roles/${roleId}`, editForm);
      
      // Rolle listesini güncelle
      setRoles(roles.map(role => 
        role.id === roleId ? response.data.role : role
      ));
      
      // Düzenleme modundan çık
      setEditingRole(null);
      setEditForm({
        name: '',
        salary_multiplier: 2,
        position_count: 1,
        special_requirements: ''
      });
      
      
    } catch (error) {
      console.error('Error updating role:', error);
      alert('Rol güncellenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  // Düzenleme formu değişiklikleri
  const handleEditFormChange = (e) => {
    const { name, value } = e.target;
    setEditForm(prev => ({
      ...prev,
      [name]: name === 'salary_multiplier' || name === 'position_count' 
        ? parseInt(value) 
        : value
    }));
  };

  // Sonraki adıma geç
  const handleNext = () => {
    if (roles.length === 0) {
      alert('En az bir rol eklemelisiniz');
      return;
    }
    onNext(contractId);
  };

  const handleNewRoleChange = (e) => {
    const { name, value } = e.target;
    setNewRole(prev => ({
      ...prev,
      [name]: name === 'salary_multiplier' || name === 'position_count' 
        ? parseInt(value) 
        : value
    }));
  };

  return (
    <div className="step-container">
      <h2>Adım 2: Roller ve Gereksinimler</h2>
      
      {/* Mevcut Roller */}
      <div className="roles-section">
        <h3>Mevcut Roller</h3>
        {roles.length === 0 ? (
          <p>Henüz rol eklenmemiş</p>
        ) : (
          <div className="roles-list">
            {roles.map((role) => (
              <div key={role.id} className="role-card">
                {editingRole === role.id ? (
                  // Düzenleme modu
                  <div className="edit-form">
                    <div className="role-header">
                      <h4>Rol Düzenle</h4>
                      <div className="edit-actions">
                        <button 
                          onClick={() => handleSaveEdit(role.id)}
                          className="btn-save"
                          disabled={loading}
                        >
                          {loading ? 'Kaydediliyor...' : 'Kaydet'}
                        </button>
                        <button 
                          onClick={handleCancelEdit}
                          className="btn-cancel"
                          disabled={loading}
                        >
                          İptal
                        </button>
                      </div>
                    </div>
                    
                    <div className="edit-form-content">
                      <div className="form-row">
                        <div className="form-group">
                          <label>Rol Adı:</label>
                          <input
                            type="text"
                            name="name"
                            value={editForm.name}
                            onChange={handleEditFormChange}
                            placeholder="Örn: Kıdemli Yazılım Geliştirme Uzmanı"
                            required
                          />
                        </div>
                        
                        <div className="form-group">
                          <label>Maaş Katsayısı:</label>
                          <select
                            name="salary_multiplier"
                            value={editForm.salary_multiplier}
                            onChange={handleEditFormChange}
                            required
                          >
                            <option value={2}>2x (Min 3 yıl tecrübe)</option>
                            <option value={3}>3x (Min 5 yıl tecrübe)</option>
                            <option value={4}>4x (Min 7 yıl tecrübe)</option>
                          </select>
                        </div>
                        
                        <div className="form-group">
                          <label>Pozisyon Sayısı:</label>
                          <input
                            type="number"
                            name="position_count"
                            value={editForm.position_count}
                            onChange={handleEditFormChange}
                            min="1"
                            required
                          />
                        </div>
                      </div>

                      <div className="form-group">
                        <label>Özel Şartlar:</label>
                        <textarea
                          name="special_requirements"
                          value={editForm.special_requirements}
                          onChange={handleEditFormChange}
                          placeholder="Bu rol için özel şartları yazın..."
                          rows="4"
                        />
                      </div>
                    </div>
                  </div>
                ) : (
                  // Normal görüntüleme modu
                  <>
                    <div className="role-header">
                      <h4>{role.name}</h4>
                      <div className="role-actions">
                        <button 
                          onClick={() => handleEditRole(role)}
                          className="btn-edit"
                        >
                          Düzenle
                        </button>
                        <button 
                          onClick={() => handleDeleteRole(role.id)}
                          className="btn-delete"
                        >
                          Sil
                        </button>
                      </div>
                    </div>
                    <div className="role-details">
                      <p><strong>Maaş Katsayısı:</strong> {role.salary_multiplier}x</p>
                      <p><strong>Pozisyon Sayısı:</strong> {role.position_count}</p>
                      {role.special_requirements && (
                        <div className="special-requirements">
                          <p><strong>Özel Şartlar:</strong></p>
                          {formatSpecialRequirements(role.special_requirements)}
                        </div>
                      )}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Yeni Rol Ekle */}
      <div className="add-role-section">
        <h3>Yeni Rol Ekle</h3>
        <form onSubmit={handleAddRole} className="form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">Rol Adı:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={newRole.name}
                onChange={handleNewRoleChange}
                placeholder="Örn: Kıdemli Yazılım Geliştirme Uzmanı"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="salary_multiplier">Maaş Katsayısı:</label>
              <select
                id="salary_multiplier"
                name="salary_multiplier"
                value={newRole.salary_multiplier}
                onChange={handleNewRoleChange}
                required
              >
                <option value={2}>2x (Min 3 yıl tecrübe)</option>
                <option value={3}>3x (Min 5 yıl tecrübe)</option>
                <option value={4}>4x (Min 7 yıl tecrübe)</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="position_count">Pozisyon Sayısı:</label>
              <input
                type="number"
                id="position_count"
                name="position_count"
                value={newRole.position_count}
                onChange={handleNewRoleChange}
                min="1"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="special_requirements">Özel Şartlar:</label>
            <textarea
              id="special_requirements"
              name="special_requirements"
              value={newRole.special_requirements}
              onChange={handleNewRoleChange}
              placeholder="Bu rol için özel şartları yazın..."
              rows="4"
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Ekleniyor...' : 'Rol Ekle'}
          </button>
        </form>
      </div>

      {/* Sonraki Adım */}
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
          disabled={roles.length === 0}
        >
          Sonraki Adıma Geç
        </button>
      </div>
    </div>
  );
};

export default Step2; 