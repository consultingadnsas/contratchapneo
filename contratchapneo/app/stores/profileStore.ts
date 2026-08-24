import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useNuxtApp } from '#imports';

export interface Mypacks {
    id?: string;
    title: string;
    description: string;
    prix: number;
    views?: number;
    download?: number;
    is_active: boolean; 
    credits_restants?: number;
    customs_restants?: number;
    cartes_pro_restantes?: number;
    date_expiration?: string;
}

export const useProfileStore = defineStore('profile', () => {
    
    const { $api } = useNuxtApp();
    
    // UX
    const isLoading = ref<boolean>(false);

    // ⚡️ CORRECTION : On sépare les packs possédés et les packs de la boutique
    const myPacks = ref<Mypacks | null>(null);
    const userPacks = ref<Mypacks[]>([]); // 👈 Stocke TOUS les packs achetés (actifs + historique)
    const availablePacks = ref<Mypacks[]>([]); // Packs de la boutique
    // ==========================================
    // ⚡️ NOUVEAU : GETTERS PINIA REUTILISABLES
    // ==========================================
    const activePacks = computed(() => {
        return userPacks.value.filter(pack => pack.is_active === true);
    });

    const expiredPacks = computed(() => {
        return userPacks.value
            .filter(pack => pack.is_active === false)
            .slice(0, 1); // Retourne un tableau avec au maximum 1 seul pack !
    });

    // Actions
    const fetchPacks = async () => {
        isLoading.value = true; 
        try {
            const response = await $api<Mypacks[]>('/contrat/packs/', {
                method: 'GET'
            });

            if (response) {
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
                // ⚡️ CORRECTION : On enregistre tout l'historique renvoyé par Django !
                userPacks.value = response;
                
                if (activePacks.value.length > 0) {
                    console.log("Vous avez au moins un pack actif :", activePacks.value);
                } else if (expiredPacks.value.length > 0) {
                    console.log("Abonnement expiré, packs à renouveler :", expiredPacks.value);
                } else {
                    console.log("Aucun pack acheté pour le moment.");
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
                // Utiliser la variante "raw" pour récupérer le Response complet (headers + body)
                const rawResp: any = await ($api as any).raw(`/contrat/packs/downloads/${contrat_id}/`, {
                    method: 'POST',
                    body: { user_inputs: payload },
                    responseType: 'blob'
                });

                if (rawResp && rawResp._data) {
                    const responseBlob = rawResp._data as Blob;
                    // Essayer d'extraire le content-type et le filename depuis les headers
                    const contentType = rawResp.headers.get('content-type') || responseBlob.type || '';
                    const disposition = rawResp.headers.get('content-disposition') || '';

                    // Récupération du nom de fichier depuis Content-Disposition si présent
                    let filename = 'contrat_genere';
                    const match = /filename\*=UTF-8''(.+)|filename="?([^\";]+)"?/.exec(disposition);
                    if (match) {
                        filename = decodeURIComponent((match[1] || match[2] || filename).trim());
                    } else if (contrat_id) {
                        filename = `contrat_${contrat_id}`;
                    }

                    // Déterminer l'extension à partir du content-type
                    let ext = '.pdf';
                    if (contentType.includes('word') || contentType.includes('offic') || filename.toLowerCase().endsWith('.docx')) {
                        ext = '.docx';
                    }

                    const blob = new Blob([responseBlob], { type: contentType || (ext === '.docx' ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : 'application/pdf') });
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', filename.endsWith(ext) ? filename : `${filename}${ext}`);
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(url);

                    console.log('Téléchargement lancé !');
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

    const customContract = async (payload: object)=> {

        isLoading.value = true;

        try{
            const response = await $api('/contrat/packs/custom_contract/',{
                method: 'POST',
                body:payload
            })

            if(response){
                console.log("Formulaire soumis avec succès!")
            }
        } catch(error){
            console.error('Un problème est survenu lors de la soumission du formulaire');
            throw error
        } finally {
            isLoading.value = false;
        }

    }

    return {
        isLoading, 
        myPacks,
        userPacks, 
        availablePacks, // 👈 NOUVEAU : On exporte la liste de la boutique
        activePacks,   // 👈 NOUVEAU : Exporter les packs actifs
        expiredPacks,  // 👈 NOUVEAU : Exporter les packs expirés
        
        fetchPacks,
        getPacks,
        downloadContractFromPack,
        clearLocalProfile,
        customContract
    }

}, { persist: true })