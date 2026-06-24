<template>
  <button
    :class="['glass-bubble', { bump } ]"
    @click="$emit('open-cart')"
    aria-label="Ouvrir le panier"
  >
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="cart-icon">
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
    </svg>

    <span v-if="cartStore.totalItems > 0" class="badge">
      {{ cartStore.totalItems }}
    </span>
  </button>
</template>

<script lang="ts">
import { ref, watch } from 'vue';
import { useCartStore } from '../../stores/cartStore'; // Ajuste le chemin selon ton arborescence

export default {
  emits: ['open-cart'], // Déclare l'événement émis par ce composant
  setup() {
    const cartStore = useCartStore();
    const bump = ref(false);
    let bumpTimeout: ReturnType<typeof setTimeout> | null = null;

    watch(
      () => cartStore.totalItems,
      (newValue, oldValue) => {
        if (typeof oldValue === 'number' && newValue > oldValue) {
          bump.value = true;
          if (bumpTimeout) clearTimeout(bumpTimeout);
          bumpTimeout = setTimeout(() => {
            bump.value = false;
            bumpTimeout = null;
          }, 400);
        }
      }
    );

    return {
      cartStore,
      bump
    };
  }
};

// On émet un événement pour dire au composant parent d'ouvrir la modale
</script>

<style scoped>
.glass-bubble {
  /* Positionnement fixe en bas à droite */
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 50; /* S'assure qu'il passe au-dessus du reste, mais sous la modale */
  
  /* Dimensions de la bulle */
  width: 64px;
  height: 64px;
  border-radius: 50%;
  
  /* Centrage de l'icône */
  display: flex;
  align-items: center;
  justify-content: center;
  
  /* 🔥 L'effet Glassmorphisme prononcé 🔥 */
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px); /* Pour la compatibilité Safari */
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
  
  /* Interactions */
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

/* Effet au survol pour le dynamisme */
.glass-bubble:hover {
  transform: translateY(-5px) scale(1.05);
  background: rgba(255, 255, 255, 0.35);
  box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.2);
}

/* L'icône à l'intérieur */
.cart-icon {
  width: 28px;
  height: 28px;
  color: #1a1a1a; /* Couleur sombre pour contraster avec le verre clair */
}

/* Le petit badge rouge/bleu pour le compteur */
.badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #007bff; /* Le même bleu que ton item-price et final-price */
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  min-width: 24px;
  height: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 6px;
  
  /* Ajoute une petite bordure pour détacher le badge de la bulle en verre */
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
/* 🔥 L'animation du "Bump" 🔥 */
.bump {
  animation: bump-animation 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes bump-animation {
  0% {
    transform: scale(1);
  }
  20% {
    /* Écrasement (anticipation) */
    transform: scale(0.85) translateY(4px);
  }
  50% {
    /* Rebond exageré (overshoot) */
    transform: scale(1.15) translateY(-8px);
  }
  80% {
    /* Retour partiel */
    transform: scale(0.95) translateY(2px);
  }
  100% {
    /* Retour normal */
    transform: scale(1) translateY(0);
  }
}
</style>