<template>
    <button 
    class="main-button" 
    :disabled="isLoading" 
    @click.stop="handleClick"
    >
        <template v-if="!isLoading">
            {{ label }}
        </template>

        <template v-else>
            <span class="loading loading-spinner loading-md"></span>
        </template>
    </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MainButton',
  // On ne garde qu'un seul événement propre : 'click'
  emits: ['click'],
  props: {
    label: {
      type: String,
      default: 'Payer mon contrat'
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    handleClick(event: Event) {
      // Si ça charge, on stoppe immédiatement toute action
      if (this.isLoading) return;
      
      // On émet l'événement au parent
      this.$emit('click', event);
    }
  }
})
</script>

<style scoped>
.main-button {
  background-color: var(--primary-color);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  border: none; /* Évite les bordures natives des boutons */
}

/* Style optionnel pour montrer visuellement que le bouton est bloqué */
.main-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>