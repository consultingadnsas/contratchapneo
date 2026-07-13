import {defineStore} from 'pinia';
import {ref, computed} from 'vue';
import type {User} from '../stores/authStore';

export const useProfileStore = defineStore('profile', ()=>{

    const { $api } = useNuxtApp();
    // UX
    const isLoading = ref<boolean>(false);

    const user = ref<User|null>(null);

    // Action 

    const getProfile = async () => {

        isLoading.value = true;

        try {
            const response = await $api<User>('/account/me/',{
                method: 'GET',
            });

            if(response){

                user.value = response;

                console.log(user.value);

            }
        } catch (err: any) {
            throw err
        } finally {
            isLoading.value = false;
        }

    }

    return{
        isLoading,
        user,
        getProfile
    }

}, {persist:true})