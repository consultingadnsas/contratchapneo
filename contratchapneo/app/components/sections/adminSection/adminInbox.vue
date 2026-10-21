<template>
  <div class="inbox-wrapper">
    
    <!-- EN-TÊTE : RECHERCHE ET ONGLETS -->
    <div class="header-section">
      <div class="title-and-search">
        <h3 class="section-title">Boîte de réception</h3>
        
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-gray" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher un client, un email..." />
        </div>
      </div>
      <div class="filter_group">
        <!-- 🖥️ ONGLETS BOUTONS : Desktop uniquement (> 1024px) -->
        <div class="tabs-group desktop-only">
          <button class="tab-btn" :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'">
            Toutes
          </button>
          <button class="tab-btn" :class="{ active: activeTab === 'review' }" @click="activeTab = 'review'">
            Révisions
          </button>
          <button class="tab-btn" :class="{ active: activeTab === 'custom' }" @click="activeTab = 'custom'">
            Sur-Mesure
          </button>
        </div>

        <!-- 📱 MENU DÉROULANT DES DEMANDES : Mobile et Tablette (<= 1024px) -->
        <div class="tabs-dropdown-wrapper mobile-tablet-only">
          <label for="request-type-select" class="dropdown-label">Type de demandes :</label>
          <div class="select-box">
            <select id="request-type-select" v-model="activeTab" class="custom-select" aria-label="Type de demandes">
              <option value="all">Toutes</option>
              <option value="review">Révisions</option>
              <option value="custom">Sur-Mesure</option>
            </select>
            <svg class="select-arrow" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
            </svg>
          </div>
        </div>

        <!-- 💳 STATUT DU PAIEMENT : Placé à droite sur desktop, et en dessous sur mobile/tablette -->
        <div class="payment-filter-wrapper">
          <label for="payment-status-select" class="dropdown-label mobile-tablet-only">Statut du paiement :</label>
          <div class="select-box">
            <select id="payment-status-select" v-model="paymentFilter" class="custom-select payment-filter-select" aria-label="Statut du paiement">
              <option value="all">Tous les paiements</option>
              <option value="paid">Payé</option>
              <option value="unpaid">Non payé</option>
            </select>
            <svg class="select-arrow" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
            </svg>
          </div>
        </div>
      </div>
      
    </div>

    <!-- SPINNER -->
    <div v-if="adminStore.isLoading" class="empty-state">
      <p class="gray-text">Chargement des demandes...</p>
    </div>

    <!-- TABLEAU DES MESSAGES -->
    <div v-else class="panel clean-list-container">
      <div class="table-scroll-container">
        <table class="minimal-table">
        <thead>
          <tr>
            <th>Date & Heure</th>
            <th>Client</th>
            <th>Type de demande</th>
            <th>Paiement</th>
            <th>Statut</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- ⚡️ MODIFICATION : On boucle sur 'paginatedMessages' au lieu de 'filteredMessages' -->
          <tr v-for="msg in paginatedMessages" :key="msg.id" :class="{ 'unread-row': !msg.isRead }">
            
            <!-- Date -->
            <td>
              <div class="info-stack">
                <span :class="!msg.isRead ? 'dark-text font-bold' : 'gray-text'">{{ msg.formattedDate }}</span>
                <span class="gray-text text-sm">{{ msg.formattedTime }}</span>
              </div>
            </td>
            
            <!-- Client -->
            <td>
              <div class="info-stack">
                <span class="dark-text font-bold">{{ msg.clientName || 'Client' }}</span>
                <span class="gray-text text-sm">{{ msg.email }}</span>
              </div>
            </td>
            
            <!-- Type (Badges Pastel) & Sujet -->
            <td>
                <div>
                  <span class="pastel-badge" :class="msg.type === 'review' ? 'badge-blue' : 'badge-purple'">
                    {{ msg.type === 'review' ? 'Révision' : 'Sur-Mesure' }}
                  </span>
                </div>

               <span v-if="msg.type === 'custom'" class="dark-text text-sm font-bold" style="margin-top: 0.4rem;">
                  {{ msg.categoryName }}
                </span>
            </td>
            
            <!-- Paiement -->
            <td>
              <span class="status-dot" :class="msg.is_paid ? 'dot-green' : 'dot-red'"></span>
              <span class="dark-text font-bold">{{ msg.is_paid ? 'Payé' : 'Non payé' }}</span>
            </td>

            <!-- Statut -->
            <td>
              <span class="status-dot" :class="getStatusDot(msg.status)"></span>
              <span class="dark-text font-bold">{{ msg.status_display || msg.status }}</span>
            </td>
            
            <!-- Action -->
            <td class="text-right">
              <button class="pill-btn" @click="openMessage(msg)">
                <component :is="EyeIcon" class="icon-sm mr-1" />
                Ouvrir
              </button>
            </td>
            
          </tr>
        </tbody>
      </table>
      </div>

      <!-- ÉTAT VIDE -->
      <div v-if="filteredMessages.length === 0" class="empty-state">
        <p class="gray-text">Aucun message trouvé dans cette catégorie.</p>
      </div>
      
      <!-- ⚡️ NOUVEAU : LE PAGINATOR -->
      <!-- Il ne s'affiche que s'il y a plus de messages que la taille d'une page -->
      <Paginator 
        v-if="filteredMessages.length > pageSize"
        :currentPage="currentPage"
        :totalCount="filteredMessages.length"
        :pageSize="pageSize"
        @page-change="handlePageChange"
      />
    </div>

    <!-- MODALE IMPORTÉE -->
    <adminInboxModal 
      v-if="selectedMessage" 
      :message="selectedMessage" 
      @close="closeMessage" 
      @mark-processed="markAsProcessed"
    />

  </div>
</template>

<script lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import adminInboxModal from '../../modale/adminInboxModale.vue';
import Paginator from '../../tools/Paginator.vue'; // ⚡️ NOUVEAU : Import du paginator[cite: 13]
import { useAdminRequestsStore } from '../../../stores/adminRequestStore';
import { 
  MagnifyingGlassIcon, 
  EyeIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminInbox',
  components: {
    adminInboxModal,
    Paginator // ⚡️ NOUVEAU : Déclaration du composant[cite: 13]
  },
  setup() {
    const adminStore = useAdminRequestsStore();
    const activeTab = ref('all');
    const searchQuery = ref('');
    const paymentFilter = ref('all'); // ⚡️ NOUVEAU : Filtre de paiement
    const selectedMessage = ref<any>(null);

    // ⚡️ NOUVEAU : Variables d'état pour la pagination
    const currentPage = ref(1);
    const pageSize = ref(10); // Tu peux ajuster ce nombre de lignes par page

    // Déclenchement de la requête API au chargement
    onMounted(async () => {
      await adminStore.fetchRevisions();
      await adminStore.fetchCustomRequests();
    });

    const formatDate = (dateString: string) => {
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
    };

    const formatTime = (dateString: string) => {
      const date = new Date(dateString);
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    };

    const allMessages = computed(() => {
      const revisions = adminStore.revisions.map(rev => ({
        ...rev,
        type: 'review',
        // ⚡️ CORRECTION : On utilise d'abord le vrai nom, sinon on coupe l'email (pour les visiteurs non connectés)
        clientName: rev.client_name || rev.email.split('@')[0], 
        formattedDate: formatDate(rev.created_at),
        formattedTime: formatTime(rev.created_at),
        isRead: rev.status !== 'PENDING',
        categoryName: undefined
      }));

      const customRequests = adminStore.customRequests.map(req => ({
        ...req,
        type: 'custom',
        // ⚡️ CORRECTION : Même logique ici
        clientName: req.client_name || req.email.split('@')[0], 
        categoryName: req.category_name,
        status: req.is_wrotten ? 'Terminé' : 'En attente', 
        status_display: req.is_wrotten ? 'Terminé' : 'En attente',
        formattedDate: formatDate(req.created_at),
        formattedTime: formatTime(req.created_at),
        isRead: req.is_wrotten 
      }));

      return [...revisions, ...customRequests].sort((a, b) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    });

    const filteredMessages = computed(() => {
      let list = allMessages.value;
      
      if (activeTab.value !== 'all') {
        list = list.filter(msg => msg.type === activeTab.value);
      }
      
      if (paymentFilter.value === 'paid') {
        list = list.filter(msg => msg.is_paid);
      } else if (paymentFilter.value === 'unpaid') {
        list = list.filter(msg => !msg.is_paid);
      }

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        list = list.filter(msg => 
          (msg.clientName && msg.clientName.toLowerCase().includes(query)) ||
          (msg.email && msg.email.toLowerCase().includes(query))
        );
      }
      return list;
    });

    // ⚡️ NOUVEAU : Découpage de la liste filtrée pour la page actuelle
    const paginatedMessages = computed(() => {
      const startIndex = (currentPage.value - 1) * pageSize.value;
      const endIndex = startIndex + pageSize.value;
      return filteredMessages.value.slice(startIndex, endIndex);
    });

    // ⚡️ NOUVEAU : Réinitialiser la page à 1 quand on change d'onglet, filtre ou qu'on cherche
    watch([activeTab, searchQuery, paymentFilter], () => {
      currentPage.value = 1;
    });

    // ⚡️ NOUVEAU : Fonction déclenchée par l'événement du paginator[cite: 13]
    const handlePageChange = (page: number) => {
      currentPage.value = page;
    };

    const getStatusDot = (status: string) => {
      const s = status ? status.toLowerCase() : '';
      if (s.includes('attente') || s === 'pending') return 'dot-green'; 
      if (s.includes('cours') || s === 'in_progress') return 'dot-yellow';
      return 'dot-gray';
    };

    const openMessage = async (msg: any) => {
      msg.isRead = true;
      selectedMessage.value = msg;

      if (msg.type === 'review' && msg.status === 'PENDING') {
        const formData = new FormData();
        formData.append('status', 'IN_PROGRESS');
        
        try {
          await adminStore.updateRevision(msg.id, formData);
        } catch (error) {
          console.error("Erreur lors de la mise à jour du statut :", error);
        }
      }
    };

    const closeMessage = () => {
      selectedMessage.value = null;
    };

    const markAsProcessed = async (msg: any) => {
      if (msg.type === 'review') {
        const formData = new FormData();
        formData.append('status', 'COMPLETED');
        await adminStore.updateRevision(msg.id, formData);
      } 
      else if (msg.type === 'custom') {
        const formData = new FormData();
        formData.append('is_wrotten', 'true');
        await adminStore.completeCustomRequest(msg.id, formData);
      }
      
      closeMessage();
    };

    return {
      adminStore,
      activeTab, 
      searchQuery,
      paymentFilter,
      filteredMessages, 
      paginatedMessages, // Exposé au template
      currentPage,       // Exposé au template
      pageSize,          // Exposé au template
      handlePageChange,  // Exposé au template
      selectedMessage,
      getStatusDot, 
      openMessage, 
      closeMessage, 
      markAsProcessed,
      MagnifyingGlassIcon, 
      EyeIcon
    };
  }
}
</script>

<style scoped>
.inbox-wrapper {
  --bg-main: #f8fafc;
  --bg-panel: #ffffff;
  --bg-panel-light: #f1f5f9;
  --text-dark: #1e293b;
  --text-gray: #94a3b8;
  --accent-blue: #2563eb;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  font-family: 'Inter', sans-serif;
  width: 100%;
  box-sizing: border-box;
}

.header-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

.title-and-search {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  width: 100%;
}

.section-title {
  font-size: 1.35rem;
  color: var(--text-dark);
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.3px;
}

/* BARRE DE RECHERCHE */
.search-box {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: var(--bg-panel);
  border: 1px solid #e2e8f0;
  border-radius: 50px;
  padding: 0.65rem 1.25rem;
  flex: 1;
  max-width: 400px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.02);
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.search-box:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.search-box input {
  background: transparent;
  border: none;
  color: var(--text-dark);
  font-size: 0.95rem;
  outline: none;
  width: 100%;
  font-weight: 500;
}

.search-box input::placeholder {
  color: #cbd5e1;
  font-weight: 400;
}

.icon-gray {
  width: 18px;
  height: 18px;
  color: var(--text-gray);
  flex-shrink: 0;
}

/* GROUPE DE FILTRES */
.filter_group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
}

/* 🖥️ ONGLETS BOUTONS (DESKTOP) */
.tabs-group {
  display: flex;
  background: var(--primary-color, #2563eb);
  border-radius: 50px;
  padding: 0.3rem;
  width: fit-content;
  gap: 0.2rem;
}

.tab-btn {
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tab-btn.active {
  background: var(--secondary-light-color, #1d4ed8);
  color: #ffffff;
  box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

/* 📱 MENUS DÉROULANTS (SÉLECTEURS) */
.tabs-dropdown-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  width: 100%;
}

.payment-filter-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  width: auto;
  min-width: 200px;
}

.dropdown-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-gray);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.select-box {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.custom-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1.25rem;
  border: 1px solid #cbd5e1;
  border-radius: 50px;
  background-color: var(--bg-panel);
  color: var(--text-dark);
  font-size: 0.95rem;
  font-weight: 500;
  outline: none;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.custom-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.select-arrow {
  position: absolute;
  right: 1.1rem;
  width: 18px;
  height: 18px;
  color: var(--text-gray);
  pointer-events: none;
  transition: transform 0.2s ease;
}

.select-box:focus-within .select-arrow {
  color: #3b82f6;
  transform: rotate(180deg);
}

/* TABLEAU ET CONTENEUR RESPONSIVE */
.clean-list-container {
  background: var(--bg-panel);
  border-radius: 24px;
  padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03);
  border: 1px solid #f1f5f9;
  width: 100%;
  box-sizing: border-box;
}

.table-scroll-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  width: 100%;
  box-sizing: border-box;
}

.table-scroll-container::-webkit-scrollbar {
  height: 6px;
}
.table-scroll-container::-webkit-scrollbar-track {
  background: #f8fafc;
  border-radius: 10px;
}
.table-scroll-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.table-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.minimal-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  min-width: 860px;
}

.minimal-table th {
  color: #94a3b8;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 1rem 0.85rem;
  border-bottom: 1px solid #f1f5f9;
  background: #f8fafc;
  white-space: nowrap;
}

.minimal-table td {
  padding: 1.1rem 0.85rem;
  border-bottom: 1px solid #f8fafc;
  vertical-align: middle;
  transition: 0.2s;
  white-space: nowrap;
}

.minimal-table tr:last-child td {
  border-bottom: none;
}

.unread-row td {
  background-color: #f8fafc;
}

.dark-text {
  color: var(--text-dark);
}

.gray-text {
  color: var(--text-gray);
  font-size: 0.9rem;
}

.font-bold {
  font-weight: 600;
}

.text-right {
  text-align: right;
}

.text-sm {
  font-size: 0.75rem;
  display: block;
  margin-top: 0.2rem;
}

.mr-1 {
  margin-right: 0.2rem;
}

.info-stack {
  display: flex;
  flex-direction: column;
}

.pastel-badge {
  padding: 0.4rem 1rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
}

.badge-blue {
  background: #eff6ff;
  color: #3b82f6;
}

.badge-purple {
  background: #faf5ff;
  color: #a855f7;
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 0.5rem;
  vertical-align: middle;
}

.dot-green {
  background-color: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.dot-yellow {
  background-color: #f59e0b;
}

.dot-gray {
  background-color: #cbd5e1;
}

.dot-red {
  background-color: #ef4444;
}

.pill-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #e2e8f0;
  color: var(--text-dark);
  padding: 0.5rem 1.2rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
  transition: 0.2s;
}

.pill-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.icon-sm {
  width: 16px;
  height: 16px;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
}

/* ========================================================
   VISIBILITÉ PAR DÉFAUT (DESKTOP > 1024px)
   ======================================================== */
.desktop-only {
  display: flex !important;
}

.mobile-tablet-only {
  display: none !important;
}

/* ========================================================
   RESPONSIVE : TÉLÉPHONES & TABLETTES (<= 1024px)
   ======================================================== */
@media (max-width: 1024px) {
  .header-section {
    gap: 1rem;
  }

  /* La barre de recherche se place sous le titre, tout en haut des contrôles */
  .title-and-search {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  /* Barre de recherche pleine largeur */
  .search-box {
    max-width: 100%;
    width: 100%;
  }

  /* Masquer les boutons onglets desktop */
  .desktop-only {
    display: none !important;
  }

  /* Afficher les menus déroulants mobile/tablette empilés :
     1. Type de demandes tout en haut
     2. Statut du paiement en dessous */
  .mobile-tablet-only {
    display: flex !important;
  }

  .filter_group {
    flex-direction: column;
    align-items: stretch;
    gap: 0.85rem;
    width: 100%;
  }

  .payment-filter-wrapper {
    max-width: 100%;
    width: 100%;
  }

  .clean-list-container {
    padding: 1.2rem;
    border-radius: 18px;
  }
}

/* ========================================================
   RESPONSIVE : SMARTPHONES (< 640px)
   ======================================================== */
@media (max-width: 640px) {
  .clean-list-container {
    padding: 0.85rem;
    border-radius: 14px;
  }

  .minimal-table th,
  .minimal-table td {
    padding: 0.85rem 0.6rem;
    font-size: 0.85rem;
  }

  .section-title {
    font-size: 1.15rem;
  }
}
</style>