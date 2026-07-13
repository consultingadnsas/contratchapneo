import {defineStore} from 'pinia';
import {ref, computed} from 'vue';
import type {User} from '../stores/authStore';
import type {Contrat} from '../stores/contratStore'

export interface Mypacks{
    id?: string,
    title: string,
    description:string,
    prix:number,
    views?: number,
    download?: number,
    isActive: boolean
}

export const useProfileStore = defineStore('profile', ()=>{
    
    const { $api } = useNuxtApp();
    // UX
    const isLoading = ref<boolean>(false);

    // State
    const myPacks = ref<Mypacks | null>(null)

    const userPack = ref<Mypacks[]>([]);

    // Actions

    const getPacks = async()=>{

        isLoading.value = false;

        try {

            const response = await $api<Mypacks[]>('/account/pack/', 
                {method: 'GET'}
            )

            userPack.value = response;

            if(userPack.value.length > 1){

                console.log("Vous avez au moins packs dans votre abonnement", userPack.value)

            };

            console.log("reponse", response);

        } catch(err:any){

            console.error('erreur', err)
        } finally {
            isLoading.value = false;
        }

    }

    

    return{
        // State
        myPacks,
        userPack,
        getPacks,
    }

}, {persist:true})