<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content panel">
      <div class="modal-header">
        <h3 class="text-white">{{ isEditing ? 'Modifier le modèle' : 'Ajouter un modèle' }}</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <form @submit.prevent="submitForm" class="modal-form">
        <div class="form-group">
          <label>Titre du document</label>
          <input type="text" v-model="localData.title" placeholder="Ex: Statuts SARL OHADA" required />
        </div>

        <div class="form-group">
          <label>Catégorie</label>
          <select v-model="localData.category" required>
            <option value="" disabled>Choisir une catégorie</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

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

        <div class="form-group mt-2">
          <label>Fichier du modèle (PDF ou Word)</label>
          <div class="file-upload-box">
            <input type="file" id="contract-file" accept=".pdf,.doc,.docx" @change="handleFileUpload" />
            <label for="contract-file" class="file-label">
              <component :is="DocumentArrowUpIcon" class="icon-md text-blue" />
              <span v-if="!localData.file">Cliquez pour uploader le fichier</span>
              <span v-else class="text-green font-bold">{{ localData.file.name || 'Fichier sélectionné' }}</span>
            </label>
          </div>
        </div>

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
    contract: {
      type: Object as PropType<any>,
      default: null
    },
    categories: {
      type: Array as PropType<string[]>,
      required: true
    }
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const isEditing = ref(!!props.contract);
    
    const localData = ref({
      id: null as number | null,
      title: '',
      category: '',
      price: '',
      isPromoActive: false,
      promoPrice: '',
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
      if (target.files && target.files.length > 0) {
        localData.value.file = target.files[0];
      }
    };

    const submitForm = () => {
      if (!localData.value.isPromoActive) {
        localData.value.promoPrice = '';
      }
      emit('save', localData.value);
    };

    return {
      isEditing,
      localData,
      handleFileUpload,
      submitForm,
      DocumentArrowUpIcon,
      CheckCircleIcon
    };
  }
}
</script>

<style scoped>
/* L'OVERLAY (Prend tout l'écran et empêche de cliquer derrière) */
.modal-overlay { 
  position: fixed; 
  top: 0; left: 0; width: 100vw; height: 100vh; 
  background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); 
  display: flex; justify-content: center; align-items: center; 
  z-index: 1000; padding: 1rem; 
}

/* LE CONTENEUR DE LA MODALE */
.modal-content { 
  width: 100%; 
  max-width: 550px; /* Légèrement plus large pour respirer */
  max-height: 90vh; /* Empêche la modale de déborder en hauteur */
  overflow-y: auto; /* Ajoute un scroll interne si le contenu est trop grand */
  background: #161618; border: 1px solid #2a2a2c; 
  border-radius: 20px; padding: 1.5rem; font-family: 'Inter', sans-serif;
}

/* Personnalisation de la barre de scroll de la modale */
.modal-content::-webkit-scrollbar { width: 6px; }
.modal-content::-webkit-scrollbar-track { background: transparent; }
.modal-content::-webkit-scrollbar-thumb { background-color: #2a2a2c; border-radius: 10px; }

/* HEADER */
.modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2a2a2c; padding-bottom: 1rem; margin-bottom: 1.5rem; }
.text-white { color: #ffffff; margin: 0; font-weight: 600; font-size: 1.1rem; }
.close-btn { background: transparent; border: none; color: #8a8a8e; font-size: 1.5rem; cursor: pointer; }
.close-btn:hover { color: #ffffff; }

/* FORMULAIRE & INPUTS */
.modal-form { display: flex; flex-direction: column; gap: 1.2rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group label { color: #8a8a8e; font-size: 0.85rem; font-weight: 500; }
.promo-label { display: flex; justify-content: space-between; align-items: center; }

.form-group input, .form-group select { background: #1e1e20; border: 1px solid #2a2a2c; color: #ffffff; padding: 0.8rem 1rem; border-radius: 10px; font-size: 0.95rem; outline: none; transition: 0.2s; }
.form-group input:focus, .form-group select:focus { border-color: #0A84FF; }
.disabled-input { opacity: 0.3; cursor: not-allowed; }

/* UPLOAD FICHIER */
.file-upload-box { position: relative; width: 100%; }
.file-upload-box input { position: absolute; width: 0; height: 0; opacity: 0; overflow: hidden; z-index: -1; }
.file-label { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; padding: 2rem; background: rgba(255, 255, 255, 0.02); border: 2px dashed rgba(255, 255, 255, 0.15); border-radius: 14px; cursor: pointer; transition: 0.3s; text-align: center; color: #8a8a8e; font-size: 0.9rem; }
.file-label:hover { background: rgba(10, 132, 255, 0.05); border-color: #0A84FF; }
.text-green { color: #30D158; }
.font-bold { font-weight: 600; }

/* FOOTER */
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid #2a2a2c; padding-top: 1.5rem; margin-top: 0.5rem; }
.btn-outline { background: transparent; border: 1px solid #2a2a2c; color: #ffffff; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: 0.2s; }
.btn-outline:hover { background: rgba(255,255,255,0.05); }
.btn-primary { display: flex; align-items: center; gap: 0.5rem; background: #ffffff; color: #000; border: none; padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { opacity: 0.9; }

/* BOUTON SWITCH */
.switch { position: relative; display: inline-block; width: 44px; height: 24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #2a2a2c; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px; background-color: #8a8a8e; transition: .4s; border-radius: 50%; }
input:checked + .slider { background-color: #30D158; }
input:checked + .slider:before { transform: translateX(20px); background-color: #fff; }

.switch-small { width: 34px; height: 20px; }
.switch-small .slider:before { height: 14px; width: 14px; left: 3px; bottom: 3px; }
.switch-small input:checked + .slider:before { transform: translateX(14px); }

.icon-md { width: 24px; height: 24px; }
.icon-sm { width: 18px; height: 18px; }
.text-blue { color: #0A84FF; }
.mt-2 { margin-top: 0.5rem; }

/* =========================================
   RESPONSIVE DESIGN POUR MOBILES
   ========================================= */
@media (max-width: 480px) {
  .modal-content {
    padding: 1.2rem; /* Légèrement moins de padding sur téléphone */
  }
  
  .form-row {
    grid-template-columns: 1fr; /* On empile le prix et la promo l'un sur l'autre */
    gap: 1.2rem;
  }
  
  .modal-footer {
    flex-direction: column; /* On empile les boutons à la fin */
  }
  
  .btn-outline, .btn-primary {
    width: 100%;
    justify-content: center;
  }
}
</style>