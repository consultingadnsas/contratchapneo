<template>
  <div class="contracts-wrapper">
    
    <div class="header-section">
      <div class="title-and-search">
        <h3 class="section-title">Gestion du Catalogue</h3>
        <button v-if="activeTab === 'contracts'" class="btn-primary" @click="openModal()">
          <component :is="PlusIcon" class="icon-sm" /> Ajouter un modèle
        </button>
      </div>

      <div class="tabs-group">
        <button class="tab-btn" :class="{ active: activeTab === 'contracts' }" @click="activeTab = 'contracts'">
          Modèles de Contrats
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'categories' }" @click="activeTab = 'categories'">
          Catégories & Dossiers
        </button>
      </div>
    </div>

    <div v-if="activeTab === 'contracts'" class="contracts-grid">
      
      <div class="contract-card" v-for="contract in contracts" :key="contract.id" :class="{'card-offline': !contract.isActive}">
        <div class="card-header">
          <div class="icon-box-light" :class="getCategoryColor(contract.category)">
            <component :is="DocumentTextIcon" class="icon-md" />
          </div>
          <span class="status-badge" :class="contract.isActive ? 'badge-green' : 'badge-gray'">
            {{ contract.isActive ? 'En ligne' : 'Hors ligne' }}
          </span>
        </div>

        <div class="card-body">
          <h4 class="dark-text">{{ contract.title }}</h4>
          <span class="gray-text text-sm">{{ contract.category }}</span>
        </div>

        <div class="card-footer">
          <div class="price-block">
            <template v-if="contract.isPromoActive">
              <span class="text-strikethrough">{{ contract.price }} F</span>
              <strong class="text-green">{{ contract.promoPrice }} F</strong>
            </template>
            <template v-else>
              <strong class="dark-text">{{ contract.price }} FCFA</strong>
            </template>
          </div>
          <div class="actions-block">
            <label class="switch" title="Mettre en ligne / Hors ligne">
              <input type="checkbox" v-model="contract.isActive" @change="toggleStatus(contract)">
              <span class="slider round"></span>
            </label>
            <button class="action-icon-btn edit-btn" @click="openModal(contract)">
              <component :is="PencilSquareIcon" class="icon-sm" />
            </button>
            <button class="action-icon-btn delete-btn" @click="deleteContract(contract.id)">
              <component :is="TrashIcon" class="icon-sm" />
            </button>
          </div>
        </div>
      </div>

      <div class="contract-card add-card" @click="openModal()">
        <div class="add-circle">
          <component :is="PlusIcon" class="icon-lg" />
        </div>
        <h4 class="dark-text mt-3">Créer un nouveau modèle</h4>
        <span class="gray-text text-sm">Ajouter au catalogue</span>
      </div>
    </div>

    <div v-if="activeTab === 'categories'" class="categories-wrapper">
      
      <div class="folders-section">
        <h3 class="section-title text-md mb-3">Modèles de Contrats (Boutique)</h3>
        <div class="add-input-group">
          <input type="text" v-model="newStdCat" placeholder="Ajouter une catégorie..." @keyup.enter="addStdCategory" />
          <button class="btn-primary-small" @click="addStdCategory"><component :is="PlusIcon" class="icon-sm"/></button>
        </div>
        
        <div class="folders-grid">
          <folderCards 
            v-for="(cat, index) in standardCategories" 
            :key="'std'+index"
            :title="cat"
            subtitle="Modèles OHADA"
            color="blue"
            :hasItems="true"
          />
        </div>
      </div>

      <div class="folders-section mt-4">
        <h3 class="section-title text-md mb-3">Services Sur-Mesure</h3>
        <div class="add-input-group">
          <input type="text" v-model="newCustomCat" placeholder="Ajouter une catégorie..." @keyup.enter="addCustomCategory" />
          <button class="btn-primary-small" @click="addCustomCategory"><component :is="PlusIcon" class="icon-sm"/></button>
        </div>
        
        <div class="folders-grid">
          <folderCards 
            v-for="(cat, index) in customCategories" 
            :key="'cus'+index"
            :title="cat"
            subtitle="Expertise juridique"
            color="purple"
            :hasItems="true"
          />
        </div>
      </div>
    </div>

    <adminContratsModal 
      v-if="isModalOpen" 
      :contract="selectedContract" 
      :categories="standardCategories"
      @close="closeModal" 
      @save="handleSaveContract"
    />

  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { PlusIcon, TrashIcon, PencilSquareIcon, DocumentTextIcon } from '@heroicons/vue/24/outline';
import adminContratsModal from '../../modale/adminContratModale.vue';
import folderCards from '../../cards/folderCards.vue'; // Ton nouveau composant

export default {
  name: 'AdminContracts',
  components: { adminContratsModal, folderCards },
  props: { targetTab: { type: String, default: 'contracts' } },
  setup(props) {
    const activeTab = ref(props.targetTab || 'contracts');
    const newStdCat = ref('');
    const newCustomCat = ref('');
    
    const standardCategories = ref(['Création d\'entreprise', 'Ressources Humaines', 'Immobilier', 'Packs']);
    const customCategories = ref(['Fusion & Acquisition', 'Audit Juridique', 'Litige Commercial', 'Montage Financier']);

    const addStdCategory = () => { if (newStdCat.value.trim() !== '') { standardCategories.value.push(newStdCat.value.trim()); newStdCat.value = ''; } };
    const addCustomCategory = () => { if (newCustomCat.value.trim() !== '') { customCategories.value.push(newCustomCat.value.trim()); newCustomCat.value = ''; } };

    const contracts = ref([
      { id: 1, title: 'Statuts SARL OHADA', category: 'Création d\'entreprise', price: 15000, isPromoActive: false, promoPrice: null, isActive: true },
      { id: 2, title: 'Contrat de Travail CDD', category: 'Ressources Humaines', price: 10000, isPromoActive: true, promoPrice: 7500, isActive: true },
    ]);

    const deleteContract = (id: number) => { if(confirm('Supprimer ?')) { contracts.value = contracts.value.filter(c => c.id !== id); } };
    const toggleStatus = (contract: any) => { console.log(`Statut changé`); };

    const isModalOpen = ref(false);
    const selectedContract = ref<any>(null);
    const openModal = (contract: any = null) => { selectedContract.value = contract; isModalOpen.value = true; };
    const closeModal = () => { isModalOpen.value = false; selectedContract.value = null; };

    const handleSaveContract = (data: any) => {
      if (data.id) {
        const index = contracts.value.findIndex(c => c.id === data.id);
        if (index !== -1) contracts.value[index] = { ...contracts.value[index], ...data, price: Number(data.price), promoPrice: data.promoPrice ? Number(data.promoPrice) : null };
      } else {
        contracts.value.unshift({ id: Date.now(), ...data, price: Number(data.price), promoPrice: data.promoPrice ? Number(data.promoPrice) : null, isActive: true });
      }
      closeModal();
    };

    // Design : Alterne les couleurs des icônes selon la catégorie
    const getCategoryColor = (cat: string) => {
      if (cat.includes('Création')) return 'bg-blue-light';
      if (cat.includes('Ressources')) return 'bg-orange-light';
      return 'bg-purple-light';
    };

    return {
      activeTab, contracts, deleteContract, toggleStatus,
      newStdCat, newCustomCat, standardCategories, customCategories, addStdCategory, addCustomCategory,
      isModalOpen, selectedContract, openModal, closeModal, handleSaveContract, getCategoryColor,
      PlusIcon, TrashIcon, PencilSquareIcon, DocumentTextIcon
    };
  }
}
</script>

<style scoped>
/* ==============================================================
   CHARTE GRAPHIQUE (MoonInc / ContratChap)
   ============================================================== */
.contracts-wrapper {
  --bg-main: #f8fafc;        
  --bg-panel: #ffffff;       
  --bg-panel-light: #f1f5f9; 
  --text-dark: #1e293b;      
  --text-gray: #94a3b8;      
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2rem; 
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

/* --- EN-TÊTE --- */
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-and-search { display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.2rem; color: var(--text-dark); font-weight: 700; margin: 0; }
.text-md { font-size: 1rem; }

/* BOUTON PRIMARY */
.btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); }
.btn-primary-small { background: var(--accent-blue); color: white; border: none; padding: 0.6rem; border-radius: 12px; cursor: pointer; transition: 0.2s; }
.btn-primary-small:hover { background: #1d4ed8; }

/* ONGLETS */
.tabs-group { display: flex; background: var(--bg-panel-light); border-radius: 50px; padding: 0.3rem; width: fit-content; }
.tab-btn { background: transparent; border: none; color: var(--text-gray); font-size: 0.85rem; font-weight: 600; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: all 0.2s ease; }
.tab-btn.active { background: var(--bg-panel); color: var(--accent-blue); box-shadow: 0px 2px 10px rgba(0,0,0,0.05); }

/* --- GRILLE DE CARTES CONTRATS --- */
.contracts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }

.contract-card {
  background: var(--bg-panel); border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #f8fafc;
  display: flex; flex-direction: column; gap: 1.2rem; transition: 0.3s ease;
}
.contract-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }
.card-offline { opacity: 0.8; filter: grayscale(40%); }

.card-header { display: flex; justify-content: space-between; align-items: flex-start; }
.icon-box-light { width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; }
.bg-blue-light { background: #eff6ff; color: #3b82f6; }
.bg-orange-light { background: #fff7ed; color: #f97316; }
.bg-purple-light { background: #faf5ff; color: #a855f7; }

.status-badge { padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.badge-green { background: #d1fae5; color: #059669; }
.badge-gray { background: #f1f5f9; color: #64748b; }

.card-body h4 { margin: 0 0 0.2rem 0; font-size: 1.05rem; font-weight: 700; color: var(--text-dark); line-height: 1.3; }
.gray-text { color: var(--text-gray); }
.dark-text { color: var(--text-dark); }
.text-sm { font-size: 0.8rem; }

.card-footer { display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid #f1f5f9; padding-top: 1.2rem; }
.price-block { display: flex; flex-direction: column; }
.text-green { color: #10b981; font-weight: 700; font-size: 1.1rem; }
.text-strikethrough { color: #cbd5e1; text-decoration: line-through; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.1rem; }

.actions-block { display: flex; align-items: center; gap: 0.5rem; }

/* BOUTON SWITCH */
.switch { position: relative; display: inline-block; width: 36px; height: 20px; margin-right: 0.5rem; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: #fff; transition: .4s; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
input:checked + .slider { background-color: #10b981; }
input:checked + .slider:before { transform: translateX(16px); }

/* Petits boutons d'action */
.action-icon-btn { background: #f8fafc; border: 1px solid #e2e8f0; color: #64748b; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }
.action-icon-btn:hover { background: #e2e8f0; color: var(--text-dark); }
.delete-btn:hover { background: #fee2e2; border-color: #fecaca; color: #ef4444; }

/* Carte Ajout */
.add-card { border: 2px dashed #cbd5e1; background: transparent; box-shadow: none; align-items: center; justify-content: center; text-align: center; cursor: pointer; min-height: 220px; }
.add-card:hover { border-color: var(--accent-blue); background: #f8fafc; }
.add-circle { width: 50px; height: 50px; border-radius: 50%; background: #eff6ff; color: var(--accent-blue); display: flex; align-items: center; justify-content: center; }
.mt-3 { margin-top: 0.8rem; }
.icon-lg { width: 24px; height: 24px; }

/* --- GRILLE CATÉGORIES (DOSSIERS) --- */
.folders-section { background: var(--bg-panel); border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
.add-input-group { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; max-width: 400px; }
.add-input-group input { flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; padding: 0.6rem 1rem; border-radius: 12px; outline: none; }
.add-input-group input:focus { border-color: var(--accent-blue); }

.folders-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }


.pastel-blue { background-color: #e0f2fe; }
.pastel-purple { background-color: #f3e8ff; }
.mt-4 { margin-top: 1.5rem; }
.mb-3 { margin-bottom: 1rem; }
.icon-sm { width: 18px; height: 18px; }
.icon-md { width: 22px; height: 22px; }
</style>