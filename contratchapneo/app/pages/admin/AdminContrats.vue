<template>
  <div class="contracts-wrapper">
    
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

        <div class="dropdown-container">
          <button class="add-global-btn" @click="toggleDropdown">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="btn-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Nouveau Contrat
          </button>

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

    <!-- ⚡️ Branchement du Store -->
    <adminCategories 
      v-if="activeTab === 'categories'"
      :categories="adminStore.categories"
      :contracts="adminStore.contracts" 
      :searchQuery="searchQuery"
      @add-contract="openModal"
      @edit-contract="openModal"
    />

    <adminSurmesure 
      v-if="activeTab === 'surmesure'"
      ref="surmesureRef"
      :contracts="adminStore.customContracts"
      :searchQuery="searchQuery"
    />

    <!-- MODALE GLOBALE D'AJOUT / ÉDITION -->
    <adminContratsModal 
      v-if="isModalOpen" 
      :contract="selectedContract" 
      :categories="adminStore.categories"
      :preselectedCategory="targetCategory"
      @close="closeModal" 
      @save="handleSaveContract"
    />

  </div>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import adminContratsModal from '../../components/modale/adminContratModale.vue';
import adminCategories from '../../components/sections/adminSection/admincontrat/adminCategory.vue'; 
import adminSurmesure from '../../components/sections/adminSection/admincontrat/adminSurmesure.vue';
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'; 
import { useAdminContratStore } from '../../stores/adminContratStore'; // 👈 Ajuste le chemin si besoin

export default {
  name: 'AdminContracts',
  components: { adminContratsModal, adminCategories, adminSurmesure },
  setup() {
    // ⚡️ Initialisation du store
    const adminStore = useAdminContratStore();
    
    const activeTab = ref('categories');
    const searchQuery = ref('');
    const surmesureRef = ref<any>(null);
    const isDropdownOpen = ref(false);
    
    const toggleDropdown = () => isDropdownOpen.value = !isDropdownOpen.value;

    const closeDropdownEvent = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('.dropdown-container')) isDropdownOpen.value = false;
    };

    onMounted(async () => { 
      document.addEventListener('click', closeDropdownEvent); 
      // ⚡️ Récupération de toutes les données du backend au chargement
      await Promise.all([
        adminStore.fetchCategories(),
        adminStore.fetchContracts(),
        adminStore.fetchCustomContracts()
      ]);
    });
    
    onBeforeUnmount(() => document.removeEventListener('click', closeDropdownEvent));

    const handleCreateStandard = () => {
      activeTab.value = 'categories';
      openModal({ isNew: true, categoryId: '' });
      isDropdownOpen.value = false;
    };

    const handleCreateCustom = () => {
      activeTab.value = 'surmesure';
      isDropdownOpen.value = false;
      setTimeout(() => { if (surmesureRef.value) surmesureRef.value.openLocalModal(); }, 50);
    };

    // --- MODALE ---
    const isModalOpen = ref(false);
    const selectedContract = ref<any>(null);
    const targetCategory = ref(''); 

    const openModal = (payload: any = null) => {
      if (payload && payload.isNew) {
        selectedContract.value = null;
        targetCategory.value = payload.categoryId || ''; 
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

    // ⚡️ Sauvegarde vers le Backend via FormData
    const handleSaveContract = async (formData: FormData, id: string | null) => {
      try {
        if (id) {
          await adminStore.updateContract(id, formData);
        } else {
          await adminStore.addNewContract(formData);
        }
        closeModal();
      } catch (e) {
        console.error("Erreur de sauvegarde:", e);
      }
    };

    return {
      adminStore,
      activeTab, 
      isModalOpen, selectedContract, targetCategory, openModal, closeModal, handleSaveContract,
      searchQuery, MagnifyingGlassIcon, surmesureRef,
      isDropdownOpen, toggleDropdown, handleCreateStandard, handleCreateCustom
    };
  }
}
</script>

<style scoped>
.admin-layout-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8fafc;
}

.admin-main-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: calc(80px + env(safe-area-inset-bottom)); 
}

@media (max-width: 728px) {
  .admin-main-content {
    margin-left: 0;
    margin-bottom: 80px;
    padding: 1rem;
  }
}
</style>