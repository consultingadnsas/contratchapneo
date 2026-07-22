import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#imports';

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

    // ⚡️ CORRECTION : On sépare les packs possédés et les packs de la boutique
    const myPacks = ref<Mypacks | null>(null);
    const userPacks = ref<Mypacks[]>([]); // Packs ACHETÉS par l'utilisateur
    const availablePacks = ref<Mypacks[]>([]); // Packs DISPONIBLES dans la boutique

    // Actions
    const fetchPacks = async () => {
        isLoading.value = true; 
        try {
            const response = await $api<Mypacks[]>('/contrat/packs/', {
                method: 'GET'
            });

            if (response) {
                // ⚡️ CORRECTION : On assigne aux packs de la boutique
                availablePacks.value = response;
                console.log("Les packs disponibles :", availablePacks.value);
            }
        } catch (err: any) {
            console.error("Erreur lors de la récupération des packs :", err);
        } finally {
            isLoading.value = false;
        }
    }

    const getPacks = async () => {
        isLoading.value = true; 

        try {
            const response = await $api<Mypacks[]>('/account/pack/', {
                method: 'GET'
            });

            if (response) {
                // ⚡️ CORRECTION : On assigne aux packs de l'utilisateur
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

    const downloadContractFromPack = async (contrat_id: string, payload: object) => {
        isLoading.value = true;

        try {
            const response = await $api(`/contrat/packs/downloads/${contrat_id}/`, {
                method: 'POST',
                body: { user_inputs: payload },
                responseType: 'blob' 
            });

            if (response) {
                const blob = new Blob([response as any], { type: 'application/pdf' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'contrat_genere.pdf'); 
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
                
                console.log("Téléchargement lancé !");
            }
        } catch (err: any) {
            console.error('Une erreur est survenue lors du téléchargement :', err);
            throw err; 
        } finally {
            isLoading.value = false;
        }
    };

    const clearLocalProfile = () => {
        userPacks.value = [];
        myPacks.value = null;
        // On ne vide pas availablePacks car c'est la vitrine publique
        console.log('[ProfileStore] Données profil local vidées suite à la déconnexion.');
    };

    return {
        isLoading, 
        myPacks,
        userPacks, 
        availablePacks, // 👈 NOUVEAU : On exporte la liste de la boutique
        
        fetchPacks,
        getPacks,
        downloadContractFromPack,
        clearLocalProfile
    }

}, { persist: true })