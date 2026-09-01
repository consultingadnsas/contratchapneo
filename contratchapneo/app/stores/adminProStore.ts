import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';

export interface Country {
    id: string | number;
    name: string;
    code: string;
    is_ohada_member: boolean;
}

export const useAdminProStore = defineStore('adminProStore', () => {
    
    const { $api } = useNuxtApp();

    // --- STATE ---
    const pros = ref<any[]>([]);
    const countries = ref<Country[]>([]); // ⚡️ État des pays
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    const domains = ref<any[]>([]);

    // --- ACTIONS PROFESSIONNELS ---
    const fetchPros = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<any>('/pro/admin/', { method: 'GET' });
            if (response) {
                const rawData = response.data ? response.data : response;
                pros.value = rawData as any[];
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des professionnels.";
        } finally {
            isLoading.value = false;
        }
    };

    const addPro = async (payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<any>('/pro/admin/', {
                method: 'POST',
                body: payload
            });
            if (response) {
                const newPro = response.data ? response.data : response;
                pros.value.unshift(newPro); // Ajoute en haut de la liste
                return newPro;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de l'ajout.";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const updatePro = async (proId: string, payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<any>(`/pro/admin/${proId}/`, {
                method: 'PUT',
                body: payload
            });
            if (response) {
                const updatedPro = response.data ? response.data : response;
                const index = pros.value.findIndex(p => p.id === proId);
                if (index !== -1) {
                    pros.value.splice(index, 1, { ...pros.value[index], ...updatedPro });
                }
                return updatedPro;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la modification.";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const deletePro = async (proId: string) => {
        isLoading.value = true;
        error.value = null;
        try {
            await $api(`/pro/admin/${proId}/`, { method: 'DELETE' });
            pros.value = pros.value.filter(p => p.id !== proId);
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la suppression.";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // --- ACTIONS PAYS ---
    const fetchCountries = async () => {
        try {
            const response = await $api<Country[]>('/pro/countries/admin/', { method: 'GET' });
            if (response) {
                countries.value = response;
            }
        } catch (err: any) {
            console.error("Erreur fetchCountries:", err);
        }
    };

    const addCountry = async (payload: { name: string; code: string; is_ohada_member: boolean }) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<Country>('/pro/countries/admin/', {
                method: 'POST',
                body: payload
            });
            // ⚡️ Mise à jour locale pour que le menu déroulant se rafraîchisse
            countries.value.push(response);
            // On trie alphabétiquement après l'ajout
            countries.value.sort((a, b) => a.name.localeCompare(b.name));
            return response;
        } catch (err: any) {
            error.value = err.response?._data || "Erreur lors de l'ajout du pays.";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const fetchDomains = async () => {
        try {
            const response = await $api<any[]>('/pro/domains/admin/', { method: 'GET' });
            if (response) domains.value = response;
        } catch (err: any) {
            console.error("Erreur fetchDomains:", err);
        }
    };

    const addDomain = async (payload: { name: string; description?: string }) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<any>('/pro/domains/admin/', {
                method: 'POST',
                body: payload
            });
            domains.value.push(response);
            domains.value.sort((a: any, b: any) => a.name.localeCompare(b.name));
            return response;
        } catch (err: any) {
            error.value = err.message || "Erreur lors de l'ajout du domaine.";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        pros,
        countries,
        domains,
        isLoading,
        error,
        fetchPros,
        addPro,
        updatePro,
        deletePro,
        fetchCountries,
        addCountry,
        fetchDomains,
        addDomain
    };
});