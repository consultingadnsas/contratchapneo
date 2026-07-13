<template>
  <div class="success__screen">
    <div class="success__icon">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="11" stroke="currentColor" stroke-width="1.5"/>
        <path d="M7 12.5L10.5 16L17 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    
    <h3 class="success__title">{{ displayMessage }}</h3>
    
    <p class="success__subtitle">
      {{ displaySubtitle }}
    </p>

    <!-- 1. CAS CONTRAT SIMPLE OU CARTE DE VISITE : On affiche le bouton de téléchargement -->
    <button
      v-if="productType === 'carte' || productType === 'contrat_simple'"
      class="success__download"
      :disabled="paiementStore.downloading"
      @click="handleDownload"
    >
      {{ paiementStore.downloading ? 'Téléchargement en cours...' : 'Télécharger votre document' }}
    </button>
    
    <!-- Bouton de redirection manuelle dont le texte s'adapte au produit -->
    <mainButton 
      :label="buttonLabel" 
      @click="handleManualAction"
    />
  </div>
</template>

<script lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { ref, onMounted, onUnmounted, computed } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import { usePaiementStore } from '../../stores/paiementStore';
import { useOrderStore } from '../../stores/orderStore';

export default {
  components: {
    mainButton
  },
  props: {
    message: {
      type: String,
      default: 'Paiement effectué avec succès !'
    }
  },
  emits: ['succes'],
  setup(props, { emit }) {
    
    const router = useRouter();
    const route = useRoute();
    const countdown = ref(3);
    let countdownTimer: any = null;

    const paiementStore = usePaiementStore();
    const orderStore = useOrderStore();

    // 💡 Détecter précisément le type de produit acheté
    const productType = computed(() => {
      const item: any = orderStore.currentOrder?.order_items?.[0] ?? orderStore.currentOrder?.items?.[0];

      if (!item) return 'inconnu';

      const isCustomContract = Boolean(
        item?.is_custom ||
        item?.type === 'custom_contract' ||
        item?.contrat_customed ||
        item?.customised_contract ||
        (item?.contrat && item?.is_custom)
      );

      // 🛑 CAS 1 : Contrat personnalisé (Rédacteur / Éditeur)
      if (isCustomContract) {
        return 'contrat_personnalise';
      }

      // 📄 CAS 2 : Contrat simple avec génération automatique
      if (item.contrat) {
        return 'contrat_simple';
      }

      // 📇 CAS 3 : Carte de visite
      return 'carte';
    });

    const isCustomContractOrder = computed(() => productType.value === 'contrat_personnalise');

    const displayMessage = computed(() => {
      if (isCustomContractOrder.value) {
        return 'Votre contrat sur mesure a bien été pris en charge.';
      }
      return props.message;
    });

    const displaySubtitle = computed(() => {
      if (isCustomContractOrder.value) {
        return 'Vous pouvez maintenant continuer vers l\'éditeur pour finaliser votre contrat.';
      }
      return `Vous serez redirigé dans ${countdown.value}s.`;
    });

    // Label dynamique pour le bouton principal
    const buttonLabel = computed(() => {
      if (productType.value === 'contrat_personnalise') return 'Rédiger mon contrat';
      return "Aller à la page d'accueil";
    });

    // 🔄 Redirection automatique après les 3 secondes
    const handleAutomaticRedirection = async () => {
      if (countdownTimer) clearInterval(countdownTimer);
      
      switch (productType.value) {
        case 'contrat_personnalise':
          // 🛑 ZÉRO REQUÊTE BACKEND : Redirection directe sur l'éditeur
          emit('succes'); 
          router.push('/');
          break;

        case 'contrat_simple':
          // ⬇️ Génération et téléchargement automatique du PDF, puis redirection accueil
          await paiementStore.downloadOrder();
          emit('succes');
          router.push('/contractWritter');
          break;

        case 'carte':
        default:
          // ⬇️ Téléchargement automatique de la carte, puis redirection accueil
          await paiementStore.downloadOrder();
          emit('succes');
          router.push('/');
          break;
      }
    };

    // 🖱️ Clic manuel sur le bouton principal
    const handleManualAction = () => {
      if (countdownTimer) clearInterval(countdownTimer);
      
      if (productType.value === 'contrat_personnalise') {
        emit('succes');
        router.push('/contractWritter');
      } else {
        router.push('/');
      }
    };

    // 📥 Clic manuel sur "Télécharger" (Disponible uniquement pour carte et contrat simple)
    const handleDownload = async () => {
      // Sécurité absolue : si c'est un contrat personnalisé, on bloque tout appel API
      if (productType.value === 'contrat_personnalise') return; 
      
      if (countdownTimer) clearInterval(countdownTimer);
      await paiementStore.downloadOrder();
    };

    onMounted(() => {
      if (Object.keys(route.query).length > 0) {
        router.replace({ path: route.path, query: {} });
      }

      countdownTimer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          handleAutomaticRedirection();
        }
      }, 1000);
    });

    onUnmounted(() => {
      if (countdownTimer) clearInterval(countdownTimer);
    });

    return {
      countdown,
      paiementStore,
      productType,
      displayMessage,
      displaySubtitle,
      buttonLabel,
      handleManualAction,
      handleDownload
    };
  }
}
</script>

<style scoped>
/* ── Conteneur global ── */
.payment-callback-wrapper {
  min-height: 100vh;
  background-color: #f8fafc;
}

/* ── 1. Écran de vérification (Le Spinner) ── */
.verify__screen {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  animation: fadeIn 0.3s ease;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(50, 244, 89, 0.2);
  border-top: 4px solid #32f459;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.verify__title {
  color: #202b4a;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.verify__subtitle {
    color: #4a5568;
    font-size: 1rem;
    line-height: 1.6;
}

/* ── 2. Écran de succès (Ton design d'origine) ── */
.success__screen {
  height: 100vh;
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
    color: #202b4a;
    font-size: 0.95rem;
    line-height: 1.7;
    margin: 0;
}

.success__download {
  background: #2f6dff;
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 0.9rem 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.success__download:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.success__download:hover:not(:disabled) {
    transform: translateY(-1px);
}
</style>