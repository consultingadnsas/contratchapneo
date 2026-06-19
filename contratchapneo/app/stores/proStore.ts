import { defineStore } from "pinia";
import { ref } from "vue";
// Note : Dans Nuxt 3, useNuxtApp et useRuntimeConfig sont auto-importés, 
// mais tu peux les importer si ton linter le demande.

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
    id: number;
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

    // --- ACTIONS ---

    /**
     * 1. Récupérer la liste des professionnels avec filtres
     */
    const getProfessionals = async (domainSlug: string = '', countryCode: string = '', searchQuery: string = '') => {
        isLoading.value = true;
        error.value = null;
        
        try {
            // Utilisation de l'objet params (comme dans getContracts)
            const params: Record<string, any> = {};
            if (domainSlug) params.domain = domainSlug;
            if (countryCode) params.country = countryCode;
            if (searchQuery) params.q = searchQuery;

            const response = await $api<LegalProfessional[]>('/pro/professionals/', {
                method: 'GET',
                params
            });

            if (response) {
                // On map pour résoudre l'URL de la photo de profil (comme pour picture dans contratStore)
                professionals.value = response.map(pro => ({
                    ...pro,
                    profile_picture: resolveMediaUrl(pro.profile_picture)
                }));
                console.log('Professionnels récupérés avec succès', professionals.value);
            }
        } catch (err: any) {
            console.error('Erreur getProfessionals:', err);
            error.value = err.message || "Erreur lors de la récupération des professionnels";
            professionals.value = [];
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
    const getSpecificProfessional = (id: number) => {
        const found = professionals.value.find(p => p.id === id);
        if (found) {
            professional.value = found;
        } else {
            console.error(`Le professionnel avec l'ID ${id} est introuvable.`);
            professional.value = null;
        }
    };

    return {
        isLoading,
        error,
        professionals,
        professional,
        countries,
        domains,
        getProfessionals,
        getFilters,
        getSpecificProfessional
    };
});