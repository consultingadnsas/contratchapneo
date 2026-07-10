import { defineStore } from "pinia";
import { ref } from "vue";
import { useCartStore } from './cartStore'

// ==========================================
// INTERFACES
// ==========================================
export interface Country {
    id: number;
    name: string;
    code: string;
    is_ohada_member: boolean;
}

export interface LegalDomain {
    id: number;
    name: string;
    slug: string;
    description?: string;
}

export interface LegalProfessional {
    id: string;
    first_name: string;
    last_name: string;
    title: string;
    title_display: string;
    professional_order: string;
    registration_number: string;
    email: string;
    phone_number: string;
    website?: string;
    profile_picture?: string | null;
    bio: string;
    years_of_experience: number;
    country: Country;
    city: string;
    domains: LegalDomain[];
    is_active: boolean;
    is_verified: boolean;
}

// ==========================================
// STORE
// ==========================================
export const useProStore = defineStore('proStore', () => {

    // --- NUXT CONTEXT & HELPERS ---
    const { $api } = useNuxtApp();
    const config = useRuntimeConfig();
    
    // ✅ On instancie le cartStore pour l'utiliser en interne
    const cartStore = useCartStore();

    const resolveMediaUrl = (path?: string | null) => {
        if (!path) return path;
        if (path.startsWith('http')) return path;
        const base = config.public.apiBase || 'http://localhost:8000';
        return path.startsWith('/') ? `${base}${path}` : `${base}/${path}`;
    };
    
    // --- ÉTAT (State) ---
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    const professionals = ref<LegalProfessional[]>([]);
    const professional = ref<LegalProfessional | null>(null);
    const countries = ref<Country[]>([]);
    const domains = ref<LegalDomain[]>([]);
    const currentPage = ref(1);
    const totalCount = ref(0);
    const pageSize = ref(10);

    // --- ACTIONS ---

    /**
     * 1. Récupérer la liste des professionnels avec filtres
     */
    const getProfessionals = async (page: number = 1, domainSlug: string = '', countryCode: string = '', searchQuery: string = '') => {
    isLoading.value = true;
    error.value = null;
    
    try {
        // 1. On inclut la page dans les paramètres
        const params: Record<string, any> = { page }; 
        if (domainSlug) params.domain = domainSlug;
        if (countryCode) params.country = countryCode;
        if (searchQuery) params.q = searchQuery;

        const response = await $api<any>('/pro/professionals/', {
            method: 'GET',
            params
        });

        if (response) {
            // 2. Mise à jour des variables de pagination du Store
            // (Assure-toi que ton backend renvoie bien un champ "count")
            totalCount.value = response.count || 0; 
            currentPage.value = page;

            // 3. On extrait les données du tableau "results" (standard de pagination)
            // Le "|| response" est une sécurité au cas où ton backend renvoie encore un tableau direct
            const resultsArray = response.results || response; 

            professionals.value = resultsArray.map((pro: any) => ({
                ...pro,
                profile_picture: resolveMediaUrl(pro.profile_picture)
            }));
            
            console.log('Professionnels de la page', page, 'récupérés avec succès', professionals.value);
        }
    } catch (err: any) {
        console.error('Erreur getProfessionals:', err);
        error.value = err.message || "Erreur lors de la récupération des professionnels";
        professionals.value = [];
        totalCount.value = 0; // On remet à 0 en cas d'erreur
    } finally {
        isLoading.value = false;
    }
};

    /**
     * 2. Charger les filtres (Pays et Domaines)
     */
    const getFilters = async () => {
        try {
            const response = await $api<{ countries: Country[], domains: LegalDomain[] }>('/pro/professionals/filters/', {
                method: 'GET'
            });

            if (response) {
                countries.value = response.countries || [];
                domains.value = response.domains || [];
                console.log('Filtres récupérés avec succès');
            }
        } catch (err: any) {
            console.error('Erreur lors du chargement des filtres:', err);
            error.value = err.message;
        }
    };

    /**
     * 3. Récupérer un professionnel spécifique par ID (pour la modale)
     */
    const getSpecificProfessional = (id: string) => {
        const found = professionals.value.find(p => p.id === id);
        if (found) {
            professional.value = found;
        } else {
            console.error(`Le professionnel avec l'ID ${id} est introuvable.`);
            professional.value = null;
        } 
    };

    return {
        // 🚨 CRITIQUE : J'AI SUPPRIMÉ `cartStore` D'ICI !
        isLoading,
        error,
        professionals,
        professional,
        countries,
        domains,
        currentPage,
        totalCount,
        pageSize,
        getProfessionals,
        getFilters,
        getSpecificProfessional,
    };
});