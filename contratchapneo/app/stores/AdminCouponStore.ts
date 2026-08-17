import { defineStore } from 'pinia';

// 1. Typage strict calqué sur le modèle Django
export interface Coupon {
  id: number;
  code: string;
  discount_type: 'percentage' | 'fixed';
  discount_value: string | number; // Souvent renvoyé sous forme de string (DecimalField)
  valid_from: string;
  valid_to: string;
  active: boolean;
  max_usages: number;
  used_count: number;
}

export const useAdminCouponStore = defineStore('adminCoupon', {
  state: () => ({
    coupons: [] as Coupon[],
    isLoading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchCoupons() {
      this.isLoading = true;
      this.error = null;

      try {
        // ⚡️ N'oublie pas le préfixe /api/ (si tu l'as configuré) pour éviter le conflit avec le panel admin Django
        const response: any = await $fetch('http://localhost:8000/admin/coupons/', {
          headers: {
            // 'Authorization': `Bearer ${token}` -> À réactiver quand IsAdminUser sera en place
          }
        });

        // Extraction ultra-sécurisée : gère la pagination (results), la réponse standard (data) ou un tableau direct
        if (response && Array.isArray(response.results)) {
            this.coupons = response.results;
        } else if (response && Array.isArray(response.data)) {
            this.coupons = response.data;
        } else if (Array.isArray(response)) {
            this.coupons = response;
        } else {
            console.warn("Format inattendu reçu du backend :", response);
            this.coupons = [];
        }
        
      } catch (err: any) {
        console.error("Erreur lors de la récupération des codes promo :", err);
        this.error = err.response?._data?.message || "Erreur de connexion au serveur.";
      } finally {
        this.isLoading = false;
      }
    }
  },
  
  getters: {
    totalCoupons: (state) => state.coupons.length,
    activeCoupons: (state) => state.coupons.filter(c => c.active).length,
  }
});