import { defineStore } from "pinia"
import { ref } from 'vue'

export interface Packs {
    id?: string,
    title: string,
    description: string,
    prix: number,
    promo_price?: number | null, // ⚡️ Ajout de promo_price
    isPromoActive?: boolean,     // ⚡️ Champ frontend pour gérer le switch
    nombre_credits: number,
    // Note: Le modèle Django semble ne pas retourner "contrats" directement 
    // ou alors c'est un champ spécifique. On le garde optionnel pour la souplesse.
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
    // -- Action : Récupérer tous les packs --
    const fetchPacks = async () => {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api<any>('/contrat/admin-pack/', { method: 'GET' });
            if(response){
                const data = response.data ? response.data : response;
                
                // ⚡️ LE BOUCLIER : On force le typage en Nombre pour éviter le warning "false"
                packs.value = data.map((pack: any) => ({
                    ...pack,
                    prix: Number(pack.prix) || 0,
                    promo_price: pack.promo_price ? Number(pack.promo_price) : null,
                    nombre_credits: Number(pack.nombre_credits) || 0,
                    nombre_customed_contract: Number(pack.nombre_customed_contract) || 0,
                    nombre_cartes_pro: Number(pack.nombre_cartes_pro) || 0,
                    duree_validite_jours: Number(pack.duree_validite_jours) || 30,
                    
                    isPromoActive: Number(pack.promo_price) > 0
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
                // On ajoute le champ local pour l'interface
                newPack.isPromoActive = newPack.promo_price > 0;
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
                        isPromoActive: updatedData.promo_price > 0
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