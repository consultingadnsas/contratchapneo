import {defineStore} from "pinia";
import {ref} from "vue"

export interface Category{
    id?: string;
    title: string;
    description: string;
    created_at: string;
    updated_at: string;
}

export interface Contrat{
    id?: string,
    category: string,
    title: string,
    description: string,
    prix: string | number,
    fichier_modele: string,
    picture: string,
    views: number | string,
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

export const useContratStore = defineStore('contrat', ()=> {

    const {$api} = useNuxtApp();

    // Ux
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // State
    const contrat = ref<Contrat | null>(null)
    const category = ref<Category | null>(null)
    const contracts =  ref<Contrat[]>([]);
    const categories = ref<Category[]>([]);
    // Ajouter dans le state :
    const currentPage = ref(1);
    const totalCount = ref(0);
    const nextPage = ref<string | null>(null);
    const previousPage = ref<string | null>(null);
    const pageSize = ref(10);

    // Actions

    const getCategories = async()=> {

        isLoading.value = true;
        error.value = "";

        try{
            const response = await $api<Category[]>('/contrat/categories/',{
                method: 'GET',
            })

            if (response){
                isLoading.value = false;
                categories.value = response;
                console.log("Response reçue", categories.value)
                return response;
            } else {
                isLoading.value = false;
                console.log('Problème lors de la reccupérations des contrats', response);
            }
        } catch(err:any){
            isLoading.value = false;
            console.error('Erreu', err)
            throw err
        } finally{
            isLoading.value = false;
            console.log("Opération de reccupérations terminée")
        }
    }

    const getCategoriesWithContrats = async (id: string) => {
        isLoading.value = true;
        error.value = "";
        try {
            // Typage correct : la réponse contient une propriété 'contrats'
            const response = await $api<{ id: string; title: string; contrats: Contrat[] }>(
            `/contrat/categories/${id}/`,
            { method: 'GET' }
            );
            if (response && response.contrats) {
            contracts.value = response.contrats; // ✅ on assigne bien un tableau
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
    isLoading.value = true;
    error.value = "";

    try {
        const params: Record<string, any> = { page };
        if (categoryId) params.category = categoryId;

        const response = await $api<PaginatedResponse<Contrat>>('/contrat/', {
            method: 'GET',
            params
        });

        if (response) {
            contracts.value = response.results;
            totalCount.value = response.count;
            nextPage.value = response.next;
            previousPage.value = response.previous;
            currentPage.value = page;
        }
        } catch (err: any) {
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    return{
        isLoading,
        error,
        contrat,
        category,
        contracts,
        categories,
        currentPage,
        totalCount,
        nextPage,
        previousPage,
        pageSize,

        // Actions
        getCategories,
        getCategoriesWithContrats,
        getContracts
    }
})