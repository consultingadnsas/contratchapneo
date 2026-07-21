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

    const downloadContractFromPack = async (contrat_id: string, payload: object) => {
        isLoading.value = true;

        try {
            const response = await $api(`/contrat/packs/downloads/${contrat_id}/`, {
                method: 'POST',
                // ATTENTION : Votre backend Django s'attend à recevoir 'user_inputs' !
                body: { user_inputs: payload },
                
                // INDISPENSABLE : Indiquer à l'outil réseau de traiter la réponse comme un fichier binaire
                // Si $api utilise Axios :
                responseType: 'blob' 
                // Si $api est un wrapper de Fetch (ex: Nuxt), cela pourrait être : responseType: 'blob' ou il faudra faire await response.blob()
            });

            if (response) {
                // 1. Création d'un objet Blob (le fichier) depuis la réponse
                // (Si votre $api renvoie déjà un Blob, la ligne suivante suffit)
                const blob = new Blob([response as any], { type: 'application/pdf' });
                
                // 2. Création d'une URL temporaire pour ce fichier
                const url = window.URL.createObjectURL(blob);
                
                // 3. Création d'un lien HTML invisible
                const link = document.createElement('a');
                link.href = url;
                
                // 4. On tente de récupérer le nom du fichier depuis les headers, sinon nom par défaut
                link.setAttribute('download', 'contrat_genere.pdf'); 
                
                // 5. Ajout au document, clic forcé, puis nettoyage
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
                
                console.log("Téléchargement lancé !");
            }
        } catch (err: any) {
            console.error('Une erreur est survenue lors du téléchargement :', err);
            throw err; // Important de propager l'erreur pour que le try/catch de votre vue puisse l'attraper
        } finally {
            isLoading.value = false;
        }
    };

    return {
        // State
        isLoading, // N'oublie pas de l'exporter pour pouvoir l'utiliser dans ton v-if !
        myPacks,
        userPacks, // Exporté avec le "s"
        
        // Actions
        fetchPacks,
        getPacks,
        downloadContractFromPack
    }

}, { persist: true })