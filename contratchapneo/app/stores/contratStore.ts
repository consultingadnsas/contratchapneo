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
    const contrat = ref<Contrat>({
        id: '',
        category: '',
        title: '',
        description: '',
        prix: 0,
        fichier_modele: '',
        picture: '',
        views: 0,
        downloads: 0,
        created_at: '',
        updated_at: ''
    })
    const category = ref<Category>({
        id: '',
        title: '',
        description: '',
        created_at: '',
        updated_at: ''
    })
    const contracts =  ref<Contrat[]>([]);
    const categories = ref<Category[]>([]);

    // Actions
    const getContracts = async()=>{
        isLoading.value = true;
        error.value = "";

        console.log('Récupération des contrats en cours → Patientez :');

        try{

            const response = await $api('/contrat/', {
                method: 'GET',
            })

            if (response){
                console.log("Response reçue", response)

                return response;
            } else {
                console.log('Problème lors de la reccupérations des contrats', response);
            }
        } catch(err:any){
            console.error('Erreu', err)
            throw err
        } finally{
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