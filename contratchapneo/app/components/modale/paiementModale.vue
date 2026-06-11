<template>
  <div v-if="isOpen" class="glass-modal-overlay" @click="closeModal">
    <div class="qr-modal-content" @click.stop>
      <button class="close-btn" @click="closeModal" aria-label="Fermer">×</button>
      
      <div class="qr-container">
        <h3>Scanner pour payer</h3>
        <img 
          :src="qrCodeUrl || defaultQr" 
          alt="QR Code de paiement" 
          class="qr-image" 
        />
        <p>Montant total : <span class="highlight">{{ totalAmount }} FCFA</span></p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { watch, onUnmounted } from 'vue';

export default {
  name: 'QrPaymentModal',

  props: {
    isOpen: { type: Boolean, default: false },
    qrCodeUrl: { type: String, default: '' }, // URL de ton vrai QR Code renvoyé par l'API
    totalAmount: { type: [Number, String], default: '0' } // Pour afficher le montant sous le QR
  },

  emits: ['close'],

  setup(props, { emit }) {
    // Un QR code générique par défaut pour tes tests
    const defaultQr = 'https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=PaiementContratchap';

    const closeModal = () => emit('close');

    // On garde ton excellente logique pour bloquer le scroll de la page quand la modale est ouverte
    watch(() => props.isOpen, (newValue) => {
      if (newValue) document.body.classList.add('overflow-hidden');
      else document.body.classList.remove('overflow-hidden');
    });

    onUnmounted(() => document.body.classList.remove('overflow-hidden'));

    return {
      closeModal,
      defaultQr,
    };
  }
}
</script>

<style scoped>
/* 1. L'overlay Glassmorphism (Le secret est ici) */
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
  
  /* L'effet verre dépoli */
  background: rgba(0, 0, 0, 0.45);      /* ← gris sombre neutre, sans couleur */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* 2. La carte contenant le QR Code */
.qr-modal-content {
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  position: relative;
  text-align: center;
  max-width: 90%;
  width: 350px;
  animation: modalFadeIn 0.3s ease-out forwards;
}

/* 3. Bouton de fermeture discret */
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

.close-btn:hover {
  color: #000;
}

/* 4. Conteneur du QR Code */
.qr-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
}

.qr-container h3 {
  margin: 0;
  color: #1a1a1a;
  font-size: 1.2rem;
  font-weight: 600;
}

.qr-image {
  width: 220px;
  height: 220px;
  border-radius: 0.75rem;
  padding: 10px;
  background: white; /* Garder un fond blanc pur derrière le QR pour qu'il soit scannable */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.qr-container p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.highlight {
  font-weight: 700;
  color: #007bff;
  font-size: 1.1rem;
}

/* Petite animation d'apparition douce */
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