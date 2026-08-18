import { defineStore } from "pinia"
import { ref } from 'vue'
import { useNuxtApp } from '#imports' // Assure-toi d'avoir cet import si tu es sur Nuxt 3

export interface Packs {
    id?: string,
    title: string,
    description: string,
    prix: number,
    prix_promo?: number | null,  // ⚡️ CORRECTION : On utilise prix_promo
    isPromoActive?: boolean,     
    nombre_credits: number,
    custom_contract_included: boolean,
    nombre_customed_contract: number,
    nombre_cartes_pro: number,
    duree_validite_jours: number,
    picture?: string | File | null,
    views?: number,
    downloads?: number,
    is_active: boolean
}

export const useAdminPackStore = defineStore('adminPackId', ()=>{
    
    const { $api } = useNuxtApp();

    // --- STATE ---
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    const packs = ref<Packs[]>([]);

    // -- Action : Récupérer tous les packs --
    const fetchPacks = async () => {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api<any>('/contrat/admin-pack/', { method: 'GET' });
            if(response){
                const data = response.data ? response.data : response;
                
                packs.value = data.map((pack: any) => ({
                    ...pack,
                    prix: Number(pack.prix) || 0,
                    // ⚡️ CORRECTION : On map bien depuis pack.prix_promo
                    prix_promo: pack.prix_promo ? Number(pack.prix_promo) : null,
                    nombre_credits: Number(pack.nombre_credits) || 0,
                    nombre_customed_contract: Number(pack.nombre_customed_contract) || 0,
                    nombre_cartes_pro: Number(pack.nombre_cartes_pro) || 0,
                    duree_validite_jours: Number(pack.duree_validite_jours) || 30,
                    
                    // ⚡️ CORRECTION
                    isPromoActive: Number(pack.prix_promo) > 0
                }));
            }
        } catch(err:any){
            error.value = err.message || "Erreur lors de la récupération des packs";
            console.error(err);
        } finally{
            isLoading.value = false;
        }
    };

    // -- Action : Créer un pack --
    const addNewPack = async (payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<any>('/contrat/admin-pack/', {
                method: 'POST',
                body: payload
            });
            if (response) {
                const newPack = response.data ? response.data : response;
                // ⚡️ CORRECTION
                newPack.isPromoActive = newPack.prix_promo > 0;
                packs.value.push(newPack);
                return newPack;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de l'ajout du pack";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // -- Action : Modifier un pack --
    const updatePack = async (packId: string, payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await $api<any>(`/contrat/admin-pack/${packId}/`, {
                method: "PATCH", 
                body: payload
            });
            if (response) {
                const updatedData = response.data ? response.data : response;
                
                const index = packs.value.findIndex(p => p.id === packId);
                if (index !== -1) {
                    packs.value.splice(index, 1, {
                        ...packs.value[index],
                        ...updatedData,
                        // ⚡️ CORRECTION
                        isPromoActive: updatedData.prix_promo > 0
                    });
                }
                return updatedData;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la modification";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // -- Action : Supprimer un pack --
    const deletePack = async (packId: string) => {
        isLoading.value = true;
        try {
            await $api(`/contrat/admin-pack/${packId}/`, { method: "DELETE" });
            packs.value = packs.value.filter(p => p.id !== packId);
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la suppression";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        isLoading,
        error,
        packs,
        fetchPacks,
        addNewPack,
        updatePack,
        deletePack
    }
});