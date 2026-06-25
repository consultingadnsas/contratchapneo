<template>
  <main class="preview-section">
    <div class="a4-document">
      <h1 class="doc-title reveal-text" style="animation-delay: 0.1s">
        CONTRAT DE PRESTATION DE SERVICES
      </h1>

      <p class="doc-paragraph reveal-text" style="animation-delay: 0.2s">
        Entre les soussignés :
      </p>

      <p class="doc-paragraph reveal-text" style="animation-delay: 0.3s">
        La société <strong>Contratchap SAS</strong>, dont le siège social est
        situé à
        <span class="dynamic-data">{{
          contractData.local || '[Local du client]'
        }}</span>
        , immatriculé RCCM
        <span class="dynamic-data">{{
          contractData.RCCM || '[RCCM du client]'
        }}</span>
        , représentée par 
        <span class="dynamic-data">{{
          contractData.name || "[Nom de l'entreprise / Votre nom]"
        }}</span>
      </p>

      <p class="doc-paragraph-end reveal-text" style="animation-delay: 0.4s">
        D'une part
      </p>

        <p class="doc-paragraph reveal-text" style="animation-delay: 0.5s">
            Et M./Mme/La société
            <span class="dynamic-data">{{
                contractData.nom_client || '[Nom du client]'
            }}</span>
            , de nationalité <span class="dynamic-data">{{ contractData.nationalité || '[Nationalité du client]'}}</span>

            résident à <span class="dynamic-data">{{
                contractData.adresse || '[Adresse du client]'
            }}</span>
            , né(e) le <span class="dynamic-data">{{ contractData.birthday || '[Date naissance]'}}</span>
            à <span class="dynamic-data">{{ contractData.birthday || '[Lieu naissance]'}}</span> ci-après dénommé(e) "Le Client".
        </p>

      <p class="doc-paragraph-end reveal-text" style="animation-delay: 0.4s">
        D'autre part,
      </p>

      <p class="doc-paragraph reveal-text" style="animation-delay: 0.6s">
        Il a été convenu ce qui suit, à compter du
        <span class="dynamic-data">{{ formattedDate || '[Date de début]' }}</span>
        :
      </p>

      <h3 class="doc-subtitle reveal-text" style="animation-delay: 0.7s">
        Article 1 : Objet
      </h3>
      <p class="doc-paragraph reveal-text" style="animation-delay: 0.8s">
        Le présent contrat a pour objet la fourniture de services juridiques.
        Le client s'engage à verser la somme de
        <span class="dynamic-data">{{
          contractData.montant
            ? contractData.montant + ' FCFA'
            : '[Montant]'
        }}</span>
        pour l'exécution de cette prestation.
      </p>

      <div
        class="signatures reveal-text"
        style="animation-delay: 0.9s"
      >
        <div class="sign-box">
          <p>Pour le Prestataire</p>
          <div class="sign-space"></div>
        </div>
        <div class="sign-box">
          <p>Pour le Client</p>
          <div class="sign-space"></div>
        </div>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { ref, computed } from 'vue';

export default {
  name: 'ContractPreview',
  setup() {
    const contractData = ref<Record<string, any>>({});

    const syncData = (newData: Record<string, any>) => {
      contractData.value = { ...newData };
    };

    const formattedDate = computed(() => {
      if (!contractData.value.date_contrat) return '';
      const dateObj = new Date(contractData.value.date_contrat);
      return dateObj.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    });

    const submitToBackend = (finalData: Record<string, any>) => {
      const payload = {
        contrat_id: 'someId',
        data: { ...finalData }
      };
      console.log('🚀 Envoi au backend (JSON pur) :', payload);
    };

    return {
      contractData,
      syncData,
      formattedDate,
      submitToBackend
    };
  }
};
</script>

<style scoped>
/* =========================================
   ANIMATION DE RÉVÉLATION PROGRESSIVE
   ========================================= */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.reveal-text {
  opacity: 0; /* caché avant l'animation */
  animation: fadeInUp 0.6s ease forwards;
}

/* =========================================
   FAUX DOCUMENT A4 (Droite/Bas)
   ========================================= */
.preview-section {
  flex: 2;
  display: flex;
  justify-content: center;
  overflow-x: auto;
}

.a4-document {
  background: #ffffff;
  width: 100%;
  max-width: 210mm;
  min-height: 297mm;
  padding: 12% 10%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  font-family: 'Times New Roman', Times, serif;
  color: #000000;
  line-height: 1.6;
}

.dynamic-data {
  color: #1a56db;
  background-color: rgba(26, 86, 219, 0.05);
  padding: 0 4px;
  border-radius: 2px;
}

.doc-title {
  text-align: center;
  font-size: 1.4rem;
  text-decoration: underline;
  margin-bottom: 3rem;
  text-transform: uppercase;
}

.doc-subtitle {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  text-decoration: underline;
}

.doc-paragraph {
  margin-bottom: 1.2rem;
  text-align: justify;
}

.doc-paragraph-end {
  margin-bottom: 1.2rem;
  text-align: end;
}

.signatures {
  display: flex;
  justify-content: space-between;
  margin-top: 5rem;
}

.sign-box {
  width: 40%;
}

.sign-box p {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.sign-space {
  border-top: 1px dotted #000;
  height: 100px;
  margin-top: 3rem;
}
</style>