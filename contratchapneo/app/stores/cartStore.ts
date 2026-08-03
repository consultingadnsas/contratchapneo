import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Contrat } from "./contratStore";
import type { GuestInfo } from './orderStore';

// L'API renvoie les items imbriqués : { id, quantity, contrat: { ... } }
export interface CartItem {
  id: string;
  quantity: number;
  unit_price: string;
  subtotal: number;
  contrat?: Contrat | null;
  pro?: ProItem | null;
  packs?: any | null;
}

export interface Cart {
  items: CartItem[];
  subtotal?: number | string;
  discount?: number | string;
  total?: number | string;
  coupon_code?: string | null;
}

export interface ProItem {
  id: string;
  first_name: string;
  last_name: string;
  title_display: string;
  prix: string;
  profile_picture: string | null;
}

export interface RevisionCustomizedContract {
  id: string;
  title: string;
  description: string;
  price: string;

}

export const useCartStore = defineStore('cart', () => {
  const { $api } = useNuxtApp();
  const config = useRuntimeConfig();

  const resolveMediaUrl = (path?: string | null) => {
    if (!path) return path;
    if (path.startsWith('http')) return path;
    const base = config.public.apiBase || 'http://localhost:8000';
    return path.startsWith('/') ? `${base}${path}` : `${base}/${path}`;
  };

  // UX
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const stripeReady = ref(false);

  // State
  const cart = ref<Cart>({ items: [] });

  // 🔥 CORRECTION CRITIQUE : On conserve total, discount et coupon_code envoyés par Django !
  const normalizeCart = (data: any): Cart => {
    const payload = data?.data ?? data;
    const rawItems = Array.isArray(payload?.items) ? payload.items : [];

    const items = rawItems.map((it: any) => {
      const normalizedItem = { ...it };

      if (it.contrat) {
        normalizedItem.contrat = {
          ...it.contrat,
          picture: resolveMediaUrl(it.contrat.picture)
        };
      }

      if (it.pro) {
        normalizedItem.pro = {
          ...it.pro,
          profile_picture: resolveMediaUrl(it.pro.profile_picture)
        };
      }

      if (it.packs) {
        normalizedItem.packs = {
          ...it.packs,
          picture: resolveMediaUrl(it.packs.picture)
        };
      }

      return normalizedItem;
    });

    return {
      items,
      subtotal: payload?.subtotal,
      discount: payload?.discount,
      total: payload?.total,
      coupon_code: payload?.coupon_code
    };
  };

  // Computed
  const cartItems = computed(() => cart.value?.items ?? []);

  const totalItems = computed(() =>
    cartItems.value.reduce((acc, item) => acc + item.quantity, 0)
  );

  // --- 1. SOUS-TOTAL (Prix normal sans réduction) ---
  const subtotalPrice = computed(() =>
    cartItems.value.reduce((acc, item) => acc + (Number(item.unit_price) * item.quantity), 0)
  );

  const formattedSubtotalPrice = computed(() =>
    subtotalPrice.value.toLocaleString('fr-FR')
  );

  // --- 2. TOTAL FINAL (Prend en compte la réduction de Django) ---
  const totalPrice = computed(() => {
    if (cart.value?.total !== undefined && cart.value?.total !== null) {
      return Number(cart.value.total);
    }
    return subtotalPrice.value;
  });

  const formattedTotalPrice = computed(() =>
    totalPrice.value.toLocaleString('fr-FR')
  );

  const isEmpty = computed(() => cartItems.value.length === 0);

  // Verrou pour éviter les requêtes en double
  const isFetchingCart = ref<boolean>(false);

  // Actions
  const applyCoupon = async (code: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await $api('/ecommerce/cart/apply-coupon/', {
        method: 'POST',
        body: { code: code }
      });

      cart.value = normalizeCart(response);
      return true;
    } catch (err: any) {
      console.error("❌ Erreur lors de l'application du code promo :", err);
      error.value = err.data?.error || "Impossible d'appliquer ce code.";
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const removeCoupon = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await $api('/ecommerce/cart/remove-coupon/', {
        method: 'POST'
      });

      cart.value = normalizeCart(response);
      return true;
    } catch (err: any) {
      console.error("❌ Erreur lors de la suppression du code :", err);
      error.value = "Une erreur est survenue.";
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const fetchCart = async () => {
    if (isFetchingCart.value) {
      return;
    }

    isFetchingCart.value = true;
    isLoading.value = true;
    error.value = null;

    try {
      const response = await $api('/ecommerce/cart/', { method: 'GET' });
      if (response) {
        cart.value = normalizeCart(response);
        console.log("cart response", cart.value.items);
      }
    } catch (err: any) {
      error.value = err.message;
      console.error("Cart error", err);
      throw err;
    } finally {
      isFetchingCart.value = false;
      isLoading.value = false;
    }
  };

  const addToCart = async (contrat: string, userInputs: Record<string, any> = {}) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await $api('/ecommerce/cart/add/', {
        method: 'POST',
        body: {
          contrat_id: contrat,
          user_inputs: userInputs
        }
      });

      if (response) {
        cart.value = normalizeCart(response);
      }
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const addProToCart = async (prodId: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await $api('/ecommerce/cart/add/', {
        method: 'POST',
        body: { pro_id: prodId }
      });

      if (response) {
        cart.value = normalizeCart(response);
      }
    } catch (err: any) {
      error.value = err.message;
      console.error("l'erreur rencontrée", error);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const addCustomizedContract = async (customedContractId: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await $api('/ecommerce/cart/add/', {
        method: 'POST',
        body: { customed_contract: customedContractId }
      });

      if (response) {
        console.log("votre reponse", response);
        cart.value = normalizeCart(response);
      }
    } catch (err: any) {
      error.value = err.message;
      console.error(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const addPackToCart = async (pack_id: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await $api('/ecommerce/cart/pack/add/', {
        method: 'POST',
        body: { pack_id: pack_id }
      });

      if (response) {
        console.log("Votre reponse de pack", response);
        cart.value = normalizeCart(response);
      }

      return response;
    } catch (err: any) {
      error.value = err.message;
      console.error("Erreur ajout pack", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const addRevisionContractToCart = async( contract_revision_id: string) => {

    isLoading.value = true;
    error.value = null;

    try {
      const response = await $api(`/ecommerce/cart/add/`, {
        method: 'POST',
        body: { contract_revision_id: contract_revision_id}
      });

      if (response) {
        console.log("Votre reponse de revision", response);
        cart.value = normalizeCart(response);
        return response;
      }
    } catch(err:any){
      error.value = err.message;
      console.error("Erreur ajout revision", err)
      throw err;
    } finally {
      isLoading.value = false;
    }

  }

  const removeFromCart = async (contratId: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await $api(`/ecommerce/cart/remove/${contratId}/`, {
        method: 'DELETE'
      });

      if (response) {
        cart.value = normalizeCart(response);
      } else {
        cart.value.items = cart.value.items.filter(item => item.id !== contratId);
      }
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateQuantity = async (contratId: string, quantity: number) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await $api(`/ecommerce/cart/update/${contratId}/`, {
        method: 'PATCH',
        body: { quantity }
      });
      if (response) {
        cart.value = normalizeCart(response);
      } else {
        const item = cart.value.items.find(i => i.id === contratId);
        if (item) item.quantity = quantity;
      }
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const clearCart = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      await $api('/ecommerce/cart/clear/', { method: 'DELETE' });
      cart.value = { items: [] };
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const checkout = async (payload?: GuestInfo | null) => {
    isLoading.value = true;
    error.value = null;
    try {
      const bodyData = payload ? payload : {};
      const response = await $api('/ecommerce/checkout/', {
        method: 'POST',
        body: bodyData
      });
      console.log("checkout response", response);
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const initiatePayment = async (payload?: any, email?: string) => {
    isLoading.value = true;
    error.value = null;

    try {
      const emailQuery = email ? `?email=${encodeURIComponent(email)}` : '';
      const bodyData = payload ? payload : {};

      const response = await $api(`/payment/initiate/${emailQuery}`, {
        method: 'POST',
        body: bodyData
      });
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const clearLocalCart = () => {
    cart.value = { items: [] };
    error.value = null;
    stripeReady.value = false;
    console.log('[CartStore] Panier local vidé suite à la déconnexion.');
  };

  return {
    isLoading,
    error,
    cart,
    stripeReady,

    // Computed
    totalItems,
    totalPrice,
    formattedTotalPrice,
    isEmpty,
    subtotalPrice,
    formattedSubtotalPrice,

    // Actions
    applyCoupon,
    removeCoupon,
    fetchCart,
    addToCart,
    addProToCart,
    addPackToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    checkout,
    initiatePayment,
    addCustomizedContract,
    clearLocalCart
  };
},
{ persist: true }
);