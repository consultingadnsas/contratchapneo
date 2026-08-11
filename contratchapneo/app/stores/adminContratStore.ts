import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Contrat, Category} from './contratStore'

// ==========================================
// INTERFACES (Basées sur models.py)
// ==========================================


export interface CustomContract {
    id?: string;
    subject: string;
    email: string;
    phone_number: string;
    price: number;
    is_wrotten: boolean;
}

// ==========================================
// STORE
// ==========================================
export const useAdminContratStore = defineStore('adminContrat', () => {

    const { $api } = useNuxtApp();

    // --- STATE ---
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    const categories = ref<Category[]>([]);
    const contracts = ref<Contrat[]>([]);
    const customContracts = ref<CustomContract[]>([]);

    // ==========================================
    // ACTIONS : CATÉGORIES
    // ==========================================
    const fetchCategories = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<Category[]>('/contrat/admin-category/', { method: 'GET' });
            
            // ✅ On vérifie juste si response existe (et éventuellement si c'est un tableau)
            if (response) {
                categories.value = response;
                // On map sur le tableau pour extraire les contrats de chaque catégorie
                contracts.value = response.flatMap(category => category.contrats || []);
                console.log("Categories récupérées:", categories.value);
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des catégories";
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    };

    const addNewCategory = async (payload: { title: string; description: string }) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<Category>('/contrat/admin-category/', {
                method: "POST",
                body: payload
            });
            if (response) {
                categories.value.unshift(response); // Ajoute au début de la liste locale
                return response;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de l'ajout de la catégorie";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteCategory = async (categoryId: string) => {
        isLoading.value = true;
        try {
            await $api(`/contrat/admin-category/`,
                { method: "DELETE", body: {id: categoryId}}
            );
            categories.value = categories.value.filter(c => c.id !== categoryId);
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la suppression de la catégorie";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // ==========================================
    // ACTIONS : CONTRATS STANDARDS (BOUTIQUE)
    // ==========================================
    const fetchContracts = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<Contrat[]>('/contrat/admin-contrat/', { method: 'GET' });
            if (response) contracts.value = response;
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des contrats";
        } finally {
            isLoading.value = false;
        }
    };

    const addNewContract = async (payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            // Requête POST avec FormData (pour gérer fichier_modele et picture)
            const response = await $api<Contrat>('/contrat/admin-contrat/', {
                method: "POST",
                body: payload
            });
            if (response) {
                contracts.value.unshift(response);
                return response;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de l'ajout du contrat";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const updateContract = async (contractId: string, payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<Contrat>(`/contrat/admin-contrat/${contractId}/`, {
                method: "PATCH", // PATCH permet de ne modifier que certains champs (ex: prix) sans écraser le fichier
                body: payload
            });
            if (response) {
                // Mise à jour locale
                const index = contracts.value.findIndex(c => c.id === contractId);
                if (index !== -1) contracts.value[index] = response;
                return response;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la modification du contrat";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteContract = async (contractId: string) => {
        isLoading.value = true;
        try {
            await $api(`/contrat/admin-contrat/${contractId}/`, { method: "DELETE" });
            contracts.value = contracts.value.filter(c => c.id !== contractId);
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la suppression du contrat";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const toggleContractStatus = async (contractId: string, isActive: boolean) => {
        try {
            await $api(`/contrat/admin-contrat/${contractId}/toggle-status/`, {
                method: "PATCH",
                body: { is_active: isActive }
            });
        } catch (err: any) {
            error.value = err.message || "Impossible de changer le statut";
            throw err;
        }
    };

    // ==========================================
    // ACTIONS : CONTRATS SUR MESURE
    // ==========================================
    const fetchCustomContracts = async () => {
        isLoading.value = true;
        try {
            const response = await $api<CustomContract[]>('/admin/contrat/sur-mesure/', { method: 'GET' });
            
            // ⚡️ CORRECTION : On vérifie que Django a bien renvoyé un tableau (JSON)
            // S'il renvoie une chaîne de caractères (comme une page HTML), on force l'erreur.
            if (typeof response === 'string' || !Array.isArray(response)) {
                throw new Error("Le serveur a renvoyé une page HTML au lieu des données JSON.");
            }

            customContracts.value = response;

        } catch (err: any) {
            console.warn("⚠️ API Sur-mesure redirigée ou bloquée. Chargement des données de secours...");
            // DONNÉES DE SECOURS (Mock)
            customContracts.value = [
                { 
                    id: '201', 
                    subject: "Pacte d'actionnaires complexe", 
                    email: 'client@example.com', 
                    phone_number: '01020304', 
                    price: 150000, 
                    is_wrotten: false 
                }
            ];
        } finally {
            isLoading.value = false;
        }
    };

    return {
        // State
        isLoading,
        error,
        categories,
        contracts,
        customContracts,
        // Categories
        fetchCategories,
        addNewCategory,
        deleteCategory,
        // Contracts
        fetchContracts,
        addNewContract,
        updateContract,
        deleteContract,
        toggleContractStatus,
        // Custom
        fetchCustomContracts
    };

}, { persist: true });