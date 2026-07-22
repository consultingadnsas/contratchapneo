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

    // --- ACTIONS ---

    /**
     * 1. Récupérer la liste des professionnels avec filtres
     */
    const getProfessionals = async (domainSlug: string = '', countryCode: string = '', searchQuery: string = '') => {
        isLoading.value = true;
        error.value = null;
        
        try {
            const params: Record<string, any> = {};
            if (domainSlug) params.domain = domainSlug;
            if (countryCode) params.country = countryCode;
            if (searchQuery) params.q = searchQuery;

            const response = await $api<LegalProfessional[]>('/pro/professionals/', {
                method: 'GET',
                params
            });

            if (response) {
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
    const getSpecificProfessional = (id: string) => {
        const found = professionals.value.find(p => p.id === id);
        if (found) {
            professional.value = found;
        } else {
            console.error(`Le professionnel avec l'ID ${id} est introuvable.`);
            professional.value = null;
        } 
    };

    const downloadProCard = async (proId: string) => {
        isLoading.value = true;
        error.value = null;

        try {
            // 🚨 Modifie l'URL ci-dessous pour qu'elle corresponde exactement à celle de ton `urls.py` Django
            const response = await $api.raw(`/pro/professionals/download/${proId}/`, {
                method: 'POST',
                responseType: 'blob', // TRÈS IMPORTANT: On dit à Nuxt qu'on attend un fichier physique !
            });

            // 1. Extraire le nom du fichier depuis les headers de la réponse
            let filename = `Carte_visite.pdf`; // Nom par défaut
            const contentDisposition = response.headers.get('content-disposition');
            if (contentDisposition && contentDisposition.includes('filename=')) {
                const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
                if (filenameMatch && filenameMatch.length === 2) {
                    filename = filenameMatch[1];
                }
            }

            // 2. Créer une URL Blob en mémoire et lancer le téléchargement
            const blob = response._data as Blob;
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();

            // 3. Nettoyer le DOM pour libérer la mémoire
            link.remove();
            window.URL.revokeObjectURL(url);

            return true;

        } catch (err: any) {
            console.error('Erreur lors du téléchargement de la carte:', err);
            
            // Puisqu'on a demandé un "blob", si le serveur renvoie une erreur JSON (ex: Plus de crédits), 
            // il faut re-transformer ce Blob d'erreur en texte pour lire le message.
            if (err.response && err.response._data instanceof Blob) {
                try {
                    const errorText = await err.response._data.text();
                    const errorJson = JSON.parse(errorText);
                    error.value = errorJson.error || "Erreur lors du téléchargement.";
                } catch (e) {
                    error.value = "Une erreur inattendue est survenue.";
                }
            } else {
                error.value = err.message || "Erreur de connexion.";
            }
            return false;
        } finally {
            isLoading.value = false;
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
        getProfessionals,
        getFilters,
        getSpecificProfessional,
        downloadProCard
    };
});