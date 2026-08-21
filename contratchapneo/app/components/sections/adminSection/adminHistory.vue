<template>
  <div class="history-wrapper">
    
    <!-- EN-TÊTE : RECHERCHE ET ONGLETS -->
    <div class="header-section">
      <div class="title-and-search">
        <h3 class="section-title">Historique des Transactions</h3>
        
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-gray" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher un nom, un email, un produit..." />
        </div>
      </div>

      <div class="tabs-group">
        <button class="tab-btn" :class="{ active: activeTab === 'models' }" @click="activeTab = 'models'">
          Contrats vendus
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'packs' }" @click="activeTab = 'packs'">
          Packs de contrats
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'custom' }" @click="activeTab = 'custom'">
          Sur-Mesure
        </button>
      </div>
    </div>

    <!-- ÉTAT DE CHARGEMENT -->
    <div v-if="transactStore.isLoading" class="loading-state">
      Chargement de l'historique des transactions...
    </div>

    <!-- TABLEAU DE L'HISTORIQUE -->
    <div v-else class="panel clean-list-container">
      <table class="minimal-table">
        <thead>
          <tr>
            <th>Type de produit</th>
            <th>Statut</th>
            <th>Client & Contact</th>
            <th>Date & Heure</th>
            <th class="text-right">Montant</th>
            <th class="text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <!-- ⚡️ UTILISATION DES TRANSACTIONS PAGINÉES DE LA PAGE COURANTE -->
          <tr v-for="item in paginatedHistory" :key="item.id">
            
            <td>
              <div class="action-cell">
                <div class="icon-box-light" :class="getIconColor(activeTab)">
                  <component :is="getIcon(activeTab)" />
                </div>
                <span class="dark-text font-bold">{{ item.productTypeLabel }}</span>
              </div>
            </td>
            
            <!-- ⚡️ BADGE STATUT DYNAMIQUE -->
            <td>
              <span class="status-badge" :class="item.status.colorClass">
                {{ item.status.label }}
              </span>
            </td>

            <td>
              <div class="client-info">
                <span class="dark-text font-bold">{{ item.clientName }}</span>
                <span class="gray-text text-sm">{{ item.clientEmail }}</span>
              </div>
            </td>
            
            <td>
              <div class="client-info">
                <span class="gray-text">{{ item.date }}</span>
                <span class="gray-text text-sm">{{ item.time }}</span>
              </div>
            </td>
            
            <td class="text-right dark-text font-bold">
              {{ item.amount }} FCFA
            </td>

            <td class="text-center">
              <button class="pill-btn" @click="openDetails(item)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
              </button>
            </td>
            
          </tr>
        </tbody>
      </table>

      <!-- ÉTAT VIDE -->
      <div v-if="paginatedHistory.length === 0" class="empty-state">
        <p class="gray-text">Aucune transaction trouvée pour cette catégorie ou recherche.</p>
      </div>
      
      <!-- ⚡️ BLOC PAGINATION DYNAMIQUE -->
      <div v-if="transactStore.totalCount > 0" class="pagination-section">
        
        <!-- Indication de la page actuelle et du total calculé sans tout télécharger -->
        <div class="page-info gray-text text-sm mb-4 text-center">
          Page <strong>{{ currentPage }}</strong> sur <strong>{{ totalPages }}</strong> 
          ({{ transactStore.totalCount }} transactions au total)
        </div>

        <Paginator 
          :currentPage="currentPage"
          :totalCount="transactStore.totalCount"
          :pageSize="itemsPerPage"
          @page-change="handlePageChange"
        />
      </div>
    </div>

    <!-- ⚡️ MODALE D'APERÇU DES DÉTAILS -->
    <div v-if="selectedTx" class="modal-overlay" @click.self="closeDetails">
      <div class="modal-content">
        <div class="modal-header">
          <h4>Détails de la transaction</h4>
          <button class="close-btn" @click="closeDetails">✕</button>
        </div>
        
        <div class="modal-body">
          <div class="detail-row">
            <span class="label">ID Commande :</span>
            <span class="value font-bold">{{ selectedTx.orderId }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Client :</span>
            <span class="value">{{ selectedTx.clientEmail }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Date :</span>
            <span class="value">{{ selectedTx.date }} à {{ selectedTx.time }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Montant Total :</span>
            <span class="value font-bold dark-text">{{ selectedTx.amount }} FCFA</span>
          </div>
          <div class="detail-row">
            <span class="label">Statut :</span>
            <span class="value">
              <!-- ⚡️ BADGE STATUT DANS LA MODALE -->
              <span class="status-badge" :class="selectedTx.status.colorClass">
                {{ selectedTx.status.label }}
              </span>
            </span>
          </div>

          <div class="items-section">
            <h5>Contenu de la commande</h5>
            <ul v-if="selectedTx.rawOrderItems && selectedTx.rawOrderItems.length > 0" class="items-list">
              <li v-for="(article, idx) in selectedTx.rawOrderItems" :key="idx">
                <span class="check-icon">✓</span>
                {{ article.contrat_title || article.pack_title || article.customised_contract || 'Article sans nom' }}
              </li>
            </ul>
            <p v-else class="gray-text">Aucun détail d'article trouvé.</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { 
  MagnifyingGlassIcon, 
  DocumentTextIcon, 
  ArchiveBoxIcon, 
  ScaleIcon
} from '@heroicons/vue/24/outline';
import { useAdminTransactStore } from '../../../stores/adminTransactStore';
import Paginator from '../../tools/Paginator.vue';

export default {
  name: 'AdminHistory',
  components: {
    Paginator
  },
  setup() {
    const transactStore = useAdminTransactStore();
    const activeTab = ref<'models' | 'packs' | 'custom'>('models');
    const searchQuery = ref('');
    
    const selectedTx = ref<any>(null);

    // ⚡️ ÉTATS POUR LA PAGINATION
    const currentPage = ref(1);
    const itemsPerPage = 10; // Doit correspondre à la page_size de ton AdminCartPagination Django

    // Chargement initial : Page 1 uniquement
    onMounted(async () => {
      await transactStore.fetchTransact(1);
    });

    // ⚡️ NOUVELLE FONCTION : DÉTERMINER LE STATUT ET LA COULEUR
    const getStatusData = (txStatus: string, orderStatus: string, defaultLabel: string | null) => {
      const rawStatus = (txStatus || orderStatus || '').toLowerCase();
      
      // Cas de succès (Vert)
      if (['success', 'completed', 'paid', 'succès', 'payé', 'successful'].includes(rawStatus)) {
        return { label: defaultLabel || 'Payé', colorClass: 'badge-green' };
      }
      
      // Cas en attente (Orange)
      if (['pending', 'en attente', 'processing'].includes(rawStatus)) {
        return { label: defaultLabel || 'En attente', colorClass: 'badge-orange' };
      }

      // Cas d'échec / annulé (Rouge)
      if (['failed', 'échoué', 'error', 'canceled', 'annulé'].includes(rawStatus)) {
         return { label: defaultLabel || 'Échoué', colorClass: 'badge-red' };
      }

      // Cas par défaut (Gris)
      return { label: defaultLabel || rawStatus || 'Inconnu', colorClass: 'badge-gray' };
    };

    // ⚡️ CALCUL DU NOMBRE TOTAL DE PAGES (basé sur count renvoyé par Django)
    const totalPages = computed(() => {
      return Math.ceil((transactStore.totalCount || 0) / itemsPerPage);
    });

    // Mapping des 10 transactions actuellement dans le store (page courante)
    const mappedTransactions = computed(() => {
      const sortedTransactions = [...transactStore.transactions].sort((a, b) => {
        const dateA = new Date(a.created_at || a.order?.created_at).getTime();
        const dateB = new Date(b.created_at || b.order?.created_at).getTime();
        return dateB - dateA;
      });

      return sortedTransactions.map((tx: any) => {
        const order = tx.order || {};
        const orderItems = order.order_items || order.items || tx.order_items || [];
        
        let productTypeLabel = 'Achat de contrat';
        let itemType = 'models';

        if (order.pack || tx.pack || order.order_type === 'pack' || orderItems[0]?.pack_title) {
          itemType = 'packs';
          productTypeLabel = 'Achat de pack';
        } else if (order.custom_contract || tx.custom_contract || order.order_type === 'custom' || orderItems[0]?.customised_contract) {
          itemType = 'custom';
          productTypeLabel = 'Demande sur-mesure';
        } else {
          itemType = 'models';
          productTypeLabel = 'Achat de contrat';
        }

        const clientEmail = order.buyer_email || order.guest?.email || order.user?.email || 'Email non renseigné';
        const clientName = order.guest?.full_name || (order.user ? `${order.user.first_name || ''} ${order.user.last_name || ''}`.trim() : null) || order.buyer_email || 'Client Invité';

        const rawDate = tx.created_at || order.created_at;
        const dateObj = rawDate ? new Date(rawDate) : new Date();
        const dateStr = dateObj.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
        const timeStr = dateObj.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });

        // ⚡️ UTILISATION DE LA FONCTION DE STATUT
        const providedLabel = tx.status_label || tx.status_labels || order.status_label || order.status_labels;
        const statusData = getStatusData(tx.status, order.status, providedLabel);

        return {
          id: tx.id || Math.random().toString(),
          orderId: order.id || tx.id,
          type: itemType,
          productTypeLabel,
          status: statusData, // 👈 Objet contenant label et colorClass
          clientName,
          clientEmail,
          date: dateStr,
          time: timeStr,
          amount: new Intl.NumberFormat('fr-FR').format(tx.amount || order.total_amount || 0),
          rawOrderItems: orderItems 
        };
      });
    });

    // Filtre local sur la page chargée (onglet + recherche)
    const paginatedHistory = computed(() => mappedTransactions.value);

    // ⚡️ CHANGEMENT DE PAGE : Appel API direct à Django
    const handlePageChange = async (page: number) => {
      currentPage.value = page;
      await transactStore.fetchTransact(page, activeTab.value, searchQuery.value);
    };

    // Réinitialise la page courante quand l'onglet change
    watch([activeTab, searchQuery], async () => {
      currentPage.value = 1;
      await transactStore.fetchTransact(1, activeTab.value, searchQuery.value);
    });

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

    const openDetails = (item: any) => {
      selectedTx.value = item;
    };

    const closeDetails = () => {
      selectedTx.value = null;
    };

    return {
      transactStore, 
      activeTab, 
      searchQuery, 
      paginatedHistory,
      totalPages,
      currentPage, 
      itemsPerPage, 
      handlePageChange,
      MagnifyingGlassIcon, 
      getIconColor, 
      getIcon,
      selectedTx, 
      openDetails, 
      closeDetails,
      getStatusData
    };
  }
}
</script>

<style scoped>
/* ⚡️ AJOUT DES CLASSES DE BADGES */
.status-badge {
  display: inline-block;
  padding: 0.35rem 0.8rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-green {
  background-color: #d1fae5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.badge-orange {
  background-color: #fef3c7;
  color: #d97706;
  border: 1px solid #fde68a;
}

.badge-red {
  background-color: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.badge-gray {
  background-color: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

/* Le reste du CSS inchangé */
.history-wrapper {
  --bg-main: #f8fafc; --bg-panel: #ffffff; --bg-panel-light: #f1f5f9; 
  --text-dark: #1e293b; --text-gray: #94a3b8; --accent-blue: #2563eb;
  display: flex; flex-direction: column; gap: 2rem; font-family: 'Inter', sans-serif;
}
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-and-search { display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.2rem; color: var(--text-dark); font-weight: 700; margin: 0; }
.search-box { display: flex; align-items: center; gap: 0.8rem; background: var(--bg-panel); border: 1px solid #e2e8f0; border-radius: 50px; padding: 0.6rem 1.2rem; flex: 1; max-width: 400px; box-shadow: 0 4px 10px rgba(0,0,0,0.02); }
.search-box input { background: transparent; border: none; color: var(--text-dark); font-size: 0.9rem; outline: none; width: 100%; font-weight: 500; }
.search-box input::placeholder { color: #cbd5e1; font-weight: 400; }
.icon-gray { width: 18px; height: 18px; color: var(--text-gray); }
.tabs-group { display: flex; background: var(--primary-color, #2563eb); border-radius: 50px; padding: 0.3rem; width: fit-content; }
.tab-btn { background: transparent; border: none; color: #ffffff; font-size: 0.85rem; font-weight: 600; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: all 0.2s ease; }
.tab-btn.active { background: var(--secondary-light-color, #1d4ed8); color: #ffffff; box-shadow: 0px 2px 10px rgba(0,0,0,0.1); }
.loading-state { text-align: center; padding: 3rem; color: var(--text-gray); font-weight: 600; }
.clean-list-container { background: var(--bg-panel); border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; overflow-x: auto; }
.minimal-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 800px; }
.minimal-table th { color: #cbd5e1; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding-bottom: 1.5rem; }
.minimal-table td { padding: 1.2rem 0; border-bottom: 1px solid #f8fafc; vertical-align: middle; }
.minimal-table tr:last-child td { border-bottom: none; }
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); font-size: 0.9rem; }
.font-bold { font-weight: 600; }
.text-right { text-align: center; }
.text-center { text-align: center; }
.text-sm { font-size: 0.75rem; display: block; margin-top: 0.2rem; }
.action-cell { display: flex; align-items: center; gap: 1rem; }
.client-info { display: flex; flex-direction: column; }
.icon-box-light { width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.icon-box-light svg { width: 20px; height: 20px; }
.bg-blue-light { background: #eff6ff; color: #3b82f6; }
.bg-purple-light { background: #faf5ff; color: #a855f7; }
.bg-orange-light { background: #fff7ed; color: #f97316; }
.empty-state { text-align: center; padding: 3rem 0; }

.pill-btn {
  background: transparent; color: var(--text-dark);
  padding: 0.4rem 1rem; border-radius: 50px; font-size: 0.8rem; font-weight: 600; cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02); transition: all 0.2s;
}
.pill-btn:hover { background: #f8fafc; border-color: #cbd5e1; }

.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-content {
  background: #ffffff; width: 100%; max-width: 500px;
  border-radius: 20px; padding: 2rem; box-shadow: 0 20px 50px rgba(0,0,0,0.1);
  display: flex; flex-direction: column; gap: 1.5rem;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; }
.modal-header h4 { margin: 0; font-size: 1.2rem; color: var(--text-dark); font-weight: 700; }
.close-btn { background: #f1f5f9; border: none; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-weight: bold; color: var(--text-gray); }
.close-btn:hover { background: #e2e8f0; color: var(--text-dark); }
.modal-body { display: flex; flex-direction: column; gap: 1rem; }
.detail-row { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.8rem; border-bottom: 1px solid #f1f5f9; }
.detail-row .label { color: var(--text-gray); font-size: 0.9rem; }
.detail-row .value { color: var(--text-dark); font-size: 0.95rem; }
.items-section { margin-top: 1rem; background: #f8fafc; padding: 1rem; border-radius: 12px; }
.items-section h5 { margin: 0 0 1rem 0; color: var(--text-dark); font-size: 0.95rem; }
.items-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.8rem; }
.items-list li { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--text-dark); }
.check-icon { color: #10b981; font-weight: bold; }
</style>