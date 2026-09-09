<template>
  <div class="filter-wrapper">
    
    <div class="mobile-filter">
      <select :value="currentActive" @change="onSelectChange">
        <option value="">{{ placeholder }}</option>
        <option 
          v-for="item in itemsList" 
          :key="getItemKey(item)" 
          :value="getItemValue(item)"
        >
          {{ getItemLabel(item) }}
        </option>
      </select>
    </div>

    <div class="desktop-filter">
      <button 
        :class="{ active: currentActive === '' }" 
        @click="selectItem('')"
      >
        Tout
      </button>
      
      <button 
        v-for="item in itemsList" 
        :key="getItemKey(item)" 
        :class="{ active: currentActive === getItemValue(item) }"
        @click="selectItem(getItemValue(item))"
      >
        {{ getItemLabel(item) }}
      </button>
    </div>
    
  </div>
</template>

<script lang="ts">
import { PropType, computed } from 'vue';

export interface FilterItem {
    id?: string | number;
    name?: string;
    label?: string;
    code?: string;
    slug?: string;
}

export default {
  name: 'BaseProFilter',
  
  props: {
    titles: {
        type: Array as PropType<any[]>,
        default: () => []
    },
    domains: {
        type: Array as PropType<any[]>,
        default: () => []
    },
    activeTitle: {
        type: String,
        default: ''
    },
    activeDomain: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: 'Tous les titres'
    }
  },
  
  emits: ['filter', 'update:activeTitle'],
  
  setup(props, { emit }) {
    const itemsList = computed(() => {
      if (props.titles && props.titles.length > 0) {
        return props.titles;
      }
      return props.domains || [];
    });

    const currentActive = computed(() => {
      if (props.activeTitle !== undefined && props.activeTitle !== '') {
        return props.activeTitle;
      }
      return props.activeDomain || '';
    });

    const getItemKey = (item: any) => item.id || item.code || item.slug || item.name;
    const getItemValue = (item: any) => item.code || item.slug || item.id || '';
    const getItemLabel = (item: any) => item.name || item.label || item.title || '';

    // Boutons Desktop & Select Mobile
    const selectItem = (value: string) => {
      emit('filter', value);
      emit('update:activeTitle', value);
    };

    const onSelectChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      selectItem(target.value);
    };

    return {
      itemsList,
      currentActive,
      getItemKey,
      getItemValue,
      getItemLabel,
      selectItem,
      onSelectChange
    };
  }
};
</script>

<style scoped>
/* ==========================================
   STYLE MOBILE (Par défaut)
   ========================================== */
.filter-wrapper {
  width: 100%;
  margin: 0;
}

.desktop-filter {
  display: none;
}

.mobile-filter select {
  width: 100%;
  /* On ajoute un padding à droite (2.5rem) pour que le texte ne chevauche pas la flèche */
  padding: 0.75rem 2.5rem 0.75rem 1rem; 
  font-size: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 50px;
  background-color: #ffffff;
  color: #1a1a1a;
  cursor: pointer;
  outline: none;
  
  /* 1. On cache la flèche native du navigateur */
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  
  /* 2. On ajoute une flèche SVG personnalisée */
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234a5568' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-size: 1.1rem;
  
  /* 3. On décale la flèche vers la gauche (ex: à 15px du bord droit) */
  background-position: right 10px center;
}

/* ==========================================
   STYLE TABLETTE & DESKTOP (Écrans >= 768px)
   ========================================== */
@media (min-width: 768px) {
  .mobile-filter {
    display: none;
  }

  .desktop-filter {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
    /* J'ai supprimé la limite de 600px pour que les boutons occupent la place qu'il faut dans ta toolbar */
    overflow-x: auto;
    padding-bottom: 0.25rem;
    
    /* Défilement fluide sur les appareils tactiles */
    -webkit-overflow-scrolling: touch;
    
    /* Firefox : barre de scroll plus fine */
    scrollbar-width: thin;
    scrollbar-color: #cbd5e0 transparent;
  }

  /* Personnalisation de la barre de défilement (Chrome, Safari, Edge) */
  .desktop-filter::-webkit-scrollbar {
    height: 6px;
  }
  
  .desktop-filter::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .desktop-filter::-webkit-scrollbar-thumb {
    background-color: #cbd5e0;
    border-radius: 20px;
  }

  .desktop-filter button {
    flex-shrink: 0;
    white-space: nowrap;
    padding: 0.4rem 1rem;
    font-size: 0.95rem;
    font-weight: 500;
    border: 1px solid #e2e8f0;
    border-radius: 999px;
    background-color: #ffffff;
    color: #4a5568;
    cursor: pointer;
    transition: all 0.2s ease;
    width: auto;
  }

  .desktop-filter button:hover {
    background-color: #f7fafc;
    border-color: #cbd5e0;
  }

  .desktop-filter button.active {
    background-color: var(--primary-color);
    color: #ffffff;
    border-color: var(--primary-color);
  }
}
</style>