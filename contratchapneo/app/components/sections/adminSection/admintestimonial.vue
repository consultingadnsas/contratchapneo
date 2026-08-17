<template>
  <div class="abandoned-carts-wrapper">
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Paniers Abandonnés</h3>
        <span class="badge">{{ totalCount }} abandons récents</span>
      </div>
      <p class="gray-text">
        Commandes validées mais non payées depuis plus de 2 heures.
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

          </tr>
        </tbody>
        
        <tbody v-else-if="isLoading">
          <tr>
            <td colspan="4" class="text-center py-4">Chargement des données...</td>
          </tr>
        </tbody>
        
        <tbody v-else>
          <tr>
            <td colspan="4" class="text-center py-4 empty-state">
              Aucun panier abandonné récent. Beau travail !
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 👈 INTÉGRATION DE LA PAGINATION -->
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
import Paginator from '../../tools/Paginator.vue'; // 👈 Ajuste le chemin si nécessaire

const adminOrderStore = useAdminOrderStore();

// Variables réactives pour la pagination
const currentPage = ref(1);
const pageSize = ref(10); // Doit correspondre à `page_size = 10` défini dans AdminPagination côté Django

// Données du store
const abandonedOrders = computed(() => adminOrderStore.abandonedOrders);
const totalCount = computed(() => adminOrderStore.totalAbandonedCount);
const isLoading = computed(() => adminOrderStore.isLoading);

onMounted(async () => {
  await loadPage(currentPage.value);
});

// Fonction pour charger une page spécifique
const loadPage = async (page: number) => {
  await adminOrderStore.fetchAbandonedOrders(page);
};

// Écouteur de l'événement émis par le composant Paginator
const handlePageChange = async (newPage: number) => {
  currentPage.value = newPage;
  await loadPage(newPage);
};

// Formatage de la date
const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '-';
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
};

// Formatage de l'heure
const formatTime = (dateString: string | undefined) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
};
</script>

<style scoped>
/* Les styles restent identiques à ton code précédent */
.abandoned-carts-wrapper { display: flex; flex-direction: column; gap: 1.5rem; font-family: 'Inter', sans-serif; }
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
</style>