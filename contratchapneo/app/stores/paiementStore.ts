import { defineStore } from "pinia";
import { ref } from "vue";
import { useCartStore } from './cartStore';
import { useOrderStore } from './orderStore'; // 👈 Import classique en haut
import type { Tags } from './contratStore';

export interface Paiement {
    amount: number;
    channel: string;
    referenceNumber: string;
    customerEmail: string;
    customerFirstName: string;
    customerLastname: string;
    customerPhoneNumber: string;
    description: string;
    merchantId?: string;
    notificationURL?: string;
    returnURL?: string;
    returnContext?: string;
}

export const usePaiementStore = defineStore('paiement', () => {

    const { $api } = useNuxtApp();

    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const sandboxMode = ref(true);
    const tags = ref<Tags[] | null>(null);

    const setSandboxMode = (enabled: boolean) => {
        sandboxMode.value = enabled;
    }

    // --- FONCTION UTILITAIRE PRIVÉE ---
    // Évite de réécrire 20 lignes pour télécharger un fichier physique
    const triggerBrowserDownload = (blob: Blob, disposition: string, fallbackPrefix: string) => {
        const filenameMatch = disposition.match(/filename="?([^"]+)"?/);
        let filename = filenameMatch?.[1];

        if (!filename) {
            const isZip = blob.type === 'application/zip';
            filename = isZip ? `${fallbackPrefix}.zip` : `${fallbackPrefix}.pdf`;
        }

        const url = window.URL.createObjectURL(blob);
        const anchor = document.createElement('a');
        anchor.href = url;
        anchor.download = filename;
        document.body.appendChild(anchor);
        anchor.click();
        document.body.removeChild(anchor);
        window.URL.revokeObjectURL(url);

        return filename;
    };


    // --- ACTIONS ---

    const downloadContracts = async (orderId: string) => {
        isLoading.value = true;
        error.value = null;
        const maxRetries: number = 5;

        try {
            const cartStore = useCartStore();
            const orderStore = useOrderStore(); // 👈 Instancié à l'intérieur de l'action (évite la dépendance circulaire)
            
            const email = orderStore.currentOrder?.guest?.email;
            if (!email) throw new Error("Email manquant pour le téléchargement.");

            // Boucle d'essais pour attendre le Webhook de Ngrok
            for (let i = 0; i < maxRetries; i++) {
                try {
                    const response = await $api.raw(`/payment/download/${orderId}/`, {
                        method: 'GET',
                        responseType: 'blob',
                        query: { email },
                    });

                    // Si on arrive ici, Django a autorisé le téléchargement
                    const filename = triggerBrowserDownload(
                        response._data as Blob, 
                        response.headers.get('Content-Disposition') || '', 
                        `commande-${orderId.slice(0, 8)}`
                    );

                    console.log("✅ Téléchargement validé et réussi pour :", filename);

                    try {
                        await cartStore.clearCart();
                    } catch (cartError) {
                        console.warn('Impossible de vider le panier:', cartError);
                    }

                    return true;

                } catch (err: any) {
                    const statusCode = err.response?.status;
                    
                    // Si Django renvoie 403, ça veut dire que la commande est encore PENDING
                    if (statusCode === 403 && i < maxRetries - 1) {
                        console.log(`⏳ Paiement en attente de validation... tentative ${i + 1}/${maxRetries}`);
                        await new Promise(resolve => setTimeout(resolve, 3000));
                        continue; 
                    }
                    throw err;
                }
            }
        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error("Erreur interceptée lors du téléchargement :", error.value);
            return false;
        } finally {
            isLoading.value = false;
        }
    };

    const editContract = async (optionalContractId?: string) => {
        isLoading.value = true;
        error.value = null;

        const orderStore = useOrderStore();

        try {
            let targetId = optionalContractId;

            if (!targetId) {
                const purchasedItem =
                    orderStore.currentOrder?.order_items?.[0] ??
                    orderStore.currentOrder?.items?.[0];

                targetId = purchasedItem?.contrat_id || purchasedItem?.contrat?.id || purchasedItem?.contrat || null;
            }

            if (targetId) {
                localStorage.setItem('backup_contrat_id', targetId);
            } else {
                targetId = localStorage.getItem('backup_contrat_id');
            }

            if (!targetId) {
                throw new Error("Impossible de trouver l'ID du contrat pour extraire les balises.");
            }

            const response = await $api(`/contrat/tags/${targetId}/`, { method: 'GET' });

            tags.value = response?.tags || [];
            return tags.value;
        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error("Erreur lors de l'extraction des balises :", error.value);
            return null;
        } finally {
            isLoading.value = false;
        }
    };
      
    const generateContract = async (userInputs: Record<string, any>, _contratId?: string) => {
        isLoading.value = true;
        error.value = null;

        try {
            const orderStore = useOrderStore();
            const orderId = orderStore.currentOrder?.id;

            if (!orderId) throw new Error("Impossible de trouver l'ID de la commande à mettre à jour.");

            const email = orderStore.currentOrder?.guest?.email;
            
            await $api.raw(`/ecommerce/orders/${orderId}/`, {
                method: 'PUT',
                query: email ? { email } : undefined,
                body: { user_inputs: userInputs ?? {} },
            });

            return { ok: true, saved: true };
        } catch (err: any) {
            error.value = err.message ?? String(err);
            return { ok: false, error: error.value, saved: false };
        } finally {
            isLoading.value = false;
        }
    };

    const downloadOrder = async (orderId?: string) => {
        isLoading.value = true;
        error.value = null;

        try {
            const orderStore = useOrderStore();
            const targetOrderId = orderId || orderStore.currentOrder?.id;

            if (!targetOrderId) throw new Error("Impossible de trouver l'ID de la commande.");

            const email = orderStore.currentOrder?.guest?.email;
            
            const response = await $api.raw(`/ecommerce/orders/${targetOrderId}/download/`, {
                method: 'GET',
                responseType: 'blob',
                query: email ? { email } : undefined,
            });

            // Utilisation de notre super fonction utilitaire !
            const filename = triggerBrowserDownload(
                response._data as Blob, 
                response.headers.get('Content-Disposition') || '', 
                `Contrats_Commande_${targetOrderId.slice(0,8)}`
            );

            console.log("✅ Téléchargement réussi :", filename);
            return true;

        } catch (err: any) {
            error.value = err.message ?? String(err);
            console.error("❌ Erreur lors du téléchargement :", error.value);
            return false;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        isLoading,
        error,
        tags,
        sandboxMode,
        setSandboxMode,
        downloadContracts,
        editContract,
        generateContract,
        downloadOrder
    }
});