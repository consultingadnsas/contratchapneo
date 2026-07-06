<template>
  <div class="settings-wrapper">
    
    <!-- EN-TÊTE -->
    <div class="header-section">
      <h3 class="section-title">Paramètres</h3>
      <p class="gray-text text-sm">Gérez les informations de votre compte et les préférences de la plateforme.</p>
    </div>

    <!-- CONTENEUR PRINCIPAL (Split View) -->
    <div class="settings-layout">
      
      <!-- Menu de navigation latéral -->
      <div class="settings-sidebar">
        <nav class="settings-nav">
          <button 
            class="nav-item" 
            :class="{ active: activeSection === 'profil' }" 
            @click="activeSection = 'profil'"
          >
            <component :is="UserIcon" class="icon-md" /> Mon Profil
          </button>
          <button 
            class="nav-item" 
            :class="{ active: activeSection === 'plateforme' }" 
            @click="activeSection = 'plateforme'"
          >
            <component :is="GlobeAltIcon" class="icon-md" /> Plateforme
          </button>
          <button 
            class="nav-item" 
            :class="{ active: activeSection === 'securite' }" 
            @click="activeSection = 'securite'"
          >
            <component :is="ShieldCheckIcon" class="icon-md" /> Sécurité
          </button>
        </nav>
      </div>

      <!-- Zone de contenu principale -->
      <div class="settings-content">
        
        <!-- SECTION 1 : PROFIL -->
        <div v-if="activeSection === 'profil'" class="settings-panel fade-in">
          <div class="panel-header">
            <h4 class="dark-text">Informations Personnelles</h4>
            <p class="gray-text text-sm">Mettez à jour votre photo et vos informations de contact.</p>
          </div>
          
          <div class="panel-body">
            <!-- Avatar Upload -->
            <div class="avatar-section">
              <div class="avatar-circle-large">
                <span v-if="!profileForm.avatar">{{ getInitials(profileForm.name) }}</span>
                <img v-else :src="profileForm.avatar" alt="Avatar" class="avatar-img" />
              </div>
              <div class="avatar-actions">
                <button class="btn-secondary-small">Changer la photo</button>
                <button class="btn-text text-red">Supprimer</button>
              </div>
            </div>

            <!-- Formulaire -->
            <div class="form-grid mt-4">
              <div class="input-group">
                <label>Nom complet</label>
                <input type="text" v-model="profileForm.name" />
              </div>
              <div class="input-group">
                <label>Rôle</label>
                <input type="text" v-model="profileForm.role" disabled class="bg-disabled" />
              </div>
              <div class="input-group">
                <label>Adresse Email</label>
                <input type="email" v-model="profileForm.email" />
              </div>
              <div class="input-group">
                <label>Téléphone</label>
                <input type="text" v-model="profileForm.phone" />
              </div>
            </div>
          </div>
          
          <div class="panel-footer">
            <button class="btn-primary" @click="saveChanges('profil')">Enregistrer les modifications</button>
          </div>
        </div>

        <!-- SECTION 2 : PLATEFORME -->
        <div v-if="activeSection === 'plateforme'" class="settings-panel fade-in">
          <div class="panel-header">
            <h4 class="dark-text">Configuration de la Plateforme</h4>
            <p class="gray-text text-sm">Informations publiques affichées aux clients de la LegalTech.</p>
          </div>
          
          <div class="panel-body">
            <div class="form-grid">
              <div class="input-group full-width">
                <label>Nom de l'application</label>
                <input type="text" v-model="platformForm.appName" />
              </div>
              <div class="input-group">
                <label>Email du support client</label>
                <input type="email" v-model="platformForm.supportEmail" />
              </div>
              <div class="input-group">
                <label>Numéro WhatsApp Business</label>
                <input type="text" v-model="platformForm.whatsapp" />
              </div>
              <div class="input-group full-width">
                <label>Adresse physique</label>
                <input type="text" v-model="platformForm.address" />
              </div>
              <div class="input-group full-width">
                <label>Cadre juridique par défaut</label>
                <select v-model="platformForm.legalFramework">
                  <option value="OHADA">Droit OHADA</option>
                  <option value="International">Droit International</option>
                  <option value="National">Droit National Spécifique</option>
                </select>
              </div>
            </div>
          </div>

          <div class="panel-footer">
            <button class="btn-primary" @click="saveChanges('plateforme')">Mettre à jour la plateforme</button>
          </div>
        </div>

        <!-- SECTION 3 : SÉCURITÉ -->
        <div v-if="activeSection === 'securite'" class="settings-panel fade-in">
          <div class="panel-header">
            <h4 class="dark-text">Mot de passe et Sécurité</h4>
            <p class="gray-text text-sm">Gérez l'accès à votre compte administrateur.</p>
          </div>
          
          <div class="panel-body">
            <div class="form-grid">
              <div class="input-group full-width">
                <label>Mot de passe actuel</label>
                <input type="password" v-model="securityForm.currentPassword" placeholder="••••••••" />
              </div>
              <div class="input-group">
                <label>Nouveau mot de passe</label>
                <input type="password" v-model="securityForm.newPassword" placeholder="••••••••" />
              </div>
              <div class="input-group">
                <label>Confirmer le mot de passe</label>
                <input type="password" v-model="securityForm.confirmPassword" placeholder="••••••••" />
              </div>
            </div>
          </div>

          <div class="panel-footer">
            <button class="btn-primary" @click="saveChanges('securite')">Mettre à jour le mot de passe</button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, markRaw } from 'vue';
import { UserIcon, GlobeAltIcon, ShieldCheckIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'AdminSettings',
  setup() {
    const activeSection = ref('profil');

    // Formulaire Profil
    const profileForm = ref({
      name: 'Yvan Pascal ANGUI',
      role: 'Administrateur Principal',
      email: 'admin@contratchapneo.com',
      phone: '+225 07 00 00 00 00',
      avatar: '' 
    });

    // Formulaire Plateforme
    const platformForm = ref({
      appName: 'ContratChap',
      supportEmail: 'contact@contratchapneo.com',
      whatsapp: '+225 05 00 00 00 00',
      address: 'Abidjan, Côte d\'Ivoire',
      legalFramework: 'OHADA'
    });

    // Formulaire Sécurité
    const securityForm = ref({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });

    const getInitials = (name: string) => {
      const parts = name.split(' ');
      if (parts.length >= 2) {
        return parts[0][0] + parts[1][0];
      }
      return name ? name.charAt(0) : '?';
    };

    const saveChanges = (section: string) => {
      // Logique d'enregistrement à implémenter plus tard (API)
      console.log(`Données enregistrées pour la section : ${section}`);
      alert('Modifications enregistrées avec succès.');
    };

    return {
      activeSection,
      profileForm,
      platformForm,
      securityForm,
      getInitials,
      saveChanges,
      UserIcon: markRaw(UserIcon),
      GlobeAltIcon: markRaw(GlobeAltIcon),
      ShieldCheckIcon: markRaw(ShieldCheckIcon)
    };
  }
}
</script>

<style scoped>
.settings-wrapper {
  --bg-main: #f8fafc;
  --bg-panel: #ffffff;
  --text-dark: #1e293b;
  --text-gray: #64748b;
  --accent-blue: #2563eb;
  --border-color: #e2e8f0;
  
  display: flex; flex-direction: column; gap: 2rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

/* UTILITAIRES */
.dark-text { color: var(--text-dark); font-weight: 700; margin: 0; }
.gray-text { color: var(--text-gray); margin: 0; }
.text-sm { font-size: 0.85rem; }
.text-red { color: #ef4444; }
.mt-4 { margin-top: 1.5rem; }
.icon-md { width: 20px; height: 20px; }

/* EN-TÊTE */
.header-section { display: flex; flex-direction: column; gap: 0.4rem; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 800; margin: 0; }

/* LAYOUT PRINCIPAL (Split View) */
.settings-layout { 
  display: grid; 
  grid-template-columns: 250px 1fr; 
  gap: 2rem; 
  align-items: start; 
}

/* SIDEBAR (Menu de gauche) */
.settings-sidebar { 
  background: var(--bg-panel); 
  border-radius: 20px; 
  padding: 1rem; 
  border: 1px solid var(--border-color); 
  box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}
.settings-nav { display: flex; flex-direction: column; gap: 0.5rem; }
.nav-item { 
  display: flex; align-items: center; gap: 0.8rem; 
  background: transparent; border: none; color: var(--text-gray); 
  font-size: 0.95rem; font-weight: 600; padding: 0.8rem 1rem; 
  border-radius: 12px; cursor: pointer; transition: 0.2s; 
  text-align: left;
}
.nav-item:hover { background: #f1f5f9; color: var(--text-dark); }
.nav-item.active { background: #eff6ff; color: var(--accent-blue); }

/* ZONE DE CONTENU (Panneaux de droite) */
.settings-content { display: flex; flex-direction: column; }
.settings-panel { 
  background: var(--bg-panel); 
  border-radius: 24px; 
  border: 1px solid var(--border-color); 
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); 
  overflow: hidden;
}

/* Animation de transition douce */
.fade-in { animation: fadeIn 0.3s ease-in-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

/* Structure interne du panneau */
.panel-header { padding: 1.5rem 2rem; border-bottom: 1px solid #f1f5f9; }
.panel-header .dark-text { font-size: 1.15rem; margin-bottom: 0.3rem; }

.panel-body { padding: 2rem; }

.panel-footer { padding: 1.5rem 2rem; background: #f8fafc; border-top: 1px solid #f1f5f9; display: flex; justify-content: flex-end; }

/* AVATAR SECTION */
.avatar-section { display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1rem; }
.avatar-circle-large { 
  width: 80px; height: 80px; border-radius: 50%; 
  background: #eff6ff; color: var(--accent-blue); 
  display: flex; align-items: center; justify-content: center; 
  font-size: 1.8rem; font-weight: 700; overflow: hidden;
  border: 2px solid #e2e8f0;
}
.avatar-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-actions { display: flex; flex-direction: column; align-items: flex-start; gap: 0.5rem; }

/* GRILLES ET FORMULAIRES */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.full-width { grid-column: 1 / -1; }

.input-group { display: flex; flex-direction: column; gap: 0.5rem; }
.input-group label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.input-group input, .input-group select { 
  background: #f8fafc; border: 1px solid #e2e8f0; padding: 0.7rem 1rem; 
  border-radius: 12px; font-size: 0.95rem; color: var(--text-dark); 
  outline: none; transition: 0.2s; font-family: inherit;
}
.input-group input:focus, .input-group select:focus { border-color: var(--accent-blue); background: #ffffff; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.bg-disabled { background: #e2e8f0 !important; color: #94a3b8 !important; cursor: not-allowed; }

/* BOUTONS */
.btn-primary { 
  background: #111827; color: #ffffff; border: none; 
  padding: 0.7rem 1.5rem; border-radius: 10px; font-weight: 600; 
  cursor: pointer; transition: 0.2s; 
}
.btn-primary:hover { background: #1f2937; transform: translateY(-2px); }

.btn-secondary-small { 
  background: #ffffff; border: 1px solid #cbd5e1; color: var(--text-dark); 
  padding: 0.4rem 1rem; border-radius: 8px; font-size: 0.85rem; 
  font-weight: 600; cursor: pointer; transition: 0.2s; 
}
.btn-secondary-small:hover { background: #f8fafc; border-color: #94a3b8; }

.btn-text { background: transparent; border: none; font-size: 0.85rem; font-weight: 600; cursor: pointer; padding: 0; }
.btn-text:hover { text-decoration: underline; }

/* RESPONSIVE */
@media (max-width: 900px) {
  .settings-layout { grid-template-columns: 1fr; }
  .settings-nav { flex-direction: row; overflow-x: auto; padding-bottom: 0.5rem; }
  .nav-item { white-space: nowrap; }
}

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
  .panel-body { padding: 1.5rem; }
  .panel-footer { padding: 1.5rem; }
  .btn-primary { width: 100%; }
}
</style>