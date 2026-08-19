import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// ==========================================
// INTERFACES (Basées sur AccountingOrderSerializer)
// ==========================================

export interface AccountingOrderItem {
    designation: string;
    quantity: number;
    unit_price: string | number;
    subtotal: string | number;
}

export interface AccountingOrder {
    id: string;
    date_transaction: string;
    status: string;
    status_label: string;
    client_name: string;
    client_email: string;
    total_amount: string | number;
    discount_amount: string | number;
    coupon_used: string | null;
    lignes_achat: AccountingOrderItem[];
}

// ==========================================
// STORE
// ==========================================
export const useAdminFinanceStore = defineStore('adminFinance', () => {

    const { $api } = useNuxtApp();

    // --- STATE ---
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    const transactions = ref<AccountingOrder[]>([]);

    // --- GETTERS (Statistiques pour le Dashboard) ---
    
    // 1. Chiffre d'affaires total (uniquement les commandes payées)
    const totalRevenue = computed(() => {
        return transactions.value
            .filter(order => order.status?.toLowerCase() === 'paid' || order.status_label === 'Payé')
            .reduce((sum, order) => sum + Number(order.total_amount || 0), 0);
    });

    // 2. Nombre de ventes réussies
    const totalSalesCount = computed(() => {
        return transactions.value
            .filter(order => order.status?.toLowerCase() === 'paid' || order.status_label === 'Payé').length;
    });

    // 3. Commandes en attente (pour relancer les clients si besoin)
    const pendingOrdersCount = computed(() => {
        return transactions.value
            .filter(order => order.status?.toLowerCase() === 'pending' || order.status_label === 'En attente de paiement').length;
    });
    // --- ACTIONS ---

    const fetchTransactions = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            // ⚠️ Ajuste le préfixe si nécessaire (ex: /order/admin/accountancy/ selon ton urls.py principal)
            const response = await $api<any>('/ecommerce/admin/accountancy/', { 
                method: 'GET' 
            });
            
            if (response) {
                const responseData = response.data ? response.data : response;

                // ⚡️ CORRECTION : Gestion de la pagination Django
                if (responseData.results) {
                    // Si paginé (objet avec count, next, previous, results)
                    transactions.value = responseData.results;
                } else if (Array.isArray(responseData)) {
                    // Si non-paginé (tableau direct)
                    transactions.value = responseData;
                } else {
                    transactions.value = [];
                }
                
                console.log("Transactions chargées :", transactions.value);
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des données financières";
            console.error("Erreur Finance:", err);
        } finally {
            isLoading.value = false;
        }
    };

    return {
        // State
        isLoading,
        error,
        transactions,
        
        // Getters
        totalRevenue,
        totalSalesCount,
        pendingOrdersCount,
        
        // Actions
        fetchTransactions
    };
});