import { defineStore } from 'pinia';

export const useAdminOrderStore = defineStore('adminOrder', {
  state: () => ({
    orders: [] as Order[],
    abandonedOrders: [] as Order[],
    totalAbandonedCount: 0, // 👈 Nouveau : pour le Paginator
    isLoading: false,
    error: null as string | null,
  }),

  actions: {
    // 👈 Nouveau : Accepte la page en paramètre (par défaut 1)
    async fetchAbandonedOrders(page: number = 1) { 
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp();

      try {
        // 👈 Nouveau : Ajout de &page= au lien
        const response: any = await $api(`/ecommerce/admin/order/?abandoned=true&page=${page}`, {
          method: 'GET'
        });
        
        // Django renvoie { count: X, next: '...', previous: '...', results: [...] }
        if (response && Array.isArray(response.results)) {
            this.abandonedOrders = response.results;
            this.totalAbandonedCount = response.count || response.results.length;
        } else if (response && Array.isArray(response.data)) {
            this.abandonedOrders = response.data;
            this.totalAbandonedCount = response.count || response.data.length;
        } else if (Array.isArray(response)) {
            this.abandonedOrders = response;
            this.totalAbandonedCount = response.length;
        } else {
            this.abandonedOrders = [];
            this.totalAbandonedCount = 0;
        }
      } catch (err: any) {
        console.error("Erreur lors de la récupération des abandons :", err);
        this.error = err.response?._data?.message || "Impossible de récupérer les paniers abandonnés.";
      } finally {
        this.isLoading = false;
      }
    },
  },
  
  getters: {
    totalAbandoned: (state) => state.abandonedOrders.length,
  }
});