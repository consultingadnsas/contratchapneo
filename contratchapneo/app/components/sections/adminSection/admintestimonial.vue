<template>
  <div class="abandoned-carts-wrapper">
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Paniers Abandonnés</h3>
        <span class="badge">{{ totalCount }} abandons récents</span>
      </div>
      <p class="gray-text">
        Commandes validées mais non payées depuis plus de 1 heures.
      </p>
    </div>

    <div class="table-container">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Date & Heure</th>
            <th>Client (Email)</th>
            <th>Contenu de la commande</th>
            <th>Montant</th>
            <th>Actions</th> <!-- 👈 Nouvelle colonne -->
          </tr>
        </thead>
        <tbody v-if="!isLoading && abandonedOrders.length > 0">
          <tr v-for="order in abandonedOrders" :key="order.id">
            
            <td>
              <div class="date-cell">
                <span class="font-bold">{{ formatDate(order.created_at || order.date_transaction) }}</span>
                <span class="text-xs gray-text">{{ formatTime(order.created_at || order.date_transaction) }}</span>
              </div>
            </td>

            <td>
              <span class="client-email">{{ order.buyer_email || order.client_email || 'Email introuvable' }}</span>
            </td>

            <td>
              <ul class="items-list">
                <li v-for="item in order.order_items" :key="item.id" class="text-sm">
                  &bull; {{ item.contrat_title || item.pack_title || item.pro_name || item.designation || 'Service Juridique' }}
                </li>
              </ul>
            </td>

            <td>
              <span class="amount-badge font-bold">{{ order.total_amount }} FCFA</span>
            </td>

            <!-- 👈 Bouton Aperçu -->
            <td>
              <button type="button" class="btn-icon view" title="Aperçu du panier" @click="openPreviewModal(order)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
              </button>
            </td>

          </tr>
        </tbody>
        
        <tbody v-else-if="isLoading">
          <tr>
            <td colspan="5" class="text-center py-4">Chargement des données...</td>
          </tr>
        </tbody>
        
        <tbody v-else>
          <tr>
            <td colspan="5" class="text-center py-4 empty-state">
              Aucun panier abandonné récent. Beau travail !
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modale d'Aperçu -->
    <div v-if="showPreviewModal && selectedOrder" class="modal-overlay" @click.self="closePreviewModal">
      <div class="admin-modal-box">
        <div class="modal-header">
          <h4>Détails du Panier #{{ selectedOrder.id.split('-')[0] }}</h4>
          <button type="button" class="close-btn" @click="closePreviewModal">&times;</button>
        </div>
        
        <div class="modal-body">
          <!-- Infos Client -->
          <div class="info-section">
            <h5 class="section-subtitle">Coordonnées du client</h5>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Nom complet :</span>
                <!-- Adapter selon comment le backend renvoie le nom (guest ou user) -->
                <span class="info-value font-bold">{{ getClientName(selectedOrder) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Email :</span>
                <span class="info-value">{{ selectedOrder.buyer_email || selectedOrder.client_email || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Téléphone :</span>
                <!-- Adapter selon comment le backend renvoie le téléphone -->
                <span class="info-value">{{ getClientPhone(selectedOrder) }}</span>
              </div>
            </div>
          </div>

          <!-- Détails de la commande -->
          <div class="info-section">
            <h5 class="section-subtitle">Contenu du panier</h5>
            <ul class="modal-items-list">
              <li v-for="item in selectedOrder.order_items" :key="item.id" class="modal-item">
                <div class="item-name">
                  {{ item.quantity }}x {{ item.contrat_title || item.pack_title || item.pro_name || item.designation || 'Article' }}
                </div>
                <div class="item-price font-bold">{{ item.unit_price || 0 }} FCFA</div>
              </li>
            </ul>
            <div class="total-row">
              <span>Total :</span>
              <span class="font-bold amount-highlight">{{ selectedOrder.total_amount }} FCFA</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-secondary" @click="closePreviewModal">Fermer</button>
        </div>
      </div>
    </div>

    <Paginator
      v-if="totalCount > pageSize && !isLoading"
      :current-page="currentPage"
      :total-count="totalCount"
      :page-size="pageSize"
      @page-change="handlePageChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAdminOrderStore } from '../../../stores/adminOrderStore';
import Paginator from '../../tools/Paginator.vue'; 

const adminOrderStore = useAdminOrderStore();

const currentPage = ref(1);
const pageSize = ref(10); 

const abandonedOrders = computed(() => adminOrderStore.abandonedOrders);
const totalCount = computed(() => adminOrderStore.totalAbandonedCount);
const isLoading = computed(() => adminOrderStore.isLoading);

// --- État de la modale ---
const showPreviewModal = ref(false);
const selectedOrder = ref<any>(null);

onMounted(async () => {
  await loadPage(currentPage.value);
});

const loadPage = async (page: number) => {
  await adminOrderStore.fetchAbandonedOrders(page);
};

const handlePageChange = async (newPage: number) => {
  currentPage.value = newPage;
  await loadPage(newPage);
};

// --- Actions de la modale ---
const openPreviewModal = (order: any) => {
  selectedOrder.value = order;
  showPreviewModal.value = true;
};

const closePreviewModal = () => {
  showPreviewModal.value = false;
  selectedOrder.value = null;
};

// --- Extracteurs de données ---
// ⚠️ Ces fonctions dépendent de comment ton OrderSerializer côté Django renvoie les données.
const getClientName = (order: any) => {
  return order.client_name || 'Nom non renseigné';
};

const getClientPhone = (order: any) => {
  return order.client_phone || 'Non renseigné';
};

// --- Formatage ---
const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
};

const formatTime = (dateString: string | undefined) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
};
</script>

<style scoped>
.abandoned-carts-wrapper { display: flex; flex-direction: column; gap: 1.5rem; font-family: 'Inter', sans-serif; position: relative;}
.header-section { display: flex; flex-direction: column; gap: 0.5rem; }
.title-row { display: flex; align-items: center; gap: 1rem; }
.section-title { font-size: 1.4rem; color: #1e293b; font-weight: 700; margin: 0; }
.badge { background: #fee2e2; color: #ef4444; padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.8rem; font-weight: 600; }
.gray-text { color: #64748b; font-size: 0.95rem; margin: 0; }
.text-xs { font-size: 0.75rem; }
.text-sm { font-size: 0.85rem; }
.font-bold { font-weight: 700; }
.text-center { text-align: center; }
.py-4 { padding-top: 2rem; padding-bottom: 2rem; }
.table-container { background: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; border: 1px solid #e2e8f0; }
.admin-table { width: 100%; border-collapse: collapse; text-align: left; }
.admin-table th { background: #f8fafc; padding: 1rem 1.2rem; font-size: 0.85rem; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e2e8f0; }
.admin-table td { padding: 1rem 1.2rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
.admin-table tr:last-child td { border-bottom: none; }
.admin-table tr:hover { background: #f8fafc; }
.date-cell { display: flex; flex-direction: column; }
.client-email { color: #0f172a; font-weight: 500; }
.items-list { margin: 0; padding: 0; list-style: none; color: #475569; }
.amount-badge { display: inline-block; background: #f1f5f9; padding: 0.4rem 0.8rem; border-radius: 8px; color: #0f172a; }
.empty-state { color: #94a3b8; font-style: italic; }

/* Bouton Icone (Œil) */
.btn-icon { background: none; border: none; cursor: pointer; padding: 0.5rem; border-radius: 6px; transition: 0.2s; color: #64748b; display: flex; align-items: center; justify-content: center;}
.btn-icon:hover { background: #f1f5f9; }
.btn-icon.view:hover { color: #2563eb; background: #eff6ff;}
.icon-sm { width: 20px; height: 20px; }

/* Modale Styles */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.admin-modal-box { background: #ffffff; border-radius: 16px; width: 100%; max-width: 550px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); overflow: hidden; animation: adminSlideUp 0.3s ease-out forwards; }
@keyframes adminSlideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 1.5rem; border-bottom: 1px solid #e2e8f0; }
.modal-header h4 { margin: 0; font-size: 1.1rem; color: #0f172a; font-weight: 700; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #94a3b8; transition: 0.2s; }
.close-btn:hover { color: #e61010; }
.modal-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1.5rem; }

/* Sections internes modale */
.info-section { display: flex; flex-direction: column; gap: 0.8rem; }
.section-subtitle { font-size: 0.9rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin: 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 0.5rem;}
.info-grid { display: grid; grid-template-columns: 1fr; gap: 0.6rem; }
.info-item { display: flex; justify-content: space-between; font-size: 0.95rem; }
.info-label { color: #475569; }
.info-value { color: #0f172a; }

.modal-items-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.5rem; }
.modal-item { display: flex; justify-content: space-between; font-size: 0.95rem; color: #334155; padding: 0.4rem 0; border-bottom: 1px dashed #e2e8f0;}
.total-row { display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem; font-size: 1.1rem; color: #0f172a; }
.amount-highlight { color: #059669; background: #dcfce7; padding: 0.3rem 0.6rem; border-radius: 6px;}

.modal-footer { display: flex; justify-content: center; padding: 1rem 1.5rem; border-top: 1px solid #e2e8f0; background: #f8fafc; }
.btn-secondary { background: #ffffff; color: #475569; border: 1px solid #cbd5e1; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-secondary:hover { background: #f1f5f9; }
</style>