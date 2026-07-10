<template>
  <div class="input-group" :class="{ 'has-error': !!errorMessage, 'is-disabled': disabled }">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>

    <div class="input-wrapper">
      <span class="input-icon input-icon-left">
        <slot name="prepend">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </slot>
      </span>

      <input
        :id="inputId"
        ref="inputRef"
        class="form-input search-padding"
        :class="{ 'pr-icon': $slots.append }"
        v-model="searchQuery"
        :disabled="disabled"
        v-bind="$attrs"
        @input="handleInput"
        @blur="handleBlur"
        @focus="isFocused = true"
        @keydown.enter="submitSearch(searchQuery)"
        :placeholder="placeholder"
        autocomplete="off"
      />

      <span v-if="$slots.append" class="input-icon input-icon-right">
        <slot name="append"></slot>
      </span>

      <!-- 
        MODIFICATION ICI : 
        On affiche le menu si l'input a le focus ET qu'il y a du texte saisi 
      -->
      <ul v-if="isFocused && searchQuery.trim() !== ''" class="suggestions-dropdown">
        
        <!-- État 1 : Chargement -->
        <li v-if="isLoading" class="suggestion-item loading-text">
          Recherche en cours...
        </li>
        
        <!-- État 2 : Résultats trouvés -->
        <template v-else-if="suggestions.length > 0">
          <li 
              v-for="sug in suggestions" 
              :key="sug.id" 
              class="suggestion-item"
              @mousedown.prevent="submitSearch(sug.title)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="sug-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            </svg>
            <span class="sug-text">{{ sug.title }}</span>
          </li>
        </template>

        <!-- État 3 : Aucun résultat (Redirection Sur-mesure) -->
        <li v-else class="suggestion-item custom-contract-item" @mousedown.prevent="goToCustomContract">
          <div class="custom-icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="sug-icon custom-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
            </svg>
          </div>
          <div class="custom-text-wrapper">
            <span class="no-result-text">Aucun modèle trouvé pour "<strong>{{ searchQuery }}</strong>"</span>
            <span class="sug-text highlight-text">Créer un contrat sur-mesure &rarr;</span>
          </div>
        </li>

      </ul>
    </div>

    <p v-if="errorMessage" :id="`${inputId}-error`" class="message error-message">
       {{ errorMessage }}
    </p>
  </div>
</template>

<script lang="ts">
import { useId, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useNuxtApp } from '#app'

export default {
  name: 'BaseResearchInput',
  inheritAttrs: false,
  props: {
    label: { type: String, default: '' },
    errorMessage: { type: String, default: '' },
    id: { type: String, default: null },
    disabled: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    placeholder: { type: String, default: 'Trouver un contrat...' }
  },
  setup(props) {
    const generatedId = useId()
    const inputId = props.id || `search-${generatedId}`
    
    const router = useRouter()
    const { $api } = useNuxtApp()

    const searchQuery = ref('')
    const suggestions = ref<any[]>([])
    const isFocused = ref(false)
    const isLoading = ref(false)
    let debounceTimeout: NodeJS.Timeout | null = null

    const handleInput = () => {
      if (debounceTimeout) clearTimeout(debounceTimeout)
      
      if (!searchQuery.value.trim()) {
        suggestions.value = []
        return
      }

      isLoading.value = true
      
      debounceTimeout = setTimeout(async () => {
        try {
          const response = await $api('/contrat/', {
            method: 'GET',
            params: { q: searchQuery.value }
          })
          
          suggestions.value = response?.results?.slice(0, 5) || []
        } catch (error) {
          console.error("Erreur lors de la recherche des suggestions:", error)
          suggestions.value = []
        } finally {
          isLoading.value = false
        }
      }, 400)
    }

    const submitSearch = (queryToSearch: string) => {
      if (!queryToSearch.trim()) return
      
      isFocused.value = false
      router.push({ 
        path: '/contractBank', 
        query: { q: queryToSearch.trim() } 
      })
    }

    // NOUVELLE ACTION : Redirection vers le contrat sur-mesure
    const goToCustomContract = () => {
      isFocused.value = false
      router.push('/contractBank/customContrat')
    }

    const handleBlur = () => {
      setTimeout(() => {
        isFocused.value = false
      }, 200)
    }

    return {
      inputId,
      searchQuery,
      suggestions,
      isFocused,
      isLoading,
      handleInput,
      handleBlur,
      submitSearch,
      goToCustomContract // On n'oublie pas d'exposer la fonction
    }
  }
}
</script>

<style scoped>
/* ==========================================
   STYLES GLOBAUX INCHANGÉS
========================================== */
.input-group {
  --glass-bg: rgba(255, 255, 255, 0.167);
  --glass-border: rgba(255, 255, 255, 0.2);
  --primary-color: #60a5fa; 
  --text-color: #ffffff;
  
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1rem;
  position: relative;
  top: 2rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.input-label{ text-align: start; }

.form-input {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  color: var(--text-color);
  background: rgba(255, 255, 255, 0.089);
  backdrop-filter: blur(15px);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding-left: 3.8rem !important;
  z-index: 10;
}

.form-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.18);
  border-color: var(--primary-color);
  box-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
  transform: scale(1.01);
}

.input-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  pointer-events: none;
  z-index: 11;
}

.input-icon-left {
  left: 8px;
  background: var(--primary-color-dark); 
  width: 40px;  
  height: 40px; 
  border-radius: 50%; 
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.input-icon-left :deep(svg), 
.input-icon-left svg {
    width: 20px;
    height: 20px;
    color: white !important; 
}

.search-icon {
  width: 20px;
  height: 20px;
  color: var(--primary-color);
  filter: drop-shadow(0 0 5px rgba(96, 165, 250, 0.4));
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
  font-weight: 300;
}

/* ==========================================
   MENU DE SUGGESTIONS
========================================== */
.suggestions-dropdown {
  position: absolute;
  top: calc(100% + 10px); 
  left: 0;
  width: 100%;
  background: rgba(30, 41, 59, 0.85); 
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  list-style: none;
  padding: 0.5rem;
  margin: 0;
  z-index: 50;
  max-height: 250px;
  overflow-y: auto;
  animation: slideDown 0.2s ease-out;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0.8rem 1.2rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.suggestion-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  transform: translateX(4px);
}

.sug-icon {
  width: 18px;
  height: 18px;
  color: var(--primary-color);
}

.sug-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.loading-text {
  color: #94a3b8;
  font-style: italic;
  justify-content: center;
  pointer-events: none;
}

/* ==========================================
   ÉTAT : AUCUN RÉSULTAT (SUR-MESURE)
========================================== */
.custom-contract-item {
  background: rgba(96, 165, 250, 0.05); /* Fond légèrement bleu */
  border: 1px dashed rgba(96, 165, 250, 0.3);
  padding: 1rem 1.2rem;
  align-items: flex-start; /* Aligne l'icône en haut si le texte passe sur 2 lignes */
}

.custom-contract-item:hover {
  background: rgba(96, 165, 250, 0.15);
  border-color: rgba(96, 165, 250, 0.6);
  transform: translateY(-2px); /* Un petit effet de soulèvement au lieu d'une translation latérale */
}

.custom-icon-wrapper {
  margin-top: 2px;
}

.custom-icon {
  color: #60a5fa; /* Couleur d'accentuation (Bleu) */
  width: 22px;
  height: 22px;
}

.custom-text-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  width: 100%;
}

.no-result-text {
  font-size: 0.85rem;
  color: #94a3b8;
}

.highlight-text {
  color: #60a5fa;
  font-weight: 700;
  font-size: 1rem;
}

/* Custom Scrollbar pour le menu */
.suggestions-dropdown::-webkit-scrollbar { width: 6px; }
.suggestions-dropdown::-webkit-scrollbar-thumb { background-color: rgba(255, 255, 255, 0.2); border-radius: 10px; }

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>