<template>
  <div class="filter-wrapper">
    <div class="mobile-filter">
      <select :value="selectedCategoryId" @change="handleMobileFilter">
        <option value="">Toutes les catégories</option>
        <option v-for="cat in categoryStore.categories" :key="cat.id" :value="cat.id">
          {{ cat.title }}
        </option>
      </select>
    </div>

    <div class="desktop-filter">
      <button 
        :class="{ active: selectedCategoryId === '' }" 
        @click="selectCategory('')"
      >
        Tout
      </button>
      <button 
        v-for="cat in categoryStore.categories" 
        :key="cat.id"
        :class="{ active: selectedCategoryId === cat.id }"
        @click="selectCategory(cat.id)"
      >
        {{ cat.title }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useContratStore } from '../../stores/contratStore';

export default {
  name: 'CategoryFilter',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const categoryStore = useContratStore();
    
    // 1. DYNAMIQUE : Le filtre actif correspond TOUJOURS à ce qui est écrit dans l'URL
    const selectedCategoryId = computed(() => {
      return (route.query.category as string) || '';
    });

    // 2. Déclenchée par les boutons Desktop
    const selectCategory = (categoryId: string) => {
      updateUrl(categoryId);
    };

    // 3. Déclenchée par le select Mobile
    const handleMobileFilter = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      updateUrl(target.value);
    };

    // 4. Logique centrale : On modifie simplement l'URL ! 
    // Le composant parent (cardSection.vue) détectera ce changement 
    // et s'occupera d'appeler l'API Django.
    const updateUrl = (categoryId: string) => {
      router.push({
        path: route.path, // Reste sur la page actuelle
        query: { 
          ...route.query, 
          // Si on clique sur "Tout" (vide), on retire 'category' de l'URL proprement
          category: categoryId || undefined 
        }
      });
    };

    onMounted(async () => {
      // Exécution forcée à chaque chargement de la page
      await categoryStore.getCategories();
    });

    return {
      categoryStore,
      selectedCategoryId,
      selectCategory,
      handleMobileFilter
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