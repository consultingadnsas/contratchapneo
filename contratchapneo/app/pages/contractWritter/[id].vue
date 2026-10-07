<template>
    <div class="main-wrapper">

        <div class="preview-container">
            <h1 class="form-title-main">Remplissez directement votre contrat</h1>
            <p class="form-subtitle-main">Cliquez sur les champs en bleu dans le document pour les remplir.</p>

            <button class="back-dashboard-btn" @click="router.push('/profile/Dashboard')">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="back-icon">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                </svg>
                <span>Retour au dashboard</span>
            </button>

            <div v-if="isMounted">
                <div v-if="hasNoTags" class="no-tags-alert">
                    Ce document ne nécessite aucune information supplémentaire. Il est prêt à être téléchargé !
                </div>

                <div class="preview-content">
                    <packsPagesPreview ref="previewRef" :contractId="contractId" @validity-change="isFormValid = $event" @tags-loaded="hasNoTags = $event" />
                </div>

                <div class="download-section">
                    <button 
                      @click="openConfirmModale" 
                      class="btn-primary" 
                      :disabled="!isFormValid"
                    >
                        Valider et Télécharger
                    </button>
                    <p v-if="!isFormValid" class="helper-text text-red">Veuillez remplir tous les champs requis pour pouvoir télécharger.</p>
                </div>
            </div>
            <div v-else style="text-align: center; margin-top: 3rem; color: #6c757d;">
                <p>Chargement du document...</p>
            </div>
        </div>

        <confirmModale 
            :isOpen="isOpen"
            :isLoading="isDownloading"
            :success="isSuccess"
            title="Valider et télécharger ?"
            description="En validant, ce contrat sera généré avec vos informations. Si ce contrat n'est pas encore débloqué, cela consommera 1 crédit de votre pack."
            @close="isOpen = false" 
            @confirm="submitAndDownload" 
        />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import confirmModale from '../../components/modale/confirmModale.vue';
import packsPagesPreview from '../../components/tools/packsPagesPreview.vue'
// Import de ton store
import { useContratStore } from '../../stores/contratStore'; 
import {useProfileStore} from '../../stores/profileStore'


const route = useRoute();
const router = useRouter();
const contratStore = useContratStore();
const profileStore = useProfileStore();
const isSuccess = ref<boolean>(false);
const isFormValid = ref<boolean>(false);
const hasNoTags = ref<boolean>(false);

// 🔥 CORRECTION ICI : On utilise un 'computed' pour être sûr à 100% que l'ID est toujours à jour
const contractId = computed(() => route.params.id as string);

const previewRef = ref<InstanceType<typeof packsPagesPreview> | null>(null);

const isOpen = ref<boolean>(false);
const isDownloading = ref<boolean>(false);
const isMounted = ref<boolean>(false);

// Petit test au chargement pour vérifier que l'ID est bien capturé !
onMounted(async () => {
    console.log("🎯 ID du contrat récupéré depuis l'URL :", contractId.value);
    if (!contratStore.tags || contratStore.tags.length === 0) {
        await contratStore.fetchContractTags(contractId.value);
    }
    isMounted.value = true;
});

// Ouverture de la modale de confirmation pour le téléchargement
const openConfirmModale = () => {
    isOpen.value = true;
};

// 3. Soumission au backend et téléchargement direct
const submitAndDownload = async () => {
    isSuccess.value = false;
    isDownloading.value = true;
    
    try {
        const formDataToSubmit = previewRef.value ? previewRef.value.getContractData() : {};
        // 🚀 Ici on utilise bien contractId.value pour l'envoyer au backend !
        await profileStore.downloadContractFromPack(contractId.value, formDataToSubmit);
        console.log("Envoi des données pour le contrat ID :", contractId.value);
        console.log("Votre contrat va être téléchargé...");

        await profileStore.getPacks();

        isSuccess.value = true;

    } catch (err: any) {
        console.error('Erreur lors de la génération du contrat via le pack', err);
        alert(err.message || "Une erreur est survenue lors de la génération du document.");
        isOpen.value = false;
    } finally {
        isDownloading.value = false;
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
   BOUTON RETOUR DASHBOARD
   ========================================= */
.back-dashboard-btn {
    display: inline-flex;
    align-items: flex-start;
    gap: 0.5rem;
    background: none;
    border: none;
    color: #64748b; /* Gris ardoise discret */
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    padding: 0.4rem 0.8rem 0.4rem 0;
    margin-bottom: 1rem;
    transition: color 0.2s ease;
    width: fit-content;
}

.back-icon {
    width: 18px;
    height: 18px;
    transition: transform 0.2s ease;
}

/* Effet au survol : le texte fonce et la flèche recule légèrement */
.back-dashboard-btn:hover {
    color: #202b4a; /* Bleu nuit profond du thème */
}

.back-dashboard-btn:hover .back-icon {
    transform: translateX(-4px);
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
    margin-bottom: 0.5rem;
    text-align: center;
    color: #202b4a;
}

.form-subtitle-main {
    text-align: center;
    color: #4b5563; /* text-gray-600 */
    margin-bottom: 2rem;
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
    min-height: 100vh;
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
    width: fit-content;
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
    width: fit-content;
}

.btn-primary:hover {
    transform: scale(1.05);
    background-color: #171f36;
}

.btn-primary:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
    transform: none;
}

.preview-content {
    width: 100%;
    overflow-y: auto;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-bottom: 3rem;
}

.download-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 2rem;
    padding-bottom: 2rem;
}

.helper-text {
    margin-top: 0.5rem;
    font-size: 0.85rem;
}
.text-red {
    color: #dc2626;
}

.no-tags-alert {
    background-color: #dcfce7;
    color: #166534;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 1px solid #bbf7d0;
}
</style>