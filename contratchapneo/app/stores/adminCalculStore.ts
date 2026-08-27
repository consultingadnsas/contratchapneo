import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp } from '#app';

// 1. Définition des données renvoyées par le backend pour l'historique
export interface SimulationDroit {
    id: number;
    email: string;
    type_contrat: string;
    motif_rupture: string;
    created_at: string;
    salaire_moyen: number;
    total_droits: number;
    // Ajoute d'autres champs si tu veux les afficher dans le tableau
    [key: string]: any;
}

export const useAdminCalculStore = defineStore('adminCalcul', () => {
    // --- STATE ---
    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const calculations = ref<SimulationDroit[]>([]);

    // --- ACTIONS ---
    async function fetchAllCalculations() {
        isLoading.value = true;
        error.value = null;

        try {
            const { $api } = useNuxtApp();
            
            // Requête GET vers l'URL de la liste des simulations
            const response = await $api('/lawcalcul/simulations/', {
                method: 'GET'
            });

            // On stocke les données
            // Si Django utilise la pagination (PageNumberPagination), les données sont dans response.results
            // Sinon, c'est directement response
            calculations.value = response.results || response;

            return response;

        } catch (err: any) {
            console.error("Erreur API Admin Calcul:", err);

            // Même logique de normalisation d'erreur que lawCalculStore
            let msg = "Une erreur est survenue lors de la récupération de l'historique.";

            try {
                if (err?.data) {
                    msg = err.data?.message || err.data?.detail || (typeof err.data === 'string' ? err.data : JSON.stringify(err.data));
                } else if (err?.response?.data) {
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

            // Optionnel : relancer l'erreur si le composant parent a besoin de l'attraper
            // throw new Error(msg);
        } finally {
            isLoading.value = false;
        }
    }

    // Fonction utilitaire pour vider l'historique localement si besoin (ex: déconnexion)
    function clearAdminStore() {
        calculations.value = [];
        error.value = null;
    }

    return {
        isLoading,
        error,
        calculations,
        fetchAllCalculations,
        clearAdminStore
    };
});