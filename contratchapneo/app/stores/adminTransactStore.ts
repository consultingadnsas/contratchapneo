import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';
import type { Order } from './orderStore';

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

export const useAdminTransactStore = defineStore('adminTransac', () => {
    
    const { $api } = useNuxtApp();

    // --- STATE ---
    const transactions = ref<Transaction[]>([]); // 🚨 Ajout de la liste des transactions
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    // --- ACTIONS ---
    async function fetchTransact() {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api<any>('/payments/admin/', {
                method: 'GET'
            });

            // 💡 On gère la pagination DRF (response.results) ou un tableau direct (response.data ou response)
            if (response) {
                transactions.value = response.results || response.data || response || [];
            }
            
        } catch (err: any) {
            error.value = err.message || "Une erreur est survenue lors de la récupération des transactions.";
            console.error("Erreur fetchTransact:", err);
        } finally {
            isLoading.value = false;
        }
    }

    return {
        transactions, // Ne pas oublier de l'exporter !
        isLoading,
        error,
        fetchTransact
    };
});