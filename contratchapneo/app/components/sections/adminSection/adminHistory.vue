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

      <!-- 🖥️ ONGLETS BOUTONS : Visible uniquement sur Desktop (> 1024px) -->
      <div class="tabs-group desktop-only">
        <button class="tab-btn" :class="{ active: activeTab === 'models' }" @click="activeTab = 'models'">
          Contrats vendus
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'packs' }" @click="activeTab = 'packs'">
          Packs de contrats
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'custom' }" @click="activeTab = 'custom'">
          Sur-Mesure
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'revisions' }" @click="activeTab = 'revisions'">
          Révisions
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'pros' }" @click="activeTab = 'pros'">
          Experts
        </button>
      </div>

      <!-- 📱 MENU DÉROULANT : Visible sur Téléphone et Tablette (<= 1024px), sous la recherche -->
      <div class="tabs-dropdown-wrapper mobile-tablet-only">
        <label for="transaction-type-select" class="dropdown-label">Type de transactions :</label>
        <div class="select-box">
          <select id="transaction-type-select" v-model="activeTab" class="tabs-select" aria-label="Type de transactions">
            <option value="models">Contrats vendus</option>
            <option value="packs">Packs de contrats</option>
            <option value="custom">Sur-Mesure</option>
            <option value="revisions">Révisions</option>
            <option value="pros">Experts</option>
          </select>
          <svg class="select-arrow" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
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
                {{ 
                  article.contrat_title || 
                  article.pack_title || 
                  article.pro_name || 
                  article.pro?.name || 
                  article.contract_revision_title || 
                  article.contract_revision?.title || 
                  article.customised_contract || 
                  'Article sans nom' 
                }}
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
  ScaleIcon,
  BriefcaseIcon,
  PencilSquareIcon
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
    const activeTab = ref<'models' | 'packs' | 'custom' | 'pros' | 'revisions'>('models');
    const searchQuery = ref('');
    
    const selectedTx = ref<any>(null);

    // ⚡️ ÉTATS POUR LA PAGINATION
    const currentPage = ref(1);
    const itemsPerPage = 10; // Doit correspondre à la page_size de ton AdminCartPagination Django

    onMounted(async () => {
      await transactStore.fetchTransact(currentPage.value, activeTab.value, searchQuery.value);
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
        const dateA = new Date(a.created_at || a.order?.created_at || 0).getTime();
        const dateB = new Date(b.created_at || b.order?.created_at || 0).getTime();
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
        } else if (orderItems.some((i: any) => i.contract_revision || i.contract_revision_id)) {
          itemType = 'revisions'; // ⚡️ NOUVEAU
          productTypeLabel = 'Révision de contrat';
        } else if (order.custom_contract || tx.custom_contract || order.order_type === 'custom' || orderItems.some((i: any) => i.customised_contract || i.contrat_customed || i.contract_revision || i.contract_revision_id)) {
          itemType = 'custom';
          productTypeLabel = 'Demande sur-mesure';
        }  else if (orderItems.some((i: any) => i.pro || i.pro_name || i.pro_id)) {
          itemType = 'pros'; // ⚡️ DÉTECTION DU PRO
          productTypeLabel = 'Sollicitation Expert';
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
      if (tab === 'pros') return 'bg-teal-light';
      if (tab === 'revisions') return 'bg-pink-light';
      return 'bg-orange-light';
    };

    const getIcon = (tab: string) => {
      if (tab === 'models') return DocumentTextIcon;
      if (tab === 'packs') return ArchiveBoxIcon;
      if (tab === 'pros') return BriefcaseIcon;
      if (tab === 'revisions') return PencilSquareIcon;
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
      BriefcaseIcon,
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

/* STRUCTURE PRINCIPALE */
.history-wrapper {
  --bg-main: #f8fafc; --bg-panel: #ffffff; --bg-panel-light: #f1f5f9; 
  --text-dark: #1e293b; --text-gray: #94a3b8; --accent-blue: #2563eb;
  display: flex; flex-direction: column; gap: 2rem; font-family: 'Inter', sans-serif;
  width: 100%; box-sizing: border-box;
}

.header-section { display: flex; flex-direction: column; gap: 1.5rem; width: 100%; }
.title-and-search { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; width: 100%; }
.section-title { font-size: 1.35rem; color: var(--text-dark); font-weight: 700; margin: 0; letter-spacing: -0.3px; }

/* BARRE DE RECHERCHE */
.search-box { 
  display: flex; align-items: center; gap: 0.8rem; background: var(--bg-panel); 
  border: 1px solid #e2e8f0; border-radius: 50px; padding: 0.65rem 1.2rem; 
  flex: 1; max-width: 400px; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
  transition: all 0.2s ease; box-sizing: border-box;
}
.search-box:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
}
.search-box input { background: transparent; border: none; color: var(--text-dark); font-size: 0.9rem; outline: none; width: 100%; font-weight: 500; }
.search-box input::placeholder { color: #cbd5e1; font-weight: 400; }
.icon-gray { width: 18px; height: 18px; color: var(--text-gray); flex-shrink: 0; }

/* 🖥️ ONGLETS BOUTONS (DESKTOP) */
.desktop-only { display: flex; }
.tabs-group { display: flex; background: var(--primary-color, #2563eb); border-radius: 50px; padding: 0.3rem; width: fit-content; gap: 0.2rem; }
.tab-btn { background: transparent; border: none; color: #ffffff; font-size: 0.85rem; font-weight: 600; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: all 0.2s ease; white-space: nowrap; }
.tab-btn.active { background: var(--secondary-light-color, #1d4ed8); color: #ffffff; box-shadow: 0px 2px 10px rgba(0,0,0,0.1); }

/* 📱 MENU DÉROULANT (TÉLÉPHONE & TABLETTE) */
.tabs-dropdown-wrapper {
  display: none;
  width: 100%;
  flex-direction: column;
  gap: 0.4rem;
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
.tabs-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1.25rem;
  border: 1px solid #cbd5e1;
  border-radius: 50px;
  background-color: var(--bg-panel);
  color: var(--text-dark);
  font-size: 0.95rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
  transition: all 0.2s ease;
}
.tabs-select:focus {
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

.loading-state { text-align: center; padding: 3rem; color: var(--text-gray); font-weight: 600; }

/* TABLEAU ET CONTENEUR RESPONSIVE */
.clean-list-container { 
  background: var(--bg-panel); 
  border-radius: 24px; 
  padding: 1.5rem; 
  box-shadow: 0 10px 40px rgba(0,0,0,0.03); 
  border: 1px solid #f1f5f9; 
  overflow-x: auto; 
  -webkit-overflow-scrolling: touch;
  width: 100%;
  box-sizing: border-box;
}

.clean-list-container::-webkit-scrollbar {
  height: 6px;
}
.clean-list-container::-webkit-scrollbar-track {
  background: #f8fafc;
  border-radius: 10px;
}
.clean-list-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.clean-list-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.minimal-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 750px; }
.minimal-table th { color: #94a3b8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding-bottom: 1.25rem; }
.minimal-table td { padding: 1.1rem 0.4rem; border-bottom: 1px solid #f8fafc; vertical-align: middle; }
.minimal-table tr:last-child td { border-bottom: none; }
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); font-size: 0.9rem; }
.font-bold { font-weight: 600; }
.text-right { text-align: center; }
.text-center { text-align: center; }
.text-sm { font-size: 0.75rem; display: block; margin-top: 0.2rem; }
.action-cell { display: flex; align-items: center; gap: 0.85rem; }
.client-info { display: flex; flex-direction: column; }
.icon-box-light { width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.icon-box-light svg { width: 20px; height: 20px; }
.bg-blue-light { background: #eff6ff; color: #3b82f6; }
.bg-purple-light { background: #faf5ff; color: #a855f7; }
.bg-orange-light { background: #fff7ed; color: #f97316; }
.bg-teal-light { background: #ccfbf1; color: #0f766e; }
.bg-pink-light { background: #fce7f3; color: #db2777; }
.empty-state { text-align: center; padding: 3rem 0; }

.pill-btn {
  background: transparent; color: var(--text-dark);
  padding: 0.4rem 0.9rem; border-radius: 50px; font-size: 0.8rem; font-weight: 600; cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02); transition: all 0.2s;
  border: 1px solid transparent;
  display: inline-flex; align-items: center; justify-content: center;
}
.pill-btn:hover { background: #f8fafc; border-color: #cbd5e1; }

/* MODALE RESPONSIVE */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.45); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
  padding: 1rem; box-sizing: border-box;
}
.modal-content {
  background: #ffffff; width: 100%; max-width: 500px;
  border-radius: 20px; padding: 2rem; box-shadow: 0 20px 50px rgba(0,0,0,0.12);
  display: flex; flex-direction: column; gap: 1.5rem;
  max-height: 85vh; overflow-y: auto; -webkit-overflow-scrolling: touch;
  box-sizing: border-box;
}
.modal-content::-webkit-scrollbar { width: 6px; }
.modal-content::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }

.modal-header { display: flex; justify-content: space-between; align-items: center; }
.modal-header h4 { margin: 0; font-size: 1.2rem; color: var(--text-dark); font-weight: 700; }
.close-btn { background: #f1f5f9; border: none; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-weight: bold; color: var(--text-gray); display: flex; align-items: center; justify-content: center; }
.close-btn:hover { background: #e2e8f0; color: var(--text-dark); }
.modal-body { display: flex; flex-direction: column; gap: 1rem; }
.detail-row { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.8rem; border-bottom: 1px solid #f1f5f9; gap: 0.75rem; }
.detail-row .label { color: var(--text-gray); font-size: 0.9rem; flex-shrink: 0; }
.detail-row .value { color: var(--text-dark); font-size: 0.95rem; text-align: right; word-break: break-word; }
.items-section { margin-top: 1rem; background: #f8fafc; padding: 1rem; border-radius: 12px; }
.items-section h5 { margin: 0 0 1rem 0; color: var(--text-dark); font-size: 0.95rem; }
.items-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.8rem; }
.items-list li { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--text-dark); }
.check-icon { color: #10b981; font-weight: bold; flex-shrink: 0; }

/* ========================================================
   RESPONSIVE : TÉLÉPHONES & TABLETTES (<= 1024px)
   ======================================================== */
@media (max-width: 1024px) {
  .history-wrapper {
    gap: 1.25rem;
  }

  .header-section {
    gap: 1rem;
  }

  /* La barre de recherche se place sous le titre et au-dessus du menu déroulant */
  .title-and-search {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  /* Recherche pleine largeur */
  .search-box {
    max-width: 100%;
    width: 100%;
  }

  /* Masquer les onglets boutons et afficher le menu déroulant */
  .desktop-only {
    display: none !important;
  }

  .tabs-dropdown-wrapper,
  .mobile-tablet-only {
    display: flex !important;
  }

  .clean-list-container {
    padding: 1rem;
    border-radius: 18px;
  }
}

/* ========================================================
   RESPONSIVE : SMARTPHONES (< 640px)
   ======================================================== */
@media (max-width: 640px) {
  .clean-list-container {
    padding: 0.75rem;
    border-radius: 14px;
  }

  .minimal-table th {
    font-size: 0.7rem;
    padding-bottom: 0.9rem;
  }

  .minimal-table td {
    padding: 0.85rem 0.25rem;
  }

  .modal-overlay {
    padding: 0.75rem;
  }

  .modal-content {
    padding: 1.25rem;
    border-radius: 16px;
    max-height: 85vh;
  }

  .detail-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
  }

  .detail-row .value {
    text-align: left;
  }
}
</style>