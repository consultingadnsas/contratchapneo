import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {useCartStore} from '../stores/cartStore'

export interface GuestInfo {
    id?: string;
    email: string;
    full_name: string;
    phone_number?: string | null;
    created_at?: string;
}

export interface Order {
    id: string;
    guest?: GuestInfo | null;
    status?: string;
    total_amount: number;
    created_at?: string;
}

export interface OrderItem {
    id: string;
    order_id?: string;
    contrat?: any;
    unit_price?: number;
    quantity?: number;
    created_at?: string;
}

const cartStore = useCartStore()

export const useOrderStore = defineStore('order', () => {
    const { $api } = useNuxtApp();

    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const orders = ref<Order[]>([]);
    const currentOrder = ref<Order | null>(null);

    const fetchOrders = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api('/ecommerce/orders/', { method: 'GET' });
            // response may be an array (serializer.data) or wrapped
            orders.value = Array.isArray(response) ? response : (response?.data ?? response ?? []);
            return orders.value;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const fetchOrder = async (orderId: string) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api(`/ecommerce/orders/${orderId}/`, { method: 'GET' });
            currentOrder.value = response?.data ?? response ?? null;
            return currentOrder.value;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const checkout = async (payload: any = {}) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api('/ecommerce/cart/checkout/', {
                method: 'POST',
                body: payload,
            });

            // backend returns { data: Order, message }
            const order = response?.data ?? response ?? null;
            currentOrder.value = order;
            //Debug my function
            console.log("La reponse du backend", currentOrder.value)
            return order;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error("erreur rencontrée", err)
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const cancelOrder = async (orderId: string) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api(`/ecommerce/orders/${orderId}/cancel/`, { method: 'POST' });
            const data = response?.data ?? response ?? null;
            // update currentOrder if it matches
            if (currentOrder.value && currentOrder.value.id === orderId) {
                currentOrder.value = data;
            }
            // optionally refresh list
            await fetchOrders();
            return data;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const hasOrders = computed(() => orders.value.length > 0);

    return {
        isLoading,
        error,
        orders,
        currentOrder,
        hasOrders,
        fetchOrders,
        fetchOrder,
        checkout,
        cancelOrder,
    };
});