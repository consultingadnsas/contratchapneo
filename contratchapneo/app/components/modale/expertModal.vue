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
        
        <div class="photo-upload-section">
          <div class="avatar-preview">
            <img v-if="formData.avatar" :src="formData.avatar" alt="Aperçu" class="avatar-img-full" />
            <span v-else class="avatar-placeholder">{{ formData.name ? formData.name.charAt(0) : '?' }}</span>
          </div>
          <div class="upload-actions">
            <label class="btn-upload">
              Charger une photo
              <input type="file" accept="image/*" class="hidden-input" @change="handleFileUpload" />
            </label>
            <span class="text-xs gray-text">Format JPG ou PNG.</span>
          </div>
        </div>

        <div class="input-row">
            <BaseInput v-model="formData.name" label="Nom complet *" placeholder="Ex: Me. Sylla Awa" />
            <div class="input-group">
              <label class="input-label">Fonction *</label>
              <select v-model="formData.role" class="form-select">
                <option disabled value="">Sélectionner...</option>
                <option value="AVOCAT">Avocat</option>
                <option value="NOTAIRE">Notaire</option>
                <option value="JURISTE">Juriste d'entreprise</option>
                <option value="CONSEIL_JURIDIQUE">Conseil Juridique</option>
                <option value="HUISSIER">Huissier</option>
              </select>
            </div>
        </div>

        <div class="input-row">
            <BaseInput v-model="formData.email" type="email" label="Email *" placeholder="contact@expert.com" />
            <BaseInput v-model="formData.phone_number" label="Téléphone *" placeholder="+225 01020304" />
        </div>
        
        <div class="input-row">
            <BaseInput v-model="formData.city" label="Ville *" placeholder="Ex: Abidjan" />
            <BaseInput v-model="formData.specialty" label="Domaine d'expertise" placeholder="Ex: Droit des Affaires" />
        </div>

        <div class="input-group">
            <label class="input-label">Biographie / Présentation *</label>
            <textarea v-model="formData.bio" class="form-select" rows="3" placeholder="Présentation de l'expert..."></textarea>
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
    }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const isEditing = computed(() => !!props.expert);
    
    const formData = ref({
      id: null,
      name: '',
      role: '',
      email: '',
      phone_number: '',
      city: '',
      bio: '',
      specialty: '',
      isVerified: false,
      isActive: true,
      avatar: '',
      avatarFile: null as File | null // ⚠️ Crucial pour envoyer l'image à Django
    });

    watch(() => props.expert, (newVal) => {
      if (newVal) {
        formData.value = { ...newVal, avatarFile: null };
      } else {
        formData.value = { id: null, name: '', role: '', email: '', phone_number: '', city: '', bio: '', specialty: '', isVerified: false, isActive: true, avatar: '', avatarFile: null };
      }
    }, { immediate: true });

    const handleFileUpload = (event: Event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (file) {
        formData.value.avatarFile = file; // On garde le vrai fichier pour l'API
        formData.value.avatar = URL.createObjectURL(file); // On garde l'URL pour l'aperçu
      }
    };

    const submitForm = () => {
      if (!formData.value.name || !formData.value.role || !formData.value.email) {
        alert("Veuillez remplir les champs obligatoires (*)");
        return;
      }
      emit('save', { ...formData.value });
    };

    return { isEditing, formData, handleFileUpload, submitForm };
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000; padding: 1rem;
}

.modal-content {
  background: #ffffff; border-radius: 24px; width: 100%; max-width: 600px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  display: flex; flex-direction: column; max-height: 90vh;
}

.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 1.5rem; border-bottom: 1px solid #f1f5f9;
}
.modal-title { margin: 0; font-size: 1.25rem; font-weight: 700; color: #0f172a; }
.close-btn { background: #f1f5f9; border: none; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #64748b; cursor: pointer; transition: 0.2s; }
.close-btn:hover { background: #e2e8f0; color: #0f172a; }
.icon-sm { width: 20px; height: 20px; }

.modal-body {
  padding: 1.5rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1.5rem;
}

/* Zone Photo */
.photo-upload-section { display: flex; align-items: center; gap: 1.5rem; background: #f8fafc; padding: 1rem; border-radius: 16px; border: 1px dashed #cbd5e1; }
.avatar-preview { width: 70px; height: 70px; border-radius: 50%; background: #e2e8f0; display: flex; align-items: center; justify-content: center; overflow: hidden; border: 2px solid #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.avatar-img-full { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { font-size: 1.8rem; font-weight: 700; color: #94a3b8; }
.upload-actions { display: flex; flex-direction: column; gap: 0.4rem; }
.btn-upload { background: #ffffff; border: 1px solid #cbd5e1; padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: #475569; cursor: pointer; display: inline-block; transition: 0.2s; }
.btn-upload:hover { border-color: #2563eb; color: #2563eb; }
.hidden-input { display: none; }
.text-xs { font-size: 0.75rem; }
.gray-text { color: #94a3b8; }

/* Formulaire */
.input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.input-group { display: flex; flex-direction: column; margin-bottom: 0.5rem;}
.input-label { font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.5rem; display: block; }
.form-select { width: 100%; padding: 0.7rem; font-size: 1rem; line-height: 1.5; color: #1f2937; background-color: #fff; border: 1px solid #d1d5db; border-radius: 1.5rem; transition: 0.15s; outline: none; -webkit-appearance: none; -moz-appearance: none; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 1rem center; background-size: 1em; }
.form-select:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25); }

/* Checkboxes */
.options-section { display: flex; flex-direction: column; gap: 0.8rem; margin-top: 0.5rem; padding: 1rem; background: #f8fafc; border-radius: 12px; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.form-checkbox { width: 1.2rem; height: 1.2rem; cursor: pointer; }
.checkbox-text { font-size: 0.9rem; color: #374151; font-weight: 500; }

.modal-footer {
  padding: 1.5rem; border-top: 1px solid #f1f5f9; background: #fafaf9; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px;
  display: flex; justify-content: flex-end; gap: 1rem;
}
</style>