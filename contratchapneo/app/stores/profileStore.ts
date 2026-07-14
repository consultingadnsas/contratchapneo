import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#imports'; // Ajout recommandé pour Nuxt 3

export interface Mypacks {
    id?: string;
    title: string;
    description: string;
    prix: number;
    views?: number;
    download?: number;
    isActive: boolean;
}

export const useProfileStore = defineStore('profile', () => {
    
    const { $api } = useNuxtApp();
    
    // UX
    const isLoading = ref<boolean>(false);

    // State
    const myPacks = ref<Mypacks | null>(null);
    
    // 🔴 CORRECTION 1 : Renommé avec un "s" pour matcher avec ton composant Vue
    const userPacks = ref<Mypacks[]>([]); 

    // Actions
    const fetchPacks = async () => {
        // 🔴 CORRECTION 2 : On lance le chargement à "true"
        isLoading.value = true; 

        try {
            const response = await $api<Mypacks[]>('/contrat/packs/', {
                method: 'GET'
            });

            if (response) {
                userPacks.value = response;
                console.log("Les packs disponibles :", userPacks.value);
            }
        } catch (err: any) {
            console.error("Erreur lors de la récupération des packs :", err);
        } finally {
            isLoading.value = false;
        }
    }

    const getPacks = async () => {
        // 🔴 CORRECTION 2 : On lance le chargement à "true"
        isLoading.value = true; 

        try {
            const response = await $api<Mypacks[]>('/account/pack/', {
                method: 'GET'
            });

            if (response) {
                userPacks.value = response;
                
                if (userPacks.value.length > 0) {
                    console.log("Vous avez au moins un pack dans votre abonnement", userPacks.value);
                }
            }
        } catch (err: any) {
            console.error('Erreur getPacks :', err);
        } finally {
            isLoading.value = false;
        }
    }

    return {
        // State
        isLoading, // N'oublie pas de l'exporter pour pouvoir l'utiliser dans ton v-if !
        myPacks,
        userPacks, // Exporté avec le "s"
        
        // Actions
        fetchPacks,
        getPacks,
    }

}, { persist: true })