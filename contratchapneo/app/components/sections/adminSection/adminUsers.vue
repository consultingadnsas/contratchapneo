<template>
  <div class="users-wrapper">
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Utilisateurs</h3>
      </div>
      <p class="gray-text text-sm">Gérez les utilisateurs inscrits et vérifiez s'ils disposent de packs de contrats.</p>
    </div>

    <!-- Filtres -->
    <div class="filters-row">
      <div class="search-wrapper">
        <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
        <input v-model="searchQuery" type="text" placeholder="Rechercher par nom ou email" class="search-input" />
      </div>
      <div class="select-wrapper">
        <select v-model="packFilter" class="filter-select" aria-label="Filtrer par pack">
          <option value="all">Tous les utilisateurs</option>
          <option value="with_pack">Utilisateurs avec pack</option>
          <option value="without_pack">Utilisateurs sans pack</option>
        </select>
        <svg class="select-arrow" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
        </svg>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="isLoading" class="loading-state">
      Chargement des utilisateurs...
    </div>

    <div v-else class="table-container">
      <div class="table-scroll-container">
        <table class="users-table">
          <thead>
            <tr>
              <th>Date d'inscription</th>
              <th>Nom Complet</th>
              <th>Email</th>
              <th>Actif</th>
              <th>Pack de contrat</th>
              <th>Pack Actif</th>
              <th>Détails</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td>{{ formatDate(user.date_joined) }}</td>
              <td>{{ user.first_name }} {{ user.last_name }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span class="badge" :class="user.is_active ? 'badge-green' : 'badge-red'">
                  {{ user.is_active ? 'Oui' : 'Non' }}
                </span>
              </td>
              <td>
                <span class="badge" :class="user.has_pack ? 'badge-green' : 'badge-red'">
                  {{ user.has_pack ? 'Oui' : 'Non' }}
                </span>
              </td>
              <td>
                <span class="badge" :class="user.has_active_pack ? 'badge-green' : 'badge-gray'">
                  {{ user.has_active_pack ? 'Actif' : 'Aucun' }}
                </span>
              </td>
              <td>
                <button class="action-btn" @click="openModal(user)" title="Voir les détails">
                  <EyeIcon class="icon-eye" />
                </button>
              </td>
            </tr>
            <tr v-if="filteredUsers.length === 0">
              <td colspan="7" class="empty-state">Aucun utilisateur trouvé.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginator Component -->
      <Paginator 
        v-if="filteredUsers.length > 0"
        :current-page="currentPage" 
        :total-count="filteredUsers.length" 
        :page-size="pageSize"
        @page-change="onPageChange" 
      />
    </div>

    <!-- Graphique -->
    <div class="chart-section" v-if="!isLoading && users.length > 0">
      <AdminUsersChart :users="users" />
    </div>
    
    <!-- Modal des détails de l'utilisateur -->
    <div v-if="selectedUser" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">Détails de l'utilisateur</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="info-group">
            <strong>ID :</strong> <span>{{ selectedUser.id }}</span>
          </div>
          <div class="info-group">
            <strong>Nom Complet :</strong> <span>{{ selectedUser.first_name }} {{ selectedUser.last_name }}</span>
          </div>
          <div class="info-group">
            <strong>Email :</strong> <span>{{ selectedUser.email }}</span>
          </div>
          <div class="info-group">
            <strong>Numéro de téléphone :</strong> <span>{{ selectedUser.phone_number || 'Non renseigné' }}</span>
          </div>
          
          <h4 class="mt-4 mb-2 font-semibold text-lg text-slate-800">Historique des packs</h4>
          <div v-if="selectedUser.packs && selectedUser.packs.length > 0" class="packs-list">
            <div v-for="pack in selectedUser.packs" :key="pack.id" class="pack-item" :class="pack.is_active ? 'border-green-500' : 'border-gray-200'">
              <div class="flex justify-between items-center mb-2">
                <span class="font-bold text-slate-700">{{ pack.pack_name }}</span>
                <span class="badge" :class="pack.is_active ? 'badge-green' : 'badge-red'">{{ pack.is_active ? 'Actif' : 'Expiré' }}</span>
              </div>
              <div class="text-sm text-slate-600 mb-1">
                <strong>Crédits :</strong> {{ pack.credits_restants }} restants
              </div>
              <div class="text-sm text-slate-600 mb-1">
                <strong>Customs :</strong> {{ pack.customs_restants }} restants
              </div>
              <div class="text-sm text-slate-600 mb-1">
                <strong>Cartes pro :</strong> {{ pack.cartes_pro_restantes }} restantes
              </div>
              <div class="text-sm text-slate-600">
                <strong>Expire le :</strong> {{ formatDate(pack.expires_at) }}
              </div>
            </div>
          </div>
          <div v-else class="text-slate-500 italic mt-2">
            Cet utilisateur n'a jamais acheté de pack.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useNuxtApp } from '#imports';
import { EyeIcon } from '@heroicons/vue/24/outline';
import AdminUsersChart from './AdminUsersChart.vue';
import Paginator from '../../tools/Paginator.vue';

export default {
  name: 'AdminUsers',
  components: {
    EyeIcon,
    AdminUsersChart,
    Paginator
  },
  setup() {
    const { $api } = useNuxtApp();
    const users = ref<any[]>([]);
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    const selectedUser = ref<any | null>(null);

    const searchQuery = ref('');
    const packFilter = ref('all');

    const filteredUsers = computed(() => {
      let result = users.value;
      if (packFilter.value === 'with_pack') {
        result = result.filter(u => u.has_pack);
      } else if (packFilter.value === 'without_pack') {
        result = result.filter(u => !u.has_pack);
      }

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(u => {
          const name = `${u.first_name || ''} ${u.last_name || ''}`.toLowerCase();
          return name.includes(query) || (u.email && u.email.toLowerCase().includes(query));
        });
      }
      return result;
    });

    const currentPage = ref(1);
    const pageSize = ref(10);

    watch([searchQuery, packFilter], () => {
      currentPage.value = 1;
    });

    const paginatedUsers = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      return filteredUsers.value.slice(start, start + pageSize.value);
    });

    const onPageChange = (page: number) => {
      currentPage.value = page;
    };

    const fetchUsers = async () => {
      isLoading.value = true;
      try {
        const response = await $api<any>('/account/admin/users/', { method: 'GET' });
        users.value = response.data ? response.data : response;
      } catch (err: any) {
        error.value = "Erreur lors de la récupération des utilisateurs.";
        console.error(err);
      } finally {
        isLoading.value = false;
      }
    };

    const formatDate = (dateStr: string) => {
      if (!dateStr) return '-';
      const date = new Date(dateStr);
      return date.toLocaleDateString('fr-FR', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      });
    };

    const openModal = (user: any) => {
      selectedUser.value = user;
    };

    const closeModal = () => {
      selectedUser.value = null;
    };

    onMounted(() => {
      fetchUsers();
    });

    return {
      users,
      filteredUsers,
      paginatedUsers,
      currentPage,
      pageSize,
      onPageChange,
      isLoading,
      searchQuery,
      packFilter,
      formatDate,
      selectedUser,
      openModal,
      closeModal
    };
  }
}
</script>

<style scoped>
.users-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding-bottom: 2rem;
  font-family: 'Inter', sans-serif;
}
.header-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.section-title {
  font-size: 1.4rem;
  color: #1e293b;
  font-weight: 700;
  margin: 0;
}
.gray-text {
  color: #94a3b8;
}
.text-sm {
  font-size: 0.85rem;
}

/* Filtres */
.filters-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  width: 100%;
}
.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 260px;
}
.search-icon {
  position: absolute;
  left: 1.1rem;
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
}
.search-input {
  width: 100%;
  padding: 0.75rem 1.25rem 0.75rem 2.6rem;
  border: 1px solid #cbd5e1;
  border-radius: 50px;
  font-size: 0.95rem;
  outline: none;
  background-color: white;
  transition: all 0.2s ease;
  box-sizing: border-box;
}
.search-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  min-width: 260px;
  flex: 1;
  max-width: 400px;
}
.filter-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1.25rem;
  border: 1px solid #cbd5e1;
  border-radius: 50px;
  font-size: 0.95rem;
  font-weight: 500;
  outline: none;
  background-color: white;
  color: #334155;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}
.filter-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}
.select-arrow {
  position: absolute;
  right: 1.1rem;
  width: 18px;
  height: 18px;
  color: #64748b;
  pointer-events: none;
  transition: transform 0.2s ease;
}
.select-wrapper:focus-within .select-arrow {
  color: #3b82f6;
  transform: rotate(180deg);
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-weight: 600;
}

/* CARTE TABLEAU ET CONTENEUR SCROLLABLE */
.table-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  border: 1px solid #f1f5f9;
  padding: 1.25rem;
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

.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  min-width: 880px;
}
.users-table th, .users-table td {
  padding: 1rem 0.85rem;
  border-bottom: 1px solid #f1f5f9;
  white-space: nowrap;
}
.users-table th {
  background: #f8fafc;
  color: #475569;
  font-weight: 600;
  font-size: 0.9rem;
}
.users-table td {
  color: #334155;
  font-size: 0.9rem;
}
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
}

.badge {
  padding: 0.3rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.badge-green { background: #dcfce7; color: #166534; }
.badge-red { background: #fee2e2; color: #991b1b; }
.badge-blue { background: #dbeafe; color: #1e40af; }
.badge-gray { background: #f1f5f9; color: #475569; }

/* Action Button */
.action-btn {
  background: #f1f5f9;
  color: #156ca9;
  border: none;
  padding: 0.4rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.action-btn:hover {
  background: #156ca9;
  color: white;
}
.icon-eye {
  width: 1.25rem;
  height: 1.25rem;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
  padding: 1rem;
  box-sizing: border-box;
}
.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%; max-width: 500px;
  max-height: 85vh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  animation: slideDown 0.3s ease-out;
  box-sizing: border-box;
}
.modal-content::-webkit-scrollbar { width: 6px; }
.modal-content::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.modal-title { margin: 0; font-size: 1.25rem; font-weight: 700; color: #0f172a; }
.close-btn { background: none; border: none; font-size: 1.5rem; color: #64748b; cursor: pointer; width:fit-content }
.close-btn:hover { color: #0f172a; }
.modal-body { padding: 1.5rem; }
.info-group {
  margin-bottom: 0.8rem;
  display: flex; flex-direction: column; gap: 0.2rem;
}
.info-group strong { color: #475569; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.info-group span { color: #0f172a; font-weight: 500; font-size: 1rem; }

.packs-list {
  display: flex; flex-direction: column; gap: 1rem;
}
.pack-item {
  border: 1px solid #e2e8f0;
  border-left-width: 4px;
  padding: 1rem;
  border-radius: 8px;
  background: #f8fafc;
}
.mt-4 { margin-top: 1rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-1 { margin-bottom: 0.25rem; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
.text-lg { font-size: 1.125rem; }
.text-sm { font-size: 0.875rem; }
.text-slate-800 { color: #1e293b; }
.text-slate-700 { color: #334155; }
.text-slate-600 { color: #475569; }
.text-slate-500 { color: #64748b; }
.italic { font-style: italic; }
.flex { display: flex; }
.justify-between { justify-content: space-between; }
.items-center { align-items: center; }

.chart-section {
  display: flex;
  justify-content: center;
}

/* ========================================================
   RESPONSIVE : TABLETTE & TÉLÉPHONE (<= 1024px)
   ======================================================== */
@media (max-width: 1024px) {
  .users-wrapper {
    gap: 1.5rem;
  }

  .table-container {
    padding: 1rem;
    border-radius: 14px;
  }
}

/* ========================================================
   RESPONSIVE : SMARTPHONES (<= 768px)
   ======================================================== */
@media (max-width: 768px) {
  .users-wrapper {
    gap: 1.25rem;
  }

  /* Filtres verticaux pleine largeur : le filtre utilisateur et la recherche s'étirent sur toute la largeur */
  .filters-row {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    width: 100%;
  }

  .search-wrapper,
  .search-input,
  .select-wrapper,
  .filter-select {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box;
  }

  .table-container {
    padding: 0.75rem;
    border-radius: 12px;
  }

  .users-table th, .users-table td {
    padding: 0.8rem 0.6rem;
    font-size: 0.85rem;
  }

  .modal-overlay {
    padding: 0.75rem;
  }

  .modal-content {
    padding: 1.25rem;
  }

  .info-group span {
    word-break: break-all;
  }
}
</style>