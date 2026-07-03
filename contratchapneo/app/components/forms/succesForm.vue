<template>
  <div class="success__screen">
    <div class="success__icon">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="11" stroke="currentColor" stroke-width="1.5"/>
        <path d="M7 12.5L10.5 16L17 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <h3 class="success__title">{{ message }}</h3>
    
    <p class="success__subtitle">
      <span v-if="isContract">Vous allez être redirigé vers l'éditeur dans <span>{{ countdown }}s</span>.</span>
      <span v-else>Votre téléchargement va démarrer dans <span>{{ countdown }}s</span>.</span>
    </p>

    <button
      class="success__download"
      :disabled="paiementStore.isLoading"
      @click="handleSuccessAction"
    >
      <span v-if="paiementStore.isLoading">Téléchargement en cours...</span>
      <span v-else>{{ isContract ? "Aller à l'éditeur maintenant" : "Télécharger ma carte" }}</span>
    </button>

    <mainButton 
      label="Retour à l'accueil" 
      @click="()=>router.push('/')"
    />
  </div>
</template>

<script lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { ref, onMounted, onUnmounted, computed } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import { usePaiementStore } from '../../stores/paiementStore';
import { useOrderStore } from '../../stores/orderStore'; // 👈 Import du store de commande

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
    const orderStore = useOrderStore(); // 👈 Initialisation du store

    // 💡 Déterminer intelligemment ce que l'utilisateur a acheté
    const isContract = computed(() => {
      // On récupère le premier article de la commande
      const item = orderStore.currentOrder?.order_items?.[0] ?? orderStore.currentOrder?.items?.[0];
      
      // À ADAPTER SELON TON BACKEND : 
      // Ici je pars du principe que si l'objet possède une propriété "contrat", c'est un contrat.
      // Sinon (ex: ça pourrait être "professional_card" ou tu peux vérifier item.type), c'est une carte.
      return !!item?.contrat; 
    });

    // 💡 La nouvelle fonction de routage intelligent
    const handleSuccessAction = async () => {
      // On arrête le compteur s'il est cliqué manuellement
      if (countdownTimer) clearInterval(countdownTimer);
      
      if (isContract.value) {
        // ➡️ PARCOURS CONTRAT : On va à l'éditeur
        emit('succes'); 
        router.push('/contractWritter');
      } else {
        // ⬇️ PARCOURS CARTE DE VISITE : On télécharge
        const success = await paiementStore.downloadOrder();
        if (success) {
           emit('succes');
           // Optionnel : tu peux rediriger vers l'accueil après le téléchargement
           // router.push('/');
        }
      }
    };

    onMounted(() => {
      if (Object.keys(route.query).length > 0) {
        router.replace({ path: route.path, query: {} });
      }

      countdownTimer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          handleSuccessAction(); // 👈 On lance l'action calculée quand le temps est écoulé
        }
      }, 1000);
    });

    onUnmounted(() => {
      if (countdownTimer) clearInterval(countdownTimer);
    });

    return {
      router,
      countdown,
      paiementStore,
      isContract,
      handleSuccessAction
    };
  }
}
</script>

<style scoped>
/* ── Écran de succès ── */
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
    color: #202b4a;
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