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
    global: {
        total_revenue: number;
    };
    transactions_status: {
        successful: number;
        pending: number;
        failed: number;
        canceled: number;
    };
    revenue_by_method: Array<{
        payment_method: string;
        total_revenue: number;
        transaction_count: number;
    }>;
    monthly_evolution: Array<{
        month: string; // La date formatée renvoyée par Django
        monthly_total: number;
        count: number;
    }>;
    custom_contracts_monthly: Array<{
        month: string;
        count: number;
    }>;
    revisions_monthly: Array<{
        month: string;
        count: number;
    }>;
    top_contracts: Array<{
        contrat__title: string;
        total_sold: number;
    }>;
    top_packs: Array<{
        pack__title: string;
        total_sold: number;
    }>;
    top_pros: Array<{
        name: string;
        total_sold: number;
    }>;
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

    return {
        // State
        transactions, accountancy, isLoading, error, totalCount, currentPage,
        // Getters pour les graphes
        computedMonthlyRevenue, demandStats, packStats, proStats, topContractsStats, topPacksStats, topProsStats,
        // Actions
        fetchTransact, fetchAccountancy
    };
});