<template>
  <div class="categories-container">

    <div v-if="!openedCategory" class="folders-section">
      <div class="add-input-group mb-4">
        <button class="btn-primary-small add-folder-btn" @click="isFolderModalOpen = true">
          <component :is="PlusIcon" class="icon-sm"/> 
          <span>Nouvelle catégorie</span>
        </button>
      </div>
      
      <div class="grid-4-cols">
        <div class="folder-wrapper" v-for="(cat, index) in contratstore.categories" :key="index" @click="openCategory(cat)">
          <folderCards 
            :title="cat.title" 
            subtitle="Dossier Boutique" 
            color="blue" 
            :hasItems="true" 
          />
          
          <button class="delete-folder-btn" @click.stop="handleDeleteFolder(index, cat)" title="Supprimer ce dossier et son contenu">
            <component :is="TrashIcon" class="icon-xs" />
          </button>
        </div>
      </div>
      
      <div v-if="filteredCategories.length === 0" class="empty-state">
        <p class="gray-text">Aucun dossier trouvé.</p>
      </div>
    </div>

    <div v-else class="opened-folder-view">
      
      <div class="opened-folder-header mb-4">
        <button class="btn-secondary" @click="closeCategory">
          <component :is="ArrowLeftIcon" class="icon-sm" /> Retour aux dossiers
        </button>
        <div class="folder-title-box">
          <h3 class="section-title text-blue">{{ openedCategory }}</h3>
        </div>
      </div>

      <div class="grid-2-cols">
        <!-- Cartes des contrats existants -->
        <div class="contract-card" v-for="category in contratstore.categories" :key="category.id" :class="{'card-offline': !contract.isActive}">
          <div class="card-header">
            <div class="icon-box-light"><component :is="DocumentTextIcon" class="icon-md" /></div>
            <span class="status-badge" :class="contract.isActive ? 'badge-green' : 'badge-gray'">
              {{ contract.isActive ? 'En ligne' : 'Hors ligne' }}
            </span>
          </div>

          <div class="card-body">
            <h4 class="dark-text">{{ contract.title }}</h4>
            <span class="gray-text text-sm">{{ contract.price }} FCFA</span>
          </div>

          <div class="card-footer">
            <div class="actions-block">
              <label class="switch" title="Mettre en ligne / Hors ligne">
                <input type="checkbox" v-model="contract.isActive" @change="$emit('toggle-status', contract)">
                <span class="slider round"></span>
              </label>
              <button class="action-icon-btn edit-btn" @click="$emit('edit-contract', contract)">
                <component :is="PencilSquareIcon" class="icon-sm" />
              </button>
              <button class="action-icon-btn delete-btn" @click="handleDeleteContract(contract.id)">
                <component :is="TrashIcon" class="icon-sm" />
              </button>
            </div>
          </div>
        </div>
        <div class="contract-card add-card" @click="$emit('add-contract', { isNew: true, categoryName: openedCategory })">
          <div class="add-circle"><component :is="PlusIcon" class="icon-lg" /></div>
          <h4 class="dark-text mt-3">Ajouter un contrat</h4>
        </div>
      </div>

    </div>

    <transition name="fade">
      <div v-if="isFolderModalOpen" class="folder-modal-overlay" @click.self="isFolderModalOpen = false">
        <div class="folder-modal">
          <div class="folder-modal-header">
            <h3>Nouvelles Catégories</h3>
            <button class="close-modal-btn" @click="isFolderModalOpen = false">&times;</button>
          </div>
          
          <form @submit.prevent="handleAdd" class="folder-modal-body">
            <div class="form-group">
              <label for="folderName">Nom de la catégorie</label>
              <input type="text" id="folderName" v-model="newFolderData.name" placeholder="Ex: Droit Immobilier" required />
            </div>
            
            <div class="form-group">
              <label for="folderDesc">Description</label>
              <textarea id="folderDesc" v-model="newFolderData.description" placeholder="Courte description de ce dossier..." rows="3" required></textarea>
            </div>

            <div class="folder-modal-footer">
              <button type="button" class="btn-cancel" @click="isFolderModalOpen = false">Annuler</button>
              <button type="submit" class="btn-save">Créer le dossier</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw, onMounted, reactive } from 'vue';
import { PlusIcon, TrashIcon, PencilSquareIcon, DocumentTextIcon, ArrowLeftIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/outline';
import folderCards from '../../../cards/folderCards.vue'; 
import {useContratStore} from '../../../../stores/contratStore';
import type {Contrat, Category} from '../../../../stores/contratStore';
import {useAdminContratStore} from '../../../../stores/adminContratStore'

export default {
  
  name: 'AdminCategories',
  
  components: { folderCards },
  
  props: {
    categories: { 
      type: Array as () => string[], 
      required: true 
    },
    contracts: { 
      type: Array as () => any[], 
      required: true 
    },
    searchQuery: { 
      type: String, 
      default: '' 
    }
  },
  
  emits: ['add-category', 'delete-category', 'add-contract', 'edit-contract', 'delete-contract', 'toggle-status'],
  
  setup(props, { emit }) {
    
    // Store pour gérer les catégories

    const contratstore = useContratStore();
    const adminStore = useAdminContratStore();

    const openedCategory = ref<string | null>(null);
    const newCategory = ref<null | string>('');

    // About Modale
    const isFolderModalOpen = ref<boolean>(false);
    const newFolderData = reactive({
      name:'',
      description:''
    })

    // --- RECHERCHE ---
    const filteredCategories = computed(() => {
      if (!props.searchQuery) return props.categories;
      return props.categories.filter(c => {
        const catName = typeof c === 'string' ? c : (c as any).name;
        return catName.toLowerCase().includes(props.searchQuery.toLowerCase());
      });
    });

    const filteredContracts = computed(() => {
      let list = props.contracts.filter(c => c.category === openedCategory.value);
      if (props.searchQuery) {
        list = list.filter(c => c.title.toLowerCase().includes(props.searchQuery.toLowerCase()));
      }
      return list;
    });

    // --- NAVIGATION ---
    const openCategory = (cat: string | any) => { 
      openedCategory.value = typeof cat === 'string' ? cat : cat.name;
    };
    const closeCategory = () => { openedCategory.value = null; };

    // --- ACTIONS DOSSIERS ---
    const handleAdd = () => {
      if (newFolderData.name.trim() !== '') {
        // 1. Appel au store avec le bon format
        adminStore.addNewCategory({ 
            title: newFolderData.name, 
            description: newFolderData.description 
        });
        
        // 2. Émission vers le parent
        emit('add-category', { 
          name: newFolderData.name, 
          description: newFolderData.description 
        });
        
        // 3. Réinitialisation
        newFolderData.name = '';
        newFolderData.description = '';
        isFolderModalOpen.value = false;

        contratstore.getCategories();
      }
    };

    const handleDeleteFolder = (index: number, catName: string) => {
      // Alerte globale de suppression de dossier et de son contenu
      if (confirm(`⚠️ ATTENTION : Si vous supprimez le dossier "${catName}", vous supprimerez également TOUT son contenu (tous les contrats associés). Voulez-vous vraiment continuer ?`)) {
        emit('delete-category', index, catName);
      }
    };

    const handleDeleteContract = (id: number) => {
      if(confirm('Supprimer ce contrat définitivement ?')) emit('delete-contract', id);
    };

    onMounted(()=>{
      contratstore.getCategories();
    })

    return {
      newFolderData,
      isFolderModalOpen,
      contratstore,
      adminStore,
      openedCategory, 
      openCategory, 
      closeCategory, 
      newCategory, 
      filteredCategories, 
      filteredContracts,
      handleAdd, handleDeleteFolder, handleDeleteContract,
      PlusIcon: markRaw(PlusIcon), TrashIcon: markRaw(TrashIcon), 
      PencilSquareIcon: markRaw(PencilSquareIcon), DocumentTextIcon: markRaw(DocumentTextIcon), 
      ArrowLeftIcon: markRaw(ArrowLeftIcon), MagnifyingGlassIcon: markRaw(MagnifyingGlassIcon)
    };
  }
}
</script>

<style scoped>
.categories-container { font-family: 'Inter', sans-serif; }

/* DOSSIERS */
.folders-section { background: #ffffff; border-radius: 24px; padding: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }

/* CORRECTION : L'ancien width: 20%; a été remplacé par fit-content pour éviter d'écraser le texte */
.add-input-group { display: flex; width: fit-content; margin-bottom: 1.5rem; }

.add-folder-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 0.8rem 1.2rem;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background 0.2s;
  white-space: nowrap; /* 👈 EMPÊCHE LE TEXTE DE REVENIR À LA LIGNE */
}
.add-folder-btn:hover { background: #1d4ed8; }

/* --- SYSTÈME DE GRILLES DEMANDÉ --- */
/* 4 dossiers par ligne */
.grid-4-cols { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; padding: 1rem 0; }
/* 2 contrats par ligne */
.grid-2-cols { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }

/* Cartes Dossiers */
.folder-wrapper { position: relative; cursor: pointer; transition: 0.2s; border-radius: 16px; }
.folder-wrapper:hover { transform: translateY(-3px); }
.delete-folder-btn { position: absolute; top: -10px; right: -10px; z-index: 10; background: #ffffff; border: 1px solid #fee2e2; color: #ef4444; border-radius: 8px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; opacity: 0; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.1); }
.folder-wrapper:hover .delete-folder-btn { opacity: 1; }
.delete-folder-btn:hover { background: #ef4444; color: white; }

/* VUE INTÉRIEUR DOSSIER */
.opened-folder-view { background: #ffffff; border-radius: 24px; padding: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
.opened-folder-header { display: flex; align-items: center; gap: 1.5rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 1.5rem; }
.btn-secondary { background: #ffffff; border: 1px solid #cbd5e1; padding: 0.6rem 1rem; border-radius: 10px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 2rem; color: #1e293b; width: fit-content; white-space: nowrap; }
.text-blue { color: #2563eb; margin: 0; font-size: 1.4rem; font-weight: 800;}
.btn-secondary *{ width: 20px; }

/* Cartes Contrats */
.contract-card { background: #ffffff; border-radius: 24px; padding: 1.5rem; border: 1px solid #e2e8f0; display: flex; flex-direction: column; gap: 1.2rem; transition: 0.3s ease; }
.contract-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }
.card-offline { opacity: 0.7; filter: grayscale(40%); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; }
.icon-box-light { width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; background: #eff6ff; color: #3b82f6; }
.status-badge { padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; white-space: nowrap; }
.badge-green { background: #d1fae5; color: #059669; }
.badge-gray { background: #f1f5f9; color: #64748b; }
.dark-text { color: var(--primary-color); margin: 0; font-size: 1.1rem; font-weight: 700;}
.gray-text { color: #64748b; font-size: 0.85rem; }

.card-footer { display: flex; justify-content: flex-end; border-top: 1px solid #f1f5f9; padding-top: 1.2rem; }
.actions-block { display: flex; align-items: center; gap: 0.5rem; }

/* Switch et boutons d'action */
.switch { position: relative; display: inline-block; width: 36px; height: 20px; margin-right: 0.5rem; flex-shrink: 0; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: #fff; transition: .4s; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
input:checked + .slider { background-color: #10b981; }
input:checked + .slider:before { transform: translateX(16px); }

.action-icon-btn { background: #f8fafc; border: 1px solid #e2e8f0; color: #64748b; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; flex-shrink: 0; }
.action-icon-btn:hover { background: #e2e8f0; color: #1e293b; }
.delete-btn:hover { background: #fee2e2; border-color: #fecaca; color: #ef4444; }

/* Carte Ajout */
.add-card { border: 2px dashed #cbd5e1; background: #f8fafc; align-items: center; justify-content: center; text-align: center; cursor: pointer; }
.add-card:hover { border-color: #2563eb; }
.add-circle { width: 50px; height: 50px; border-radius: 50%; background: #eff6ff; color: #2563eb; display: flex; align-items: center; justify-content: center; }


/* --- MODALE D'AJOUT DE DOSSIER --- */
.folder-modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 100;
  padding: 1rem;
}
.folder-modal {
  background: white; border-radius: 20px; width: 100%; max-width: 450px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
}
.folder-modal-header {
  display: flex; justify-content: space-between; align-items: center; text-align: center; background: var(--primary-color);
  padding: 1.5rem 2rem; border-bottom: 1px solid #e2e8f0;
}
/* CORRECTION : L'en-tête ne passe plus à la ligne */
.folder-modal-header h3 { margin: 0; font-size: 1.2rem; color: #ffffff; white-space: nowrap; }
.close-modal-btn { background: transparent; border: none; font-size: 1.5rem; color: #94a3b8; cursor: pointer }
.close-modal-btn:hover { color: #ef4444; }

.folder-modal-body { padding: 2rem; }
.form-group { margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-weight: 600; font-size: 0.9rem; color: #334155; }
.form-group input, .form-group textarea {
  width: 100%; padding: 0.8rem; border: 1px solid #cbd5e1; border-radius: 8px;
  background: #f8fafc; font-family: inherit; font-size: 0.95rem; outline: none;
  box-sizing: border-box;
}
.form-group input:focus, .form-group textarea:focus { border-color: #2563eb; background: #fff; }

.folder-modal-footer {
  display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; flex-wrap: nowrap;
}

/* CORRECTION : Les boutons de la modale ne passent plus à la ligne */
.btn-cancel { background: transparent; border: 1px solid #cbd5e1; color: #64748b; padding: 0.6rem 1.2rem; border-radius: 8px; cursor: pointer; font-weight: 600; white-space: nowrap; }
.btn-cancel:hover { background: #f1f5f9; }
.btn-save { background: var(--primary-color); border: none; color: white; padding: 0.6rem 1.2rem; border-radius: 8px; cursor: pointer; font-weight: 600; white-space: nowrap; }
.btn-save:hover { background: #1d4ed8; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }


/* RESPONSIVE DES GRILLES */
@media (max-width: 1024px) {
  .grid-4-cols { grid-template-columns: repeat(2, 1fr); }
  .grid-2-cols { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
  .grid-4-cols { grid-template-columns: 1fr; }
}
</style>