import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Contrat } from "./contratStore";
import type { GuestInfo } from './orderStore';

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

    // UX
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // State
    const cart = ref<Cart>({ items: [] });

    // Persistance des infos de commande pour l'après-redirection
    const currentOrderId = ref<number | string | null>(null);
    const currentGuestEmail = ref<string>('');

    const resolveMediaUrl = (path?: string | null) => {
        if (!path) return path;
        if (path.startsWith('http')) return path;
        const base = config.public.apiBase || 'http://localhost:8000';
        return path.startsWith('/') ? `${base}${path}` : `${base}/${path}`;
    };

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
    const totalItems = computed(() => cartItems.value.reduce((acc, item) => acc + item.quantity, 0));
    const totalPrice = computed(() => cartItems.value.reduce((acc, item) => acc + (Number(item.contrat.prix) * item.quantity), 0));
    const formattedTotalPrice = computed(() => totalPrice.value.toLocaleString('fr-FR'));
    const isEmpty = computed(() => cartItems.value.length === 0);

    // Actions
    const fetchCart = async () => {
        isLoading.value = true;
        try {
            const response = await $api('/ecommerce/cart/', { method: 'GET' });
            if (response) cart.value = normalizeCart(response);
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const checkout = async (payload: GuestInfo) => {
        isLoading.value = true;
        try {
            const response = await $api('/ecommerce/checkout/', {
                method: 'POST',
                body: { ...payload, cart: cart.value }
            });
            
            // 💡 On sauvegarde les infos ici avant la redirection vers xpaye
            currentOrderId.value = response.id;
            currentGuestEmail.value = payload.guest.email;
            
            return response;
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const initiatePayment = async (payload: Object) => {
        isLoading.value = true;
        try {
            return await $api('/payment/initiate/', {
                method: 'POST',
                body: payload
            });
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const clearCart = async () => {
        try {
            await $api('/ecommerce/cart/clear/', { method: 'DELETE' });
            cart.value = { items: [] };
            currentOrderId.value = null; // Nettoyage
            currentGuestEmail.value = '';
        } catch (err) {
            throw err;
        }
    };

    return {
        isLoading, error, cart,
        currentOrderId, currentGuestEmail, // Exposé pour ton composant succès
        cartItems, totalItems, totalPrice, formattedTotalPrice, isEmpty,
        fetchCart, checkout, initiatePayment, clearCart
    };
}, 
{
    persist: true // Maintenant, même après redirection, tes variables survivent !
});