<template>
  <div class="history-wrapper">
    
    <!-- EN-TÊTE : RECHERCHE ET ONGLETS -->
    <div class="header-section">
      <div class="title-and-search">
        <h3 class="section-title">Historique des Transactions</h3>
        
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-gray" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher un nom, un email..." />
        </div>
      </div>

      <div class="tabs-group">
        <button class="tab-btn" :class="{ active: activeTab === 'models' }" @click="activeTab = 'models'">
          Contrats vendu
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'packs' }" @click="activeTab = 'packs'">
          Packs de contrats
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'custom' }" @click="activeTab = 'custom'">
          Sur-Mesure
        </button>
      </div>
    </div>

    <!-- TABLEAU DE L'HISTORIQUE (Style MoonInc) -->
    <div class="panel clean-list-container">
      <table class="minimal-table">
        <thead>
          <tr>
            <th>Produit Acheté</th>
            <th>Statut</th>
            <th>Client & Contact</th>
            <th>Date & Heure</th>
            <th class="text-right">Montant</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredHistory" :key="item.id">
            
            <!-- Colonne Produit (Avec la petite icône pastel) -->
            <td>
              <div class="action-cell">
                <span class="dark-text font-bold">{{ item.product }}</span>
              </div>
            </td>
            
            <!-- Colonne Statut -->
            <td>
              <span class="status-dot dot-green"></span> 
              <span class="gray-text">Payé</span>
            </td>

            <!-- Colonne Client -->
            <td>
              <div class="client-info">
                <span class="dark-text font-bold">{{ item.clientName }}</span>
                <span class="gray-text text-sm">{{ item.clientEmail }}</span>
              </div>
            </td>
            
            <!-- Colonne Date -->
            <td>
              <div class="client-info">
                <span class="gray-text">{{ item.date }}</span>
                <span class="gray-text text-sm">{{ item.time }}</span>
              </div>
            </td>
            
            <!-- Colonne Montant -->
            <td class="text-right dark-text font-bold">
              {{ item.amount }} FCFA
            </td>
            
          </tr>
        </tbody>
      </table>

      <!-- ÉTAT VIDE -->
      <div v-if="filteredHistory.length === 0" class="empty-state">
        <p class="gray-text">Aucune transaction trouvée pour cette recherche.</p>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import { 
  MagnifyingGlassIcon, 
  DocumentTextIcon, 
  ArchiveBoxIcon, 
  ScaleIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminHistory',
  setup() {
    const activeTab = ref('models'); // 'models', 'packs', 'custom'
    const searchQuery = ref('');

    // --- FAUSSES BASES DE DONNÉES ---
    const historyModels = ref([
      { id: 1, date: '12 Juin 2026', time: '14:30', clientName: 'Koffi Armand', clientEmail: 'koffi.a@gmail.com', clientPhone: '+225 07070707', product: 'Statuts SARL OHADA', amount: '15 000' },
      { id: 2, date: '12 Juin 2026', time: '09:15', clientName: 'Sylla Awa', clientEmail: 'awa.sylla@yahoo.fr', clientPhone: '+225 05050505', product: 'Contrat de Prestation', amount: '10 000' },
    ]);

    const historyPacks = ref([
      { id: 101, date: '11 Juin 2026', time: '16:45', clientName: 'Entreprise TechCI', clientEmail: 'contact@techci.com', clientPhone: '+225 01010101', product: 'Pack Création Entreprise', amount: '45 000' },
      { id: 102, date: '09 Juin 2026', time: '10:00', clientName: 'Bamba Lamine', clientEmail: 'bamba.l@outlook.com', clientPhone: '+225 09090909', product: 'Pack Freelance', amount: '20 000' },
    ]);

    const historyCustom = ref([
      { id: 201, date: '10 Juin 2026', time: '11:20', clientName: 'Groupe EBOMAF', clientEmail: 'legal@ebomaf.com', clientPhone: '+226 70707070', product: 'Contrat de Fusion (Devis)', amount: '150 000' },
      { id: 202, date: '05 Juin 2026', time: '15:30', clientName: 'Startup Z', clientEmail: 'hello@startupz.ci', clientPhone: '+225 03030303', product: 'Audit Juridique Complet', amount: '300 000' },
    ]);

    // --- LOGIQUE DE FILTRAGE ---
    const filteredHistory = computed(() => {
      let currentList = [];
      if (activeTab.value === 'models') currentList = historyModels.value;
      else if (activeTab.value === 'packs') currentList = historyPacks.value;
      else if (activeTab.value === 'custom') currentList = historyCustom.value;

      if (!searchQuery.value) return currentList;
      
      const query = searchQuery.value.toLowerCase();
      return currentList.filter(item => 
        item.clientName.toLowerCase().includes(query) ||
        item.clientEmail.toLowerCase().includes(query) ||
        item.product.toLowerCase().includes(query)
      );
    });

    // --- DESIGN DYNAMIQUE (Icônes et Couleurs selon l'onglet) ---
    const getIconColor = (tab: string) => {
      if (tab === 'models') return 'bg-blue-light';
      if (tab === 'packs') return 'bg-purple-light';
      return 'bg-orange-light';
    };

    const getIcon = (tab: string) => {
      if (tab === 'models') return DocumentTextIcon;
      if (tab === 'packs') return ArchiveBoxIcon;
      return ScaleIcon;
    };

    return {
      activeTab, searchQuery, filteredHistory,
      MagnifyingGlassIcon, getIconColor, getIcon
    };
  }
}
</script>

<style scoped>
/* ==============================================================
   CHARTE GRAPHIQUE (MoonInc / ContratChap)
   ============================================================== */
.history-wrapper {
  --bg-main: #f8fafc;        
  --bg-panel: #ffffff;       
  --bg-panel-light: #f1f5f9; 
  --text-dark: #1e293b;      
  --text-gray: #94a3b8;      
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2rem; 
  font-family: 'Inter', sans-serif;
}

/* --- EN-TÊTE --- */
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-and-search { display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.2rem; color: var(--text-dark); font-weight: 700; margin: 0; }

.search-box {
  display: flex; align-items: center; gap: 0.8rem; background: var(--bg-panel);
  border: 1px solid #e2e8f0; border-radius: 50px; padding: 0.6rem 1.2rem; 
  flex: 1; max-width: 400px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}
.search-box input { background: transparent; border: none; color: var(--text-dark); font-size: 0.9rem; outline: none; width: 100%; font-weight: 500; }
.search-box input::placeholder { color: #cbd5e1; font-weight: 400; }
.icon-gray { width: 18px; height: 18px; color: var(--text-gray); }

/* --- ONGLETS (Pillules claires) --- */
.tabs-group { display: flex; background: var(--primary-color); border-radius: 50px; padding: 0.3rem; width: fit-content; }
.tab-btn { 
  background: transparent; border: none; color: #ffffff; 
  font-size: 0.85rem; font-weight: 600; padding: 0.6rem 1.2rem; 
  border-radius: 50px; cursor: pointer; transition: all 0.2s ease; 
}
.tab-btn.active { 
  background: var(--secondary-light-color); color: #ffffff; 
  box-shadow: 0px 2px 10px rgba(0,0,0,0.05); 
}

/* --- PANNEAU & TABLEAU ÉPURÉ --- */
.clean-list-container {
  background: var(--bg-panel); border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9;
  overflow-x: auto;
}
.minimal-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 800px; }
.minimal-table th { color: #cbd5e1; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding-bottom: 1.5rem; }
.minimal-table td { padding: 1.2rem 0; border-bottom: 1px solid #f8fafc; vertical-align: middle; }
.minimal-table tr:last-child td { border-bottom: none; }

/* --- ÉLÉMENTS DE LA TABLE --- */
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); font-size: 0.9rem; }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.text-sm { font-size: 0.75rem; display: block; margin-top: 0.2rem; }

/* Cellules Spéciales */
.action-cell { display: flex; align-items: center; gap: 1rem; }
.client-info { display: flex; flex-direction: column; }

/* Icônes Pastel (Couleurs dynamiques selon l'onglet) */
.icon-box-light { width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.icon-box-light svg { width: 20px; height: 20px; }
.bg-blue-light { background: #eff6ff; color: #3b82f6; }
.bg-purple-light { background: #faf5ff; color: #a855f7; }
.bg-orange-light { background: #fff7ed; color: #f97316; }

/* Statut Point */
.status-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 0.5rem; vertical-align: middle; }
.dot-green { background-color: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }

.empty-state { text-align: center; padding: 3rem 0; }
</style>