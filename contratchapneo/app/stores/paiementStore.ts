import { useHead } from '#imports';
import { ref } from 'vue';
import { defineStore } from 'pinia';
import { useCartStore } from './cartStore'
import type { Order } from '../stores/orderStore'

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

    const order = ref<Order | null>(null)
    const paiement = ref<Paiement | null>(null)
    const sandboxMode = ref(true)

    const setSandboxMode = (enabled: boolean) => {
        sandboxMode.value = enabled
    }

    // ── TÉLÉCHARGEMENT & GARDIEN INTÉGRÉ ──
    // On ajoute un paramètre maxRetries (par défaut 5 essais = 15 secondes max)
    const downloadContracts = async (orderId: string, maxRetries = 5) => {
        isLoading.value = true;
        error.value = null;

        try {
            const cartStore = useCartStore();
            const { useOrderStore } = await import('./orderStore');
            const orderStore = useOrderStore();
            
            const email = orderStore.currentOrder?.guest?.email || 'consultingadnsas@gmail.com';

            // Boucle d'essais pour attendre le Webhook de Ngrok
            for (let i = 0; i < maxRetries; i++) {
                try {
                    const response = await $api.raw(`/payment/download/${orderId}/`, {
                        method: 'GET',
                        responseType: 'blob',
                        query: email ? { email } : undefined,
                    });

                    // Si on arrive ici, Django a autorisé le téléchargement (Commande = PAID)
                    const blob = response._data as Blob
                    const disposition = response.headers.get('Content-Disposition') || ''
                    
                    const filenameMatch = disposition.match(/filename="?([^"]+)"?/)
                    let filename = filenameMatch?.[1]

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

                    console.log("✅ Téléchargement validé et réussi pour :", filename)

                    try {
                        await cartStore.clearCart();
                    } catch (cartError) {
                        console.warn('Impossible de vider le panier:', cartError);
                    }

                    isLoading.value = false;
                    return true; // Le PDF est téléchargé avec succès !

                } catch (err: any) {
                    const statusCode = err.response?.status;
                    
                    // Si Django renvoie 403, ça veut dire que la commande est encore PENDING
                    if (statusCode === 403 && i < maxRetries - 1) {
                        console.log(`⏳ Webhook Ngrok en attente... tentative ${i + 1}/${maxRetries}`);
                        // On attend 3 secondes avant de retenter
                        await new Promise(resolve => setTimeout(resolve, 3000));
                        continue; 
                    }
                    
                    // Si c'est une autre erreur (404) ou qu'on a épuisé les essais, on déclenche l'erreur
                    throw err;
                }
            }

        } catch (err: any) {
            error.value = err.message ?? String(err)
            console.error("❌ Échec de la vérification/téléchargement :", error.value)
            isLoading.value = false
            return false
        }
    }

    return {
        isLoading,
        error,
        order,
        paiement,
        sandboxMode,
        setSandboxMode,
        downloadContracts
    }
})