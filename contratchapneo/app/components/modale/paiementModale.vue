<template>
  
  <div v-if="isOpen" class="glass-modal-overlay" @click="closeModal">
    
    <div class="stripe-modal-content" @click.stop>
      
      <button class="close-btn" @click="closeModal" :disabled="cartStore.isLoading" aria-label="Fermer">x</button>
      
      <div class="stripe-container">
        <h3>Paiement par Carte Bancaire</h3>
        
        <div id="payment-element" class="stripe-element-container"></div>

        <p v-if="cartStore.error" class="error-message">{{ cartStore.error }}</p>

        <button 
          class="btn-pay" 
          @click="handleSubmit" 
          :disabled="cartStore.isLoading || !cartStore.stripeReady"
        >
          {{ cartStore.isLoading ? 'Traitement sécurisé...' : 'Confirmer le règlement' }}
        </button>
      </div>
    </div>

  </div>
  
</template>

<script lang="ts">
import { watch, onUnmounted, nextTick } from 'vue';
import { useCartStore } from '../../stores/cartStore';
import { useOrderStore } from '../../stores/orderStore';

export default {
  
  name: 'PaiementModale',

  props: {
    isOpen: { type: Boolean, default: false }
  },

  emits: ['close', 'payment-success'],

  setup(props, { emit }) {
    const cartStore = useCartStore();
    const orderStore = useOrderStore();

    const closeModal = () => {
      if (!cartStore.isLoading) emit('close');
    };

    const initializeStripe = async () => {
      cartStore.error = null;

      const currentOrder = orderStore.currentOrder;
      if (!currentOrder?.id) {
        cartStore.error = "Aucune commande disponible pour le paiement Stripe.";
        return;
      }

      try {
        const elements = await cartStore.initializeStripe(currentOrder.id, currentOrder.guest?.email || '');
        await nextTick();

        if (elements) {
          const paymentElement = elements.create('payment');
          paymentElement.mount('#payment-element');
        }
      } catch (err) {
        console.error('Stripe Initialization Error:', err);
      }
    };

    const handleSubmit = async () => {
      if (!cartStore.stripeReady) return;

      try {
        // 💡 Récupération de l'ID de la commande en cours pour fabriquer l'URL de redirection sécurisée
        const currentOrderId = orderStore.currentOrder?.id;
        const returnUrl = `${window.location.origin}/ecommerce/orders/${currentOrderId}`;

        // On passe l'URL à l'action de ton cartStore
        const paymentIntent = await cartStore.confirmStripePayment(returnUrl);
        
        if (paymentIntent?.status === 'succeeded') {
          emit('payment-success');
        }
      } catch (err) {
        console.error('Stripe confirmation failed:', err);
      }
    };

    watch(() => props.isOpen, (newValue) => {
      if (newValue) {
        document.body.classList.add('overflow-hidden');
        initializeStripe();
      } else {
        document.body.classList.remove('overflow-hidden');
        cartStore.resetStripeState();
      }
    });

    onUnmounted(() => document.body.classList.remove('overflow-hidden'));

    return {
      closeModal,
      handleSubmit,
      cartStore
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
  width: 90%;
  max-width: 500px;
  height: 90%;
  max-height: 600px;
  overflow-y: auto;
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