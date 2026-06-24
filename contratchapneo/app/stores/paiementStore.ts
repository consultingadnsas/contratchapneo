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

   // ── NOUVEAU : Fonction de vérification avec "Polling" (Patience) ──
    const verifyPayment = async (reference: string, maxRetries = 5): Promise<boolean> => {
        isLoading.value = true;
        error.value = null;

        // On va essayer jusqu'à 5 fois (avec 2.5s de pause = 12 secondes d'attente max)
        for (let i = 0; i < maxRetries; i++) {
            try {
                const response: any = await $api(`/payment/verify/${reference}/`, {
                    method: 'GET'
                });

                // Si Django confirme que le webhook a mis la transaction à SUCCESSFUL
                if (response && (response.status === 'success' || response.is_paid === true)) {
                    isLoading.value = false;
                    return true;
                } 
                // Si Django confirme un échec explicite (FAILED)
                else if (response && response.status === 'failed') {
                    isLoading.value = false;
                    return false; 
                } 
                // Si c'est toujours PENDING, on attend un peu que le Webhook arrive
                else {
                    console.log(`⏳ Webhook non reçu, transaction PENDING. Essai ${i+1}/${maxRetries}`);
                    await new Promise(resolve => setTimeout(resolve, 2500)); // Pause de 2.5 secondes
                }

            } catch (err: any) {
                console.error("Erreur réseau, nouvelle tentative...", err);
                await new Promise(resolve => setTimeout(resolve, 2500));
            }
        }

        // Si après 12 secondes, Xpay n'a toujours rien envoyé, on bloque (sécurité)
        isLoading.value = false;
        return false;
    }

    // ── MAGIE DE PRÉSENTATION : Simuler la réponse du Webhook ──
    const simulatePayment = async (transactionId: string, outcome: 'SUCCESS' | 'FAILED') => {
        try {
            await $api('/payment/simulate/', {
                method: 'POST',
                body: {
                    transaction_id: transactionId,
                    outcome: outcome
                }
            });
            console.log(`[Simulation Sandbox] Transaction marquée comme ${outcome} !`);
            return true;
        } catch (err) {
            console.error("Erreur lors de la simulation automatique :", err);
            return false;
        }
    }

    // ── Fonction de téléchargement (inchangée) ──
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

    return {
        isLoading,
        error,
        order,
        paiement,
        sandboxMode,
        setSandboxMode,
        verifyPayment, // <-- N'oublie pas qu'il a été ajouté ici
        simulatePayment,
        downloadContracts
    }
})