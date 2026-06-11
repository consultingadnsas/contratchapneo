import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Contrat } from "./contratStore";
import type { GuestInfo} from './orderStore';

// L'API renvoie les items imbriqués : { id, quantity, contrat: { ... } }
export interface CartItem {
  id: string;
  quantity: number;
  contrat: Contrat;
}

export interface Cart {
  items: CartItem[];
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

    // State
    const cart = ref<Cart>({ items: [] });

        const normalizeCart = (data: any): Cart => {
            const payload = data?.data ?? data;
            const rawItems = Array.isArray(payload?.items) ? payload.items : [];
            const items = rawItems.map((it: any) => ({
                ...it,
                contrat: it.contrat ? { ...it.contrat, picture: resolveMediaUrl(it.contrat.picture) } : it.contrat
            }));
            return { items };
        };

    // Computed
    const cartItems = computed(() => cart.value?.items ?? []);

    const totalItems = computed(() =>
      cartItems.value.reduce((acc, item) => acc + item.quantity, 0)
    );

    const totalPrice = computed(() =>
      cartItems.value.reduce((acc, item) => acc + (Number(item.contrat.prix) * item.quantity), 0)
    );

    const formattedTotalPrice = computed(() =>
      totalPrice.value.toLocaleString('fr-FR')
    );

    const isEmpty = computed(() => cartItems.value.length === 0);

    // Actions
    const fetchCart = async () => {
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
          isLoading.value = false;
      }
    };

    const addToCart = async (contrat: string) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api('/ecommerce/cart/add/', {
                method: 'POST',
                body: { contrat_id: contrat }
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
                // Fallback local si l'API ne renvoie pas le panier mis à jour
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
                // Fallback local
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

    const checkout = async (payload:GuestInfo) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api('/ecommerce/checkout/', {
                method: 'POST',
                body: { ...payload, cart: cart.value }
            });
            console.log("checkout response", response)
            return response;
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // About the paiement flow with the frontend

    const initiatePayment = async (payload: GuestInfo) => {

        // UX:UI

        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api('/ecommerce/checkout/', {
                method: 'POST',
                body: { ...payload, cart: cart.value }
            });
            console.log("checkout response", response)
            return response;
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    }

    return {
        isLoading,
        error,
        cart,

        // Computed
        totalItems,
        totalPrice,
        formattedTotalPrice,
        isEmpty,

        // Actions
        fetchCart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        checkout,
    };
},
    {persist: true}
);