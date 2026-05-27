<template>
  <div class="filter-wrapper">
    <div class="mobile-filter">
      <select v-model="selectedCategory" @change="emitFilter">
        <option value="">Toutes les catégories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>
    </div>

    <div class="desktop-filter">
      <button 
        :class="{ active: selectedCategory === '' }" 
        @click="selectCategory('')"
      >
        Tout
      </button>
      <button 
        v-for="cat in categories" 
        :key="cat"
        :class="{ active: selectedCategory === cat }"
        @click="selectCategory(cat)"
      >
        {{ cat }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
  name: 'CategoryFilter',
  emits: ['filter-change'],
  setup(props, { emit }) {
    // Catégories mises à jour pour s'adapter à une gestion d'événements
    const categories = ref(['Concert', 'Festival', 'Théâtre', 'Exposition', 'Conférence', 'Sport']);
    const selectedCategory = ref('');

    const selectCategory = (cat: string) => {
      selectedCategory.value = cat;
      emitFilter();
    };

    const emitFilter = () => {
      emit('filter-change', selectedCategory.value);
    };

    return {
      categories,
      selectedCategory,
      selectCategory,
      emitFilter
    };
  }
};
</script>

<style scoped>
.filter-wrapper {
  width: 100%;
  margin: 1rem 0;
}

/* ==========================================
   STYLE MOBILE (Par défaut)
   ========================================== */
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
    max-width: 600px; /* Ajusté pour une meilleure largeur */
    overflow-x: auto;
    padding-bottom: 0.5rem; /* Espace pour la barre de défilement */
    
    /* Défilement fluide sur les appareils tactiles (tablettes) */
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
    /* Propriétés essentielles pour le scroll horizontal */
    flex-shrink: 0; /* Empêche le bouton de se compresser */
    white-space: nowrap; /* Empêche le texte de passer à la ligne */
    
    padding: 0.4rem 1rem;
    font-size: 0.95rem;
    font-weight: 500;
    border: 1px solid #e2e8f0;
    border-radius: 999px;
    background-color: #ffffff;
    color: #4a5568;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
    max-width: 100px;
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