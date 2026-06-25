<template>
  <div class="contracts-wrapper">
    
    <div class="header-section">
      <h2 class="page-title">Gestion du Catalogue</h2>
      <div class="tabs-group">
        <button class="tab-btn" :class="{ active: activeTab === 'contracts' }" @click="activeTab = 'contracts'">
          Modèles de Contrats
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'categories' }" @click="activeTab = 'categories'">
          Catégories & Sur-Mesure
        </button>
      </div>
    </div>

    <!-- ONGLET 1 : CONTRATS -->
    <div v-if="activeTab === 'contracts'" class="panel">
      <div class="panel-header-simple">
        <span class="text-gray">Liste des contrats disponibles</span>
        <button class="btn-primary" @click="openModal()">
          <component :is="PlusIcon" class="icon-sm" /> Ajouter un modèle
        </button>
      </div>

      <table class="clean-table">
        <thead>
          <tr>
            <th>Document</th>
            <th>Catégorie</th>
            <th>Prix (FCFA)</th>
            <th class="text-center">En ligne</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contract in contracts" :key="contract.id">
            <td class="font-bold text-white flex-align">
              <span class="doc-icon" :class="{ 'opacity-50': !contract.isActive }">📄</span> 
              <span :class="{ 'text-offline': !contract.isActive }">{{ contract.title }}</span>
            </td>
            <td class="text-gray">{{ contract.category }}</td>
            
            <td class="font-bold">
              <div v-if="contract.isPromoActive" class="price-container">
                <span class="text-strikethrough text-xs">{{ contract.price }}</span>
                <span class="text-green">{{ contract.promoPrice }}</span>
              </div>
              <div v-else class="text-blue">
                {{ contract.price }}
              </div>
            </td>
            
            <td class="text-center">
              <label class="switch">
                <input type="checkbox" v-model="contract.isActive" @change="toggleStatus(contract)">
                <span class="slider round"></span>
              </label>
            </td>
            
            <td class="text-right flex-align-right">
              <button class="action-btn edit-btn" @click="openModal(contract)" title="Modifier">
                <component :is="PencilSquareIcon" class="icon-sm text-gray" />
              </button>
              <button class="action-btn delete-btn" @click="deleteContract(contract.id)" title="Supprimer">
                <component :is="TrashIcon" class="icon-sm text-red" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ONGLET 2 : CATÉGORIES -->
    <div v-if="activeTab === 'categories'" class="categories-grid">
      <div class="panel">
        <div class="panel-header-simple">
          <span class="text-gray">Modèles de Contrats (Boutique)</span>
        </div>
        <div class="add-input-group">
          <input type="text" v-model="newStdCat" placeholder="Nouvelle catégorie boutique..." @keyup.enter="addStdCategory" />
          <button class="btn-add" @click="addStdCategory"><component :is="PlusIcon" class="icon-sm"/></button>
        </div>
        <ul class="cat-list">
          <li v-for="(cat, index) in standardCategories" :key="index">
            <span class="text-white">{{ cat }}</span>
            <button class="action-btn delete-btn" @click="standardCategories.splice(index, 1)">
              <component :is="TrashIcon" class="icon-sm text-red" />
            </button>
          </li>
        </ul>
      </div>

      <div class="panel">
        <div class="panel-header-simple">
          <span class="text-gray">Services Sur-Mesure (Devis)</span>
        </div>
        <div class="add-input-group">
          <input type="text" v-model="newCustomCat" placeholder="Nouvelle catégorie sur-mesure..." @keyup.enter="addCustomCategory" />
          <button class="btn-add" @click="addCustomCategory"><component :is="PlusIcon" class="icon-sm"/></button>
        </div>
        <ul class="cat-list">
          <li v-for="(cat, index) in customCategories" :key="index">
            <span class="text-white">{{ cat }}</span>
            <button class="action-btn delete-btn" @click="customCategories.splice(index, 1)">
              <component :is="TrashIcon" class="icon-sm text-red" />
            </button>
          </li>
        </ul>
      </div>
    </div>

    <!-- APPEL DE LA MODALE -->
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
import { PlusIcon, TrashIcon, PencilSquareIcon } from '@heroicons/vue/24/outline';
import adminContratsModal from '../../modale/adminContratModale.vue';

export default {
  name: 'AdminContracts',
  components: {
    // CORRECTION : Bien déclarer le composant enfant ici
    adminContratsModal
  },
  setup() {
    const activeTab = ref('contracts');

    const newStdCat = ref('');
    const newCustomCat = ref('');
    
    const standardCategories = ref(['Création d\'entreprise', 'Ressources Humaines', 'Immobilier', 'Packs']);
    const customCategories = ref(['Fusion & Acquisition', 'Audit Juridique', 'Litige Commercial', 'Montage Financier']);

    const addStdCategory = () => {
      if (newStdCat.value.trim() !== '') { 
        standardCategories.value.push(newStdCat.value.trim()); 
        newStdCat.value = ''; 
      }
    };

    const addCustomCategory = () => {
      if (newCustomCat.value.trim() !== '') { 
        customCategories.value.push(newCustomCat.value.trim()); 
        newCustomCat.value = ''; 
      }
    };

    const contracts = ref([
      { id: 1, title: 'Statuts SARL OHADA', category: 'Création d\'entreprise', price: 15000, isPromoActive: false, promoPrice: null, isActive: true },
      { id: 2, title: 'Contrat de Travail CDD', category: 'Ressources Humaines', price: 10000, isPromoActive: true, promoPrice: 7500, isActive: true },
      { id: 3, title: 'Contrat de Bail Commercial', category: 'Immobilier', price: 15000, isPromoActive: false, promoPrice: null, isActive: false },
    ]);

    const deleteContract = (id: number) => {
      if(confirm('Êtes-vous sûr de vouloir supprimer ce contrat ?')) {
        contracts.value = contracts.value.filter(c => c.id !== id);
      }
    };

    const toggleStatus = (contract: any) => {
      console.log(`Contrat ${contract.id} est maintenant ${contract.isActive ? 'En ligne' : 'Hors ligne'}`);
    };

    const isModalOpen = ref(false);
    const selectedContract = ref<any>(null);

    const openModal = (contract: any = null) => {
      selectedContract.value = contract;
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
      selectedContract.value = null;
    };

    const handleSaveContract = (data: any) => {
      if (data.id) {
        const index = contracts.value.findIndex(c => c.id === data.id);
        if (index !== -1) {
          contracts.value[index] = { 
            ...contracts.value[index], 
            title: data.title,
            category: data.category,
            price: Number(data.price),
            isPromoActive: data.isPromoActive,
            promoPrice: data.promoPrice ? Number(data.promoPrice) : null
          };
        }
      } else {
        contracts.value.unshift({
          id: Date.now(),
          title: data.title,
          category: data.category,
          price: Number(data.price),
          isPromoActive: data.isPromoActive,
          promoPrice: data.promoPrice ? Number(data.promoPrice) : null,
          isActive: true
        });
      }
      closeModal();
    };

    return {
      activeTab, contracts, deleteContract, toggleStatus,
      newStdCat, newCustomCat, standardCategories, customCategories, addStdCategory, addCustomCategory,
      isModalOpen, selectedContract, openModal, closeModal, handleSaveContract,
      // CORRECTION : Toujours retourner les icônes utilisées dans ce template
      PlusIcon, TrashIcon, PencilSquareIcon
    };
  }
}
</script>

<style scoped>
.contracts-wrapper {
  --bg-panel: #161618;
  --bg-panel-light: #1e1e20;
  --border-color: #2a2a2c;
  --text-main: #ffffff;
  --text-muted: #8a8a8e;
  --accent-blue: #0A84FF;
  --accent-green: #30D158;
  --accent-red: #FF453A;
  display: flex; flex-direction: column; gap: 1.5rem; font-family: 'Inter', sans-serif;
}

.header-section { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; }
.page-title { color: var(--text-main); font-size: 1.2rem; font-weight: 600; margin: 0; }
.tabs-group { display: flex; background: var(--bg-panel); border-radius: 50px; padding: 0.3rem; border: 1px solid var(--border-color); }
.tab-btn { background: transparent; border: none; color: var(--text-muted); font-size: 0.85rem; font-weight: 500; padding: 0.5rem 1.2rem; border-radius: 50px; cursor: pointer; transition: 0.2s; }
.tab-btn.active { background: var(--bg-panel-light); color: var(--text-main); border: 1px solid var(--border-color); }

.panel { background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 20px; padding: 1.5rem; overflow-x: auto; }
.panel-header-simple { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.text-gray { color: var(--text-muted); font-size: 0.9rem; font-weight: 500; }
.text-white { color: var(--text-main); }
.text-blue { color: var(--accent-blue); }
.text-green { color: var(--accent-green); }
.text-red { color: var(--accent-red); }
.text-offline { color: #555; text-decoration: line-through; }
.text-strikethrough { color: #8a8a8e; text-decoration: line-through; margin-right: 0.5rem; }
.opacity-50 { opacity: 0.5; filter: grayscale(100%); }

.btn-primary { display: flex; align-items: center; gap: 0.5rem; background: var(--text-main); color: #000; border: none; padding: 0.5rem 1rem; border-radius: 50px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { opacity: 0.8; }
.icon-sm { width: 18px; height: 18px; }

.clean-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 600px; }
.clean-table th { color: var(--text-muted); font-size: 0.8rem; font-weight: 500; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }
.clean-table td { padding: 1rem 0; font-size: 0.9rem; border-bottom: 1px solid rgba(255,255,255,0.02); vertical-align: middle; }
.flex-align { display: flex; align-items: center; gap: 1rem; }
.flex-align-right { display: flex; justify-content: flex-end; align-items: center; gap: 0.5rem; }
.doc-icon { background: var(--bg-panel-light); padding: 0.5rem; border-radius: 10px; font-size: 1.2rem; }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.text-center { text-align: center; }

.switch { position: relative; display: inline-block; width: 44px; height: 24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: var(--border-color); transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px; background-color: var(--text-muted); transition: .4s; border-radius: 50%; }
input:checked + .slider { background-color: var(--accent-green); }
input:checked + .slider:before { transform: translateX(20px); background-color: #fff; }

.action-btn { background: var(--bg-panel-light); border: 1px solid var(--border-color); cursor: pointer; padding: 0.4rem; border-radius: 8px; transition: 0.2s; display: inline-flex; align-items: center; justify-content: center; }
.delete-btn:hover { background: rgba(255, 69, 58, 0.1); border-color: rgba(255, 69, 58, 0.3); }
.edit-btn:hover { background: rgba(255, 255, 255, 0.1); }

.categories-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 768px) { .categories-grid { grid-template-columns: 1fr 1fr; } }
.add-input-group { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }
.add-input-group input { flex: 1; background: var(--bg-panel-light); border: 1px solid var(--border-color); color: var(--text-main); padding: 0.6rem 1rem; border-radius: 10px; font-size: 0.9rem; outline: none; }
.add-input-group input::placeholder { color: var(--text-muted); }
.btn-add { background: var(--accent-blue); border: none; color: #fff; border-radius: 10px; padding: 0 1rem; cursor: pointer; display: flex; align-items: center; transition: 0.2s; }
.btn-add:hover { filter: brightness(1.1); }
.cat-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.5rem; }
.cat-list li { display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); padding: 0.8rem 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.03); }
</style>