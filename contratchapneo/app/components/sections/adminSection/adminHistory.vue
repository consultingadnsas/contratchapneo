<template>
  <div class="history-wrapper">
    
    <!-- EN-TÊTE : RECHERCHE ET ONGLETS -->
    <div class="header-section">
      <div class="title-and-search">
        <h2 class="page-title">Historique des Transactions</h2>
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-sm text-gray" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher un nom, un email, un document..." />
        </div>
      </div>

      <div class="tabs-group">
        <button class="tab-btn" :class="{ active: activeTab === 'models' }" @click="activeTab = 'models'">
          <component :is="DocumentArrowDownIcon" class="icon-sm" /> Modèles à l'unité
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'packs' }" @click="activeTab = 'packs'">
          <component :is="ArchiveBoxIcon" class="icon-sm" /> Packs Premium
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'custom' }" @click="activeTab = 'custom'">
          <component :is="ScaleIcon" class="icon-sm" /> Sur-Mesure
        </button>
      </div>
    </div>

    <!-- TABLEAU DE L'HISTORIQUE -->
    <div class="panel">
      <table class="clean-table">
        <thead>
          <tr>
            <th>Date & Heure</th>
            <th>Client (Contact)</th>
            <th>Produit Acheté</th>
            <th>Montant</th>
            <th class="text-right">Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredHistory" :key="item.id">
            
            <!-- Colonne Date -->
            <td class="text-gray time-cell">
              <span class="date">{{ item.date }}</span>
              <span class="time">{{ item.time }}</span>
            </td>
            
            <!-- Colonne Client (Infos groupées) -->
            <td>
              <div class="client-info">
                <span class="font-bold text-white">{{ item.clientName }}</span>
                <span class="client-contact">{{ item.clientEmail }} • {{ item.clientPhone }}</span>
              </div>
            </td>
            
            <!-- Colonne Produit -->
            <td class="font-bold text-white">
              {{ item.product }}
            </td>
            
            <!-- Colonne Montant -->
            <td class="font-bold" :class="item.amount > 0 ? 'text-green' : 'text-white'">
              {{ item.amount }} F
            </td>
            
            <!-- Colonne Statut -->
            <td class="text-right flex-align-right text-green font-bold">
              Payé <component :is="CheckCircleIcon" class="icon-sm" />
            </td>
            
          </tr>
        </tbody>
      </table>

      <!-- ÉTAT VIDE -->
      <div v-if="filteredHistory.length === 0" class="empty-state">
        <p class="text-gray">Aucune transaction trouvée pour cette recherche.</p>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import { 
  MagnifyingGlassIcon, 
  DocumentArrowDownIcon, 
  ArchiveBoxIcon, 
  ScaleIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminHistory',
  setup() {
    const activeTab = ref('models'); // 'models', 'packs', 'custom'
    const searchQuery = ref('');

    // --- FAUSSES BASES DE DONNÉES (Séparées par type) ---
    const historyModels = ref([
      { id: 1, date: '12 Juin 2024', time: '14:30', clientName: 'Koffi Armand', clientEmail: 'koffi.a@gmail.com', clientPhone: '+225 07070707', product: 'Statuts SARL OHADA', amount: '15 000' },
      { id: 2, date: '12 Juin 2024', time: '09:15', clientName: 'Sylla Awa', clientEmail: 'awa.sylla@yahoo.fr', clientPhone: '+225 05050505', product: 'Contrat de Prestation', amount: '10 000' },
    ]);

    const historyPacks = ref([
      { id: 101, date: '11 Juin 2024', time: '16:45', clientName: 'Entreprise TechCI', clientEmail: 'contact@techci.com', clientPhone: '+225 01010101', product: 'Pack Création Entreprise', amount: '45 000' },
      { id: 102, date: '09 Juin 2024', time: '10:00', clientName: 'Bamba Lamine', clientEmail: 'bamba.l@outlook.com', clientPhone: '+225 09090909', product: 'Pack Freelance', amount: '20 000' },
    ]);

    const historyCustom = ref([
      { id: 201, date: '10 Juin 2024', time: '11:20', clientName: 'Groupe EBOMAF', clientEmail: 'legal@ebomaf.com', clientPhone: '+226 70707070', product: 'Contrat de Fusion (Devis)', amount: '150 000' },
      { id: 202, date: '05 Juin 2024', time: '15:30', clientName: 'Startup Z', clientEmail: 'hello@startupz.ci', clientPhone: '+225 03030303', product: 'Audit Juridique Complet', amount: '300 000' },
    ]);

    // --- LOGIQUE DE FILTRAGE ---
    const filteredHistory = computed(() => {
      // 1. Sélectionner la bonne liste en fonction de l'onglet actif
      let currentList = [];
      if (activeTab.value === 'models') currentList = historyModels.value;
      else if (activeTab.value === 'packs') currentList = historyPacks.value;
      else if (activeTab.value === 'custom') currentList = historyCustom.value;

      // 2. Appliquer la recherche (sur le nom, l'email, le téléphone ou le produit)
      if (!searchQuery.value) return currentList;
      
      const query = searchQuery.value.toLowerCase();
      return currentList.filter(item => 
        item.clientName.toLowerCase().includes(query) ||
        item.clientEmail.toLowerCase().includes(query) ||
        item.clientPhone.includes(query) ||
        item.product.toLowerCase().includes(query)
      );
    });

    return {
      activeTab, searchQuery, filteredHistory,
      MagnifyingGlassIcon, DocumentArrowDownIcon, ArchiveBoxIcon, ScaleIcon, CheckCircleIcon
    };
  }
}
</script>

<style scoped>
.history-wrapper {
  --bg-panel: #161618;
  --bg-panel-light: #1e1e20;
  --border-color: #2a2a2c;
  --text-main: #ffffff;
  --text-muted: #8a8a8e;
  --accent-blue: #0A84FF;
  --accent-green: #30D158;
  display: flex; flex-direction: column; gap: 1.5rem; font-family: 'Inter', sans-serif;
}

/* --- EN-TÊTE --- */
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-and-search { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.page-title { color: var(--text-main); font-size: 1.2rem; font-weight: 600; margin: 0; }

.search-box {
  display: flex; align-items: center; gap: 0.5rem; background: var(--bg-panel);
  border: 1px solid var(--border-color); border-radius: 50px; padding: 0.6rem 1.2rem; flex: 1; max-width: 400px;
}
.search-box input { background: transparent; border: none; color: var(--text-main); font-size: 0.9rem; outline: none; width: 100%; }
.search-box input::placeholder { color: var(--text-muted); }

/* --- ONGLETS (TABS) --- */
.tabs-group { display: flex; background: var(--bg-panel); border-radius: 50px; padding: 0.3rem; border: 1px solid var(--border-color); width: fit-content; }
.tab-btn { display: flex; align-items: center; gap: 0.5rem; background: transparent; border: none; color: var(--text-muted); font-size: 0.85rem; font-weight: 500; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: 0.2s; }
.tab-btn.active { background: var(--bg-panel-light); color: var(--text-main); border: 1px solid var(--border-color); }
.icon-sm { width: 18px; height: 18px; }

/* --- PANNEAU & TABLEAU --- */
.panel { background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 20px; padding: 1.5rem; overflow-x: auto; }
.clean-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 800px; }
.clean-table th { color: var(--text-muted); font-size: 0.8rem; font-weight: 500; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }
.clean-table td { padding: 1rem 0; font-size: 0.9rem; border-bottom: 1px solid rgba(255,255,255,0.02); vertical-align: middle; }
.clean-table tr:last-child td { border-bottom: none; }
.clean-table tr:hover td { background-color: rgba(255,255,255,0.01); }

/* --- ÉLÉMENTS DE LA TABLE --- */
.text-white { color: var(--text-main); }
.text-gray { color: var(--text-muted); }
.text-green { color: var(--accent-green); }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.flex-align-right { display: flex; justify-content: flex-end; align-items: center; gap: 0.4rem; }

/* Cellule Date */
.time-cell { display: flex; flex-direction: column; gap: 0.2rem; }
.time { font-size: 0.75rem; }

/* Cellule Client */
.client-info { display: flex; flex-direction: column; gap: 0.2rem; }
.client-contact { font-size: 0.75rem; color: var(--text-muted); }

.empty-state { text-align: center; padding: 3rem 0; }
</style>