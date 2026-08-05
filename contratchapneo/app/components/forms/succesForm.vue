<template>
  <div class="success__screen">
    
    <div class="success__icon">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="11" stroke="currentColor" stroke-width="1.5"/>
        <path d="M7 12.5L10.5 16L17 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    
    <h3 class="success__title">{{ message }}</h3>
    
    <!-- ==========================================
         1. ACHAT PRO (Carte de visite - Sans Countdown)
         ========================================== -->
    <div v-if="isPro" class="pro-actions-wrapper">
      <p class="success__subtitle">
        Votre paiement a bien été pris en compte. Vous pouvez maintenant télécharger votre carte de visite.
      </p>

      <button 
        class="btn-download-pro" 
        @click="$emit('download-pro')" 
        :disabled="isDownloading"
      >
        <svg v-if="!isDownloading" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="btn-icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        <span v-else class="loading-spinner"></span>
        <span>{{ isDownloading ? 'Téléchargement en cours...' : 'Télécharger ma carte de visite' }}</span>
      </button>

      <div class="home-link-wrapper">
        <router-link to="/" class="home-link">
          &larr; Revenir à la page d'accueil
        </router-link>
      </div>
    </div>

    <!-- ==========================================
         2. ACHAT PACK DE CRÉDITS (Countdown -> Dashboard)
         ========================================== -->
    <div v-else-if="isPack" class="success__subtitle">
      <p>
        Votre paiement a bien été pris en compte. Vos crédits ont été ajoutés à votre compte. <br>
        Redirection vers votre dashboard dans <span class="countdown-highlight">{{ countdown }}s</span>...
      </p>
    </div>

    <!-- ==========================================
         3. SUR-MESURE & RÉVISION DE CONTRAT (Countdown -> Accueil)
         ========================================== -->
    <div v-else-if="isCustomContract || isRevision" class="success__subtitle">
      <p>
        Votre demande a bien été enregistrée, un expert s'en occupera. <br>
        Redirection vers l'accueil dans <span class="countdown-highlight">{{ countdown }}s</span>...
      </p>
    </div>

    <!-- ==========================================
         4. CONTRAT STANDARD (Countdown -> ContractWritter)
         ========================================== -->
    <div v-else class="success__subtitle">
      <p>
        Votre paiement a bien été pris en compte. <br>
        Redirection vers la personnalisation de votre contrat dans <span class="countdown-highlight">{{ countdown }}s</span>...
      </p>
    </div>

  </div>
</template>

<script lang="ts">
export default {
  name: 'SuccesForm',
  props: {
    message: {
      type: String,
      default: 'Paiement effectué avec succès !'
    },
    countdown: {
      type: Number,
      required: true
    },
    isPro: {
      type: Boolean,
      default: false
    },
    isPack: {
      type: Boolean,
      default: false
    },
    isCustomContract: {
      type: Boolean,
      default: false
    },
    isRevision: {
      type: Boolean,
      default: false
    },
    isDownloading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['download-pro']
};
</script>

<style scoped>
/* ── Écran de succès ── */
.success__screen {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.25rem;
  padding: 2.5rem 1.5rem;
  text-align: center;
  animation: fadeInUp 0.4s ease both;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.success__icon {
  width: 72px;
  height: 72px;
  color: #32f459;
  animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes popIn {
  from { opacity: 0; transform: scale(0.4); }
  to   { opacity: 1; transform: scale(1); }
}

.success__title {
  color: #202b4a;
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0;
}

.success__subtitle {
  color: #4a5568;
  font-size: 1.05rem;
  line-height: 1.7;
  margin: 0;
  max-width: 480px;
}

.countdown-highlight {
  font-weight: 800;
  color: #156ca9;
  font-size: 1.15rem;
}

/* ── STYLES SPÉCIFIQUES ACTIONS PRO ── */
.pro-actions-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
  width: 100%;
  max-width: 380px;
}

.btn-download-pro {
  width: 100%;
  background-color: #202b4a;
  color: #ffffff;
  border: none;
  border-radius: 50px;
  padding: 0.95rem 1.5rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  gap: 0.6rem;
  box-shadow: 0 4px 12px rgba(32, 43, 74, 0.15);
}

.btn-download-pro:hover:not(:disabled) {
  background-color: #156ca9;
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(21, 108, 169, 0.25);
}

.btn-download-pro:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.home-link-wrapper {
  margin-top: 0.2rem;
}

.home-link {
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
}

.home-link:hover {
  color: #202b4a;
  text-decoration: underline;
}
</style>