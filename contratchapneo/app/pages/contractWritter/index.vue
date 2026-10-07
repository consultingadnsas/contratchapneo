<template>
    <div class="main-wrapper" :class="{ 'step1-view': step === 1, 'step2-view': step === 2 }">
        
        <!-- ÉTAPE 1 : FORMULAIRE -->
        <div v-show="step === 1" class="form-container">
            <h1 class="form-title-main">Remplissez les informations</h1>
            <div class="form-box">
                <contract-generator-form 
                    @update-data="syncData"
                    @submit-data="handlePreviewStep"
                    @focus-field="handleFocusField"
                />
            </div>
        </div>

        <!-- ÉTAPE 2 : PRÉVISUALISATION -->
        <div v-show="step === 2" class="preview-container">
            <div class="preview-header">
                <button @click="step = 1" class="btn-secondary">
                    ← Retour au formulaire
                </button>
                <button @click="openConfirmModale" class="btn-primary">
                    Valider et Télécharger
                </button>
            </div>
            
            <div class="preview-content">
                <contratPreviewPage ref="previewRef" />
            </div>
        </div>

        <confirmModale 
            :isOpen="isOpen"
            @close="isOpen = false" 
            @confirm="submitToBackend" 
        />
    </div>
</template>
 
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import contractGeneratorForm from '../../components/forms/contractGeneratorForm.vue';
import contratPreviewPage from '../../components/tools/contratPreviewPage.vue';
import confirmModale from '../../components/modale/confirmModale.vue';

import { useContratStore } from '../../stores/contratStore';
import { usePaiementStore } from '../../stores/paiementStore';

const router = useRouter();

const contratStore = useContratStore();
const paiementStore = usePaiementStore();

const previewRef = ref<InstanceType<typeof contratPreviewPage> | null>(null);

const step = ref<number>(1);
const isOpen = ref<boolean>(false);
const formDataToSubmit = ref<Record<string, any>>({}); 

// 2. Le formulaire a été validé, on passe à l'étape de prévisualisation
const handlePreviewStep = (data: Record<string, any>) => {
    formDataToSubmit.value = data; 
    step.value = 2;           
};

// Ouverture de la modale de confirmation pour le téléchargement
const openConfirmModale = () => {
    isOpen.value = true;
};

// Fonction de mise à jour en temps réel sur le document A4
const syncData = (newData: Record<string, any>) => {
    if (previewRef.value) {
        previewRef.value.syncData(newData);
    }
};


// 3. L'utilisateur a cliqué sur "Valider" dans la modale
const submitToBackend = async () => {
    
    console.log("Données transmises au Store :", formDataToSubmit.value);

    // 🔥 LA CORRECTION EST ICI : Injection manuelle de l'email
    if (typeof window !== 'undefined') {
        // 1. On tente d'extraire l'email des données que l'utilisateur vient de saisir
        // (Vérifie le nom exact du champ email de ton form : 'email', 'courriel', etc.)
        const formEmail = formDataToSubmit.value.email || formDataToSubmit.value.guest_email;

        // 2. S'il y a un email, on le grave dans le localStorage pour le paiementStore
        if (formEmail) {
            localStorage.setItem('backup_checkout_email', formEmail);
            console.log("💉 Email sécurisé depuis le formulaire :", formEmail);
        }
    }

    try {
        const result = await paiementStore.generateContract(
            formDataToSubmit.value,
            contratStore.currentContratId || undefined
        );

        if(result && result.ok){ // ⚠️ Ajout de result.ok pour être plus précis
            router.push('/contractWritter/contractGenerator');
        }

        if (!result?.ok) {
            throw new Error(result?.error || 'L\'enregistrement des données a échoué.');
        }

        isOpen.value = false;
    } catch (err: any) {
        console.error('Une erreur est survenue lors de l\'enregistrement des données', err);
    }
};

const handleFocusField = (tagName: string) => {
  if (previewRef.value) {
    previewRef.value.scrollToField(tagName);
  }
};
</script>

<style scoped>
/* =========================================
   MISE EN PAGE GLOBALE
   ========================================= */
.main-wrapper {
    min-height: 100vh;
    width: 100%;
    background-color: #f3f4f6; /* bg-gray-100 */
    position: relative;
    display: flex;
    flex-direction: column;
}

.step1-view {
    overflow-y: auto;
    height: auto;
}

.step2-view {
    overflow: hidden;
    height: 100vh;
}

/* =========================================
   ÉTAPE 1 : FORMULAIRE
   ========================================= */
.form-container {
    width: 100%;
    max-width: 896px; /* max-w-4xl */
    margin: 0 auto;
    padding: 1rem;
}

@media (min-width: 768px) {
    .form-container {
        padding: 2rem;
    }
}

.form-title-main {
    font-size: 1.875rem; /* text-3xl */
    font-weight: bold;
    margin-bottom: 2rem; /* mb-8 */
    text-align: center;
    color: #202b4a;
}

.form-box {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 0.75rem; /* rounded-xl */
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* shadow-lg */
}

@media (min-width: 768px) {
    .form-box {
        padding: 2.5rem;
    }
}

/* =========================================
   ÉTAPE 2 : PRÉVISUALISATION
   ========================================= */
.preview-container {
    width: 100%;
    max-width: 1152px; /* max-w-6xl */
    margin: 0 auto;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    overflow: hidden;
}

@media (min-width: 768px) {
    .preview-container {
        padding: 2rem;
    }
}

.preview-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-shrink: 0;
}

.btn-secondary {
    padding: 0.625rem 1.25rem;
    background-color: #d1d5db; /* bg-gray-300 */
    color: #1f2937; /* text-gray-800 */
    border-radius: 0.5rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.btn-secondary:hover {
    background-color: #9ca3af; /* hover:bg-gray-400 */
}

.btn-primary {
    padding: 0.625rem 1.5rem;
    background-color: #202b4a;
    color: #ffffff;
    border-radius: 0.5rem;
    font-weight: bold;
    border: none;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    cursor: pointer;
    transition: transform 0.2s ease, background-color 0.2s ease;
}

.btn-primary:hover {
    transform: scale(1.05);
    background-color: #171f36;
}

.preview-content {
    width: 100%;
    height: 100%;
    overflow-y: auto;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-bottom: 3rem;
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
   FAUX DOCUMENT A4
   ========================================= */

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