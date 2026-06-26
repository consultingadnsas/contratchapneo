<template>
  <div class="main-wrapper">
    
    <aside class="form-section">
        <h2 class="form-title flex gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            </svg>
            Remplir le contrat
        </h2>
        <p class="form-subtitle">Vos modifications s'affichent en temps réel sur le document.</p>

        <contract-generator-form 
            @update-data="syncData"
            @submit-data="submitToBackend"
        />
    </aside>

    <contratPreviewPage ref="previewRef" />

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import contractGeneratorForm from '../../components/forms/contractGeneratorForm.vue';
import contratPreviewPage from '../../components/tools/contratPreviewPage.vue';

const route = useRoute();

// 1. Référence vers le composant enfant (le document A4)
const previewRef = ref<InstanceType<typeof contratPreviewPage> | null>(null);

// 2. Fonction déclenchée à chaque frappe dans le formulaire (Temps Réel)
const syncData = (newData: Record<string, any>) => {
  // On vérifie que le composant A4 est bien chargé
  if (previewRef.value) {
    // On appelle la fonction `syncData` qui est à l'intérieur de contratPreviewPage.vue
    previewRef.value.syncData(newData);
  }
};

// 3. Fonction déclenchée au clic sur "Valider les informations"
const submitToBackend = (finalData: Record<string, any>) => {
  console.log("Les données finales prêtes pour l'API :", finalData);
  
  // Tu peux soit appeler ton API ici (ce qui est recommandé),
  // soit appeler la fonction submitToBackend de ton A4 comme ceci :
  if (previewRef.value && previewRef.value.submitToBackend) {
     previewRef.value.submitToBackend(finalData);
  }
};
</script>

<style scoped>
/* =========================================
   MISE EN PAGE GLOBALE (RESPONSIVE)
   ========================================= */
.main-wrapper {
    display: flex;
    flex-direction: column; /* Sur mobile : on empile */
    gap: 2rem;
    padding: 1rem;
    max-width: 1400px;
    margin: 0 auto;
    background-color: #f4f6f9; /* Petit fond gris léger pour contraster avec la page A4 */
    min-height: 100vh;
}

/* Écrans de tablette et PC : on met côte à côte */
@media (min-width: 992px) {
    .main-wrapper {
        flex-direction: row;
        align-items: flex-start;
        padding: 2rem;
    }
}

/* =========================================
   FORMULAIRE (Gauché/Haut)
   ========================================= */
.form-section {
    flex: 1;
    background: #ffffff;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    position: sticky; /* Reste visible quand on scroll le document sur PC */
    top: 2rem;
}

.form-title {
    font-size: 1.5rem;
    color: #202b4a; /* Bleu Contratchap */
    margin-bottom: 0.5rem;
}

.form-subtitle {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 2rem;
}

.input-group {
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.input-group label {
    font-weight: 600;
    font-size: 0.95rem;
    color: #333;
}

.input-group input {
    padding: 0.8rem 1rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
}

.input-group input:focus {
    outline: none;
    border-color: #202b4a;
}

.submit-btn {
    width: 100%;
    padding: 1rem;
    background-color: #202b4a;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
    transition: background-color 0.2s, transform 0.1s;
}

.submit-btn:hover {
    background-color: #2c3a61;
}
.submit-btn:active {
    transform: scale(0.98);
}

/* =========================================
   FAUX DOCUMENT A4 (Droite/Bas)
   ========================================= */
.preview-section {
    flex: 2; /* Prend deux fois plus de place que le formulaire sur PC */
    display: flex;
    justify-content: center;
    overflow-x: auto; /* Permet de scroller horizontalement sur mobile si nécessaire */
}

.a4-document {
    background: #ffffff;
    width: 100%;
    max-width: 210mm; /* Largeur exacte d'un A4 */
    min-height: 297mm; /* Hauteur exacte d'un A4 */
    padding: 12% 10%; /* Marges intérieures typiques d'un Word */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
    
    /* Typographie juridique */
    font-family: 'Times New Roman', Times, serif;
    color: #000000;
    line-height: 1.6;
}

/* Style des textes remplis dynamiquement */
.dynamic-data {
    color: #1a56db; /* Bleu pour montrer que c'est une variable */
    background-color: rgba(26, 86, 219, 0.05); /* Surlignage très léger */
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