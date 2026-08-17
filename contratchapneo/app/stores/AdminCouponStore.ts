import { defineStore } from 'pinia';

// 1. Typage strict calqué sur le modèle Django
export interface Coupon {
  id?: number;
  code: string;
  discount_type: 'percentage' | 'fixed';
  discount_value: string | number; 
  valid_from: string;
  valid_to: string;
  active: boolean;
  max_usages: number;
  used_count?: number; // Optionnel à la création
}

export const useAdminCouponStore = defineStore('adminCoupon', {
  state: () => ({
    coupons: [] as Coupon[],
    currentCoupon: null as Coupon | null,
    isLoading: false,
    error: null as string | null,
  }),

  actions: {
    // --------------------------------------------------
    // LISTER LES COUPONS
    // --------------------------------------------------
    async fetchCoupons() {
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp(); // ⚡️ Appel de ton instance personnalisée

      try {
        // Plus besoin de l'URL complète ni d'injecter le token manuellement
        const response: any = await $api('/ecommerce/admin/coupons/', {
          method: 'GET'
        });
        console.log("RÉPONSE BRUTE DU BACKEND :", response);

        if (response && Array.isArray(response.results)) {
            this.coupons = response.results;
        } else if (response && Array.isArray(response.data)) {
            this.coupons = response.data;
        } else if (Array.isArray(response)) {
            this.coupons = response;
        } else {
            this.coupons = [];
        }
      } catch (err: any) {
        console.error("Erreur (fetchCoupons) :", err);
        this.error = err.response?._data?.message || "Impossible de charger la liste des codes promo.";
      } finally {
        this.isLoading = false;
      }
    },

    // --------------------------------------------------
    // CRÉER UN COUPON
    // --------------------------------------------------
    async createCoupon(payload: Coupon) {
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp();

      try {
        const response: any = await $api('/ecommerce/admin/coupons/create/', {
          method: 'POST',
          body: payload
        });

        if (response && response.data) {
            this.coupons.unshift(response.data);
        }
        return response;
      } catch (err: any) {
        console.error("Erreur (createCoupon) :", err);
        this.error = err.response?._data?.error || "Impossible de créer le code promo.";
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    // --------------------------------------------------
    // DÉTAIL D'UN COUPON
    // --------------------------------------------------
    async getCoupon(id: number) {
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp();

      try {
        const response: any = await $api(`/ecommerce/admin/coupons/${id}/`, {
          method: 'GET'
        });

        if (response && response.data) {
            this.currentCoupon = response.data;
        }
        return response;
      } catch (err: any) {
        console.error(`Erreur (getCoupon ${id}) :`, err);
        this.error = "Impossible de récupérer les détails du code promo.";
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    // --------------------------------------------------
    // MODIFIER UN COUPON
    // --------------------------------------------------
    async updateCoupon(id: number, payload: Partial<Coupon>) {
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp();

      try {
        const response: any = await $api(`/ecommerce/admin/coupons/${id}/`, {
          method: 'PUT',
          body: payload
        });

        if (response && response.data) {
            const index = this.coupons.findIndex(c => c.id === id);
            if (index !== -1) {
                this.coupons[index] = response.data;
            }
        }
        return response;
      } catch (err: any) {
        console.error(`Erreur (updateCoupon ${id}) :`, err);
        this.error = err.response?._data?.error || "Impossible de mettre à jour le code promo.";
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    // --------------------------------------------------
    // SUPPRIMER UN COUPON
    // --------------------------------------------------
    async deleteCoupon(id: number) {
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp();

      try {
        await $api(`/ecommerce/admin/coupons/${id}/`, {
          method: 'DELETE'
        });

        this.coupons = this.coupons.filter(c => c.id !== id);
      } catch (err: any) {
        console.error(`Erreur (deleteCoupon ${id}) :`, err);
        this.error = err.response?._data?.error || "Impossible de supprimer ce code promo.";
        throw err;
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