<template>
    <form @submit.prevent="submitForm" class="contrat-form">
        <div v-if="store.isLoading" class="loading-state">
          <p>Analyse du document et extraction des balises en cours...</p>
        </div>

        <div v-else-if="store.error" class="error-state">
            <p>🚨 Erreur : {{ store.error }} </p>
        </div>

        <div v-else-if="uniqueTags.length > 0" class="contract-prev-form">
          <!-- 🔹 Affichage séquentiel -->
          <transition name="fade" mode="out-in">
            <div v-if="currentTagIndex < uniqueTags.length" :key="currentTag" class="input-group">
              <BaseInputContract
                v-model="formData[currentTag]"
                :label="formatLabel(currentTag)"
                :type="getInputType(currentTag)"
                :placeholder="'Entrez : ' + formatLabel(currentTag).toLowerCase()"
                :disabled="store.isLoading"
                @focus="scrollToField(currentTag)"
              />
              <div class="progress-indicator">
                {{ currentTagIndex + 1 }} / {{ uniqueTags.length }}
              </div>
            </div>
          </transition>

          <!-- 🔹 Boutons de navigation -->
          <div class="navigation-buttons">
            <button
              type="button"
              @click="prevTag"
              :disabled="currentTagIndex === 0"
              class="nav-btn prev-btn"
            >
              Précédent
            </button>
            <button
              v-if="currentTagIndex < uniqueTags.length - 1"
              type="button"
              @click="nextTag"
              class="nav-btn next-btn"
            >
              Suivant
            </button>
            <button
              v-else
              type="submit"
              class="nav-btn submit-btn"
              :disabled="store.isLoading"
            >
              Valider
            </button>
          </div>
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

const emit = defineEmits(['submit-data', 'update-data', 'scroll-to-field'])
const store = useContratStore()
const formData = ref<Record<string, string>>({})
const route = useRoute()
const currentTagIndex = ref(0) // Index du champ actuel

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

const currentTag = computed(() => uniqueTags.value[currentTagIndex.value])

onMounted(async () => {
  if (!store.currentContratId) return;
  await store.fetchContractTags(store.currentContratId)
  if (uniqueTags.value.length > 0) {
    uniqueTags.value.forEach(tagName => { formData.value[tagName] = '' })
  }
});

// 🔹 Navigation
const nextTag = () => {
  if (currentTagIndex.value < uniqueTags.value.length - 1) {
    currentTagIndex.value++
  }
}

const prevTag = () => {
  if (currentTagIndex.value > 0) {
    currentTagIndex.value--
  }
}

// 🔹 Scroll vers le champ dans le document
const scrollToField = (tagName: string) => {
  emit('scroll-to-field', tagName)
}

// 🔹 Mise à jour en temps réel
watch(formData, (newValues) => {
  emit('update-data', newValues)
}, { deep: true })

const formatLabel = (tagName: string) =>
  tagName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())

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

/* 🎬 Animation de transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>