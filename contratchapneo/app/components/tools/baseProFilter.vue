<template>
  <div class="filter-wrapper">
    
    <div class="mobile-filter">
      <select :value="activeDomain" @change="onSelectChange">
        <option value="">Tous les domaines</option>
        <option v-for="domain in domains" :key="domain.id" :value="domain.slug">
          {{ domain.name }}
        </option>
      </select>
    </div>

    <div class="desktop-filter">
      <button 
        :class="{ active: activeDomain === '' }" 
        @click="selectDomain('')"
      >
        Tout
      </button>
      
      <button 
        v-for="domain in domains" 
        :key="domain.id" 
        :class="{ active: activeDomain === domain.slug }"
        @click="selectDomain(domain.slug)"
      >
        {{ domain.name }}
      </button>
    </div>
    
  </div>
</template>

<script lang="ts">
import { PropType } from 'vue';

export interface LegalDomain {
    id: number;
    name: string;
    slug: string;
}

export default {
  name: 'BaseProFilter',
  
  props: {
    domains: {
        type: Array as PropType<LegalDomain[]>,
        default: () => []
    },
    // NOUVEAU : On écoute le filtre actif dicté par l'URL/le parent
    activeDomain: {
        type: String,
        default: ''
    }
  },
  
  emits: ['filter'],
  
  setup(props, { emit }) {
    // Boutons Desktop
    const selectDomain = (slug: string) => {
      emit('filter', slug);
    };

    // Select Mobile
    const onSelectChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      emit('filter', target.value);
    };

    return {
      selectDomain,
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
  margin: 1rem 0;
}

.desktop-filter {
  display: none;
}

.mobile-filter select {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #ffffff;
  color: #1a1a1a;
  cursor: pointer;
  outline: none;
  /* Optionnel : cacher la flèche native pour mettre une custom */
  /* appearance: none; */
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
    gap: 0.5rem;
    width: 100%;
    /* J'ai supprimé la limite de 600px pour que les boutons occupent la place qu'il faut dans ta toolbar */
    overflow-x: auto;
    padding-bottom: 0.5rem;
    
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