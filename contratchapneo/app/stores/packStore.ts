import { defineStore } from 'pinia';

// Typage calqué sur ton modèle Pack Django
export interface Pack {
  id: string;
  title: string;
  description: string;
  prix: number | string;
  prix_promo: number | string;
  nombre_credits: number;
  contrats: any[]; 
  custom_contract_included: boolean;
  nombre_customed_contract: number;
  consultation_pro_incluse: boolean;
  nombre_cartes_pro: number;
  duree_validite_jours: number;
  picture: string | null;
  views: number;
  downloads: number;
  is_active: boolean;
}

export const usePackStore = defineStore('pack', {
  state: () => ({
    packs: [] as Pack[],
    isLoading: false,
    error: null as string | null,
  }),

  actions: {
    // --------------------------------------------------
    // 1. LISTER LES PACKS (VUE PUBLIQUE)
    // --------------------------------------------------
    async fetchPacks() {
      if (this.packs.length > 0) return;

      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp(); 

      try {
        const response: any = await $api('/contrat/packs/', {
          method: 'GET'
        });

        if (response && Array.isArray(response.results)) {
            this.packs = response.results;
        } else if (response && Array.isArray(response.data)) {
            this.packs = response.data;
        } else if (Array.isArray(response)) {
            this.packs = response;
        } else {
            this.packs = [];
        }
      } catch (err: any) {
        console.error("Erreur (fetchPacks) :", err);
        this.error = err.response?._data?.message || "Impossible de charger les offres pour le moment.";
      } finally {
        this.isLoading = false;
      }
    },

    // --------------------------------------------------
    // 2. TÉLÉCHARGER UN CONTRAT DEPUIS UN PACK
    // --------------------------------------------------
    async downloadContractFromPack(contractId: string) {
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp();

      try {
        // L'utilisation de responseType: 'blob' est vitale pour récupérer un fichier (PDF/Word)
        const response: any = await $api(`/contrat/packs/downloads/${contractId}/`, {
          method: 'GET',
          responseType: 'blob' 
        });

        // Création d'un lien invisible pour forcer le téléchargement du fichier par le navigateur
        const url = window.URL.createObjectURL(new Blob([response]));
        const link = document.createElement('a');
        link.href = url;
        
        // Optionnel : on peut mettre un nom par défaut, 
        // ou extraire le nom réel si le backend renvoie le header 'Content-Disposition'
        link.setAttribute('download', `Document_${contractId}.pdf`); 
        document.body.appendChild(link);
        link.click();
        
        // Nettoyage
        link.parentNode?.removeChild(link);
        window.URL.revokeObjectURL(url);
        
      } catch (err: any) {
        console.error(`Erreur (downloadContractFromPack ${contractId}) :`, err);
        this.error = err.response?._data?.message || "Le téléchargement du contrat a échoué.";
        throw err; // On renvoie l'erreur pour pouvoir afficher un toast/alerte côté Vue
      } finally {
        this.isLoading = false;
      }
    },

    // --------------------------------------------------
    // 3. DEMANDER UN CONTRAT SUR MESURE VIA UN PACK
    // --------------------------------------------------
    async requestCustomContractFromPack(payload: any) {
      this.isLoading = true;
      this.error = null;
      const { $api } = useNuxtApp();

      try {
        // Envoi des données (POST) pour initier la demande de contrat sur mesure
        const response: any = await $api('/contrat/packs/custom_contract/', {
          method: 'POST',
          body: payload
        });
        
        return response;
      } catch (err: any) {
        console.error("Erreur (requestCustomContractFromPack) :", err);
        this.error = err.response?._data?.message || "Impossible de soumettre la demande sur mesure.";
        throw err;
      } finally {
        this.isLoading = false;
      }
    }
  },
  
  getters: {
    activePacks: (state) => state.packs.filter((p) => p.is_active),
    totalPacks: (state) => state.packs.length
  }
});