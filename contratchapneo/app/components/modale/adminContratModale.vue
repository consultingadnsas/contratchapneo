<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      
      <div class="modal-header">
        <h3 class="dark-text">{{ isEditing ? 'Modifier le modèle' : 'Ajouter un modèle' }}</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <form @submit.prevent="submitForm" class="modal-form">
        <div class="form-row">
          <div class="form-group">
            <label>Titre du document</label>
            <input type="text" v-model="localData.title" placeholder="Ex: Statuts SARL OHADA" required />
          </div>

          <!-- Catégorie -->
          <div class="form-group">
            <label>Catégorie</label>
            <select v-model="localData.category" required>
              <option value="" disabled>Choisir une catégorie</option>
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
        </div>

        <!-- Prix et Promo -->
        <div class="form-row">
          <div class="form-group">
            <label>Prix de base (FCFA)</label>
            <input type="number" v-model="localData.price" placeholder="Ex: 15000" required />
          </div>
          
          <div class="form-group promo-group">
            <label class="promo-label">
              Activer la promotion
              <label class="switch switch-small">
                <input type="checkbox" v-model="localData.isPromoActive">
                <span class="slider round"></span>
              </label>
            </label>
            <input 
              type="number" 
              v-model="localData.promoPrice" 
              placeholder="Prix promotionnel" 
              :disabled="!localData.isPromoActive"
              :required="localData.isPromoActive"
              :class="{ 'disabled-input': !localData.isPromoActive }"
            />
          </div>
        </div>

        <!-- Zone d'Upload -->
        <div class="form-group mt-2">
          <label>Fichier du modèle (PDF ou Word)</label>
          <div class="file-upload-box">
            <input type="file" id="contract-file" accept=".pdf,.doc,.docx" @change="handleFileUpload" />
            <label for="contract-file" class="file-label">
              <div class="icon-circle">
                <component :is="DocumentArrowUpIcon" class="icon-md" />
              </div>
              <div class="upload-text">
                <span v-if="!localData.file" class="dark-text font-bold">Cliquez pour uploader le fichier</span>
                <span v-else class="text-green font-bold">{{ localData.file.name || 'Fichier sélectionné' }}</span>
                <span v-if="!localData.file" class="gray-text text-sm">Formats acceptés : PDF, DOCX (Max 5MB)</span>
              </div>
            </label>
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button type="button" class="btn-outline" @click="$emit('close')">Annuler</button>
          <button type="submit" class="btn-primary">
            <component :is="CheckCircleIcon" class="icon-sm" />
            {{ isEditing ? 'Enregistrer' : 'Publier le modèle' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, PropType } from 'vue';
import { DocumentArrowUpIcon, CheckCircleIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'AdminContratsModal',
  props: {
    contract: { type: Object as PropType<any>, default: null },
    categories: { type: Array as PropType<string[]>, required: true }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const isEditing = ref(!!props.contract);
    
    const localData = ref({
      id: null as number | null,
      title: '', category: '', price: '',
      isPromoActive: false, promoPrice: '',
      file: null as File | null
    });

    if (props.contract) {
      localData.value = { 
        ...props.contract, 
        price: props.contract.price.toString(),
        promoPrice: props.contract.promoPrice ? props.contract.promoPrice.toString() : '',
        file: null 
      };
    }

    const handleFileUpload = (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files.length > 0) localData.value.file = target.files[0];
    };

    const submitForm = () => {
      if (!localData.value.isPromoActive) localData.value.promoPrice = '';
      emit('save', localData.value);
    };

    return { isEditing, localData, handleFileUpload, submitForm, DocumentArrowUpIcon, CheckCircleIcon };
  }
}
</script>

<style scoped>
/* OVERLAY */
.modal-overlay { 
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
  background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px); 
  display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem; 
}

/* CONTENT */
.modal-content { 
  width: 100%; max-width: 600px; max-height: 90vh; overflow-y: auto; 
  background: #ffffff; border-radius: 24px; padding: 2rem; 
  font-family: 'Inter', sans-serif; box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}
.modal-content::-webkit-scrollbar { width: 6px; }
.modal-content::-webkit-scrollbar-thumb { background-color: #e2e8f0; border-radius: 10px; }

/* HEADER */
.modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem; margin-bottom: 1.5rem; }
.dark-text { color: #1e293b; margin: 0; font-weight: 700; font-size: 1.2rem; }
.close-btn { background: #f1f5f9; border: none; color: #64748b; font-size: 1.5rem; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }
.close-btn:hover { background: #e2e8f0; color: #1e293b; }

/* FORMULAIRE (MoonInc Style) */
.modal-form { display: flex; flex-direction: column; gap: 1.2rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.form-group label { color: #64748b; font-size: 0.85rem; font-weight: 600; }
.promo-label { display: flex; justify-content: space-between; align-items: center; }

/* Inputs très doux */
.form-group input, .form-group select { 
  background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; 
  padding: 0.8rem 1rem; border-radius: 12px; font-size: 0.95rem; outline: none; transition: 0.2s; 
}
.form-group input:focus, .form-group select:focus { border-color: #2563eb; background: #ffffff; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.disabled-input { opacity: 0.4; cursor: not-allowed; background: #f1f5f9 !important; }

/* UPLOAD (Encart stylisé) */
.file-upload-box { position: relative; width: 100%; }
.file-upload-box input { position: absolute; width: 0; height: 0; opacity: 0; overflow: hidden; z-index: -1; }
.file-label { 
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1rem; 
  padding: 2rem; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 16px; 
  cursor: pointer; transition: 0.3s; text-align: center; 
}
.file-label:hover { background: #eff6ff; border-color: #2563eb; }
.icon-circle { background: #e0e7ff; color: #4f46e5; padding: 0.8rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.upload-text { display: flex; flex-direction: column; gap: 0.2rem; }
.text-green { color: #10b981; }
.font-bold { font-weight: 600; }
.gray-text { color: #94a3b8; }
.text-sm { font-size: 0.75rem; }

/* FOOTER & BOUTONS */
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid #f1f5f9; padding-top: 1.5rem; margin-top: 0.5rem; }
.btn-outline { background: white; border: 1px solid #e2e8f0; color: #475569; padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-outline:hover { background: #f8fafc; }
.btn-primary { display: flex; align-items: center; gap: 0.5rem; background: #2563eb; color: #ffffff; border: none; padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); }
.btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); }

/* SWITCH TOGGLE */
.switch { position: relative; display: inline-block; width: 40px; height: 22px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #e2e8f0; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px; background-color: #fff; transition: .4s; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
input:checked + .slider { background-color: #10b981; }
input:checked + .slider:before { transform: translateX(18px); }

.icon-md { width: 28px; height: 28px; }
.icon-sm { width: 18px; height: 18px; }
.mt-2 { margin-top: 0.5rem; }

/* RESPONSIVE */
@media (max-width: 480px) {
  .modal-content { padding: 1.2rem; }
  .form-row { grid-template-columns: 1fr; gap: 1.2rem; }
  .modal-footer { flex-direction: column; }
  .btn-outline, .btn-primary { width: 100%; justify-content: center; }
}
</style>