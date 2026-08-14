import { defineStore } from 'pinia';

interface Order {
  id: string;
  status: string;
  status_label: string;
  total_amount: number;
  buyer_email?: string;
  client_email?: string; // Plan B
  created_at?: string;
  date_transaction?: string; // Plan B
  order_items: any[];
}

export const useAdminOrderStore = defineStore('adminOrder', {
  state: () => ({
    orders: [] as Order[],
    abandonedOrders: [] as Order[],
    isLoading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchAbandonedOrders() {
      this.isLoading = true;
      this.error = null;
      try {
        // ⚡️ CORRECTION ICI : On utilise la route principale avec le paramètre
        const response: any = await $fetch('http://localhost:8000/admin/order/?abandoned=true', {
             headers: {}
        });
        
        // Comme AdminOrderView utilise AdminPagination, la réponse sera dans response.results
        this.abandonedOrders = response.results || response.data || response;
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