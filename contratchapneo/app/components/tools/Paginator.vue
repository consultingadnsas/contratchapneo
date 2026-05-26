<template>
  <div class="pagination-container">
    <button 
      class="pagination-btn" 
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
    >
      &laquo; Précédent
    </button>

    <div class="pages-list">
      <button 
        v-for="page in totalPages" 
        :key="page"
        class="page-number"
        :class="{ active: currentPage === page }"
        @click="changePage(page)"
      >
        {{ page }}
      </button>
    </div>

    <button 
      class="pagination-btn" 
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
    >
      Suivant &raquo;
    </button>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'

export default {
  name: 'StaticPagination',
  emits: ['page-change'],
  setup(props, { emit }) {
    // Configuration statique
    const currentPage = ref(1)
    const totalPages = ref(5) // Nombre de pages fixe pour le côté statique

    const changePage = (page: number) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        // Émet l'événement au cas où le composant parent en aurait besoin
        emit('page-change', page)
      }
    }

    return {
      currentPage,
      totalPages,
      changePage
    }
  }
}
</script>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
  width: 100%;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #ffffff;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #edf2f7;
}

.pages-list {
  display: flex;
  gap: 0.5rem;
}

.page-number {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  font-size: 0.95rem;
  font-weight: 500;
  border: 1px solid #e2e8f0;
  border-radius: 50%; /* Style rond */
  background-color: #ffffff;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-number:hover {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

/* Style de la page active (s'accorde avec le style de ton filtre) */
.page-number.active {
  background-color: #1a1a1a;
  color: #ffffff;
  border-color: #1a1a1a;
}
</style>