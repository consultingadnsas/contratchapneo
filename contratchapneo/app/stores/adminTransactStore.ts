import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useNuxtApp } from '#app';
import type { Order } from './orderStore';

// --- INTERFACES ---
export interface Transaction {
    id: string;
    order: Order;
    amount: number;
    status: string;
    status_labels: string;
    payment_method: string;
    provider_reference: string;
    error_message: string;
    created_at: string;
}

export interface AccountingSummary {
    global: { total_revenue: number; };
    transactions_status: { successful: number; pending: number; failed: number; canceled: number; };
    revenue_by_method: Array<{ payment_method: string; total_revenue: number; transaction_count: number; }>;
    monthly_evolution: Array<{ month: string; monthly_total: number; count: number; }>;
    custom_contracts_monthly: Array<{ month: string; count: number; }>;
    revisions_monthly: Array<{ month: string; count: number; }>;
    
    // ⚡️ NOUVEAU : Ajout officiel pour éviter les erreurs TypeScript
    packs_monthly: Array<{ month: string; count: number; }>;
    pros_monthly: Array<{ month: string; count: number; }>;
    
    top_contracts: Array<{ contrat__title: string; total_sold: number; }>;
    top_packs: Array<{ pack__title: string; total_sold: number; }>;
    top_pros: Array<{ name: string; total_sold: number; }>;
}

export const useAdminTransactStore = defineStore('adminTransac', () => {

    const { $api } = useNuxtApp();

    // --- STATE ---
    const transactions = ref<Transaction[]>([]);
    const accountancy = ref<AccountingSummary | null>(null);
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    const totalCount = ref<number>(0);
    const currentPage = ref<number>(1);

    // --- ACTIONS ---
    async function fetchTransact(page: number = 1, tab: string = 'models', search: string = '') {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<any>('/payments/admin/', {
                method: 'GET',
                params: { page, tab, search }
            });
            if (response && response.results) {
                transactions.value = response.results;
                totalCount.value = response.count || 0;
                currentPage.value = page;
            } else {
                transactions.value = response?.data || response || [];
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des transactions.";
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    }

    async function fetchAccountancy() {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<AccountingSummary>('/payments/admin/accounting/', { method: 'GET' });
            accountancy.value = response;
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération de la comptabilité.";
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    }

    // --- ⚡️ HELPER INTERNE ---
    const mapMonthlyData = (dataArray: Array<any> | undefined, valueKey: string = 'count') => {
        const months = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        if (!dataArray) return months;
        dataArray.forEach(item => {
            const date = new Date(item.month);
            if (!isNaN(date.getTime())) {
                months[date.getMonth()] += Number(item[valueKey] || 0);
            }
        });
        return months;
    };

    // --- ⚡️ GETTERS POUR LES GRAPHIQUES ---
    const computedMonthlyRevenue = computed(() => mapMonthlyData(accountancy.value?.monthly_evolution, 'monthly_total'));
    
    const demandStats = computed(() => ({
        customContracts: mapMonthlyData(accountancy.value?.custom_contracts_monthly),
        revisions: mapMonthlyData(accountancy.value?.revisions_monthly)
    }));

    const packStats = computed(() => mapMonthlyData(accountancy.value?.packs_monthly));
    const proStats = computed(() => mapMonthlyData(accountancy.value?.pros_monthly));

    const topContractsStats = computed(() => {
        const raw = accountancy.value?.top_contracts || [];
        return { 
            labels: raw.map(c => c.contrat__title || 'Inconnu'), 
            data: raw.map(c => c.total_sold || 0) 
        };
    });

    const topPacksStats = computed(() => {
        const raw = accountancy.value?.top_packs || [];
        return { 
            labels: raw.map(p => p.pack__title || 'Inconnu'), 
            data: raw.map(p => p.total_sold || 0) 
        };
    });

    const topProsStats = computed(() => {
        const raw = accountancy.value?.top_pros || [];
        return { 
            labels: raw.map(p => p.name || 'Inconnu'), 
            data: raw.map(p => p.total_sold || 0) 
        };
    });

    return {
        // State
        transactions, accountancy, isLoading, error, totalCount, currentPage,
        
        // Getters exposés
        computedMonthlyRevenue, demandStats, packStats, proStats, 
        topContractsStats, topPacksStats, topProsStats,
        
        // Actions
        fetchTransact, fetchAccountancy
    };
});