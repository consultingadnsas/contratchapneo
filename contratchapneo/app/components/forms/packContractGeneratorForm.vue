<template>
  <form @submit.prevent="submitForm" class="contrat-form">
    <div v-if="store.isLoading" class="loading-state">
      <p>Analyse du document et préparation de votre contrat Premium...</p>
    </div>

    <div v-else-if="store.error" class="error-state">
      <p>🚨 Erreur : {{ store.error }} </p>
    </div>

    <div v-else-if="uniqueTags.length > 0" class="contract-prev-form">
      <transition name="fade" mode="out-in">
        <div v-if="currentTagIndex < uniqueTags.length" :key="currentTag" class="input-group">
          <!-- ⚡️ AJOUT : @keydown.enter.prevent="handleEnterKey" -->
          <BaseInputContract
            v-model="formData[currentTag]"
            :label="formatLabel(currentTag)"
            :type="getInputType(currentTag)"
            :placeholder="'Entrez : ' + formatLabel(currentTag).toLowerCase()"
            :disabled="store.isLoading"
            @focus="emit('focus-field', currentTag)"
            @keydown.enter.prevent="handleEnterKey"
          />
          <div class="progress-indicator">
            {{ currentTagIndex + 1 }} / {{ uniqueTags.length }}
          </div>
        </div>
      </transition>

      <div class="navigation-buttons">
        <button
          type="button"
          @click="prevTag"
          :disabled="currentTagIndex === 0"
          class="nav-btn prev-btn"
        >
          Précédent
        </button>

        <!-- ⚡️ AJOUT : :disabled="isCurrentFieldEmpty" -->
        <button
          v-if="currentTagIndex < uniqueTags.length - 1"
          type="button"
          @click="nextTag"
          :disabled="isCurrentFieldEmpty"
          class="nav-btn next-btn"
        >
          Suivant
        </button>

        <!-- ⚡️ AJOUT : :disabled="isCurrentFieldEmpty" sur le bouton de fin aussi -->
        <generatorButton 
          v-else 
          label="Générer mon contrat" 
          @click="submitForm" 
          :disabled="isCurrentFieldEmpty"
        />
      </div>
    </div>

    <div v-else>
      <p>Ce contrat standard est prêt. Il ne nécessite aucune information supplémentaire.</p>
      <generatorButton label="Télécharger le contrat" @click="submitForm" />
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
const currentTagIndex = ref(0) 

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

// ⚡️ AJOUT : Vérifie de manière réactive si le champ courant est vide
const isCurrentFieldEmpty = computed(() => {
  if (!currentTag.value) return true;
  const val = formData.value[currentTag.value];
  return !val || val.toString().trim() === '';
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

const nextTag = () => {
  // ⚡️ SÉCURITÉ : Empêche l'action si le champ est vide
  if (isCurrentFieldEmpty.value) return;

  if (currentTagIndex.value < uniqueTags.value.length - 1) {
    currentTagIndex.value++
  }
}

const prevTag = () => {
  if (currentTagIndex.value > 0) {
    currentTagIndex.value--
  }
}

// ⚡️ AJOUT : Gestionnaire pour la touche Entrée
const handleEnterKey = () => {
  // 1. Si le champ est vide, on ignore la touche Entrée
  if (isCurrentFieldEmpty.value) return;

  // 2. Si on n'est pas sur le dernier champ, on passe au suivant comme un clic sur "Suivant"
  if (currentTagIndex.value < uniqueTags.value.length - 1) {
    nextTag();
  } else {
    // 3. Si on est sur le TOUT DERNIER champ et qu'il est rempli, on soumet
    submitForm();
  }
};

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
  // ⚡️ SÉCURITÉ : On bloque aussi la soumission directe par le bouton si le dernier champ est vide
  if (isCurrentFieldEmpty.value) return;
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