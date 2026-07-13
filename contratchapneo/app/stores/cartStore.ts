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
  unit_price: string;
  subtotal: number;
  contrat?: Contrat | null; // Peut désormais être nul
  pro?: ProItem | null;     // Nouvel élément !
}

export interface Cart {
  items: CartItem[];
}

export interface ProItem {
  id: string;
  first_name: string;
  last_name: string;
  title_display: string;
  prix: string;
  profile_picture: string | null;
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
        
        const items = rawItems.map((it: any) => {
            // On copie l'item de base
            const normalizedItem = { ...it };

            // S'il y a un contrat, on résout son image
            if (it.contrat) {
                normalizedItem.contrat = { 
                    ...it.contrat, 
                    picture: resolveMediaUrl(it.contrat.picture) 
                };
            }

            // S'il y a un pro, on résout sa photo de profil
            if (it.pro) {
                normalizedItem.pro = { 
                    ...it.pro, 
                    profile_picture: resolveMediaUrl(it.pro.profile_picture) 
                };
            }

            return normalizedItem;
        });
        return { items };
    };

    // Computed
    const cartItems = computed(() => cart.value?.items ?? []);

    const totalItems = computed(() =>
      cartItems.value.reduce((acc, item) => acc + item.quantity, 0)
    );

    const totalPrice = computed(() =>
      cartItems.value.reduce((acc, item) => acc + (Number(item.unit_price) * item.quantity), 0)
    );

    const formattedTotalPrice = computed(() =>
      totalPrice.value.toLocaleString('fr-FR')
    );

    const isEmpty = computed(() => cartItems.value.length === 0);

    // --- NOUVEAU : Le verrou pour le panier ---
    const isFetchingCart = ref<boolean>(false);

    // Actions
    const fetchCart = async () => {
        // SÉCURITÉ : Si la Navbar et la Page demandent le panier en même temps, 
        // le deuxième appel sera bloqué ici.
        if (isFetchingCart.value) {
            return; 
        }

        isFetchingCart.value = true; // 🔒 On ferme le verrou
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
            isFetchingCart.value = false; // 🔓 On rouvre le verrou
            isLoading.value = false;
        }
    };

    // Ici c'est pour l'ajout des contrats dans le panier!
    const addToCart = async (contrat: string, userInputs: Record<string, any> = {}) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api('/ecommerce/cart/add/', {
                method: 'POST',
                body: { 
                    contrat_id: contrat,
                    user_inputs: userInputs // 💡 On ajoute le JSON des réponses ici !
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
                body: {pro_id: prodId}
            });

            if (response) {
                cart.value = normalizeCart(response);
            }
            isLoading.value = false;
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
                body: { customed_contract: customedContractId }   // ✅ clé alignée avec la vue Django
            });

            if (response) {
                console.log("votre reponse", response)
                cart.value = normalizeCart(response);
            }
        } catch (err: any) {
            error.value = err.message;
            console.error(err);   // ✅ appel réel de la fonction
            throw err;             // ✅ pour que le formulaire puisse afficher l'erreur si besoin
        } finally {
            isLoading.value = false;   // ✅ corrigé
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
        addProToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        checkout,
        initiatePayment,
        addCustomizedContract
    };
},
    {persist: true}
);