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
    const addNewCategory = async(categoryTitle:string|'')=>{

        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api('/contrat/admin-category/', {
                method:"POST",
                body: {
                    title: categoryTitle,
                    description: ""
                }
            })
            if(response){
                console.log("Ajout de catégorie réussie", response)
                return response
            }
        } catch(err:any){
            error.value = err.message || "Erreur lors de l'ajout de catégorie"
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