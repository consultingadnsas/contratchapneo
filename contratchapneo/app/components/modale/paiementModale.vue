<template>
  <div v-if="isOpen" class="glass-modal-overlay" @click="closeModal">
    <div class="stripe-modal-content" @click.stop>
      <button class="close-btn" @click="closeModal" :disabled="isLoading" aria-label="Fermer">×</button>
      
      <div class="stripe-container">
        <h3>Paiement par Carte Bancaire</h3>
        
        <div id="payment-element" class="stripe-element-container"></div>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <button 
          class="btn-pay" 
          @click="handleSubmit" 
          :disabled="isLoading || !isStripeReady"
        >
          {{ isLoading ? 'Traitement sécurisé...' : 'Confirmer le règlement' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, watch, onUnmounted, nextTick } from 'vue';
import { loadStripe } from '@stripe/stripe-js';

export default {
  name: 'PaiementModale',

  props: {
    isOpen: { type: Boolean, default: false },
    orderId: { type: String, required: true },       // L'ID de la commande générée au checkout
    guestEmail: { type: String, default: '' }       // L'email s'il s'agit d'un achat invité
  },

  emits: ['close', 'payment-success'],

  setup(props, { emit }) {
    // Récupération de ton instance d'API configurée et de tes variables de config
    const { $api } = useNuxtApp();
    const config = useRuntimeConfig();
    
    // États Stripe
    const stripe = ref<any>(null);
    const elements = ref<any>(null);
    const isStripeReady = ref<boolean>(false);
    
    // États de l'interface graphique (UI)
    const isLoading = ref<boolean>(false);
    const errorMessage = ref<string | null>(null);

    const closeModal = () => {
      if (!isLoading.value) emit('close');
    };

    // Initialisation du formulaire Stripe Elements
    const initializeStripe = async () => {
      isLoading.value = true;
      errorMessage.value = null;

      try {
        // 1. Chargement de Stripe avec ta clé publique configurée
        stripe.value = await loadStripe(config.public.stripePublicKey);

        // 2. Préparation de la route Django pour l'initiation
        const url = props.guestEmail 
          ? `/payments/initiate/?email=${encodeURIComponent(props.guestEmail)}`
          : `/payments/initiate/`;

        // 3. Appel de ton backend avec ton plugin global $api (l'URL de base est gérée automatiquement !)
        const response: any = await $api(url, {
          method: 'POST',
          body: {
            order_id: props.orderId,
            payment_method: 'STRIPE'
          }
        });

        if (response?.client_secret) {
          // Personnalisation sobre du thème des inputs de carte
          const appearance = {
            theme: 'flat',
            variables: { 
              colorPrimary: '#007bff', 
              fontFamily: 'sans-serif' 
            }
          };

          // 4. Instanciation du composant Elements
          elements.value = stripe.value.elements({
            clientSecret: response.client_secret,
            appearance,
          });

          // ✨ LE SECRET : On attend le prochain tick pour s'assurer que Vue 
          // a bien injecté la div #payment-element avant d'y greffer Stripe !
          await nextTick();

          const paymentElement = elements.value.create('payment');
          paymentElement.mount('#payment-element');

          isStripeReady.value = true;
        } else {
          errorMessage.value = response?.error || "Impossible d'initier la clé d'intention de paiement.";
        }
      } catch (err: any) {
        errorMessage.value = err?.message || "Erreur de liaison avec le serveur de paiement.";
        console.error("Stripe Initialization Error:", err);
      } finally {
        isLoading.value = false;
      }
    };

    // Soumission définitive des informations de paiement
    const handleSubmit = async () => {
      if (!stripe.value || !elements.value) return;

      isLoading.value = true;
      errorMessage.value = null;

      try {
        // Envoi direct de la carte aux serveurs sécurisés de Stripe sans rafraîchir la page entière
        const { error, paymentIntent } = await stripe.value.confirmPayment({
          elements: elements.value,
          redirect: 'if_required', 
        });

        if (error) {
          // Erreur instantanée renvoyée par Stripe (ex: provision insuffisante)
          errorMessage.value = error.message || "La transaction a été refusée.";
        } else if (paymentIntent && paymentIntent.status === 'succeeded') {
          // 🎉 Succès total ! On informe le composant parent pour afficher succesFormVue
          emit('payment-success');
        }
      } catch (err) {
        errorMessage.value = "Une erreur inattendue est survenue lors de la validation.";
      } finally {
        isLoading.value = false;
      }
    };

    // Surveillance de l'état d'ouverture pour bloquer le scroll de l'arrière-plan
    watch(() => props.isOpen, (newValue) => {
      if (newValue) {
        document.body.classList.add('overflow-hidden');
        initializeStripe(); // Lance l'intégration au moment précis où la modale s'affiche !
      } else {
        document.body.classList.remove('overflow-hidden');
        // Nettoyage à la fermeture
        elements.value = null;
        isStripeReady.value = false;
      }
    });

    onUnmounted(() => document.body.classList.remove('overflow-hidden'));

    return {
      closeModal,
      handleSubmit,
      isLoading,
      errorMessage,
      isStripeReady
    };
  }
}
</script>

<style scoped>
/* 1. Ton overlay Glassmorphism d'origine préservé */
.glass-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* 2. La boîte de contenu ajustée pour Stripe (Élargie à 440px pour l'alignement des champs de carte) */
.stripe-modal-content {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  position: relative;
  max-width: 90%;
  width: 440px;
  animation: modalFadeIn 0.3s ease-out forwards;
}

/* 3. Bouton de fermeture tactile */
.close-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #666;
  transition: color 0.2s;
}

.close-btn:hover:not(:disabled) {
  color: #000;
}

.close-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* 4. Organisation interne */
.stripe-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.stripe-container h3 {
  margin: 0;
  color: #1a1a1a;
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
}

.stripe-element-container {
  min-height: 200px; /* Conserve une structure stable pendant que l'iframe Stripe charge */
}

/* 5. Ton bouton de soumission */
.btn-pay {
  width: 100%;
  padding: 13px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.btn-pay:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-pay:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-pay:disabled {
  background-color: #a0a0a0;
  box-shadow: none;
  cursor: not-allowed;
}

/* Design des messages d'alertes */
.error-message {
  margin: 0;
  color: #d9534f;
  background: rgba(217, 83, 79, 0.1);
  padding: 10px;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  text-align: center;
  font-weight: 500;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>