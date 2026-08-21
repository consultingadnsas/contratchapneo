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

    // --- GETTERS (POUR LES GRAPHIQUES ADMINFINANCE) ---

    // 1. Courbe des revenus (Donnée globale via Django)
    const computedMonthlyRevenue = computed(() => {
        const months = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        if (accountancy.value?.monthly_evolution) {
            accountancy.value.monthly_evolution.forEach(item => {
                const dateObj = new Date(item.month);
                if (!isNaN(dateObj.getTime())) {
                    months[dateObj.getMonth()] += Number(item.monthly_total || 0);
                }
            });
        }
        return months;
    });

    // 2. Demandes : Sur-mesure vs Révisions (Sur les transactions chargées)
    const demandStats = computed(() => {
        const customContracts = [0,0,0,0,0,0,0,0,0,0,0,0];
        const revisions = [0,0,0,0,0,0,0,0,0,0,0,0];
        (transactions.value || []).forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const dateStr = tx.created_at || tx.order?.created_at;
                if (dateStr && !isNaN(new Date(dateStr).getTime())) {
                    const monthIndex = new Date(dateStr).getMonth();
                    const items = tx.order?.order_items || tx.order_items || [];
                    items.forEach((item: any) => {
                        if (item.customised_contract || item.contrat_customed) customContracts[monthIndex] += (item.quantity || 1);
                        if (item.revision_subject || item.contract_revision) revisions[monthIndex] += (item.quantity || 1);
                    });
                }
            }
        });
        return { customContracts, revisions };
    });

    // 3. Ventes de Packs (Sur les transactions chargées)
    const packStats = computed(() => {
        const counts = [0,0,0,0,0,0,0,0,0,0,0,0];
        (transactions.value || []).forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const dateStr = tx.created_at || tx.order?.created_at;
                if (dateStr && !isNaN(new Date(dateStr).getTime())) {
                    const monthIndex = new Date(dateStr).getMonth();
                    const items = tx.order?.order_items || tx.order_items || [];
                    items.forEach((item: any) => {
                        if (item.pack || item.pack_title) counts[monthIndex] += (item.quantity || 1);
                    });
                }
            }
        });
        return counts;
    });

    // 4. Sollicitations Pros (Sur les transactions chargées)
    const proStats = computed(() => {
        const counts = [0,0,0,0,0,0,0,0,0,0,0,0];
        (transactions.value || []).forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const dateStr = tx.created_at || tx.order?.created_at;
                if (dateStr && !isNaN(new Date(dateStr).getTime())) {
                    const monthIndex = new Date(dateStr).getMonth();
                    const items = tx.order?.order_items || tx.order_items || [];
                    items.forEach((item: any) => {
                        if (item.pro || item.pro_name) counts[monthIndex] += (item.quantity || 1);
                    });
                }
            }
        });
        return counts;
    });

    // 5. Palmarès Contrats
    const topContractsStats = computed(() => {
        const counts: Record<string, number> = {};
        (transactions.value || []).forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const items = tx.order?.order_items || tx.order_items || [];
                items.forEach((item: any) => {
                    const designation = item.designation || item.contrat_title || '';
                    if (designation.includes('Contrat') || item.contrat) {
                        const cleanName = designation.replace('Contrat :', '').trim();
                        if (cleanName) counts[cleanName] = (counts[cleanName] || 0) + (item.quantity || 1);
                    }
                });
            }
        });
        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
        return { labels: sorted.map(s => s[0]), data: sorted.map(s => s[1]) };
    });

    // 6. Palmarès Packs
    const topPacksStats = computed(() => {
        const counts: Record<string, number> = {};
        (transactions.value || []).forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const items = tx.order?.order_items || tx.order_items || [];
                items.forEach((item: any) => {
                    const designation = item.designation || '';
                    const packTitle = item.pack_title || (designation.includes('Pack') ? designation.replace('Pack :', '').trim() : null);
                    if (packTitle) counts[packTitle] = (counts[packTitle] || 0) + (item.quantity || 1);
                });
            }
        });
        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
        return { labels: sorted.map(s => s[0]), data: sorted.map(s => s[1]) };
    });

    // 7. Palmarès Pros
    const topProsStats = computed(() => {
        const counts: Record<string, number> = {};
        (transactions.value || []).forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const items = tx.order?.order_items || tx.order_items || [];
                items.forEach((item: any) => {
                    const designation = item.designation || '';
                    const proName = item.pro_name || (designation.includes('Carte Expert') ? designation.replace('Carte Expert :', '').trim() : null);
                    if (proName) counts[proName] = (counts[proName] || 0) + (item.quantity || 1);
                });
            }
        });
        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
        return { labels: sorted.map(s => s[0]), data: sorted.map(s => s[1]) };
    });

    return {
        // State
        transactions, accountancy, isLoading, error, totalCount, currentPage,
        // Getters pour les graphes
        computedMonthlyRevenue, demandStats, packStats, proStats, topContractsStats, topPacksStats, topProsStats,
        // Actions
        fetchTransact, fetchAccountancy
    };
});