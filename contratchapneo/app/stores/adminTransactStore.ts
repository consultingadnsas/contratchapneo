import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';
import type { Order, OrderItem } from './orderStore';

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

    const transactions = ref<Transaction[]>([]);
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    // --- ACTIONS ---
    async function fetchTransact() {
        isLoading.value = true;
        error.value = null;

        try {
            let allTransactions: Transaction[] = [];
            
            // ⚡️ On commence par la première page
            let currentEndpoint: string | null = '/payments/admin/';

            // ⚡️ Tant qu'il y a une page suivante (next), on continue de boucler
            while (currentEndpoint) {
                const response = await $api<any>(currentEndpoint, { method: 'GET' });

                if (response && response.results) {
                    // C'est une réponse paginée de Django
                    allTransactions = [...allTransactions, ...response.results];
                    
                    // Si Django renvoie une URL absolue (http://localhost:8000/api/...), 
                    // on nettoie l'URL pour ne garder que le chemin relatif pour notre $api Nuxt
                    if (response.next) {
                        const url = new URL(response.next);
                        currentEndpoint = url.pathname + url.search; // ex: /api/payments/admin/?page=2
                    } else {
                        currentEndpoint = null; // Plus de page, on arrête la boucle
                    }
                } else {
                    // Si le backend n'a finalement pas activé la pagination
                    allTransactions = response?.data || response || [];
                    currentEndpoint = null;
                }
            }

            transactions.value = allTransactions;
            
        } catch (err: any) {
            error.value = err.message || "Une erreur est survenue lors de la récupération des transactions.";
            console.error("Erreur fetchTransact:", err);
        } finally {
            isLoading.value = false;
        }
    }

    return {
        transactions,
        isLoading,
        error,
        fetchTransact
    };
});