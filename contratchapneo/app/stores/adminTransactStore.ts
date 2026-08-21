import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';
import type { Order } from './orderStore';

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
    // ⚡️ TRADUCTEUR POUR LE GRAPHIQUE
    // Transforme { month: "2026-08-01", monthly_total: 150000 } en [0, 0, 0, 0, 0, 0, 0, 150000, 0, 0, 0, 0]
    const computedMonthlyRevenue = computed(() => {
        const months = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        
        if (accountancy.value && accountancy.value.monthly_evolution) {
            accountancy.value.monthly_evolution.forEach(item => {
                // On transforme la chaîne de caractères (ex: "2026-10-01") en date Javascript
                const dateObj = new Date(item.month);
                
                // On s'assure que la date est valide
                if (!isNaN(dateObj.getTime())) {
                    const monthIndex = dateObj.getMonth(); // Janvier = 0, Février = 1... Décembre = 11
                    months[monthIndex] += Number(item.monthly_total || 0);
                }
            });
        }
        
        return months;
    });

    // ⚡️ CALCUL DE LA DEMANDE : Sur-mesure vs Révisions
    const demandStats = computed(() => {
        // Tableaux pour stocker les quantités vendues sur 12 mois
        const customContracts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        const revisions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

        const orderList = transactions.value || [];

        orderList.forEach((tx: any) => {
            // On ne compte que les ventes réussies
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                
                // Récupération du mois de la transaction
                const dateStr = tx.created_at || (tx.order && tx.order.created_at);
                if (dateStr) {
                    const dateObj = new Date(dateStr);
                    if (!isNaN(dateObj.getTime())) {
                        const monthIndex = dateObj.getMonth();

                        // On parcourt les articles de la commande
                        const items = tx.order?.order_items || [];
                        items.forEach((item: any) => {
                            // On vérifie si c'est un contrat sur-mesure
                            if (item.contrat_customed || item.customised_contract) {
                                customContracts[monthIndex] += (item.quantity || 1);
                            }
                            // On vérifie si c'est une révision
                            if (item.contract_revision || item.revision_subject) {
                                revisions[monthIndex] += (item.quantity || 1);
                            }
                        });
                    }
                }
            }
        });

        return { customContracts, revisions };
    });

    // ⚡️ CALCUL : Demande des Packs
    const packStats = computed(() => {
        const counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        const orderList = transactions.value || [];

        orderList.forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const dateStr = tx.created_at || (tx.order && tx.order.created_at);
                if (dateStr) {
                    const dateObj = new Date(dateStr);
                    if (!isNaN(dateObj.getTime())) {
                        const monthIndex = dateObj.getMonth();
                        const items = tx.order?.order_items || tx.order_items || tx.order?.lignes_achat || [];
                        
                        items.forEach((item: any) => {
                            // Détection des Packs
                            if (item.pack || item.pack_title) {
                                counts[monthIndex] += (item.quantity || 1);
                            }
                        });
                    }
                }
            }
        });
        return counts;
    });

    // ⚡️ CALCUL : Demande des Professionnels (Pros)
    const proStats = computed(() => {
        const counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        const orderList = transactions.value || [];

        orderList.forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const dateStr = tx.created_at || (tx.order && tx.order.created_at);
                if (dateStr) {
                    const dateObj = new Date(dateStr);
                    if (!isNaN(dateObj.getTime())) {
                        const monthIndex = dateObj.getMonth();
                        const items = tx.order?.order_items || tx.order_items || tx.order?.lignes_achat || [];
                        
                        items.forEach((item: any) => {
                            // Détection des Pros (Avocats, Notaires, etc.)
                            if (item.pro || item.pro_name) {
                                counts[monthIndex] += (item.quantity || 1);
                            }
                        });
                    }
                }
            }
        });
        return counts;
    });
    // ⚡️ CALCUL : Top 5 des contrats les plus populaires
    const topContractsStats = computed(() => {
        const contractCounts: Record<string, number> = {};
        const orderList = transactions.value || [];

        orderList.forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const items = tx.order?.order_items || tx.order_items || tx.order?.lignes_achat || [];
                
                items.forEach((item: any) => {
                    const designation = item.designation || item.contrat_title || '';
                    
                    // On cible uniquement les contrats standards (pas les packs ni le sur-mesure)
                    if (designation.includes('Contrat') || item.contrat) {
                        // On nettoie le titre pour l'affichage (enlève le préfixe "Contrat : " si présent)
                        const cleanName = designation.replace('Contrat :', '').trim();
                        if (cleanName) {
                            contractCounts[cleanName] = (contractCounts[cleanName] || 0) + (item.quantity || 1);
                        }
                    }
                });
            }
        });

        // Tri décroissant et sélection des 5 premiers
        const sorted = Object.entries(contractCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);

        return {
            labels: sorted.map(s => s[0]), // Les noms des contrats
            data: sorted.map(s => s[1])    // Les quantités vendues
        };
    });

    // ⚡️ CALCUL : Top 5 des Packs les plus vendus
    const topPacksStats = computed(() => {
        const counts: Record<string, number> = {};
        const orderList = transactions.value || [];

        orderList.forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const items = tx.order?.order_items || tx.order_items || tx.order?.lignes_achat || [];
                
                items.forEach((item: any) => {
                    const designation = item.designation || '';
                    const packTitle = item.pack_title || (designation.includes('Pack') ? designation.replace('Pack :', '').trim() : null);
                    
                    if (packTitle) {
                        counts[packTitle] = (counts[packTitle] || 0) + (item.quantity || 1);
                    }
                });
            }
        });

        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
        return { labels: sorted.map(s => s[0]), data: sorted.map(s => s[1]) };
    });

    // ⚡️ CALCUL : Top 5 des Pros les plus sollicités
    const topProsStats = computed(() => {
        const counts: Record<string, number> = {};
        const orderList = transactions.value || [];

        orderList.forEach((tx: any) => {
            const status = tx.status?.toLowerCase() || '';
            if (status === 'paid' || status === 'successful') {
                const items = tx.order?.order_items || tx.order_items || tx.order?.lignes_achat || [];
                
                items.forEach((item: any) => {
                    const designation = item.designation || '';
                    const proName = item.pro_name || (designation.includes('Carte Expert') ? designation.replace('Carte Expert :', '').trim() : null);
                    
                    if (proName) {
                        counts[proName] = (counts[proName] || 0) + (item.quantity || 1);
                    }
                });
            }
        });

        const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
        return { labels: sorted.map(s => s[0]), data: sorted.map(s => s[1]) };
    });

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
