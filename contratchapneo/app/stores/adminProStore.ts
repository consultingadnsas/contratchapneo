import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';

// ============================================================================
// 1. INTERFACES (Calquées sur tes serializers et models Django)
// ============================================================================

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
}

export interface LegalProfessional {
    id: string;
    first_name: string;
    last_name: string;
    title: string;
    title_display?: string; // Ajouté via le Serializer
    professional_order?: string | null;
    registration_number?: string | null;
    email: string;
    phone_number: string;
    website?: string | null;
    profile_picture?: string | File | null;
    visiting_card?: string | File | null;
    bio: string;
    years_of_experience: number;
    prix: number;
    city: string;
    is_active: boolean;
    is_verified: boolean;
    
    // Relations renvoyées par le backend
    country?: Country | null; 
    domains?: LegalDomain[]; 
    
    created_at?: string;
    updated_at?: string;
}

// ============================================================================
// 2. STORE PINIA
// ============================================================================

export const useAdminProStore = defineStore('adminProStore', () => {
    
    const { $api } = useNuxtApp();

    // --- STATE ---
    const pros = ref<LegalProfessional[]>([]);
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    // --- ACTIONS ---

    /**
     * Récupère la liste complète des professionnels pour l'admin
     */
    const fetchPros = async () => {
        isLoading.value = true;
        error.value = null;

        try {
            // Note : Adapte le préfixe de l'URL si besoin (ex: /api/pro/admin/ au lieu de /pro/admin/)
            const response = await $api<any>('/pro/admin/', { 
                method: 'GET' 
            });

            if (response) {
                // Ton ProAdminView renvoie Response({"data": serializer.data})
                const rawData = response.data ? response.data : response;
                pros.value = rawData as LegalProfessional[];
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des professionnels.";
            console.error("Erreur fetchPros:", err);
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * Ajoute un nouveau professionnel
     * On utilise FormData car le modèle contient des ImageField et FileField
     */
    const addPro = async (payload: FormData) => {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api<any>('/pro/admin/', {
                method: 'POST',
                body: payload
            });

            if (response) {
                // Ton ProAdminView renvoie Response({"data": serializer.data})
                const newPro = response.data ? response.data : response;
                pros.value.push(newPro);
                return newPro;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de l'ajout du professionnel.";
            console.error("Erreur addPro:", err);
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * Met à jour un professionnel existant
     */
    const updatePro = async (proId: string, payload: FormData) => {
        isLoading.value = true;
        error.value = null;

        try {
            // Ton ProAdminView attend un paramètre pro_id pour la méthode PUT
            const response = await $api<any>(`/pro/admin/${proId}/`, {
                method: 'PUT',
                body: payload
            });

            if (response) {
                // Ton ProAdminView renvoie Response({'data': serializer.data, 'message': '...'})
                const updatedPro = response.data ? response.data : response;
                
                const index = pros.value.findIndex(p => p.id === proId);
                if (index !== -1) {
                    pros.value.splice(index, 1, {
                        ...pros.value[index],
                        ...updatedPro
                    });
                }
                return updatedPro;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la modification du professionnel.";
            console.error("Erreur updatePro:", err);
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * Supprime un professionnel
     */
    const deletePro = async (proId: string) => {
        isLoading.value = true;
        error.value = null;

        try {
            // Ton ProAdminView attend un paramètre pro_id pour la méthode DELETE
            await $api(`/pro/admin/${proId}/`, { 
                method: 'DELETE' 
            });
            
            // Mise à jour locale de la liste
            pros.value = pros.value.filter(p => p.id !== proId);
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la suppression du professionnel.";
            console.error("Erreur deletePro:", err);
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        // État
        pros,
        isLoading,
        error,
        // Actions
        fetchPros,
        addPro,
        updatePro,
        deletePro
    };
});