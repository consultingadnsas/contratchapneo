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
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="adminStore.isLoading">
                        <td colspan="5" style="text-align: center;">Récupération des données...</td>
                    </tr>
                    <tr v-else-if="adminStore.calculations.length === 0">
                        <td colspan="5" style="text-align: center;">Aucune simulation trouvée.</td>
                    </tr>
                    <tr v-else v-for="calc in adminStore.calculations" :key="calc.id">
                        <!-- Date -->
                        <td>{{ formatDate(calc.created_at) }}</td>
                        
                        <!-- ⚡️ CORRECTION : On utilise calc.email, car c'est le champ exact de ton modèle -->
                        <td>
                            <strong>{{ calc.email || 'Anonyme' }}</strong>
                        </td>
                        
                        <!-- Informations RH -->
                        <td>
                            {{ calc.type_contrat }} <br>
                            <span class="sub-text">{{ calc.motif_rupture }}</span>
                        </td>
                        
                        <!-- Salaire de Base (champ exact du modèle) -->
                        <td>{{ formatCurrency(calc.salaire_base) }}</td>
                        
                        <!-- ⚡️ CORRECTION : On utilise le nouveau champ dynamique du sérialiseur -->
                        <td class="highlight-amount">
                            <span v-if="calc.resultats_financiers">
                                {{ formatCurrency(calc.resultats_financiers.total_droits) }}
                            </span>
                            <span v-else>Non calculable</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useAdminCalculStore } from '../../../stores/adminCalculStore';

export default defineComponent({
    name: 'AdminCalculList',
    setup() {
        const adminStore = useAdminCalculStore();

        const loadData = () => {
            adminStore.fetchAllCalculations();
        };

        const formatCurrency = (value: number) => {
            if (!value) return '0 FCFA';
            return new Intl.NumberFormat('fr-FR').format(Math.round(value)) + ' FCFA';
        };

        const formatDate = (dateString: string) => {
            if (!dateString) return '-';
            return new Date(dateString).toLocaleDateString('fr-FR', {
                day: '2-digit', month: 'short', year: 'numeric',
                hour: '2-digit', minute: '2-digit'
            });
        };

        onMounted(() => {
            loadData();
        });

        return { adminStore, loadData, formatCurrency, formatDate };
    }
});
</script>

<style scoped>
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

.btn-action {
    background: #e2e8f0;
    border: none;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    font-size: 0.85rem;
    cursor: pointer;
    color: #0f172a;
}
.btn-action:hover { background: #cbd5e1; }
.error-msg { color: #ef4444; font-weight: 500; }
</style>