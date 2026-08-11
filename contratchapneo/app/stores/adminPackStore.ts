import { defineStore } from "pinia"
import { ref } from 'vue'
import type {Contrat} from "./contratStore"

export interface Packs{
    id: string,
    title: string,
    description: string,
    prix: number,
    nombre_credits: number,
    contrats: Contrat,
    custom_contract_included: boolean,
    nombre_customed_contract: number,
    consultation_pro_incluse: number,
    duree_validite_jours: number
    picture: string,
    views: number,
    downloads: number,
    is_active: boolean
}

export const useAdminPackStore = defineStore('adminPackId', ()=>{
    
    const { $api } = useNuxtApp();

    // --- STATE ---
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    const packs = ref<Packs[]>([]);


    // --  Action --
    async function fetchPacks(){
        
        isLoading.value = true;
        error.value = null;

        try {

            const response = await $api<Packs[]>('/contrat/admin-pack/', {
                method: 'GET'
            })

            if(response){
                packs.value = response;
            }

            console.log("Les packs côté admin", response)

        } catch(err:any){
            console.error(err);
        } finally{
            isLoading.value = false;
        }
    }

    return{
        isLoading,
        error,
        packs,
        fetchPacks
    }

})