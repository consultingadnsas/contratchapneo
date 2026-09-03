<template>
    <div class="admin-panel-wrapper">
        <div class="panel-header">
            <h2>Historique des Simulations de Droits</h2>
            <button class="btn-refresh" @click="loadData" :disabled="adminStore.isLoading">
                {{ adminStore.isLoading ? 'Chargement...' : 'Actualiser' }}
            </button>
        </div>

        <p v-if="adminStore.error" class="error-msg">{{ adminStore.error }}</p>

        <div class="table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Email</th>
                        <th>Type de Contrat</th>
                        <th>Salaire Brut Moyen</th>
                        <th>Total Droits Estimés</th>
                        <th>Détails</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="adminStore.isLoading">
                        <td colspan="6" style="text-align: center;">Récupération des données...</td>
                    </tr>
                    <tr v-else-if="adminStore.calculations.length === 0">
                        <td colspan="6" style="text-align: center;">Aucune simulation trouvée.</td>
                    </tr>
                    <tr v-else v-for="calc in adminStore.calculations" :key="calc.id">
                        <td>{{ formatDate(calc.created_at) }}</td>
                        <td><strong>{{ calc.email || 'Anonyme' }}</strong></td>
                        <td>
                            {{ calc.type_contrat }} <br>
                            <span class="sub-text">{{ calc.motif_rupture }}</span>
                        </td>
                        <td>{{ formatCurrency(calc.salaire_base) }}</td>
                        <td class="highlight-amount">
                            <span v-if="calc.resultats_financiers">
                                {{ formatCurrency(calc.resultats_financiers.total_droits) }}
                            </span>
                            <span v-else>Non calculable</span>
                        </td>
                        <!-- Bouton Action (Oeil) -->
                        <td>
                            <button class="btn-icon" @click="openDetails(calc)" title="Voir les détails">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-eye">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                </svg>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modale de détails -->
        <div v-if="isModalOpen" class="modal-overlay" @click.self="closeDetails">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Détails de la simulation</h3>
                    <button class="btn-close" @click="closeDetails">✕</button>
                </div>
                <div class="modal-body" v-if="selectedCalc">
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="label">Date Embauche</span>
                            <span class="value">{{ formatDate(selectedCalc.date_embauche) }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">Date Rupture</span>
                            <span class="value">{{ formatDate(selectedCalc.date_rupture) }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">Préavis Effectué ?</span>
                            <span class="value">{{ selectedCalc.preavis_effectue ? 'Oui' : 'Non' }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">Congés Restants</span>
                            <span class="value">{{ selectedCalc.jours_conges_restants || 0 }} jours</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">Salaire de base</span>
                            <span class="value">{{ formatCurrency(selectedCalc.salaire_base) }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">Variables incluses</span>
                            <span class="value">{{ formatCurrency(selectedCalc.moyenne_variables) }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useAdminCalculStore } from '../../../stores/adminCalculStore';

export default defineComponent({
    name: 'AdminCalculList',
    setup() {
        const adminStore = useAdminCalculStore();
        
        // État pour la modale
        const isModalOpen = ref(false);
        const selectedCalc = ref<any>(null);

        const loadData = () => {
            adminStore.fetchAllCalculations();
        };

        const openDetails = (calc: any) => {
            selectedCalc.value = calc;
            isModalOpen.value = true;
        };

        const closeDetails = () => {
            isModalOpen.value = false;
            selectedCalc.value = null;
        };

        const formatCurrency = (value: number) => {
            if (!value) return '0 FCFA';
            return new Intl.NumberFormat('fr-FR').format(Math.round(value)) + ' FCFA';
        };

        const formatDate = (dateString: string) => {
            if (!dateString) return '-';
            return new Date(dateString).toLocaleDateString('fr-FR', {
                day: '2-digit', month: 'short', year: 'numeric'
            });
        };

        onMounted(() => {
            loadData();
        });

        return { 
            adminStore, 
            loadData, 
            formatCurrency, 
            formatDate,
            isModalOpen,
            selectedCalc,
            openDetails,
            closeDetails
        };
    }
});
</script>

<style scoped>
/* Tes styles existants */
.admin-panel-wrapper {
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.panel-header h2 {
    font-size: 1.5rem;
    color: #1f2937;
    margin: 0;
}

.btn-refresh {
    background: #0f172a;
    color: #ffffff;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}

.btn-refresh:disabled { opacity: 0.7; cursor: not-allowed; }

.table-container {
    overflow-x: auto;
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.admin-table th, .admin-table td {
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;
}

.admin-table th {
    background: #f1f5f9;
    font-size: 0.85rem;
    text-transform: uppercase;
    color: #475569;
}

.sub-text {
    font-size: 0.8rem;
    color: #64748b;
}

.highlight-amount {
    font-weight: 700;
    color: #10b981;
}

/* Nouveaux styles pour le bouton icône et la modale */
.btn-icon {
    background: transparent;
    border: none;
    cursor: pointer;
    color: #3b82f6;
    padding: 0.4rem;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}
.btn-icon:hover {
    background: #eff6ff;
}
.icon-eye {
    width: 20px;
    height: 20px;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: #ffffff;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    padding: 1.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.modal-header h3 {
    margin: 0;
    font-size: 1.25rem;
    color: #1f2937;
}

.btn-close {
    background: transparent;
    border: none;
    margin: -10rem;
    font-size: 1.5rem;
    cursor: pointer;
    color: #6b7280;
}

.btn-close:hover{
    color: #ef4444;
}

.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.detail-item {
    display: flex;
    flex-direction: column;
}

.detail-item .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.detail-item .value {
    font-size: 0.95rem;
    color: #0f172a;
    font-weight: 500;
}
</style>