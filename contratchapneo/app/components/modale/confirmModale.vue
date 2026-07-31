<template>
    <Teleport to="body">
        <div
            v-if="isOpen"
            class="modal-overlay"
            @click.self="handleClose"
            @keydown.esc="handleClose"
            role="dialog"
            aria-modal="true"
            :aria-label="`Confirmation de suppression - ${itemName}`"
        >
        <div class="modal-container" ref="modalContainer" >
        <template v-if="!success">
            <!-- En-tête -->
            <div class="modal-header">
                <h2 class="modal-title">{{ title }}</h2>
                <button
                    class="close-button"
                    @click="handleClose"
                    aria-label="Fermer"
                    :disabled="isDeleting"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="close-icon">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            </div>

            <!-- Corps -->
            <div class="modal-body">
            
            <!-- ⚡️ NOUVELLE ICÔNE : Document avec validation (couleur du thème) -->
            <div class="icon-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="info-icon">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 0 1 9 9v.375M10.125 2.25A3.375 3.375 0 0 1 13.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 0 1 3.375 3.375M9 15l2.25 2.25L15 12" />
                </svg>
            </div>

            <!-- Message principal -->
            <p class="confirmation-message">
                Assurez-vous que vos informations soient correctes 
                avant la génération du contrat.
            </p>

            <!-- Détail de l'élément -->
            <div v-if="itemName" class="item-details">
                <span class="item-label">Élément concerné :</span>
                <strong class="item-name">{{ itemName }}</strong>
            </div>
            </div>

            <!-- Actions -->
            <div class="modal-actions">
                
                <!-- ⚡️ NOUVEAU BOUTON : Télécharger -->
                <button
                    class="btn btn-primary action-btn"
                    @click="$emit('confirm')"
                    :disabled="isLoading || isDeleting"
                >
                    <!-- Icône de téléchargement (masquée si chargement) -->
                    <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="btn-icon">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                    </svg>
                    
                    <!-- Spinner de chargement -->
                    <div v-else class="loading-spinner"></div>
                    
                    <!-- Texte dynamique -->
                    <span>{{ isLoading ? 'Génération en cours...' : 'Télécharger votre contrat' }}</span>
                </button>

                <button
                    class="btn btn-secondary action-btn"
                    @click="handleClose"
                    :disabled="isDeleting"
                    ref="cancelButton"
                >
                    Annuler
                </button>
            </div>
        </template>
        </div>
    </div>
    </Teleport>
</template>

<script lang="ts">
import { defineComponent, computed, ref, watch, nextTick, type PropType } from 'vue'

interface OperationRow {
  created_at: string
  title: string
  description: string
  city: string
  country: string
  type: string
}

export default defineComponent({
  name: 'DeleteModal',
  props: {
    isOpen: {
      type: Boolean,
      default: true,
    },
    selectedItem: {
      type: Object as PropType<OperationRow | null>,
      default: null,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    title:{
      type:String,
      default:"Confirmation des informations"
    },
    success:{
      type:Boolean,
      default: false
    },
    description: { 
      type: String, 
      default: '' 
    }
  },
  components:{
  },
  emits: ['close', 'confirm'],
  setup(props, { emit }) {
    const cancelButton = ref<HTMLButtonElement | null>(null)
    const modalContainer = ref<HTMLElement | null>(null)
    const isDeleting = ref(false)

    const itemName = computed(() => {
      if (!props.selectedItem) return ''
      return props.selectedItem.title || props.selectedItem.description || 'cet élément'
    })

    const handleClose = () => {
      if (isDeleting.value) return
      emit('close')
    }

    const handleConfirm = async () => {
      if (isDeleting.value) return
      isDeleting.value = true
      try {
        await emit('confirm')
      } finally {
        isDeleting.value = false
      }
    }

    watch(
      () => props.isOpen,
      async (newVal) => {
        if (newVal) {
          await nextTick()
          cancelButton.value?.focus()
          document.body.style.overflow = 'hidden'
        } else {
          document.body.style.overflow = ''
        }
      },
    )

    const onAfterLeave = () => {
      document.body.style.overflow = ''
    }

    return {
      cancelButton,
      modalContainer,
      isDeleting,
      itemName,
      handleClose,
      handleConfirm,
      onAfterLeave,
    }
  },
})
</script>

<style scoped>
/* Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

/* Conteneur de la modale */
.modal-container {
  background-color: #ffffff;
  border-radius: 1.25rem;
  width: 100%;
  max-width: 28rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

/* En-tête */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  min-width: fit-content;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.close-button {
  width: fit-content;
  background: transparent;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  color: #f30606;
  border-radius: 10px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover:not(:disabled) {
  background-color: rgb(230, 14, 14);
  color: #ffffff;
}

.close-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.close-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Corps */
.modal-body {
  padding: 1.5rem;
  text-align: center;
}

.icon-wrapper {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

/* ⚡️ STYLE DE LA NOUVELLE ICÔNE */
.info-icon {
  width: 3.5rem;
  height: 3.5rem;
  color: #202b4a; /* Couleur bleue foncée classique pour l'info */
  stroke-width: 1.5;
}

.confirmation-message {
  font-size: 1.125rem;
  font-weight: 500;
  color: #111827;
  margin-bottom: 0.75rem;
}

.item-details {
  background-color: #f9fafb;
  border-radius: 0.75rem;
  padding: 0.75rem 1rem;
  margin: 1rem 0;
  font-size: 0.875rem;
}

.item-label {
  color: #6b7280;
  margin-right: 0.5rem;
}

.item-name {
  color: #111827;
  word-break: break-word;
}

/* Actions */
.modal-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem 1.5rem 1.5rem;
}

/* ⚡️ CORRECTION DES TAILLES DE BOUTONS */
.action-btn {
  width: 100%;
}

/* Cette règle force le bouton interne de mainButton et ton bouton annuler à faire la même taille */
.modal-actions button {
  width: 100%;
  height: 48px; /* Hauteur fixe pour symétrie parfaite */
  padding: 0;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem; /* Espace entre l'icône et le texte */
  cursor: pointer;
  transition: all 0.2s;
  box-sizing: border-box;
  border: none;
}

.modal-actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #202b4a; /* Bleu Contratchap */
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2c3a61;
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.btn-secondary {
  background-color: #ffffff;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #f3f4f6;
  border-color: #9ca3af;
}

.loading-spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container {
  transform: scale(0.95);
}

.modal-leave-to .modal-container {
  transform: scale(0.95);
}

/* Mode sombre */
@media (prefers-color-scheme: dark) {
  .modal-container {
    background-color: #1f2937;
  }

  .modal-title, .confirmation-message, .item-name {
    color: #f9fafb;
  }

  .modal-header {
    border-bottom-color: #374151;
  }

  .info-icon {
    color: #60a5fa; /* Bleu clair pour mode sombre */
  }

  .item-details {
    background-color: #111827;
  }

  .item-label {
    color: #9ca3af;
  }

  .modal-actions {
    background-color: #111827;
    border-top-color: #374151;
  }

  .btn-secondary {
    background-color: #374151;
    border-color: #4b5563;
    color: #f9fafb;
  }

  .btn-secondary:hover:not(:disabled) {
    background-color: #4b5563;
  }
}

/* Responsive */
@media (max-width: 640px) {
  .modal-container {
    max-width: 90%;
    border-radius: 1rem;
  }

  .modal-header,
  .modal-body,
  .modal-actions {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>