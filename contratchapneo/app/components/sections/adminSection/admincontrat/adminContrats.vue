<template>
  <div class="contracts-wrapper">
    
    <!-- EN-TÊTE ET ONGLETS -->
   <div class="header-section">
      <div class="title-and-search">
        <h3 class="section-title">Gestion du Catalogue</h3>
        
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-gray icon-sm" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher un dossier ou contrat..." />
        </div>
      </div>

      <!-- NOUVEAU : Wrapper pour aligner les onglets et le bouton global -->
      <div class="tabs-and-actions">
        <div class="tabs-group">
          <button class="tab-btn" :class="{ active: activeTab === 'categories' }" @click="activeTab = 'categories'">
            Catégories de contrats
          </button>
          <button class="tab-btn" :class="{ active: activeTab === 'surmesure' }" @click="activeTab = 'surmesure'">
            Contrats Sur-Mesure
          </button>
        </div>

        <!-- BOUTON D'AJOUT GLOBAL -->
        <button class="add-global-btn" @click="openModal({ isNew: true, categoryName: '' })">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="btn-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          Nouveau Contrat
        </button>
      </div>
    </div>

    <!-- ONGLET 1 : COMPOSANT CATÉGORIES (BOUTIQUE) -->
    <adminCategories 
      v-if="activeTab === 'categories'"
      :categories="standardCategories"
      :contracts="contratStore.contracts"
      :searchQuery="searchQuery"
      @add-category="addStdCategory"
      @delete-category="deleteStdCategory"
      @add-contract="openModal"
      @edit-contract="openModal"
      @delete-contract="deleteStdContract"
      @toggle-status="toggleStdStatus"
    />

    <!-- ONGLET 2 : COMPOSANT SUR-MESURE -->
    <adminSurmesure 
      v-if="activeTab === 'surmesure'"
      :categories="customCategories"
      :contracts="customContracts"
      :searchQuery="searchQuery"
      @add-category="addCustomCategory"
      @delete-category="deleteCustomCategory"
      @add-contract="openModal"
      @edit-contract="openModal"
      @delete-contract="deleteCustomContract"
      @toggle-status="toggleCustomStatus"
    />

    <!-- MODALE GLOBALE D'AJOUT / ÉDITION -->
    <adminContratsModal 
      v-if="isModalOpen" 
      :contract="selectedContract" 
      :categories="activeTab === 'categories' ? standardCategories : customCategories"
      :preselectedCategory="targetCategory"
      @close="closeModal" 
      @save="handleSaveContract"
    />

  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import adminContratsModal from '../../../modale/adminContratModale.vue';
import adminCategories from './adminCategory.vue'; 
import adminSurmesure from './adminSurmesure.vue';
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'; 
import {useContratStore} from '../../../../stores/contratStore';

export default {
  name: 'AdminContracts',
  components: { adminContratsModal, adminCategories, adminSurmesure },
  setup() {
    const contratStore = useContratStore();
    const activeTab = ref('categories');
    const searchQuery = ref('');
    
    // --- DONNÉES : BOUTIQUE ---
    const standardCategories = ref(['Création d\'entreprise', 'Ressources Humaines', 'Immobilier']);
    const standardContracts = ref([
      { id: 1, title: 'Statuts SARL OHADA', category: 'Création d\'entreprise', price: 15000, isActive: true },
      { id: 2, title: 'Contrat de Travail CDD', category: 'Ressources Humaines', price: 10000, isActive: true },
    ]);

    // --- DONNÉES : SUR-MESURE ---
    const customCategories = ref(['Fusion & Acquisition', 'Audit Juridique']);
    const customContracts = ref([
      { id: 3, title: 'Pacte d\'actionnaires complexe', category: 'Fusion & Acquisition', price: 150000, isActive: true }
    ]);

    // --- LOGIQUE : DOSSIERS ---
    const addStdCategory = (cat: string) => standardCategories.value.push(cat);
    const addCustomCategory = (cat: string) => customCategories.value.push(cat);

    // Suppression d'un dossier ET de son contenu
    const deleteStdCategory = (index: number, catName: string) => {
      standardCategories.value.splice(index, 1);
      standardContracts.value = standardContracts.value.filter(c => c.category !== catName);
    };
    const deleteCustomCategory = (index: number, catName: string) => {
      customCategories.value.splice(index, 1);
      customContracts.value = customContracts.value.filter(c => c.category !== catName);
    };

    // --- LOGIQUE : CONTRATS ---
    const deleteStdContract = (id: number) => { standardContracts.value = standardContracts.value.filter(c => c.id !== id); };
    const deleteCustomContract = (id: number) => { customContracts.value = customContracts.value.filter(c => c.id !== id); };
    
    const toggleStdStatus = (contract: any) => console.log(`Statut modifié (Boutique) : ${contract.title}`);
    const toggleCustomStatus = (contract: any) => console.log(`Statut modifié (Sur-Mesure) : ${contract.title}`);

    // --- GESTION DE LA MODALE ---
    const isModalOpen = ref(false);
    const selectedContract = ref<any>(null);
    const targetCategory = ref(''); 

    const openModal = (payload: any = null) => {
      if (payload && payload.isNew) {
        selectedContract.value = null;
        targetCategory.value = payload.categoryName; 
      } else {
        selectedContract.value = payload; 
        targetCategory.value = payload ? payload.category : '';
      }
      isModalOpen.value = true;
    };
    
    const closeModal = () => { 
      isModalOpen.value = false; 
      selectedContract.value = null; 
      targetCategory.value = '';
    };

    const handleSaveContract = (data: any) => {
      const activeContracts = activeTab.value === 'categories' ? standardContracts : customContracts;
      
      if (data.id) {
        const index = activeContracts.value.findIndex(c => c.id === data.id);
        if (index !== -1) activeContracts.value[index] = { ...activeContracts.value[index], ...data };
      } else {
        activeContracts.value.unshift({ id: Date.now(), ...data, isActive: true });
      }
      closeModal();
    };

    return {
      contratStore,
      activeTab, 
      standardCategories, standardContracts, 
      customCategories, customContracts,
      addStdCategory, deleteStdCategory, deleteStdContract, toggleStdStatus,
      addCustomCategory, deleteCustomCategory, deleteCustomContract, toggleCustomStatus,
      isModalOpen, selectedContract, targetCategory, openModal, closeModal, handleSaveContract,
      searchQuery, MagnifyingGlassIcon,
    };
  }
}
</script>

<style scoped>
.contracts-wrapper {
  --bg-main: #f8fafc; --bg-panel: #ffffff; --bg-panel-light: #f1f5f9; 
  --text-dark: #1e293b; --text-gray: #94a3b8; --accent-blue: #2563eb;
  display: flex; flex-direction: column; gap: 2rem; font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

.header-section { display: flex; flex-direction: column; gap: 1.5rem; }

.title-and-search { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  flex-wrap: wrap; 
  gap: 1rem; 
}

/* NOUVEAU : Flexbox pour séparer les onglets et le bouton global */
.tabs-and-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  width: 100%;
}

.search-box {
  display: flex; align-items: center; background: #ffffff; 
  border: 1px solid #e2e8f0; border-radius: 50px; 
  padding: 0.6rem 1.2rem; max-width: 500px; width: 100%;
}
.search-box:focus-within { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.search-box input { border: none; outline: none; width: 100%; margin-left: 0.5rem; font-size: 0.9rem; color: #1e293b; }

.icon-gray { width: 20px; height: 20px; color: #94a3b8; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 700; margin: 0; }

.tabs-group { display: flex; background: var(--primary-color); border-radius: 50px; padding: 0.3rem; width: fit-content; }
.tab-btn { background: transparent; border: none; color: #ffffff; font-size: 0.85rem; font-weight: 600; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: all 0.2s ease; }
.tab-btn.active { background: var(--secondary-light-color); color: #ffffff; box-shadow: 0px 2px 10px rgba(0,0,0,0.05); }

/* NOUVEAU : Style du bouton d'ajout global */
.add-global-btn {
  display: flex;
  align-items: center;
  width: fit-content;
  gap: 0.4rem;
  background-color: var(--primary-color);
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.6rem 1.4rem;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
}

.add-global-btn:hover {
  background-color: #1d4ed8;
  transform: translateY(-2px);
}

.btn-icon {
  width: 18px;
  height: 18px;
}
</style>