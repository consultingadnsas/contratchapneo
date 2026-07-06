import {defineStore} from 'pinia';
import {ref, computed} from 'vue';
import type {Category, Contrat, PaginatedResponse, Tags} from './contratStore';


export const useAdminContratStore = defineStore('adminContrat', ()=>{

    const { $api } = useNuxtApp()

    // State
    const isLoading = ref<boolean>(false);
    const error = ref<null | string>(null);

    const category = ref<Category | string>('');

    // Compute

    // Actions
    const addNewCategory = async(category:string|'')=>{

        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api('/contrat/admin-catgory/', {
                method:"POST",
                body:category
            })
            if(response){
                console.log("Ajout de catégorie réussie")
            }
        } catch(err:any){
            console.error("Un soucis est intervenue:", err)
        } finally{
            isLoading.value = false;
        }

    }

    return{
        isLoading,
        error,
        addNewCategory
    }

}, {persist:true})