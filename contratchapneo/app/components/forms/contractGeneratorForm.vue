<template>
    <form @submit.prevent="submitForm" class="contrat-form">
    
        <div v-if="store.isLoading" class="loading-state">
          <p>Analyse du document et extraction des balises en cours...</p>
        </div>

        <div v-else-if="store.error" class="error-state">
            <p>🚨 Erreur : {{ store.error }}</p>
        </div>

        <div v-else-if="uniqueTags.length > 0" class="contract-prev-form">
        
          <div v-for="tagName in uniqueTags" :key="tagName" class="input-group">
              <BaseInputContract
                v-model="formData[tagName]"
                :label="formatLabel(tagName)"
                :type="getInputType(tagName)"
                :placeholder="'Entrez : ' + formatLabel(tagName).toLowerCase()"
                :disabled="store.isLoading"
              />
          </div>

          <button type="submit" class="submit-btn" :disabled="store.isLoading">
            Valider les informations
          </button>
        </div>

        <div v-else>
          <p>Ce contrat ne nécessite aucune information à remplir.</p>
        </div>
    
    </form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useContratStore } from '../../stores/contratStore'
import { useRoute } from 'vue-router'
import BaseInputContract from '../input/BaseInputContract.vue'

const emit = defineEmits(['submit-data', 'update-data'])

const store = useContratStore()
const formData = ref<Record<string, string>>({}) 
const route = useRoute() 

// 🪄 L'ASTUCE CONTRATCHAP : Aplatir les tags et retirer les doublons
const uniqueTags = computed(() => {
  if (!store.tags || store.tags.length === 0) return [];
  
  // Le Set permet de stocker des valeurs uniques (pas de doublons)
  const allTags = new Set<string>();
  
  // On parcourt chaque bloc renvoyé par Django
  store.tags.forEach((block: any) => {
    // Si le bloc contient des variables, on les ajoute au Set
    if (block.tags && Array.isArray(block.tags)) {
      block.tags.forEach((tag: string) => allTags.add(tag));
    }
  });
  
  // On re-transforme le Set en tableau classique pour le v-for
  return Array.from(allTags);
})

onMounted(async () => {
  if (!store.currentContratId) return;
  
  await store.fetchContractTags(store.currentContratId)

  // On initialise formData avec nos tags UNIQUES
  if (uniqueTags.value.length > 0) {
    uniqueTags.value.forEach(tagName => {
      formData.value[tagName] = ''
    })
  }
})

// Déclenche la mise à jour en temps réel vers le parent
watch(formData, (newValues) => {
  emit('update-data', newValues)
}, { deep: true })

const formatLabel = (tagName: string) => tagName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())

const getInputType = (tagName: string) => {
  if (tagName.startsWith('date_')) return 'date'
  if (tagName.startsWith('num_')) return 'number'
  if (tagName.startsWith('email_')) return 'email'
  return 'text' 
}

const submitForm = () => {
  emit('submit-data', formData.value)
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
</style>