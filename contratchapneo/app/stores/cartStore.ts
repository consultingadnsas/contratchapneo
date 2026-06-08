import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Contrat } from "./contratStore";

export interface CartItem extends Contrat {
  quantity: number;
}

export interface Cart {
  items: CartItem[];
}

export const useCartStore = defineStore('cart', () => {

    const { $api } = useNuxtApp();

    // UX
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // State
    const cart = ref<Cart>({ items: [] });

    // Computed
    const totalItems = computed(() =>
      cart.value.items.reduce((acc, item) => acc + item.quantity, 0)
    );

    const totalPrice = computed(() =>
      cart.value.items.reduce((acc, item) => acc + (Number(item.prix) * item.quantity), 0)
    );

    const formattedTotalPrice = computed(() =>
      totalPrice.value.toLocaleString('fr-FR')
    );

    const isEmpty = computed(() => cart.value.items.length === 0);

    // Actions
    const fetchCart = async () => {
      isLoading.value = true;
      error.value = null;
      try {
        const response = await $api<Cart>('/ecommerce/cart/', { method: 'GET' });
        if (response) {
          cart.value.items = response?.items;
          console.log("cart response", cart.value.items)
        }
      } catch (err: any) {
          error.value = err.message;
          console.error("Cart error", err)
          throw err;
      } finally {
          isLoading.value = false;
      }
    };

    const addToCart = async (contrat: Contrat) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<Cart>('/cart/add/', {
                method: 'POST',
                body: { contrat_id: contrat.id }
            });
            if (response) {
                cart.value = response;
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
            const response = await $api<Cart>(`/cart/remove/${contratId}/`, {
                method: 'DELETE'
            });
            if (response) {
                cart.value = response;
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
            const response = await $api<Cart>(`/cart/update/${contratId}/`, {
                method: 'PATCH',
                body: { quantity }
            });
            if (response) {
                cart.value = response;
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
            await $api('/cart/clear/', { method: 'DELETE' });
            cart.value = { items: [] };
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

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
    };
});