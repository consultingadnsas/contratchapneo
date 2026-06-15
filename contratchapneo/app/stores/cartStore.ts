import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { loadStripe } from '@stripe/stripe-js';
import type { Contrat } from "./contratStore";
import type { GuestInfo} from './orderStore';
import { useHead } from '#imports';

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
    const stripeReady = ref(false);

    // State
    const cart = ref<Cart>({ items: [] });
    let stripeInstance: any = null;
    let stripeElements: any = null;
    let stripeClientSecret: string | null = null;

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

    const initiatePayment = async (payload: Object, email: string) => {

        isLoading.value = true;
        error.value = null;

        try {
            const emailQuery = email ? `?email=${encodeURIComponent(email)}` : '';
            const response = await $api(`/payments/initiate/${emailQuery}`, {
                method: 'POST',
                body: { ...payload, cart: cart.value }
            });
            return response;
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const initializeStripe = async (orderId: string, email: string) => {
        if (!orderId) {
            const err = new Error('Aucun identifiant de commande pour Stripe.');
            error.value = err.message;
            throw err;
        }

        isLoading.value = true;
        error.value = null;
        stripeReady.value = false;

        try {
            const config = useRuntimeConfig();
            if (!config.public.stripePublicKey) {
                throw new Error('Clé publique Stripe non configurée.');
            }

            stripeInstance = await loadStripe(config.public.stripePublicKey);
            if (!stripeInstance) {
                throw new Error('Impossible de charger Stripe.');
            }

            const response: any = await initiatePayment({ order_id: orderId, payment_method: 'STRIPE' }, email);
            if (!response?.client_secret) {
                throw new Error(response?.error || 'Impossible d/initier la clé d/intention de paiement.');
            }

            stripeClientSecret = response.client_secret;

            const appearance = {
                theme: 'flat',
                variables: {
                    colorPrimary: '#007bff',
                    fontFamily: 'sans-serif'
                }
            };

            stripeElements = stripeInstance.elements({
                clientSecret: stripeClientSecret,
                appearance,
            });

            stripeReady.value = true;
            return stripeElements;
        } catch (err: any) {
            error.value = err.message || 'Erreur lors de l\'initialisation de Stripe.';
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const confirmStripePayment = async (returnUrl: string) => {
        if (!stripeInstance || !stripeElements) {
            const err = new Error('Stripe n\'est pas encore initialisé.');
            error.value = err.message;
            throw err;
        }

        isLoading.value = true;
        error.value = null;

        try {
            const { error: stripeError, paymentIntent } = await stripeInstance.confirmPayment({
                elements: stripeElements,
                confirmParams: {
                    // 💡 OBLIGATOIRE : Ajout de la clé attendue par Stripe pour valider la requête
                    return_url: returnUrl,
                },
                redirect: 'if_required',
            });

            if (stripeError) {
                const alreadySucceeded = stripeError.code === 'payment_intent_unexpected_state' && stripeError?.payment_intent?.status === 'succeeded';
                if (alreadySucceeded) {
                    return stripeError.payment_intent;
                }

                // Si on obtient un état inattendu, on tente de relire l'intention existante.
                if (stripeError.code === 'payment_intent_unexpected_state' && stripeClientSecret) {
                    const retrieval = await stripeInstance.retrievePaymentIntent(stripeClientSecret);
                    if (retrieval?.paymentIntent?.status === 'succeeded') {
                        return retrieval.paymentIntent;
                    }
                }

                error.value = stripeError.message || 'La transaction a été refusée.';
                throw stripeError;
            }

            return paymentIntent;
        } catch (err: any) {
            error.value = err.message || 'Une erreur inattendue est survenue lors de la validation.';
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const resetStripeState = () => {
        stripeInstance = null;
        stripeElements = null;
        stripeClientSecret = null;
        stripeReady.value = false;
        error.value = null;
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

        // Actions
        fetchCart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        checkout,
        initiatePayment,
        initializeStripe,
        confirmStripePayment,
        resetStripeState,
    };
},
    {persist: true}
);