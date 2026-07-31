<template>
    <div class="main-wrapper flex h-screen w-full overflow-hidden bg-gray-200 relative">
        
        <div v-if="isDownloading" class="absolute inset-0 bg-white/80 z-50 flex flex-col items-center justify-center">
            <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-[#202b4a] mb-4"></div>
            <p class="text-[#202b4a] font-bold text-lg">Génération de votre contrat en cours...</p>
        </div>

        <!-- ⚡️ MODIFICATION : w-full sur mobile, lg:w-1/3 sur PC -->
        <aside class="form-section w-full lg:w-1/3 h-full p-6 overflow-y-auto bg-white shadow-2xl z-10 relative">

            <div class="mb-6">
                <h2 class="form-title">Génération sur-mesure</h2>
                <p class="form-subtitle">Remplissez les informations ci-dessous pour personnaliser ce contrat via votre pack.</p>
            </div>

            <packContractGeneratorForm 
                :contractId="contractId"
                @update-data="syncData"
                @submit-data="handleModale"
                @focus-field="handleFocusField" 
            />
            <button class="back-dashboard-btn" @click="router.push('/profile/Dashboard')">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="back-icon">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                </svg>
                <span>Retour au dashboard</span>
            </button>
        </aside>

        <!-- ⚡️ MODIFICATION : w-full sur mobile, lg:w-2/3 sur PC -->
        <div class="preview-section w-full lg:w-2/3 h-full p-8 overflow-y-auto flex justify-center items-start">
            <packsPagesPreview ref="previewRef" :contractId="contractId" />
        </div>

        <confirmModale 
            :isOpen="isOpen"
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
import contractGeneratorForm from '../../components/forms/contractGeneratorForm.vue';
import contratPreviewPage from '../../components/tools/contratPreviewPage.vue';
import confirmModale from '../../components/modale/confirmModale.vue';
import packContractGeneratorForm from '../../components/forms/packContractGeneratorForm.vue'
import packsPagesPreview from '../../components/tools/packsPagesPreview.vue'
// Import de ton store
import { useContratStore } from '../../stores/contratStore'; 
import {useProfileStore} from '../../stores/profileStore'


const route = useRoute();
const router = useRouter();
const contratStore = useContratStore();
const profileStore = useProfileStore();

// 🔥 CORRECTION ICI : On utilise un 'computed' pour être sûr à 100% que l'ID est toujours à jour
const contractId = computed(() => route.params.id as string);

const previewRef = ref<InstanceType<typeof contratPreviewPage> | null>(null);

const isOpen = ref<boolean>(false);
const isDownloading = ref<boolean>(false);
const formDataToSubmit = ref<Record<string, any>>({}); 

// Petit test au chargement pour vérifier que l'ID est bien capturé !
onMounted(() => {
    console.log("🎯 ID du contrat récupéré depuis l'URL :", contractId.value);
});

// 1. Mise à jour en temps réel sur le document A4
const syncData = (newData: Record<string, any>) => {
    if (previewRef.value) {
        previewRef.value.syncData(newData);
    }
};

// 2. Ouverture de la modale quand le formulaire est soumis
const handleModale = (data: Record<string, any>) => {
    formDataToSubmit.value = data; 
    isOpen.value = true;           
};

// 3. Soumission au backend et téléchargement direct
const submitAndDownload = async () => {
    isOpen.value = false;
    isDownloading.value = true;
    
    try {
        // 🚀 Ici on utilise bien contractId.value pour l'envoyer au backend !
        await profileStore.downloadContractFromPack(contractId.value, formDataToSubmit.value);
        console.log("Envoi des données pour le contrat ID :", contractId.value);
        console.log("Votre contrat va être téléchargé...");

        // ⚡️ LA CORRECTION : On force le rafraîchissement pour déduire le crédit de l'interface
        await profileStore.getPacks();

    } catch (err: any) {
        console.error('Erreur lors de la génération du contrat via le pack', err);
        alert(err.message || "Une erreur est survenue lors de la génération du document.");
    } finally {
        isDownloading.value = false;
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
   MISE EN PAGE GLOBALE (RESPONSIVE)
   ========================================= */
.main-wrapper {
    display: flex;
    /* ⚡️ MODIFICATION : column-reverse place l'aperçu au-dessus du formulaire sur mobile */
    flex-direction: column-reverse;
    gap: 2rem;
    padding: 1rem;
    max-width: 1400px;
    margin: 0 auto;
    background-color: #f4f6f9;
    min-height: 100vh;
}

@media (min-width: 1028px) {
    .main-wrapper {
        /* ⚡️ Sur PC, on remet côte à côte dans le bon ordre */
        flex-direction: row;
        align-items: flex-start;
        padding: 2rem;
    }
    .form-section {
        width: 100%;
        height: auto;
    }
}

/* =========================================
   FORMULAIRE (Gauche)
   ========================================= */
.form-section {
    width: fit-content;
    flex: 1;
    background: #ffffff;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    position: sticky;
    top: 2rem;
}

.form-title {
    font-size: 1.5rem;
    color: #202b4a;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.form-subtitle {
    font-size: 0.9rem;
    color: #666;
}

/* =========================================
   FAUX DOCUMENT A4 (Droite)
   ========================================= */
.preview-section {
    flex: 2;
    display: flex;
    justify-content: center;
    overflow-x: auto;
}
/* =========================================
   BOUTON RETOUR DASHBOARD
   ========================================= */
.back-dashboard-btn {
    display: inline-flex;
    align-items: center;
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
</style>