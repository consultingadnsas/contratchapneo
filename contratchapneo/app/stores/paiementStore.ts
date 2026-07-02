import { useHead } from '#imports';
import { ref } from 'vue';
import { defineStore } from 'pinia';
import { useCartStore } from './cartStore'
import type { Order } from '../stores/orderStore'

import type { Tags } from './contratStore'

/*
{
  "merchantId": "PP-F324",
  "amount": 1000,
  "description": "Abonnement Premium",
  "channel": "CARD",
  "countryCurrencyCode": "952",
  "referenceNumber": "REF-772105",
  "customerEmail": "test@gmail.com",
  "customerFirstName": "Ishola",
  "customerLastname": "Lamine",
  "customerPhoneNumber": "01234567",
  "notificationURL": "https://votre-site.com/webhook",
  "returnURL": "https://votre-site.com/retour",
  "returnContext": "{\"order_id\":\"123\", \"user\":\"88\"}"
}
*/

export interface Paiement {
    amount: number,
    channel: string,
    referenceNumber: string,
    customerEmail: string,
    customerFirstName: string,
    customerLastname: string,
    customerPhoneNumber: string,
    description: string,
    merchantId?: string,
    notificationURL?: string,
    returnURL?: string,
    returnContext?: string,
}

export const usePaiementStore = defineStore('paiement', () => {

    const { $api } = useNuxtApp();

    const isLoading = ref(false);

    const error = ref<string | null>(null);

    //
    const order = ref<Order | null>(null)

    const paiement = ref<Paiement | null>(null)

    const sandboxMode = ref(true)

    const setSandboxMode = (enabled: boolean) => {
        sandboxMode.value = enabled
    }

    // State

    const tags = ref<Tags[] | null>(null);

    // Actions

    const downloadContracts = async (orderId: string) => {

        isLoading.value = true;
        error.value = null;

        try {
            const cartStore = useCartStore();

            const { useOrderStore } = await import('./orderStore');
            const orderStore = useOrderStore();
            
            // ⚠️ Remets la ligne dynamique pour la production !
            const email = orderStore.currentOrder?.guest?.email || 'consultingadnsas@gmail.com';

            // 1. On laisse l'objet "query" construire les paramètres d'URL proprement
            const response = await $api.raw(`/payment/download/${orderId}/`, {
                method: 'GET',
                responseType: 'blob',
                query: email ? { email } : undefined,
            })

            const blob = response._data as Blob
            const disposition = response.headers.get('Content-Disposition') || ''
            
            // Regex un peu plus robuste pour attraper le nom du fichier
            const filenameMatch = disposition.match(/filename="?([^"]+)"?/)
            
            let filename = filenameMatch?.[1]

            // 2. Fallback intelligent basé sur le type MIME si le header est vide
            if (!filename) {
                const isZip = blob.type === 'application/zip'
                filename = isZip ? `commande-${orderId.slice(0,8)}.zip` : `contrat-${orderId.slice(0,8)}.pdf`
            }

            const url = window.URL.createObjectURL(blob)
            const anchor = document.createElement('a')
            anchor.href = url
            anchor.download = filename
            document.body.appendChild(anchor)
            anchor.click()
            document.body.removeChild(anchor)
            window.URL.revokeObjectURL(url)

            console.log("Téléchargement réussi pour :", filename)

            return true
        } catch (err: any) {
            error.value = err.message ?? String(err)
            console.error("Erreur interceptée lors du téléchargement :", error.value)
            return false
        } finally {
            isLoading.value = false
        }
    }

    const editContract = async (optionalContractId?: string) => {
        isLoading.value = true;
        error.value = null;

        const { useOrderStore } = await import('./orderStore');
        const orderStore = useOrderStore();

        try {
            // 1. Détermination de l'ID du contrat
            let targetId = optionalContractId;

            // Si on ne lui passe pas d'ID explicitement, on fouille dans la commande !
            if (!targetId) {
                const purchasedItem =
                    orderStore.currentOrder?.order_items?.[0] ??
                    orderStore.currentOrder?.items?.[0];

                targetId = purchasedItem?.contrat_id || purchasedItem?.contrat?.id || purchasedItem?.contrat || null;
            }

            // PLAN C (Le fameux parachute au cas où !)
            if (targetId) {
                localStorage.setItem('backup_contrat_id', targetId);
            } else {
                targetId = localStorage.getItem('backup_contrat_id');
            }

            // Si on n'a vraiment rien trouvé, on bloque tout
            if (!targetId) {
                throw new Error("Impossible de trouver l'ID du contrat pour extraire les balises.");
            }

            console.log("ID du contrat trouvé pour extraction :", targetId);

            // 2. Appel à l'API
            // ⚠️ J'ai corrigé "contract" par "contrat" dans l'URL pour être cohérent avec ton backend
            const response = await $api(`/contrat/tags/${targetId}/`, {
                method: 'GET'
            });

            console.log("Réponse de l'API pour l'édition", response);

            // 3. Stockage des tags extraits
            tags.value = response?.tags || [];

            console.log("Tags extraits avec succès pour l'édition :", tags.value);

            return tags.value;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error("Erreur lors de l'extraction des balises du contrat", error.value);
            return null;
        } finally {
            isLoading.value = false;
        }
    }

      
    const generateContract = async (userInputs: Record<string, any>, _contratId?: string) => {
        isLoading.value = true;
        error.value = null;

        try {
            const { useOrderStore } = await import('./orderStore');
            const orderStore = useOrderStore();

            const orderId = orderStore.currentOrder?.id;

            if (!orderId) {
                throw new Error("Impossible de trouver l'ID de la commande à mettre à jour.");
            }

            const email = orderStore.currentOrder?.guest?.email || 'consultingadnsas@gmail.com';
            await $api.raw(`/ecommerce/orders/${orderId}/?email=${email}`, {
                method: 'PUT',
                body: {
                    user_inputs: userInputs ?? {},
                },
            });

            console.log('Données utilisateur enregistrées dans user_inputs :', userInputs);
            return { ok: true, saved: true };
        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error('Erreur lors de l’enregistrement des données utilisateur', error.value);
            return { ok: false, error: error.value, saved: false };
        } finally {
            isLoading.value = false;
        }
    }

    return {
        isLoading,
        error,
        order,
        tags,
        paiement,
        sandboxMode,
        setSandboxMode,
        downloadContracts,
        editContract,
        generateContract
    }
})