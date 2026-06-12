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
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Rechercher...'
    },
    theme: {
            type: String,
            default: 'light'
        }
  },
  emits: ['update:modelValue', 'focus', 'blur'],
  
  // Directive personnalisée locale pour fermer la recherche si on clique ailleurs
  directives: {
    clickOutside: {
      mounted(el, binding) {
        el.clickOutsideEvent = (event) => {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value();
          }
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

    // CORRECTION : On détecte tout de suite au lieu de mettre 'false' par défaut
    const isMobile = ref(typeof window !== 'undefined' ? window.innerWidth < 768 : false);

    const checkBreakpoint = () => {
      isMobile.value = window.innerWidth < 768;
      // Si on repasse sur écran large, on réinitialise l'état étendu
      if (!isMobile.value) isExpanded.value = false;
    };

    const expandSearch = async () => {
      isExpanded.value = true;
      await nextTick();
      inputRef.value?.focus();
    };

    const closeSearch = () => {
      if (!props.modelValue) {
        isExpanded.value = false;
      }
    };

    const handleInput = (event) => {
      emit('update:modelValue', event.target.value);
    };

    const clearSearch = () => {
      emit('update:modelValue', '');
      inputRef.value?.focus();
    };

    onMounted(() => {
      // Double vérification par sécurité au montage
      checkBreakpoint();
      window.addEventListener('resize', checkBreakpoint);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', checkBreakpoint);
    });

    return {
      isExpanded,
      isMobile,
      inputRef,
      expandSearch,
      closeSearch,
      handleInput,
      clearSearch
    };
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
  transition: all 0.3s ease;
  width: auto;
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

/* --- THÈME SUR FOND SOMBRE (theme="dark") --- */
.search-container.theme-dark {
  --bg-color: rgba(255, 255, 255, 0.1); /* Fond légèrement translucide */
  --text-color: #ffffff; /* Texte blanc */
  --border-color: rgba(255, 255, 255, 0.3); /* Bordure discrète */
  --icon-color: #e2e8f0; /* Icône blanche/gris clair */
  --focus-ring: rgba(255, 255, 255, 0.3);
  --primary-color: #ffffff;
}

/* Le fond devient tout blanc uniquement quand on clique dessus (focus) */
.search-container.theme-dark .search-input:focus {
  background-color: #ffffff;
  color: #0f172a; /* Texte noir/sombre */
}
/* Quand l'input devient blanc, les icônes (loupe/croix) doivent devenir sombres */
.search-container.theme-dark .search-input:focus ~ .clear-button,
.search-container.theme-dark:focus-within .internal-icon {
  color: #64748b; 
}


/* ==========================================
   APPLICATION DES VARIABLES
========================================== */
.search-input {
  width: 100%;
  padding: 0.7rem 2.5rem 0.7rem 2.7rem;
  font-size: 1rem;
  
  /* Utilisation des variables ici */
  background-color: var(--bg-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  
  border-radius: 1.5rem;
  outline: none;
  transition: all 0.2s ease;
}

/* Le placeholder prend la couleur de l'icône */
.search-input::placeholder {
  color: var(--icon-color);
}

.internal-icon, .clear-button {
  color: var(--icon-color);
}

.search-trigger:hover {
  background-color: #e5e7eb;
}

.search-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Wrapper du champ de saisie */
.search-input-wrapper {
  position: relative;
  display: none; /* Caché par défaut sur mobile */
  align-items: center;
  width: 100%;
}

.internal-icon {
  position: absolute;
  left: 1rem;
  color: #9ca3af;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.7rem 2.5rem 0.7rem 2.7rem;
  font-size: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 1.5rem; /* Reprise du style arrondi du BaseInput */
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.clear-button {
  position: absolute;
  right: 0.8rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 2px;
  display: flex;
  max-width: 50px
}

.clear-icon {
  width: 1.2rem;
  height: 1.2rem;
}

/* --- LOGIQUE RESPONSIVE (MOBILE EXPANDED & TABLETTE+) --- */

/* Quand la loupe est cliquée sur mobile */
.search-container.is-mobile.is-expanded {
  flex: 1;
  width: 100%;
}

.search-container.is-mobile.is-expanded .search-input-wrapper {
  display: flex;
  animation: fadeIn 0.2s ease-out;
}

/* Rendu naturel sur Tablette et Desktop (>= 768px) */
@media (min-width: 768px) {
  .search-container {
    width: 100%;
    max-width: 400px; /* S'affiche proprement dans une barre d'outils */
    flex: 1;
  }

  .search-trigger {
    display: none; /* Plus besoin du bouton déclencheur */
  }

  .search-input-wrapper {
    display: flex; /* Toujours visible */
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>