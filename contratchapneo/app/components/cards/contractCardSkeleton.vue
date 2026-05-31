<template>
  <div class="skeleton-grid">
    <div 
      v-for="n in cardsCount" 
      :key="n" 
      class="pro-card-skeleton"
    >
      <div class="skeleton-bg"></div>

      <div class="skeleton-overlay"></div>

      <div class="skeleton-info">
        <div class="skeleton-line title-line"></div>
        <div class="skeleton-line desc-line-1"></div>
        <div class="skeleton-line desc-line-2"></div>
        <div class="skeleton-line sub-line"></div>
      </div>

      <div class="skeleton-buttons">
        <div class="skeleton-circle btn-small"></div>
        <div class="skeleton-circle btn-large"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const cardsCount = ref(1)

// Gestion adaptative du nombre de skeletons à afficher (1 sur mobile, 4 sur laptop)
const updateCardsCount = () => {
  if (typeof window !== 'undefined') {
    // Si l'écran est supérieur ou égal à 1024px (breakpoint laptop standard)
    if (window.innerWidth >= 1024) {
      cardsCount.value = 4
    } else {
      cardsCount.value = 1
    }
  }
}

onMounted(() => {
  updateCardsCount()
  window.addEventListener('resize', updateCardsCount)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateCardsCount)
})
</script>

<style scoped>
/* Grille de skeletons calquée sur votre .cards-container */
.skeleton-grid {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr;
  place-items: center;
  gap: 30px;
}

@media (min-width: 1024px) {
  .skeleton-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Structure de la carte Skeleton (Dimensions identiques à vos cartes réelles) */
.pro-card-skeleton {
  position: relative;
  width: 100%;
  max-width: 320px;
  height: 270px;
  border-radius: 20px;
  background-color: #e5e7eb; /* Base grise */
  overflow: hidden;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
}

.skeleton-bg {
  width: 100%;
  height: 100%;
  background-color: #e5e7eb;
}

.skeleton-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0) 100%);
  z-index: 1;
}

/* Zone d'information */
.skeleton-info {
  position: absolute;
  bottom: 12px;
  left: 14px;
  right: 14px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: calc(100% - 120px); /* Laisse de la place pour les boutons à droite */
}

/* Animation d'onde Shimmer (Effet de balayage brillant) */
.skeleton-line, .skeleton-circle, .skeleton-bg {
  position: relative;
  overflow: hidden;
}

.skeleton-line::after, .skeleton-circle::after, .skeleton-bg::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.4) 20%,
    rgba(255, 255, 255, 0.6) 60%,
    rgba(255, 255, 255, 0) 100-percent
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

/* Lignes de texte fictives */
.skeleton-line {
  height: 12px;
  background-color: #d1d5db;
  border-radius: 4px;
}

.title-line {
  height: 16px;
  width: 90%;
  background-color: #9ca3af; /* Plus foncé pour le titre */
}

.desc-line-1 {
  width: 100%;
}

.desc-line-2 {
  width: 75%;
}

.sub-line {
  height: 10px;
  width: 50%;
  background-color: rgba(52, 211, 153, 0.4); /* Teinte verte pour mimer votre badge */
  margin-top: 4px;
}

/* Boutons fictifs (En bas à droite) */
.skeleton-buttons {
  position: absolute;
  bottom: 9px;
  right: 9px;
  display: flex;
  align-items: center;
  gap: 6px;
  z-index: 2;
}

.skeleton-circle {
  background-color: #9ca3af;
  border-radius: 999px;
}

.btn-small {
  width: 35px;
  height: 35px;
  background-color: rgba(255, 255, 255, 0.2); /* Mime le bouton d'aperçu transparent */
}

.btn-large {
  width: 45px;
  height: 45px;
  background-color: #bdc3c7; /* Mime le bouton d'achat principal */
}
</style>