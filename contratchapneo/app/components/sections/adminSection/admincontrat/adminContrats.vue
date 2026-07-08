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

      <div class="tabs-and-actions">
        <div class="tabs-group">
          <button class="tab-btn" :class="{ active: activeTab === 'categories' }" @click="activeTab = 'categories'">
            Catégories de contrats
          </button>
          <button class="tab-btn" :class="{ active: activeTab === 'surmesure' }" @click="activeTab = 'surmesure'">
            Contrats Sur-Mesure
          </button>
        </div>

        <!-- NOUVEAU : BOUTON D'AJOUT GLOBAL AVEC MENU DÉROULANT -->
        <div class="dropdown-container">
          <button class="add-global-btn" @click="toggleDropdown">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="btn-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Nouveau Contrat
          </button>

          <!-- Le menu déroulant -->
          <div v-if="isDropdownOpen" class="dropdown-menu">
            <button class="dropdown-item" @click="handleCreateStandard">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="dropdown-icon"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" /></svg>
              Modèle de contrat
            </button>
            <button class="dropdown-item" @click="handleCreateCustom">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="dropdown-icon"><path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z" /></svg>
              Contrat sur-mesure
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ONGLET 1 : COMPOSANT CATÉGORIES (BOUTIQUE) -->
    <adminCategories 
      v-if="activeTab === 'categories'"
      :categories="standardCategories"
      :contracts="standardContracts"
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
      ref="surmesureRef"
      :contracts="customContracts"
      :searchQuery="searchQuery"
      @delete-contract="deleteCustomContract"
      @toggle-status="toggleCustomStatus"
    />

    <!-- MODALE GLOBALE D'AJOUT / ÉDITION (Uniquement pour Modèles) -->
    <adminContratsModal 
      v-if="isModalOpen" 
      :contract="selectedContract" 
      :categories="standardCategories"
      :preselectedCategory="targetCategory"
      @close="closeModal" 
      @save="handleSaveContract"
    />

  </div>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import adminContratsModal from '../../../modale/adminContratModale.vue';
import adminCategories from './adminCategory.vue'; 
import adminSurmesure from './adminSurmesure.vue';
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'; 

export default {
  name: 'AdminContracts',
  components: { adminContratsModal, adminCategories, adminSurmesure },
  setup() {
    const activeTab = ref('categories');
    const searchQuery = ref('');
    const surmesureRef = ref<any>(null); // Pour appeler la méthode de l'enfant
    
    // --- GESTION DU DROPDOWN ---
    const isDropdownOpen = ref(false);
    
    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value;
    };

    const closeDropdownEvent = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('.dropdown-container')) {
        isDropdownOpen.value = false;
      }
    };

    onMounted(() => { document.addEventListener('click', closeDropdownEvent); });
    onBeforeUnmount(() => { document.removeEventListener('click', closeDropdownEvent); });

    // --- ACTIONS DU MENU ---
    const handleCreateStandard = () => {
      activeTab.value = 'categories';
      openModal({ isNew: true, categoryName: '' });
      isDropdownOpen.value = false;
    };

    const handleCreateCustom = () => {
      activeTab.value = 'surmesure';
      isDropdownOpen.value = false;
      // On attend que l'onglet s'affiche avant d'ouvrir sa modale
      setTimeout(() => {
        if (surmesureRef.value) {
          surmesureRef.value.openLocalModal();
        }
      }, 50);
    };

    // --- DONNÉES : BOUTIQUE ---
    const standardCategories = ref(['Création d\'entreprise', 'Ressources Humaines', 'Immobilier']);
    const standardContracts = ref([
      { id: 1, title: 'Statuts SARL OHADA', category: 'Création d\'entreprise', price: 15000, isActive: true },
    ]);

    // --- DONNÉES : SUR-MESURE ---
    const customContracts = ref([
      { id: 3, title: 'Pacte d\'actionnaires complexe', price: 150000, isActive: true }
    ]);

    // --- LOGIQUE : DOSSIERS ---
    const addStdCategory = (cat: string) => standardCategories.value.push(cat);
    const deleteStdCategory = (index: number, catName: string) => {
      standardCategories.value.splice(index, 1);
      standardContracts.value = standardContracts.value.filter(c => c.category !== catName);
    };

    // --- LOGIQUE : CONTRATS ---
    const deleteStdContract = (id: number) => { standardContracts.value = standardContracts.value.filter(c => c.id !== id); };
    const deleteCustomContract = (id: number) => { customContracts.value = customContracts.value.filter(c => c.id !== id); };
    
    const toggleStdStatus = (contract: any) => console.log(`Statut modifié (Boutique) : ${contract.title}`);
    const toggleCustomStatus = (contract: any) => console.log(`Statut modifié (Sur-Mesure) : ${contract.title}`);

    // --- GESTION DE LA MODALE PRINCIPALE ---
    const isModalOpen = ref(false);
    const selectedContract = ref<any>(null);
    const targetCategory = ref(''); 

    const openModal = (payload: any = null) => {
      if (payload && payload.isNew) {
        selectedContract.value = null;
        targetCategory.value = payload.categoryName || ''; 
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
      if (data.id) {
        const index = standardContracts.value.findIndex(c => c.id === data.id);
        if (index !== -1) standardContracts.value[index] = { ...standardContracts.value[index], ...data };
      } else {
        standardContracts.value.unshift({ id: Date.now(), ...data, isActive: true });
      }
      closeModal();
    };

    return {
      activeTab, 
      standardCategories, standardContracts, customContracts,
      addStdCategory, deleteStdCategory, deleteStdContract, toggleStdStatus,
      deleteCustomContract, toggleCustomStatus,
      isModalOpen, selectedContract, targetCategory, openModal, closeModal, handleSaveContract,
      searchQuery, MagnifyingGlassIcon, surmesureRef,
      isDropdownOpen, toggleDropdown, handleCreateStandard, handleCreateCustom
    };
  }
}
</script>

<style scoped>
/* Les styles de base restent identiques[cite: 11] */
.contracts-wrapper {
  --bg-main: #f8fafc; --bg-panel: #ffffff; --bg-panel-light: #f1f5f9; 
  --text-dark: #1e293b; --text-gray: #94a3b8; --accent-blue: #2563eb;
  display: flex; flex-direction: column; gap: 2rem; font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

.header-section { display: flex; flex-direction: column; gap: 1.5rem; }

.title-and-search { 
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; 
}

.tabs-and-actions {
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; width: 100%;
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

/* --- STYLE DU MENU DÉROULANT --- */
.dropdown-container {
  position: relative;
}

.add-global-btn {
  display: flex; align-items: center; width: fit-content; gap: 0.4rem;
  background-color: var(--primary-color); color: #ffffff; font-size: 0.9rem;
  font-weight: 600; padding: 0.6rem 1.4rem; border: none; border-radius: 50px;
  cursor: pointer; transition: background-color 0.2s ease, transform 0.2s ease;
}
.add-global-btn:hover { background-color: #1d4ed8; }

.btn-icon { width: 18px; height: 18px; }

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  min-width: 220px;
  display: flex;
  flex-direction: column;
  padding: 0.5rem;
  z-index: 50;
  animation: fadeIn 0.2s ease-out;
}

.dropdown-item {
  display: flex; align-items: center; gap: 0.8rem;
  background: transparent; border: none; padding: 0.8rem 1rem;
  font-size: 0.9rem; font-weight: 500; color: #334155;
  text-align: left; cursor: pointer; border-radius: 8px;
  transition: background 0.2s; white-space: nowrap;
}
.dropdown-item:hover { background: #f1f5f9; color: #1e293b; }
.dropdown-icon { width: 18px; height: 18px; color: #64748b; }
.dropdown-item:hover .dropdown-icon { color: #2563eb; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>