import { defineStore } from 'pinia';
import { ref } from 'vue';

// L'interface correspond exactement à ton DailyVisitSerializer
export interface DailyVisit {
    id: number | string;
    date: string;
    country: string;
    visits: number;
}

export const useAdminTrackerStore = defineStore('adminTracker', () => {
    const { $api } = useNuxtApp();

    // --- STATE ---
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    const visits = ref<DailyVisit[]>([]);
    
    // Outils de pagination correspondant à AdminCartPagination
    const currentPage = ref(1);
    const totalCount = ref(0);

    // ==========================================
    // ACTIONS
    // ==========================================
    
    // Récupération de la liste filtrée
    const fetchVisits = async (
        page: number = 1, 
        filters: { country?: string; start_date?: string; end_date?: string } = {}
    ) => {
        isLoading.value = true;
        error.value = null;
        try {
            // Construction dynamique de l'URL avec les filtres définis dans AdminDailyVisitView
            const params = new URLSearchParams();
            params.append('page', page.toString());
            
            if (filters.country) params.append('country', filters.country.trim());
            if (filters.start_date) params.append('start_date', filters.start_date);
            if (filters.end_date) params.append('end_date', filters.end_date);

            // Adapte le préfixe `/stats/` si ton ROOT_URLCONF utilise un autre chemin
            const url = `/stats/admin/visitors/?${params.toString()}`;

            const response = await $api<any>(url, { method: 'GET' });
            
            if (response) {
                // Gestion de la pagination (results/count)
                visits.value = response.results || response.data || response;
                totalCount.value = response.count || 0;
                currentPage.value = page;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des visites.";
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    };

    return {
        isLoading,
        error,
        visits,
        currentPage,
        totalCount,
        fetchVisits
    };
});