import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';
import type { Order } from './orderStore';

// --- INTERFACES ---
// (Garde tes interfaces Transaction et AccountingSummary telles quelles, elles sont parfaites)

export const useAdminTransactStore = defineStore('adminTransac', () => {

    const { $api } = useNuxtApp();

    // --- STATE ---
    const transactions = ref<Transaction[]>([]);
    const accountancy = ref<AccountingSummary | null>(null);
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    // 🌟 NOUVEAU : État pour gérer la pagination
    const totalCount = ref<number>(0);
    const currentPage = ref<number>(1);

    // --- ACTIONS ---

    // 1. Récupérer les transactions (Une seule page à la fois)
    async function fetchTransact(page: number = 1, tab: string = 'models', search: string = '') {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api<any>('/payments/admin/', {
                method: 'GET',
                params: { page, tab, search } // ⚡️ Envoi des filtres à Django
            });

            if (response && response.results) {
                transactions.value = response.results;
                totalCount.value = response.count || 0;
                currentPage.value = page;
            } else {
                transactions.value = response?.data || response || [];
            }
        } catch (err: any) {
            error.value = err.message || "Une erreur est survenue lors de la récupération des rapports comptables.";
            console.error("Erreur fetchAccountancy:", err);
        } finally {
          isLoading.value = false;
        }
    }

    // 2. Récupérer le rapport comptable (Inchangé)
    async function fetchAccountancy() {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api<AccountingSummary>('/payments/admin/accounting/', {
                method: 'GET'
            });
            accountancy.value = response;
        } catch (err: any) {
            error.value = err.message || "Une erreur est survenue lors de la récupération des rapports comptables.";
            console.error("Erreur fetchAccountancy:", err);
        } finally {
            isLoading.value = false;
        }
    }

    // --- RETURN ---
    return {
        // State
        transactions,
        accountancy,
        isLoading,
        error,
        totalCount,    // 🌟 Exporté pour le frontend
        currentPage,   // 🌟 Exporté pour le frontend

        // Actions
        fetchTransact,
        fetchAccountancy
    };
});
