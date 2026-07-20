<template>
  <!-- Le conteneur global qui gère la file d'attente -->
  <div class="toast-container">
    <TransitionGroup name="toast">
      
      <!-- On boucle sur la liste interne des notifications -->
      <div 
        v-for="toast in internalToasts" 
        :key="toast.id" 
        class="notification-toast" 
        :class="`toast-${toast.type}`"
      >
        
        <!-- Icône dynamique -->
        <div class="toast-icon">
          <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          <svg v-else-if="toast.type === 'error'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3Z" />
          </svg>
        </div>

        <!-- Contenu du message -->
        <div class="toast-content">
          <h4 class="toast-title">{{ toast.title }}</h4>
          <p v-if="toast.message" class="toast-message">{{ toast.message }}</p>
        </div>

        <!-- Bouton de fermeture manuelle -->
        <button class="toast-close" @click="removeToast(toast.id)" aria-label="Fermer">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Barre de progression animée -->
        <div class="toast-progress" :style="{ animationDuration: `${duration}ms` }"></div>
        
      </div>
    </TransitionGroup>
  </div>
</template>

<script lang="ts">
import { ref, watch } from 'vue';

export default {
  name: 'BaseNotification',
  props: {
    show: { type: Boolean, default: false },
    type: { type: String, default: 'success' },
    title: { type: String, default: '' },
    message: { type: String, default: '' },
    duration: { type: Number, default: 4000 }
  },
  emits: ['update:show'],
  
  setup(props, { emit }) {
    // Liste interne qui gère toutes les notifications actives
    const internalToasts = ref<Array<any>>([]);

    // Fonction pour supprimer une notification spécifique
    const removeToast = (id: number) => {
      internalToasts.value = internalToasts.value.filter(t => t.id !== id);
    };

    // On écoute la variable "show" du parent
    watch(() => props.show, (newVal) => {
      if (newVal) {
        // 1. On crée une nouvelle notification avec un ID unique
        const newToast = {
          id: Date.now() + Math.random(),
          type: props.type,
          title: props.title,
          message: props.message
        };
        
        // 2. On l'ajoute à la file d'attente
        internalToasts.value.push(newToast);
        
        // 3. MAGIE : On dit immédiatement au parent de remettre `show` à false.
        // Cela permet au parent de déclencher d'autres alertes sans bloquer.
        emit('update:show', false);

        // 4. On programme sa suppression automatique
        setTimeout(() => {
          removeToast(newToast.id);
        }, props.duration);
      }
    });

    return {
      internalToasts,
      removeToast
    };
  }
}
</script>

<style scoped>
/* --- CONTENEUR GLOBAL (La file d'attente) --- */
.toast-container {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 99999;
  display: flex;
  flex-direction: column; /* Empile les éléments en colonne */
  gap: 1rem; /* Espace entre les notifications */
  pointer-events: none; /* Laisse passer les clics à travers le conteneur invisible */
}

/* --- LA NOTIFICATION INDIVIDUELLE --- */
.notification-toast {
  position: relative; /* N'est plus en absolute/fixed ! C'est le conteneur qui s'en charge */
  width: 350px;
  max-width: 90vw;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: flex-start;
  padding: 1.2rem;
  overflow: hidden;
  pointer-events: auto; /* Réactive les clics sur la notification elle-même */
}

/* --- ANIMATION D'APPARITION ET DE LISTE (TransitionGroup) --- */
.toast-enter-active,
.toast-leave-active,
.toast-move {
  transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%); /* Elle glisse vers la droite en disparaissant */
}

/* Permet aux autres alertes de glisser doucement vers le haut quand l'une d'elles disparaît */
.toast-leave-active {
  position: absolute; 
}

/* --- STYLES PAR TYPE --- */
.toast-success { border-left: 6px solid #32f459; }
.toast-error { border-left: 6px solid #ef4444; }

.toast-success .toast-icon { color: #32f459; background: rgba(50, 244, 89, 0.1); }
.toast-error .toast-icon { color: #ef4444; background: rgba(239, 68, 68, 0.1); }

.toast-success .toast-progress { background: #32f459; }
.toast-error .toast-progress { background: #ef4444; }

/* --- CONTENU --- */
.toast-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 1rem;
}

.toast-icon svg { width: 24px; height: 24px; }

.toast-content {
  flex-grow: 1;
  padding-right: 1rem;
}

.toast-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: #1e293b;
}

.toast-message {
  width: 200px;
  display: flex;
  flex-direction: row;
  margin: 0;
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.4;
}

/* --- BOUTON FERMER --- */
.toast-close {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.2rem;
  transition: color 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}

.toast-close:hover { color: #0f172a; }
.toast-close svg { width: 20px; height: 20px; }

/* --- BARRE DE PROGRESSION --- */
.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  width: 100%;
  transform-origin: left;
  animation: shrink linear forwards;
}

@keyframes shrink {
  from { transform: scaleX(1); }
  to { transform: scaleX(0); }
}

/* --- RESPONSIVE MOBILE --- */
@media (max-width: 600px) {
  .toast-container {
    top: 1rem;
    right: 1rem;
    left: 1rem;
  }
  .notification-toast {
    width: 100%;
    max-width: none;
  }
}
</style>