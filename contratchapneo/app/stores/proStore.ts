import { defineStore } from "pinia";
import { ref } from "vue";
import { useCartStore } from './cartStore'

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
    // --- NOUVEAU : Le verrou pour éviter les requêtes en double ---
    const isFetchingFilters = ref<boolean>(false);

    /**
     * 2. Charger les filtres (Pays et Domaines)
     */
    const getFilters = async () => {
        // SÉCURITÉ 1 : Si on a déjà les données en mémoire, on ne fait rien.
        if (countries.value.length > 0 && domains.value.length > 0) {
            return;
        }

        // SÉCURITÉ 2 : Si une requête est déjà en train de tourner, on ne fait rien.
        if (isFetchingFilters.value) {
            return;
        }

        isFetchingFilters.value = true; // On ferme le verrou !

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
        } finally {
            isFetchingFilters.value = false; // On réouvre le verrou une fois terminé
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
            const orderStore = useOrderStore();
        
            // 1. 🔒 SÉCURITÉ : Récupération de l'email de l'acheteur
            const backupEmailCookie = useCookie('backup_checkout_email');
            const email = orderStore.currentOrder?.guest?.email 
                    || orderStore.currentOrder?.user?.email 
                    || backupEmailCookie.value;

            if (!email) {
                console.warn("⚠️ Aucun email trouvé, tentative de téléchargement sans paramètre email...");
            }

            console.log(`📥 [proStore] Lancement du téléchargement pour le Pro ID : ${proId}`);
            // 🚨 Modifie l'URL ci-dessous pour qu'elle corresponde exactement à celle de ton `urls.py` Django
            const response = await $api.raw(`/pro/professionals/download/${proId}/`, {
                method: 'POST',
                responseType: 'blob', // TRÈS IMPORTANT: On dit à Nuxt qu'on attend un fichier physique !
                query: email ? { email } : undefined, // Permet à Django d'authentifier l'invité
                body: { email } // On l'envoie aussi dans le body au cas où ton API le cherche là   
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

           console.log(`✅ [proStore] Fichier téléchargé avec succès : ${filename}`);
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

    // ====================== Admin Section ========================

    // --- HELPER : Création du FormData pour gérer les fichiers et ManyToMany ---
    const buildFormData = (data: any) => {
        const formData = new FormData();
        
        for (const key in data) {
            // On ignore les valeurs nulles, indéfinies ou vides
            if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
                
                // Cas 1 : Fichiers (Images / PDF)
                if (data[key] instanceof File) {
                    formData.append(key, data[key]);
                } 
                // Cas 2 : Relations ManyToMany (ex: domains)
                else if (Array.isArray(data[key])) {
                    data[key].forEach((item: any) => {
                        const id = typeof item === 'object' ? item.id : item;
                        formData.append(key, id.toString());
                    });
                } 
                // Cas 3 : Clés étrangères (ex: country)
                else if (typeof data[key] === 'object' && data[key].id) {
                    formData.append(key, data[key].id.toString());
                }
                // Cas standard : Texte, Nombres, Booléens
                else {
                    formData.append(key, data[key].toString());
                }
            }
        }
        return formData;
    };

    /**
     * POST : Ajouter un professionnel
     */
    const addPro = async (proData: any) => {
        isLoading.value = true;
        error.value = null;
        try {
            const formData = buildFormData(proData);
            
            // (⚠️ Remplace l'URL par celle de ton fichier urls.py, ex: /pro/admin/)
            const response = await $api<any>(`/pro/admin/`, { 
                method: 'POST',
                body: formData
            });

            if (response && response.data) {
                // Ajoute le pro créé au début de la liste pour qu'il s'affiche direct
                professionals.value.unshift({
                    ...response.data,
                    profile_picture: resolveMediaUrl(response.data.profile_picture)
                });
                return true;
            }
        } catch (err: any) {
            console.error('Erreur addPro:', err);
            error.value = err.response?._data?.error || err.response?._data || "Erreur lors de la création.";
            return false;
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * PUT : Modifier un professionnel existant
     */
    const updatePro = async (id: string, proData: any) => {
        isLoading.value = true;
        error.value = null;
        try {
            const formData = buildFormData(proData);
            
            const response = await $api<any>(`/pro/admin/${id}/`, {
                method: 'PUT',
                body: formData
            });

            if (response && response.data) {
                // Met à jour le pro dans la liste locale
                const index = professionals.value.findIndex(p => p.id === id);
                if (index !== -1) {
                    professionals.value[index] = {
                        ...response.data,
                        profile_picture: resolveMediaUrl(response.data.profile_picture)
                    };
                }
                return true;
            }
        } catch (err: any) {
            console.error('Erreur updatePro:', err);
            error.value = err.response?._data?.error || err.response?._data || "Erreur lors de la modification.";
            return false;
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * DELETE : Supprimer un professionnel
     */
    const deletePro = async (id: string) => {
        isLoading.value = true;
        error.value = null;
        try {
            await $api(`/pro/admin/${id}/`, { 
                method: 'DELETE' 
            });
            
            // Retire l'élément supprimé de l'interface en temps réel
            professionals.value = professionals.value.filter(p => p.id !== id);
            return true;
        } catch (err: any) {
            console.error('Erreur deletePro:', err);
            error.value = err.response?._data?.error || "Erreur lors de la suppression.";
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
        currentPage,
        totalCount,
        pageSize,
        getProfessionals,
        getFilters,
        getSpecificProfessional,
        downloadProCard,
        addPro,
        updatePro,
        deletePro
    };
});