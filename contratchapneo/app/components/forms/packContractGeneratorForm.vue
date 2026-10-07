<template>
  <form @submit.prevent="submitForm" class="contrat-form">
    <div v-if="store.isLoading" class="loading-state">
      <p>Analyse du document et préparation de votre contrat Premium...</p>
    </div>

    <div v-else-if="store.error" class="error-state">
      <p>🚨 Erreur : {{ store.error }} </p>
    </div>

    <div v-else-if="uniqueTags.length > 0" class="contract-prev-form">
      <!-- 🔹 Affichage de tous les champs -->
      <div class="input-list">
        <div v-for="tag in uniqueTags" :key="tag" class="input-group">
          <BaseInputContract
            v-model="formData[tag]"
            :label="formatLabel(tag)"
            :type="getInputType(tag)"
            :placeholder="'Entrez : ' + formatLabel(tag).toLowerCase()"
            :disabled="store.isLoading"
            @focus="emit('focus-field', tag)"
          />
        </div>
      </div>

      <!-- 🔹 Boutons de validation -->
      <div class="navigation-buttons">
        <generatorButton 
          label="Prévisualiser le contrat" 
          @click="submitForm" 
          :disabled="!isFormValid"
        />
      </div>
    </div>

    <div v-else class="no-tags-state">
      <p class="ready-text">Ce contrat standard est prêt. Il ne nécessite aucune information supplémentaire.</p>
      <generatorButton 
        label="Prévisualiser le contrat" 
        @click="submitForm" 
      />
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useContratStore } from '../../stores/contratStore' 

import BaseInputContract from '../input/BaseInputContract.vue'
import generatorButton from '.././buttons/generatorButton.vue'

const emit = defineEmits(['update-data', 'submit-data', 'focus-field']);

const store = useContratStore() 
const route = useRoute()
const formData = ref<Record<string, string>>({})
const uniqueTags = computed(() => {
  if (!store.tags || store.tags.length === 0) return [];
  const allTags = new Set<string>();
  
  store.tags.forEach((block: any) => {
    if (block.tags && Array.isArray(block.tags)) {
      block.tags.forEach((tag: string) => allTags.add(tag));
    }
  });
  return Array.from(allTags);
});

const isFormValid = computed(() => {
  if (uniqueTags.value.length === 0) return true;
  return uniqueTags.value.every(tag => {
    const value = formData.value[tag];
    return value !== undefined && value !== null && String(value).trim() !== '';
  });
});

onMounted(async () => {
  const contractId = route.params.id as string
  if (contractId) {
    await store.fetchContractTags(contractId) 
  }

  if (uniqueTags.value.length > 0) {
    uniqueTags.value.forEach(tagName => { formData.value[tagName] = '' })
  }
});



watch(formData, (newValues) => {
  emit('update-data', newValues)
}, { deep: true })

const formatLabel = (tagName: string) =>
  tagName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())

const getInputType = (tagName: string) => {
  if (tagName.startsWith('date_')) return 'date'
  if (tagName.startsWith('num_') || tagName.startsWith('montant_')) return 'number'
  if (tagName.startsWith('email_')) return 'email'
  return 'text'
}

const submitForm = () => {
  if (isFormValid.value) {
    emit('submit-data', formData.value)
  }
}
</script>

<style scoped>
.contrat-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.contract-prev-form{
  width: 100%;
}

.loading-state, .error-state {
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}
.error-state {
  background-color: #ffebee;
  color: #c62828;
}
.submit-btn {
  padding: 0.75rem 1.5rem;
  background-color: #202b4a; /* Les couleurs Contratchap ! */
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.submit-btn:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}
.input-group {
  position: relative;
  margin-bottom: 2rem;
}

.progress-indicator {
  position: absolute;
  right: 0;
  top: -1.5rem;
  color: #666;
  font-size: 0.8rem;
}

.navigation-buttons {
  width: 100%;
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.nav-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.prev-btn {
  background-color: #f0f0f0;
  color: #333;
}

.next-btn, .submit-btn {
  background-color: #202b4a;
  color: white;
}

.submit-btn {
  background-color: #1a56db;
}

.no-tags-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.5rem;
  padding: 2rem;
  background-color: #f8fafc;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
}

.ready-text {
  color: #334155;
  font-weight: 500;
  margin: 0;
}
</style>