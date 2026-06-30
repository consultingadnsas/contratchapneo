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

export interface Tags{
    name: string;
    context: string;
}

export const useContratStore = defineStore('contrat', ()=> {

    const {$api} = useNuxtApp();
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
    const contracts =  ref<Contrat[]>([]);
    const categories = ref<Category[]>([]);
    const tags = ref<Tags[] | null>(null);

    const currentContratId = ref<string | null>(null)

    /* Tools */
    const currentPage = ref(1);
    const totalCount = ref(0);
    const nextPage = ref<string | null>(null);
    const previousPage = ref<string | null>(null);
    const pageSize = ref(10);

    /* computed */

    const toCurrentId = async(id:string)=>{
        currentContratId.value = id;
        console.log('contrat attribué', id);
    }

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
        error.value = "";

        try 
        {
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
            isLoading.value = false;
        }
    };

    const getSpecificContract = async(contratId:string)=> {
        error.value = ""

        try{
            const response = await $api<Contrat>(`/contrat/${contratId}/`,
                {method: 'GET'}
            );
            if(response){
                contrat.value = { ...response, picture: resolveMediaUrl(response.picture) };
                console.log("Reponse du contrat", contrat.value)
            } else{
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
        isLoading.value = true;
        error.value = null;

        try {
            // 1. On construit l'URL de base (adapte le chemin selon tes routes d'API, ex: /contrat/ ou /ecommerce/contrats/)
            let url = `/contrat/?page=${page}`;
            
            // 2. On ajoute dynamiquement le filtre de catégorie s'il existe
            if (categoryId) {
                url += `&category=${categoryId}`;
            }
            
            // 3. NOUVEAU : On ajoute le paramètre de recherche s'il est fourni
            if (searchQuery && searchQuery.trim() !== '') {
                url += `&q=${encodeURIComponent(searchQuery.trim())}`;
            }

            const response = await $api<PaginatedResponse<Contrat>>(url, { method: 'GET' });
            
            if (response && response.results) {
                // 4. On met à jour le tableau des contrats qui alimente ta vue/vue-table
                contracts.value = response.results.map(c => ({ 
                    ...c, 
                    picture: resolveMediaUrl(c.picture) 
                }));
                
                // 5. On met à jour la pagination
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
            isLoading.value = false;
        }
    };

    const fetchContractTags = async (contrat_id: string) => {
        isLoading.value = true;
        error.value = "";

        try {
            const response = await $api(`/contrat/tags/${contrat_id}/`, {
                method: 'GET'
            });
            
            console.log("Votre réponse brute :", response);

            // CORRECTION ICI 👇
            // On vérifie si response existe et si response.tags est un tableau.
            // Si oui on le prend, sinon on met un tableau vide par défaut.
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

    return{
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

        // Guetters
        toCurrentId,

        // Actions
        getCategories,
        getCategoriesWithContrats,
        getContracts,
        getSpecificContract,
        fetchContracts,
        fetchContractTags
    }
}, {persist: true})