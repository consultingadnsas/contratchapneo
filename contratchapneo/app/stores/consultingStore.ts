import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';

export interface ConsultingPayload {
    full_name: string;
    phone_number: string;
    email: string;
    description: string;
    meet_day: string;
    consulting_hour: string;
    title?: string;
}

export interface ConsultingResponse {
    id: string;
    title: string;
    full_name: string;
    phone_number: string;
    email: string;
    description: string;
    meet_day: string;
    consulting_hour: string;
    status: string;
    status_display: string;
    created_at: string;
    updated_at: string;
}

export const useConsultingStore = defineStore('consulting', () => {
    const { $api } = useNuxtApp();
    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const bookedSlots = ref<string[]>([]);
    const lastBooking = ref<ConsultingResponse | null>(null);

    async function fetchBookedSlots(date: string) {
        if (!date) {
            bookedSlots.value = [];
            return [];
        }
        try {
            const response: any = await $api('/consulting/booked-slots/', {
                method: 'GET',
                params: { date }
            });
            if (response && response.booked_slots) {
                bookedSlots.value = response.booked_slots;
                return response.booked_slots;
            }
            return [];
        } catch (err: any) {
            console.error("Erreur lors de la récupération des créneaux réservés :", err);
            return [];
        }
    }

    async function bookConsulting(payload: ConsultingPayload) {
        isLoading.value = true;
        error.value = null;

        try {
            const response: any = await $api('/consulting/consultings/', {
                method: 'POST',
                body: {
                    title: payload.title || 'Diagnostic juridique',
                    full_name: payload.full_name,
                    phone_number: payload.phone_number,
                    email: payload.email,
                    description: payload.description,
                    meet_day: payload.meet_day,
                    consulting_hour: payload.consulting_hour
                }
            });

            lastBooking.value = response;
            return response;
        } catch (err: any) {
            console.error("Erreur API Consulting :", err);
            let msg = "Une erreur est survenue lors de la prise de rendez-vous.";
            if (err?.data?.detail) {
                msg = err.data.detail;
            } else if (err?.data?.non_field_errors) {
                msg = Array.isArray(err.data.non_field_errors) ? err.data.non_field_errors[0] : String(err.data.non_field_errors);
            } else if (err?.data && typeof err.data === 'object') {
                const firstKey = Object.keys(err.data)[0];
                if (firstKey) {
                    const firstVal = (err.data as Record<string, any>)[firstKey];
                    msg = Array.isArray(firstVal) ? firstVal[0] : String(firstVal);
                }
            } else if (err?.message) {
                msg = err.message;
            }
            error.value = msg;
            throw new Error(msg);
        } finally {
            isLoading.value = false;
        }
    }

    return {
        isLoading,
        error,
        bookedSlots,
        lastBooking,
        fetchBookedSlots,
        bookConsulting
    };
});
