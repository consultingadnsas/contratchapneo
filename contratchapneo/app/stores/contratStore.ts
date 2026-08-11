import { defineStore } from "pinia";
import { ref } from "vue";

export interface Category { 
    id?: string;
    title: string;
    description: string;
    contrats?: Contrat[];
    created_at: string;
    updated_at: string;
}

export interface Contrat {
    id?: string,
    category: string,
    title: string,
    description: string,
    prix: string | number,
    promo_price?: string | number, // ⚡️ NOUVEAU : Pour que TS reconnaisse la promotion
    is_active?: boolean,
    fichier_modele: string,
    picture: string,
    views: number | string,
    document_preview?: string,
    downloads: number,
    created_at: string,
    updated_at: string
}

export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

export interface Tags {
    name: string;
    context: string;
}

export const useContratStore = defineStore('contrat', () => {

    const { $api } = useNuxtApp();
    const config = useRuntimeConfig();

    const resolveMediaUrl = (path?: string | null) => {
        if (!path) return path;
        if (path.startsWith('http')) return path;
        const base = config.public.apiBase || 'http://localhost:8000';
        return path.startsWith('/') ? `${base}${path}` : `${base}/${path}`;
    };

    // Ux
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // State
    const contrat = ref<Contrat | null>(null)
    const category = ref<Category | null>(null)
    const contracts = ref<Contrat[]>([]);
    const categories = ref<Category[]>([]);
    const tags = ref<Tags[] | null>(null);

    const currentContratId = ref<string | null>(null)

    /* Tools */
    const currentPage = ref(1);
    const totalCount = ref(0);
    const nextPage = ref<string | null>(null);
    const previousPage = ref<string | null>(null);
    const pageSize = ref(10);

    // --- NOUVEAU : Le verrou anti-concurrence pour éviter les requêtes en triple ---
    const isFetchingContracts = ref<boolean>(false);

    /* computed */
    const toCurrentId = async (id: string) => {
        currentContratId.value = id;
        console.log('contrat attribué', id);
    }

    // Actions

    const getCategories = async () => {
        isLoading.value = true;
        error.value = "";

        try {
            const response = await $api<Category[]>('/contrat/categories/', {
                method: 'GET',
            })

            if (response) {
                isLoading.value = false;
                categories.value = response;
                console.log("Response reçue", categories.value)
                return response;
            } else {
                isLoading.value = false;
                console.log('Problème lors de la reccupérations des contrats', response);
            }
        } catch (err: any) {
            isLoading.value = false;
            console.error('Erreu', err)
            throw err
        } finally {
            isLoading.value = false;
            console.log("Opération de reccupérations terminée")
        }
    }

    const getCategoriesWithContrats = async (id: string) => {
        isLoading.value = true;
        error.value = "";
        try {
            const response = await $api<{ id: string; title: string; contrats: Contrat[] }>(
                `/contrat/categories/${id}/`,
                { method: 'GET' }
            );
            if (response && response.contrats) {
                contracts.value = response.contrats.map(c => ({ ...c, picture: resolveMediaUrl(c.picture) }));
            } else {
                contracts.value = [];
            }
        } catch (err: any) {
            console.error('Erreur', err);
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const getContracts = async (page: number = 1, categoryId: string = '') => {
        // 🔒 Sécurité : Si une requête pour les contrats est déjà en cours, on bloque poliment
        if (isFetchingContracts.value) return;

        isFetchingContracts.value = true; // On ferme le verrou
        error.value = "";

        try {
            const params: Record<string, any> = { page };
            if (categoryId) params.category = categoryId;

            const response = await $api<PaginatedResponse<Contrat>>('/contrat/', {
                method: 'GET',
                params
            });

            if (response) {
                contracts.value = response.results.map((c: Contrat) => ({ ...c, picture: resolveMediaUrl(c.picture) }));
                totalCount.value = response.count;
                nextPage.value = response.next;
                previousPage.value = response.previous;
                currentPage.value = page;

                console.log('Réponse générée', response)
            }
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isFetchingContracts.value = false; // 🔓 On rouvre le verrou
            isLoading.value = false;
        }
    };

    const getSpecificContract = async (contratId: string) => {
        error.value = ""

        try {
            const response = await $api<Contrat>(`/contrat/${contratId}/`,
                { method: 'GET' }
            );
            if (response) {
                contrat.value = { ...response, picture: resolveMediaUrl(response.picture) };
                console.log("Reponse du contrat", contrat.value)
            } else {
                console.log("Reponse du contrat", contrat.value)
            }
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    }

    const fetchContracts = async (page = 1, categoryId: string | null = null, searchQuery: string | null = null) => {
        // 🔒 Sécurité : Si une requête pour les contrats est déjà en cours, on bloque
        if (isFetchingContracts.value) return;

        isFetchingContracts.value = true; // On ferme le verrou
        isLoading.value = true;
        error.value = null;

        try {
            let url = `/contrat/?page=${page}`;
            
            if (categoryId) {
                url += `&category=${categoryId}`;
            }
            
            if (searchQuery && searchQuery.trim() !== '') {
                url += `&q=${encodeURIComponent(searchQuery.trim())}`;
            }

            const response = await $api<PaginatedResponse<Contrat>>(url, { method: 'GET' });
            
            if (response && response.results) {
                contracts.value = response.results.map(c => ({ 
                    ...c, 
                    picture: resolveMediaUrl(c.picture) 
                }));
                
                totalCount.value = response.count;
                nextPage.value = response.next;
                previousPage.value = response.previous;
                currentPage.value = page;

                console.log('Contrats récupérés avec succès', response.results);
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des contrats";
            throw err;
        } finally {
            isFetchingContracts.value = false; // 🔓 On rouvre le verrou
            isLoading.value = false;
        }
    };

    const submitCustomContract = async (payload: object) => {
        isLoading.value = true;

        const { useCartStore } = await import('./cartStore');
        const cartStore = useCartStore();

        try {
            const response = await $api('/contrat/custom-requests/', {
                method: 'POST',
                body: payload
            });

            const createdContract = response?.data ?? response;
            const customContractId = createdContract?.id;

            if (customContractId) {
                console.log('Votre nouveau contrat sur demande', customContractId);
                await cartStore.addCustomizedContract(customContractId);
                return createdContract;
            }

            throw new Error('Aucun identifiant n\'a été renvoyé pour la demande de contrat sur mesure.');
        } catch (error) {
            console.error('Erreur lors de la création de la demande :', error);
            throw error;
        } finally {
            isLoading.value = false;
        }
    }

    const fetchContractTags = async (contrat_id: string) => {
        isLoading.value = true;
        error.value = "";

        try {
            const response = await $api(`/contrat/tags/${contrat_id}/`, {
                method: 'GET'
            });
            
            console.log("Votre réponse brute :", response);

            tags.value = response?.tags || [];
            console.log("Tags extraits avec succès :", tags.value);

            return tags.value;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error('Erreur lors de la récupération des tags :', error.value);
        } finally {
            isLoading.value = false;
        }
    }

    const fillContractTags = async (contrat_id: string) => {
        isLoading.value = true;
        error.value = "";

        try {
            const response = await $api(`/contrat/tags/${contrat_id}/`, {
                method: 'POST',
                body: {}
            });
            
            console.log("Votre réponse brute :", response);

            tags.value = response?.tags || [];
            console.log("Tags extraits avec succès :", tags.value);

            return tags.value;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error('Erreur lors de la récupération des tags :', error.value);
        } finally {
            isLoading.value = false;
        }
    }

    return {
        isLoading,
        error,
        contrat,
        category,
        contracts,
        categories,
        tags,
        currentPage,
        totalCount,
        nextPage,
        previousPage,
        pageSize,
        currentContratId,

        // Getters / Mappers
        toCurrentId,

        // Actions
        getCategories,
        getCategoriesWithContrats,
        getContracts,
        getSpecificContract,
        fetchContracts,
        fetchContractTags,
        fillContractTags,
        submitCustomContract
    }
}, { persist: true })