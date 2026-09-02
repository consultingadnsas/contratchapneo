<template>
    <div class="admin-tracker-container">
        <div class="header-section">
            <h2>Suivi des Visites</h2>
            <p>Analyse du trafic journalier par pays.</p>
        </div>

        <!-- 🎛 SECTION FILTRES -->
        <div class="filters-card">
            <div class="filter-group">
                <label>Pays</label>
                <input 
                    type="text" 
                    v-model="filters.country" 
                    placeholder="Ex: France, Côte d'Ivoire..." 
                    class="filter-input"
                    @keyup.enter="applyFilters"
                />
            </div>
            <div class="filter-group">
                <label>Date de début</label>
                <input type="date" v-model="filters.start_date" class="filter-input" />
            </div>
            <div class="filter-group">
                <label>Date de fin</label>
                <input type="date" v-model="filters.end_date" class="filter-input" />
            </div>
            <div class="filter-actions">
                <button @click="resetFilters" class="btn-reset">Réinitialiser</button>
                <button @click="applyFilters" class="btn-submit">Filtrer</button>
            </div>
        </div>

        <!-- 📊 SECTION TABLEAU -->
        <div class="table-card">
            <div v-if="trackerStore.isLoading" class="loading-state">
                Chargement des données...
            </div>
            
            <div v-else-if="trackerStore.error" class="error-state">
                {{ trackerStore.error }}
            </div>

            <table v-else class="admin-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Pays</th>
                        <th>Nombre de visites</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="visit in trackerStore.visits" :key="visit.id">
                        <td>{{ formatDate(visit.date) }}</td>
                        <td>
                            <span class="country-badge">{{ visit.country }}</span>
                        </td>
                        <td class="visits-count">{{ visit.visits }}</td>
                    </tr>
                    <tr v-if="trackerStore.visits.length === 0">
                        <td colspan="3" class="empty-state">Aucune visite trouvée pour ces critères.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 🧭 PAGINATION -->
        <div class="pagination-section" v-if="trackerStore.totalCount > 0">
            <button 
                :disabled="trackerStore.currentPage === 1" 
                @click="changePage(trackerStore.currentPage - 1)"
                class="page-btn"
            >
                Précédent
            </button>
            <span class="page-info">
                Page {{ trackerStore.currentPage }} sur {{ totalPages }}
            </span>
            <button 
                :disabled="trackerStore.currentPage >= totalPages" 
                @click="changePage(trackerStore.currentPage + 1)"
                class="page-btn"
            >
                Suivant
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAdminTrackerStore } from '../../../stores/adminTrackerStore';

export default {
    name: 'AdminTracker',
    setup() {
        const trackerStore = useAdminTrackerStore();

        // État local pour les filtres
        const filters = ref({
            country: '',
            start_date: '',
            end_date: ''
        });

        // Calcul du nombre total de pages (en supposant une pagination par défaut de 10)
        const pageSize = 10;
        const totalPages = computed(() => Math.ceil(trackerStore.totalCount / pageSize));

        // Actions
        const applyFilters = () => {
            trackerStore.fetchVisits(1, filters.value);
        };

        const resetFilters = () => {
            filters.value = { country: '', start_date: '', end_date: '' };
            trackerStore.fetchVisits(1);
        };

        const changePage = (newPage: number) => {
            if (newPage > 0 && newPage <= totalPages.value) {
                trackerStore.fetchVisits(newPage, filters.value);
            }
        };

        // Utilitaire de formatage de date (YYYY-MM-DD vers DD/MM/YYYY)
        const formatDate = (dateString: string) => {
            if (!dateString) return '-';
            const date = new Date(dateString);
            return date.toLocaleDateString('fr-FR');
        };

        // Chargement initial
        onMounted(() => {
            trackerStore.fetchVisits();
        });

        // N'oublie pas d'exposer tes variables et fonctions pour le template
        return {
            trackerStore,
            filters,
            totalPages,
            applyFilters,
            resetFilters,
            changePage,
            formatDate
        };
    }
};
</script>

<style scoped>
.admin-tracker-container {
    padding: 2rem;
    color: #1f2937;
    font-family: 'Inter', sans-serif;
}

.header-section {
    margin-bottom: 2rem;
}
.header-section h2 {
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.header-section p {
    color: #6b7280;
}

/* 🎛 Filtres */
.filters-card {
    background: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    display: flex;
    gap: 1.5rem;
    align-items: flex-end;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
    min-width: 200px;
}
.filter-group label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #4b5563;
}
.filter-input {
    padding: 0.6rem 1rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.2s;
}
.filter-input:focus {
    border-color: #3b82f6;
}
.filter-actions {
    display: flex;
    gap: 1rem;
}
.btn-submit {
    background: #3b82f6;
    color: white;
    padding: 0.6rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
}
.btn-reset {
    background: transparent;
    color: #6b7280;
    padding: 0.6rem 1rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    cursor: pointer;
}

/* 📊 Tableau */
.table-card {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    overflow: hidden;
}
.admin-table {
    width: 100%;
    border-collapse: collapse;
}
.admin-table th {
    background: #f9fafb;
    padding: 1rem;
    text-align: left;
    font-size: 0.85rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #e5e7eb;
}
.admin-table td {
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;
    font-size: 0.95rem;
}
.country-badge {
    background: #f3f4f6;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 500;
}
.visits-count {
    font-weight: 600;
    color: #111827;
}
.empty-state {
    text-align: center;
    color: #6b7280;
    padding: 3rem !important;
}

/* 🧭 Pagination */
.pagination-section {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 1.5rem;
    margin-top: 1.5rem;
}
.page-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #d1d5db;
    background: #ffffff;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}
.page-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
.page-btn:not(:disabled):hover {
    background: #f3f4f6;
}
.page-info {
    font-size: 0.9rem;
    color: #4b5563;
}
</style>