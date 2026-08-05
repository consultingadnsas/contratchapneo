<template>
    <div class="loading-wrapper">
        <div class="loading-content">
            
            <div class="icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" 
                     class="doc-icon" 
                     :class="{ 'icon-finished': isFinished }"
                     fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
            </div>

            <h2>{{ isFinished ? 'Contrat généré avec succès !' : 'Génération de votre contrat...' }}</h2>
            
            <div class="progress-section">
                <div class="progress-track">
                    <div 
                        class="progress-fill" 
                        :class="{ 'fill-finished': isFinished }"
                        :style="{ width: `${progress}%` }"
                    ></div>
                </div>
                <div class="progress-text">
                    <span>{{ isFinished ? 'Document prêt' : 'Préparation du document' }}</span>
                    <span class="percentage">{{ progress }}%</span>
                </div>
            </div>

            <div v-if="!isFinished">
                <p class="helper-text">Veuillez patienter, Contratchap rédige vos clauses sur-mesure.</p>
            </div>
            <div v-else class="success-section">
                <p class="helper-text">Le téléchargement devrait démarrer automatiquement.</p>
                <p class="helper-text small-text">Si rien ne se passe, cliquez ci-dessous :</p>
                
                <button @click="forceDownload" class="fallback-btn" :disabled="isDownloading">
                    <svg v-if="!isDownloading" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="btn-icon">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    <svg v-else class="spinner btn-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    {{ isDownloading ? 'Téléchargement...' : 'Télécharger manuellement' }}
                </button>
                <div class="home-link-wrapper">
                    <router-link to="/" class="home-link">
                        &larr; Retourner à la page d'accueil
                    </router-link>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { usePaiementStore } from '../../stores/paiementStore';

const paiementStore = usePaiementStore();
const progress = ref(0);
const isFinished = ref(false);
const isDownloading = ref(false); // Pour éviter les clics multiples sur le bouton manuel
let intervalId = null;

onMounted(() => {
  // Simule une progression fluide mais asymétrique
  intervalId = setInterval(() => {
    if (progress.value < 50) {
      progress.value += Math.floor(Math.random() * 15) + 5; 
    } else if (progress.value < 85) {
      progress.value += Math.floor(Math.random() * 5) + 2;
    } else if (progress.value < 98) {
      progress.value += 1;
    }

    if (progress.value > 99) {
      progress.value = 99;
    }
  }, 300); 

  // Appel initial pour générer et télécharger le contrat
  paiementStore.downloadOrder().then(() => {
    progress.value = 100;
    isFinished.value = true;
    clearInterval(intervalId);
  }).catch((error) => {
    console.error('Erreur lors de la génération du contrat:', error);
    clearInterval(intervalId);
    // Tu pourrais aussi gérer l'affichage d'une erreur ici !
  });
});

// Fonction appelée si l'utilisateur clique sur le bouton manuel
const forceDownload = async () => {
    isDownloading.value = true;
    try {
        await paiementStore.downloadOrder();
    } catch (error) {
        console.error('Erreur lors du téléchargement manuel:', error);
    } finally {
        isDownloading.value = false;
    }
};

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});
</script>

<style scoped>
.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f3f4f6;
}

.loading-content {
  text-align: center;
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  max-width: 500px;
  width: 100%;
}

.icon-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.doc-icon {
  width: 64px;
  height: 64px;
  color: #2563eb;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* On arrête l'animation quand c'est fini et on met un vert de succès (optionnel) */
.icon-finished {
  animation: none;
  color: #10b981; /* Vert succès */
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: .7; transform: scale(0.95); }
}

h2 {
  color: #111827;
  font-size: 1.5rem;
  margin-bottom: 2rem;
  transition: color 0.3s;
}

.progress-section {
  margin-bottom: 2rem;
}

.progress-track {
  width: 100%;
  height: 12px;
  background-color: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background-color: #2563eb;
  border-radius: 9999px;
  transition: width 0.3s ease-out, background-color 0.5s; 
  background-image: linear-gradient(
    45deg, 
    rgba(255, 255, 255, 0.15) 25%, 
    transparent 25%, 
    transparent 50%, 
    rgba(255, 255, 255, 0.15) 50%, 
    rgba(255, 255, 255, 0.15) 75%, 
    transparent 75%, 
    transparent
  );
  background-size: 1rem 1rem;
  animation: progress-stripes 1s linear infinite;
}

/* Quand c'est à 100%, on retire l'animation zébrée et on passe en vert */
.fill-finished {
    background-image: none;
    background-color: #10b981;
    animation: none;
}

@keyframes progress-stripes {
  from { background-position: 1rem 0; }
  to { background-position: 0 0; }
}

.progress-text {
  display: flex;
  justify-content: space-between;
  margin-top: 0.75rem;
  font-size: 0.875rem;
  color: #4b5563;
  font-weight: 500;
}

.percentage {
  color: #2563eb;
  font-weight: 700;
}

.helper-text {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.small-text {
    font-size: 0.75rem;
    margin-bottom: 1rem;
}

/* --- STYLES DU BOUTON FALLBACK --- */
.success-section {
    animation: fadeIn 0.5s ease-in-out;
}

.fallback-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s, transform 0.1s;
    font-size: 0.95rem;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
}

.fallback-btn:hover:not(:disabled) {
    background-color: #1d4ed8;
}

.fallback-btn:active:not(:disabled) {
    transform: scale(0.98);
}

.fallback-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.btn-icon {
    width: 20px;
    height: 20px;
}

.spinner {
    animation: spin 1s linear infinite;
}

.home-link-wrapper {
    margin-top: 1.5rem;
}

.home-link {
    display: inline-block;
    color: #4b5563;
    font-size: 0.9rem;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.2s ease, transform 0.2s ease;
}

.home-link:hover {
    color: #2563eb;
    text-decoration: underline;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>