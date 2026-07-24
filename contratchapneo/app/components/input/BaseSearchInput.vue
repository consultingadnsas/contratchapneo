<template>
    <div 
        class="search-container" 
        :class="[`theme-${theme}`, { 'is-expanded': isExpanded || !isMobile, 'is-mobile': isMobile }]"
          v-click-outside="closeSearch"
    >
        <button 
            v-if="isMobile && !isExpanded" 
            class="search-trigger" 
            @click.stop="expandSearch"
            aria-label="Ouvrir la recherche"
        >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="search-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.604 10.604z" />
            </svg>
        </button>

        <div class="search-input-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="search-icon internal-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.604 10.604z" />
            </svg>
            
            <input
              ref="inputRef"
              class="search-input"
              :value="modelValue"
              @input="handleInput"
              :placeholder="placeholder"
              @focus="$emit('focus')"
              @blur="handleBlur"
            />

            <button v-if="modelValue" class="clear-button" @click="clearSearch" aria-label="Effacer">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="clear-icon">
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
            </svg>
            </button>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

export default {
  name: 'SearchInput',
  props: {
    modelValue: { type: String, default: '' },
    placeholder: { type: String, default: 'Rechercher...' },
    theme: { type: String, default: 'light' }
  },
  emits: ['update:modelValue', 'focus', 'blur'],
  
  directives: {
    clickOutside: {
      mounted(el, binding) {
        el.clickOutsideEvent = (event) => {
          if (!(el === event.target || el.contains(event.target))) binding.value();
        };
        document.addEventListener('click', el.clickOutsideEvent);
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent);
      }
    }
  },

  setup(props, { emit }) {
    const isExpanded = ref(false);
    const inputRef = ref(null);
    const isMobile = ref(typeof window !== 'undefined' ? window.innerWidth < 768 : false);

    const checkBreakpoint = () => {
      isMobile.value = window.innerWidth < 768;
      if (!isMobile.value) isExpanded.value = false;
    };

    const expandSearch = async () => {
      isExpanded.value = true;
      await nextTick();
      inputRef.value?.focus();
    };

    const closeSearch = () => {
      if (!props.modelValue) isExpanded.value = false;
    };

    const handleInput = (event) => emit('update:modelValue', event.target.value);

    const clearSearch = () => {
      emit('update:modelValue', '');
      inputRef.value?.focus();
    };

    onMounted(() => {
      checkBreakpoint();
      window.addEventListener('resize', checkBreakpoint);
    });

    onUnmounted(() => window.removeEventListener('resize', checkBreakpoint));

    return { isExpanded, isMobile, inputRef, expandSearch, closeSearch, handleInput, clearSearch };
  }
}
</script>

<style scoped>
.search-container {
  --border-color: #d1d5db;
  --focus-ring: rgba(59, 130, 246, 0.25);
  --primary-color: #3b82f6;
  
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  font-family: sans-serif;
  width: 100%; /* 👈 La barre prend 100% de la largeur du parent */
}

/* Style de la loupe seule sur Mobile */
.search-trigger {
  background: #f3f4f6;
  border: 1px solid var(--border-color);
  border-radius: 50%;
  width: 2.8rem;
  height: 2.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #4b5563;
  transition: background-color 0.2s;
}

.search-trigger:hover {
  background-color: #e5e7eb;
}

/* --- THÈME SOMBRE --- */
.search-container.theme-dark {
  --bg-color: rgba(255, 255, 255, 0.1); 
  --text-color: #ffffff; 
  --border-color: rgba(255, 255, 255, 0.3); 
  --icon-color: #e2e8f0; 
  --focus-ring: rgba(255, 255, 255, 0.3);
  --primary-color: #ffffff;
}

.search-container.theme-dark .search-input:focus {
  background-color: #ffffff;
  color: #0f172a; 
}
.search-container.theme-dark .search-input:focus ~ .clear-button,
.search-container.theme-dark:focus-within .internal-icon {
  color: #64748b; 
}

/* --- INPUT --- */
.search-input {
  width: 100%;
  /* ⚡️ MODIFIÉ : padding-left passe à 3.2rem (au lieu de 2.6rem) pour faire de la place au rond */
  padding: 0.65rem 2.5rem 0.65rem 3.2rem; 
  font-size: 0.95rem; 
  
  background-color: var(--bg-color, #ffffff);
  color: var(--text-color, #111827);
  border: 1px solid var(--border-color);
  border-radius: 50px;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.search-input::placeholder {
  color: var(--icon-color, #9ca3af);
}

.internal-icon, .clear-button {
  color: var(--icon-color, #9ca3af);
}

.search-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.search-input-wrapper {
  position: relative;
  display: none; 
  align-items: center;
  width: 100%;
}

.internal-icon {
  position: absolute;
  /* ⚡️ MODIFIÉ : Ajustement de la position et création du cercle */
  left: 0.7rem; /* Collé un peu plus à gauche pour un bel effet "pilule" */
  pointer-events: none;
  
  background-color: var(--primary-color); /* Le rond bleu */
  color: #ffffff !important; /* La loupe en blanc (le !important empêche le thème sombre de la griser au clic) */
  border-radius: 50%; /* Création du rond */
  padding: 0.4rem; /* Espace interne pour que la loupe respire */
  
  /* Taille globale du cercle */
  width: 2.2rem;
  height: 2.2rem;
  box-sizing: border-box; /* S'assure que le padding ne déforme pas le rond */
}

/* --- LE BOUTON X --- */
.clear-button {
  position: absolute;
  right: -7rem; /* 👈 Bien calé à droite */
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.clear-button:hover {
  background-color: transparent;
}

.clear-icon {
  width: 1.2rem;
  height: 1.2rem;
}

/* --- RESPONSIVE --- */
.search-container.is-mobile.is-expanded {
  flex: 1;
  width: 100%;
}
.search-container.is-mobile.is-expanded .search-input-wrapper {
  display: flex;
  animation: fadeIn 0.2s ease-out;
}

@media (min-width: 768px) {
  .search-container {
    width: 100%;
    /* Pas de max-width fixe ici, le parent décide ! */
  }
  .search-trigger { display: none; }
  .search-input-wrapper { display: flex; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>