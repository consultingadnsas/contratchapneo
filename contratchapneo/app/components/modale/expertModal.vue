<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      
      <div class="modal-header">
        <h3 class="modal-title">{{ isEditing ? 'Modifier le profil' : 'Ajouter un expert' }}</h3>
        <button class="close-btn" @click="$emit('close')">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon-sm">
            <path fill-rule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div class="modal-body">
        
        <div class="upload-grid">
          <div class="photo-upload-section">
            <div class="avatar-preview">
              <img v-if="formData.avatar" :src="formData.avatar" alt="Aperçu" class="avatar-img-full" />
              <span v-else class="avatar-placeholder">{{ formData.name ? formData.name.charAt(0) : '?' }}</span>
            </div>
            <div class="upload-actions">
              <label class="btn-upload">
                Photo de profil
                <input type="file" accept="image/*" class="hidden-input" @change="handleFileUpload" />
              </label>
              <span class="text-xs gray-text">Format JPG ou PNG.</span>
            </div>
          </div>

          <div class="document-upload-section">
            <div class="document-icon">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-lg text-gray">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
              </svg>
            </div>
            <div class="upload-actions">
              <label class="btn-upload">
                Carte de visite (PDF)
                <input type="file" accept="application/pdf" class="hidden-input" @change="handleDocumentUpload" />
              </label>
              <span class="text-xs text-blue font-bold" v-if="formData.visitingCardFile">Nouveau fichier : {{ formData.visitingCardFile.name }}</span>
              <a :href="formData.visiting_card" target="_blank" class="text-xs text-green font-bold" style="text-decoration: underline;" v-else-if="formData.visiting_card">Voir le document actuel</a>
              <span class="text-xs gray-text" v-else>Document de légitimité</span>
            </div>
          </div>
        </div>

        <div class="input-row">
            <div class="input-wrapper">
              <BaseInput v-model="formData.name" label="Nom complet *" placeholder="Ex: Me. Sylla Awa" />
              <span v-if="errors.name" class="error-text">{{ errors.name }}</span>
            </div>
            <div class="input-wrapper">
              <div class="input-group">
                <label class="input-label">Fonction *</label>
                <select v-model="formData.role" class="form-select" :class="{'border-red': errors.role}">
                  <option disabled value="">Sélectionner...</option>
                  <option value="AVOCAT">Avocat</option>
                  <option value="NOTAIRE">Notaire</option>
                  <option value="JURISTE">Juriste d'entreprise</option>
                  <option value="CONSEIL_JURIDIQUE">Conseil Juridique</option>
                  <option value="HUISSIER">Huissier</option>
                  <option value="MANDATAIRE">Mandataire Judiciaire</option>
                  <option value="EXPERT_COMPTABLE">Expert-Comptable</option>
                </select>
              </div>
              <span v-if="errors.role" class="error-text">{{ errors.role }}</span>
            </div>
        </div>

        <div class="input-row">
            <div class="input-wrapper">
              <BaseInput v-model="formData.email" type="email" label="Email *" placeholder="contact@expert.com" />
              <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
            </div>
            <div class="input-wrapper">
              <BaseInput v-model="formData.phone_number" label="Téléphone *" placeholder="+225 01020304" />
              <span v-if="errors.phone_number" class="error-text">{{ errors.phone_number }}</span>
            </div>
        </div>
        
        <div class="input-row">
            <div class="input-wrapper">
              <div class="input-group">
                <label class="input-label">Pays d'exercice *</label>
                <select v-model="formData.country" class="form-select" :class="{'border-red': errors.country}">
                  <option disabled value="">Sélectionner un pays...</option>
                  <option v-for="c in countries" :key="c.id" :value="c.id">{{ c.name }}</option>
                </select>
              </div>
              <span v-if="errors.country" class="error-text">{{ errors.country }}</span>
            </div>
            <div class="input-wrapper">
              <BaseInput v-model="formData.city" label="Ville *" placeholder="Ex: Abidjan" />
              <span v-if="errors.city" class="error-text">{{ errors.city }}</span>
            </div>
        </div>

        <div class="input-row">
            <div class="input-wrapper">
              <BaseInput v-model="formData.years_of_experience" type="number" min="0" label="Années d'expérience *" placeholder="Ex: 5" />
              <span v-if="errors.years_of_experience" class="error-text">{{ errors.years_of_experience }}</span>
            </div>
            <!-- ⚡️ REMPLACEMENT DE SPECIALTY PAR DOMAINS (SELECT MULTIPLE) -->
            <div class="input-wrapper">
              <div class="input-group">
                <label class="input-label">Domaines d'expertise</label>
                <select v-model="formData.domains" class="form-select form-select-multiple" multiple size="3">
                  <option v-for="d in domains" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
                <span class="text-xs gray-text mt-1">Maintenez Ctrl/Cmd pour en sélectionner plusieurs.</span>
              </div>
            </div>
        </div>

        <div class="input-wrapper">
            <div class="input-group">
                <label class="input-label">Biographie / Présentation *</label>
                <textarea v-model="formData.bio" class="form-select" :class="{'border-red': errors.bio}" rows="3" placeholder="Présentation de l'expert..."></textarea>
            </div>
            <span v-if="errors.bio" class="error-text">{{ errors.bio }}</span>
        </div>

        <div class="options-section">
            <label class="checkbox-label">
                <input type="checkbox" v-model="formData.isVerified" class="form-checkbox">
                <span class="checkbox-text">Profil certifié (Badge de confiance)</span>
            </label>
            <label class="checkbox-label">
                <input type="checkbox" v-model="formData.isActive" class="form-checkbox">
                <span class="checkbox-text">Profil actif (Visible sur la plateforme)</span>
            </label>
        </div>

      </div>

      <div class="modal-footer">
        <secondButton label="Annuler" @click="$emit('close')" />
        <mainButton :label="isEditing ? 'Enregistrer' : 'Ajouter'" @click="submitForm" />
      </div>

    </div>
  </div>
</template>

<script lang="ts">
import { ref, computed, watch } from 'vue';
import BaseInput from '../input/BaseInput.vue';
import mainButton from '../buttons/mainButton.vue';
import secondButton from '../buttons/secondButton.vue';

export default {
  name: 'ExpertModal',
  components: { BaseInput, mainButton, secondButton },
  props: {
    expert: {
      type: Object,
      default: () => null
    },
    countries: {
      type: Array,
      default: () => []
    },
    // ⚡️ NOUVEAU : Réception de la liste des domaines
    domains: {
      type: Array,
      default: () => []
    }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const isEditing = computed(() => !!props.expert);
    const errors = ref<Record<string, string>>({});
    
    const formData = ref({
      id: null,
      name: '',
      role: '',
      email: '',
      phone_number: '',
      country: '',
      city: '',
      years_of_experience: 0,
      bio: '',
      domains: [] as string[], // ⚡️ Tableau d'IDs pour les domaines
      isVerified: false,
      isActive: true,
      avatar: '',
      avatarFile: null as File | null,
      visiting_card: '',
      visitingCardFile: null as File | null
    });

    watch(() => props.expert, (newVal) => {
      errors.value = {}; 
      if (newVal) {
        const countryId = newVal.country?.id ? newVal.country.id : (newVal.country || '');
        // ⚡️ Extraction des IDs si le backend a renvoyé des objets complets
        const domainIds = newVal.domains ? newVal.domains.map((d: any) => d.id || d) : [];
        
        formData.value = { 
            ...newVal, 
            country: countryId,
            domains: domainIds,
            years_of_experience: newVal.years_of_experience || 0,
            avatarFile: null, 
            visitingCardFile: null 
        };
      } else {
        formData.value = { 
          id: null, name: '', role: '', email: '', phone_number: '', country: '', city: '', 
          years_of_experience: 0, bio: '', domains: [], isVerified: false, isActive: true, 
          avatar: '', avatarFile: null, visiting_card: '', visitingCardFile: null 
        };
      }
    }, { immediate: true });

    const handleFileUpload = (event: Event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (file) {
        formData.value.avatarFile = file;
        formData.value.avatar = URL.createObjectURL(file); 
      }
    };

    const handleDocumentUpload = (event: Event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (file && file.type === 'application/pdf') {
        formData.value.visitingCardFile = file;
      } else if (file) {
        alert("Seuls les fichiers PDF sont autorisés pour la carte de visite.");
      }
    };

    const submitForm = () => {
      errors.value = {};
      let isValid = true;

      if (!formData.value.name.trim()) { errors.value.name = "Le nom complet est requis."; isValid = false; }
      if (!formData.value.role) { errors.value.role = "La fonction est requise."; isValid = false; }
      if (!formData.value.email.trim()) { errors.value.email = "L'adresse email est requise."; isValid = false; }
      if (!formData.value.phone_number.trim()) { errors.value.phone_number = "Le numéro de téléphone est requis."; isValid = false; }
      if (!formData.value.country) { errors.value.country = "Le pays est requis."; isValid = false; }
      if (!formData.value.city.trim()) { errors.value.city = "La ville est requise."; isValid = false; }
      
      if (formData.value.years_of_experience === null || formData.value.years_of_experience === undefined || Number(formData.value.years_of_experience) < 0) { 
          errors.value.years_of_experience = "Une valeur valide est requise."; 
          isValid = false; 
      }
      
      if (!formData.value.bio.trim()) { errors.value.bio = "Une biographie est requise."; isValid = false; }

      if (isValid) {
        emit('save', { ...formData.value });
      }
    };

    return { isEditing, formData, errors, handleFileUpload, handleDocumentUpload, submitForm };
  }
}
</script>

<style scoped>
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px); display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem; }
.modal-content { background: #ffffff; border-radius: 24px; width: 100%; max-width: 650px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); display: flex; flex-direction: column; max-height: 90vh; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem; border-bottom: 1px solid #f1f5f9; }
.modal-title { margin: 0; font-size: 1.25rem; font-weight: 700; color: #0f172a; }
.close-btn { background: #f1f5f9; border: none; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #64748b; cursor: pointer; transition: 0.2s; }
.close-btn:hover { background: #e2e8f0; color: #0f172a; }
.icon-sm { width: 20px; height: 20px; }
.icon-lg { width: 28px; height: 28px; }
.modal-body { padding: 1.5rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1.5rem; }
.upload-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.photo-upload-section, .document-upload-section { display: flex; align-items: center; gap: 1rem; background: #f8fafc; padding: 1rem; border-radius: 16px; border: 1px dashed #cbd5e1; }
.document-upload-section { justify-content: flex-start; }
.avatar-preview, .document-icon { width: 60px; height: 60px; border-radius: 50%; background: #e2e8f0; display: flex; align-items: center; justify-content: center; overflow: hidden; border: 2px solid #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex-shrink: 0;}
.avatar-img-full { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { font-size: 1.5rem; font-weight: 700; color: #94a3b8; }
.upload-actions { display: flex; flex-direction: column; gap: 0.4rem; overflow: hidden; }
.btn-upload { background: #ffffff; border: 1px solid #cbd5e1; padding: 0.4rem 0.8rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; color: #475569; cursor: pointer; display: inline-block; transition: 0.2s; text-align: center;}
.btn-upload:hover { border-color: #2563eb; color: #2563eb; }
.hidden-input { display: none; }
.text-xs { font-size: 0.75rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.gray-text { color: #94a3b8; }
.text-blue { color: #3b82f6; }
.text-green { color: #10b981; }
.font-bold { font-weight: 700; }
.input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.input-wrapper { display: flex; flex-direction: column; width: 100%; }
.error-text { color: #ef4444; font-size: 0.75rem; font-weight: 500; margin-top: 0.3rem; margin-left: 0.5rem; }
.border-red { border-color: #ef4444 !important; }
.input-group { display: flex; flex-direction: column; margin-bottom: 0.2rem;}
.input-label { font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.5rem; display: block; }
.form-select { width: 100%; padding: 0.7rem; font-size: 1rem; line-height: 1.5; color: #1f2937; background-color: #fff; border: 1px solid #d1d5db; border-radius: 1.5rem; transition: 0.15s; outline: none; -webkit-appearance: none; -moz-appearance: none; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 1rem center; background-size: 1em; }
.form-select:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25); }

/* ⚡️ NOUVEAU : Supprime la flèche pour le select multiple */
.form-select-multiple {
    background-image: none;
    padding-right: 0.7rem;
    height: auto;
    min-height: 85px;
    border-radius: 12px;
}
.mt-1 { margin-top: 0.3rem; }

.options-section { display: flex; flex-direction: column; gap: 0.8rem; margin-top: 0.5rem; padding: 1rem; background: #f8fafc; border-radius: 12px; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.form-checkbox { width: 1.2rem; height: 1.2rem; cursor: pointer; }
.checkbox-text { font-size: 0.9rem; color: #374151; font-weight: 500; }
.modal-footer { padding: 1.5rem; border-top: 1px solid #f1f5f9; background: #fafaf9; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px; display: flex; justify-content: flex-end; gap: 1rem; }
</style>