<template>
  <div class="contracts-wrapper">
    
    <!-- EN-TÊTE & ONGLET DE NAVIGATION -->
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

    <!-- =========================================
         ONGLET 1 : GESTION DES CONTRATS
         ========================================= -->
    <div v-if="activeTab === 'contracts'" class="panel">
      <div class="panel-header-simple">
        <span class="text-gray">Liste des contrats en ligne</span>
        <button class="btn-primary" @click="openAddContract">
          <component :is="PlusIcon" class="icon-sm" /> Mettre en ligne
        </button>
      </div>

      <table class="clean-table">
        <thead>
          <tr>
            <th>Document</th>
            <th>Catégorie</th>
            <th>Prix</th>
            <th class="text-center">Statut (En ligne)</th>
            <th class="text-right">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contract in contracts" :key="contract.id">
            <td class="font-bold text-white flex-align">
              <span class="doc-icon" :class="{ 'opacity-50': !contract.isActive }">📄</span> 
              <span :class="{ 'text-muted': !contract.isActive }">{{ contract.title }}</span>
            </td>
            <td class="text-gray">{{ contract.category }}</td>
            <td class="font-bold text-white">{{ contract.price }} F</td>
            
            <!-- BOUTON SWITCH (ACTIVER / DÉSACTIVER) -->
            <td class="text-center">
              <label class="switch">
                <input type="checkbox" v-model="contract.isActive">
                <span class="slider round"></span>
              </label>
            </td>
            
            <!-- ACTION (SUPPRIMER) -->
            <td class="text-right">
              <button class="action-btn delete-btn" @click="deleteContract(contract.id)" title="Supprimer définitivement">
                <component :is="TrashIcon" class="icon-sm text-red" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- =========================================
         ONGLET 2 : GESTION DES CATÉGORIES
         ========================================= -->
    <div v-if="activeTab === 'categories'" class="categories-grid">
      
      <!-- COLONNE 1 : Catégories Catalogue Standard -->
      <div class="panel">
        <div class="panel-header-simple">
          <span class="text-gray">Catégories du Catalogue (Modèles)</span>
        </div>
        <div class="add-input-group">
          <input type="text" v-model="newStdCat" placeholder="Nouvelle catégorie catalogue..." @keyup.enter="addStdCategory" />
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

      <!-- COLONNE 2 : Catégories Sur-Mesure -->
      <div class="panel">
        <div class="panel-header-simple">
          <span class="text-gray">Catégories Sur-Mesure (Devis)</span>
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

  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { PlusIcon, TrashIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'AdminContracts',
  setup() {
    const activeTab = ref('contracts'); // 'contracts' ou 'categories'

    // --- DONNÉES : CONTRATS ---
    const contracts = ref([
      { id: 1, title: 'Statuts SARL OHADA', category: 'Création d\'entreprise', price: '15 000', isActive: true },
      { id: 2, title: 'Contrat de Travail CDD', category: 'Ressources Humaines', price: '10 000', isActive: true },
      { id: 3, title: 'Contrat de Bail Commercial', category: 'Immobilier', price: '15 000', isActive: false }, // Désactivé par défaut
    ]);

    const deleteContract = (id: number) => {
      contracts.value = contracts.value.filter(c => c.id !== id);
    };

    const openAddContract = () => console.log("Ouverture de la fenêtre d'upload de document");

    // --- DONNÉES : CATÉGORIES ---
    const newStdCat = ref('');
    const newCustomCat = ref('');
    
    const standardCategories = ref(['Création d\'entreprise', 'Ressources Humaines', 'Immobilier', 'Packs']);
    const customCategories = ref(['Fusion & Acquisition', 'Audit Juridique', 'Litige Commercial']);

    const addStdCategory = () => {
      if (newStdCat.value.trim() !== '') { standardCategories.value.push(newStdCat.value.trim()); newStdCat.value = ''; }
    };

    const addCustomCategory = () => {
      if (newCustomCat.value.trim() !== '') { customCategories.value.push(newCustomCat.value.trim()); newCustomCat.value = ''; }
    };

    return {
      activeTab, contracts, deleteContract, openAddContract,
      newStdCat, newCustomCat, standardCategories, customCategories, addStdCategory, addCustomCategory,
      PlusIcon, TrashIcon
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

/* EN-TÊTE & ONGLET */
.header-section { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; }
.page-title { color: var(--text-main); font-size: 1.2rem; font-weight: 600; margin: 0; }
.tabs-group { display: flex; background: var(--bg-panel); border-radius: 50px; padding: 0.3rem; border: 1px solid var(--border-color); }
.tab-btn { background: transparent; border: none; color: var(--text-muted); font-size: 0.85rem; font-weight: 500; padding: 0.5rem 1.2rem; border-radius: 50px; cursor: pointer; transition: 0.2s; }
.tab-btn.active { background: var(--bg-panel-light); color: var(--text-main); border: 1px solid var(--border-color); }

/* PANNEAUX */
.panel { background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 20px; padding: 1.5rem; overflow-x: auto; }
.panel-header-simple { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.text-gray { color: var(--text-muted); font-size: 0.9rem; font-weight: 500; }
.text-white { color: var(--text-main); }
.text-muted { color: #555; text-decoration: line-through; }
.opacity-50 { opacity: 0.5; filter: grayscale(100%); }

.btn-primary { display: flex; align-items: center; gap: 0.5rem; background: var(--text-main); color: #000; border: none; padding: 0.5rem 1rem; border-radius: 50px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { opacity: 0.8; }
.icon-sm { width: 18px; height: 18px; }

/* TABLEAU (ONGLET 1) */
.clean-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 600px; }
.clean-table th { color: var(--text-muted); font-size: 0.8rem; font-weight: 500; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }
.clean-table td { padding: 1rem 0; font-size: 0.9rem; border-bottom: 1px solid rgba(255,255,255,0.02); vertical-align: middle; }
.flex-align { display: flex; align-items: center; gap: 1rem; }
.doc-icon { background: var(--bg-panel-light); padding: 0.5rem; border-radius: 10px; font-size: 1.2rem; }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.text-center { text-align: center; }

/* BOUTON SWITCH (APPLE STYLE) */
.switch { position: relative; display: inline-block; width: 44px; height: 24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: var(--border-color); transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px; background-color: var(--text-muted); transition: .4s; border-radius: 50%; }
input:checked + .slider { background-color: var(--accent-green); }
input:checked + .slider:before { transform: translateX(20px); background-color: #fff; }

/* BOUTONS ACTIONS */
.action-btn { background: transparent; border: none; cursor: pointer; padding: 0.4rem; border-radius: 6px; transition: 0.2s; display: inline-flex; align-items: center; }
.delete-btn:hover { background: rgba(255, 69, 58, 0.1); }
.text-red { color: var(--accent-red); }

/* GRILLE CATÉGORIES (ONGLET 2) */
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