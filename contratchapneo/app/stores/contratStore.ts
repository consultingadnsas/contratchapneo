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
    downloads: number,
    created_at: string,
    updated_at: string
}

export const useContratStore = defineStore('contrat', ()=> {

    const {$api} = useNuxtApp();

    // Ux
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // State
    const contrat = ref<Contrat | null>(null)
    const category = ref<Category | null>(null)
    const contracts =  ref<Contrat[]>([]);
    const categories = ref<Category[]>([]);

    // Actions
    const getContracts = async()=>{
        isLoading.value = true;
        error.value = "";

        console.log('Récupération des contrats en cours → Patientez :');

        try{

            const response = await $api<Contrat[]>('/contrat/', {
                method: 'GET',
            })

            if (response){
                isLoading.value = false;
                contracts.value = response;
                console.log("Response reçue", contracts.value)
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

    return{
        isLoading,
        error,
        contrat,
        category,
        contracts,
        categories,

        // Actions
        getContracts
    }
})