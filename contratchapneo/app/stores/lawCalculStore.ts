import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp, useRouter } from '#app';

// 1. Définition du Payload attendu par Django (SimulationDroitsSerializer)
export interface SimulationPayload {
    email: string;
    type_contrat: string;
    motif_rupture: string;
    categorie_pro: string;
    date_embauche: string;
    date_rupture: string;
    salaire_base: number;
    surtaux_accords: number;
    salaires_12_mois: number[]; // Doit être un tableau de 12 nombres maximum
    preavis_effectue: boolean;
    jours_conges_acquis: number;
}

// 2. Définition des résultats renvoyés par le backend
export interface ResultatsFinanciers {
    salaire_moyen: number;
    indemnite_licenciement: number;
    indemnite_preavis: number;
    indemnite_conges: number;
    total_droits: number;
}

export const useLawCalculStore = defineStore('lawCalcul', () => {
    // --- STATE ---
    const { $api } = useNuxtApp();
    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const resultats = ref<ResultatsFinanciers | null>(null);
    const donneesSaisies = ref<any>(null);

    // --- ACTIONS ---
    async function calculateDroits(payload: SimulationPayload) {
        isLoading.value = true;
        error.value = null;
        resultats.value = null;

        try {
            // Requête POST vers l'URL définie dans urls.py
            // Remplace $fetch par ton utilitaire Axios/$api si tu en utilises un spécifique
            const response = await $api('/lawcalcul/simulations/calculer/', {
                method: 'POST',
                body: payload
            });

            // Sauvegarde des résultats retournés par la vue Django
            resultats.value = response.resultats_financiers;
            donneesSaisies.value = response.donnees_saisies;
            
            return response;

        } catch (err: any) {
            console.error("Erreur API Calcul:", err);

            // Normalise le message d'erreur pour différents formats ($fetch, axios, DRF)
            let msg = "Une erreur est survenue lors du calcul.";

            try {
                if (err?.data) {
                    // $fetch renvoie souvent err.data
                    msg = err.data?.message || err.data?.detail || (typeof err.data === 'string' ? err.data : JSON.stringify(err.data));
                } else if (err?.response?.data) {
                    // axios-like
                    msg = err.response.data?.message || err.response.data?.detail || JSON.stringify(err.response.data);
                } else if (err?.message) {
                    msg = err.message;
                } else {
                    msg = String(err);
                }
            } catch (e) {
                msg = String(err);
            }

            error.value = msg;

            // Rethrow with a normalized Error for callers qui catchent l'exception
            throw new Error(msg);
        } finally {
            isLoading.value = false;
        }
    }

    // Fonction utilitaire pour réinitialiser le store si l'utilisateur veut refaire un calcul
    function resetSimulation() {
        resultats.value = null;
        donneesSaisies.value = null;
        error.value = null;
    }

    return {
        isLoading,
        error,
        resultats,
        donneesSaisies,
        calculateDroits,
        resetSimulation
    };
});