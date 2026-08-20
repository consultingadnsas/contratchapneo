import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';
import type { Order, OrderItem } from './orderStore';

// --- INTERFACES DES TRANSACTIONS ---
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

// --- INTERFACES DE LA COMPTABILITÉ (Basé sur notre vue Django) ---
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
}

export const useAdminTransactStore = defineStore('adminTransac', () => {
    
    const { $api } = useNuxtApp();

    // --- STATE ---
    const transactions = ref<Transaction[]>([]);
    const accountancy = ref<AccountingSummary | null>(null); // 🌟 Nouvel état pour la compta
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    // --- ACTIONS ---

    // 1. Récupérer les transactions (Déjà parfait)
    async function fetchTransact() {
        isLoading.value = true;
        error.value = null;

        try {
            let allTransactions: Transaction[] = [];
            let currentEndpoint: string | null = '/payments/admin/'; // Vérifie bien ton URL

            while (currentEndpoint) {
                const response = await $api<any>(currentEndpoint, { method: 'GET' });

                if (response && response.results) {
                    allTransactions = [...allTransactions, ...response.results];
                    
                    if (response.next) {
                        const url = new URL(response.next);
                        currentEndpoint = url.pathname + url.search;
                    } else {
                        currentEndpoint = null;
                    }
                } else {
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

    // 2. Récupérer le rapport comptable (COMPLÉTÉ)
    async function fetchAccountancy() {
        isLoading.value = true;
        error.value = null;

        try {
            // 🌟 On appelle la route Django créée précédemment. 
            // Vérifie que l'URL correspond exactement à ce que tu as dans ton urls.py côté Django.
            const response = await $api<AccountingSummary>('/payments/admin/accounting/', { 
                method: 'GET' 
            });

            // On stocke la réponse dans notre état
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
        accountancy, // 🌟 Ne pas oublier de l'exporter
        isLoading,
        error,
        // Actions
        fetchTransact,
        fetchAccountancy // 🌟 Ne pas oublier de l'exporter
    };
});