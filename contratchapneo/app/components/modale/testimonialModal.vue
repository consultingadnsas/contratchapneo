<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      
      <!-- En-tête -->
      <div class="modal-header">
        <h3 class="modal-title">{{ isEditing ? 'Modifier le témoignage' : 'Nouveau témoignage' }}</h3>
        <button class="close-btn" @click="$emit('close')">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon-sm">
            <path fill-rule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Corps du formulaire -->
      <div class="modal-body">
        
        <!-- Zone Upload Photo -->
        <div class="photo-upload-section">
          <div class="avatar-preview">
            <img v-if="formData.avatarUrl" :src="formData.avatarUrl" alt="Aperçu" class="avatar-img-full" />
            <span v-else class="avatar-placeholder">{{ formData.author ? formData.author.charAt(0) : '?' }}</span>
          </div>
          <div class="upload-actions">
            <label class="btn-upload">
              Charger une photo
              <input type="file" accept="image/*" class="hidden-input" @change="handleFileUpload" />
            </label>
            <span class="text-xs gray-text">Format JPG ou PNG. Max 2Mo.</span>
          </div>
        </div>

        <!-- Informations Personnelles -->
        <BaseInput 
          v-model="formData.author" 
          label="Nom complet de la personne *" 
          placeholder="Ex: Sylla Awa" 
        />
        
        <div class="input-row">
          <BaseInput 
            v-model="formData.role" 
            label="Poste occupé" 
            placeholder="Ex: Directrice Générale" 
          />
          <BaseInput 
            v-model="formData.company" 
            label="Nom de l'entreprise" 
            placeholder="Ex: Startup Tech Abidjan" 
          />
        </div>

        <!-- Message -->
        <div class="textarea-group">
          <label class="input-label">Message du client *</label>
          <textarea 
            v-model="formData.message" 
            rows="4" 
            class="form-textarea" 
            placeholder="Saisissez le texte du témoignage ici..."
          ></textarea>
        </div>

      </div>

      <!-- Pied de la modale -->
      <div class="modal-footer">
        <secondButton label="Annuler" @click="$emit('close')" />
        <mainButton :label="isEditing ? 'Enregistrer les modifications' : 'Ajouter le témoignage'" @click="submitForm" />
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
  name: 'TestimonialModal',
  components: { BaseInput, mainButton, secondButton },
  props: {
    testimonial: {
      type: Object,
      default: () => null
    }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const isEditing = computed(() => !!props.testimonial);
    
    // Initialisation des données du formulaire
    const formData = ref({
      id: null,
      author: '',
      role: '',
      company: '',
      message: '',
      avatarUrl: ''
    });

    // Remplir le formulaire si on est en mode édition
    watch(() => props.testimonial, (newVal) => {
      if (newVal) {
        formData.value = { ...newVal };
      } else {
        formData.value = { id: null, author: '', role: '', company: '', message: '', avatarUrl: '' };
      }
    }, { immediate: true });

    // Simulation de l'upload d'image (crée une URL locale temporaire)
    const handleFileUpload = (event: Event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (file) {
        formData.value.avatarUrl = URL.createObjectURL(file);
      }
    };

    const submitForm = () => {
      if (!formData.value.author || !formData.value.message) {
        alert("Le nom et le message sont obligatoires.");
        return;
      }
      emit('save', { ...formData.value });
    };

    return {
      isEditing,
      formData,
      handleFileUpload,
      submitForm
    };
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

.textarea-group { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem; }
.input-label { font-size: 0.875rem; font-weight: 500; color: #374151; }
.form-textarea { width: 100%; padding: 0.7rem; font-size: 1rem; color: #1f2937; background-color: #fff; border: 1px solid #d1d5db; border-radius: 1rem; transition: 0.15s; font-family: inherit; resize: vertical; }
.form-textarea:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25); }

.modal-footer {
  padding: 1.5rem; border-top: 1px solid #f1f5f9; background: #fafaf9; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px;
  display: flex; justify-content: flex-end; gap: 1rem;
}
</style>