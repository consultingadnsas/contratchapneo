import { defineStore } from "pinia"
import { ref } from 'vue'
import { useNuxtApp } from '#imports' 

// ==========================================
// 1. INTERFACES (Typage strict basé sur tes modèles)
// ==========================================

export interface ContractRevision {
    id: string;
    subject: string;
    client_name?: string;
    phone_number: string;
    email: string;
    client_instructions: string;
    original_file: string; 
    revised_file: string | null; 
    price: number;
    promo_price: number;
    status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'REJECTED';
    status_display: string; // ⚡️ Le champ bonus que tu as ajouté
    is_revised: boolean;
    expert_comments: string | null;
    user: string | null;
    user_pack: string | null;
    created_at: string;
    updated_at: string;
}

export interface CustomContractRequest {
    id: string;
    subject: string;
    client_name?: string;
    category_name?: string | null;
    phone_number: string;
    email: string;
    description: string;
    price: number;
    is_wrotten: boolean;
    user: string | null;
    user_pack: string | null;
    final_document?: string | null;
    created_at: string;
    updated_at: string;
}

// ==========================================
// 2. LE STORE
// ==========================================

export const useAdminRequestsStore = defineStore('adminRequestsStore', () => {
    
    const { $api } = useNuxtApp();

    // --- STATE ---
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);
    
    const revisions = ref<ContractRevision[]>([]);
    const customRequests = ref<CustomContractRequest[]>([]);

    // ==========================================
    // ACTIONS : RÉVISIONS DE CONTRATS
    // ==========================================

    // -- Lister les révisions --
    const fetchRevisions = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            // Basé sur ton URL : path('admin-contrat/revision/', AdminContractRevision.as_view())
            const response = await $api<any>('/contrat/admin-contrat/revision/', { method: 'GET' });
            if (response && response.data) {
                revisions.value = response.data;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des révisions";
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    };

    // -- Télécharger un fichier (Original ou Révisé) --
    // -- Télécharger un fichier (Original ou Révisé) --
    const downloadRevisionFile = async (revisionId: string, fileType: 'original' | 'revised') => {
        isLoading.value = true;
        error.value = null;
        try {
            const response: any = await $api(`/contrat/admin/revisions/${revisionId}/download/?file_type=${fileType}`, {
                method: 'GET',
                responseType: 'blob'
            });

            // ⚡️ CORRECTION : On utilise le type MIME réel renvoyé par Django (Word ou PDF)
            const blob = new Blob([response], { type: response.type });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            
            // ⚡️ CORRECTION : Déduction automatique de l'extension selon le type MIME
            let ext = '.pdf'; // Par défaut
            if (response.type.includes('word') || response.type.includes('document')) {
                ext = '.docx';
            }

            link.setAttribute('download', `${fileType}_document_${revisionId}${ext}`); 
            document.body.appendChild(link);
            link.click();
            link.parentNode?.removeChild(link);
            window.URL.revokeObjectURL(url);
            
        } catch (err: any) {
            error.value = err.message || "Erreur lors du téléchargement du fichier";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // -- Mettre à jour le statut / Uploader le fichier révisé (A prévoir côté Django) --
    const updateRevision = async (revisionId: string, payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            // URL suggérée pour la mise à jour (nécessitera une vue PATCH côté Django)
            const response = await $api<any>(`/contrat/admin/revisions/${revisionId}/`, {
                method: 'PATCH',
                body: payload
            });
            if (response && response.data) {
                const index = revisions.value.findIndex(r => r.id === revisionId);
                if (index !== -1) {
                    revisions.value[index] = { ...revisions.value[index], ...response.data };
                }
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la mise à jour de la révision";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // ==========================================
    // ACTIONS : CONTRATS SUR MESURE
    // ==========================================

    // -- Lister les demandes de contrats sur mesure (A prévoir côté Django) --
    const fetchCustomRequests = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            // URL suggérée (nécessitera une vue GET IsAdminUser côté Django)
            const response = await $api<any>('/contrat/admin/custom-requests/', { method: 'GET' });
            if (response && response.data) {
                customRequests.value = response.data;
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la récupération des demandes sur mesure";
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    };

    // -- Uploader le document final du contrat sur mesure (A prévoir côté Django) --
    const completeCustomRequest = async (requestId: string, payload: FormData) => {
        isLoading.value = true;
        error.value = null;
        try {
            // URL suggérée
            const response = await $api<any>(`/contrat/admin/custom-requests/${requestId}/`, {
                method: 'PATCH',
                body: payload
            });
            if (response && response.data) {
                const index = customRequests.value.findIndex(r => r.id === requestId);
                if (index !== -1) {
                    customRequests.value[index] = { ...customRequests.value[index], ...response.data };
                }
            }
        } catch (err: any) {
            error.value = err.message || "Erreur lors de la validation du contrat sur mesure";
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        isLoading,
        error,
        revisions,
        customRequests,
        fetchRevisions,
        downloadRevisionFile,
        updateRevision,
        fetchCustomRequests,
        completeCustomRequest
    };
});