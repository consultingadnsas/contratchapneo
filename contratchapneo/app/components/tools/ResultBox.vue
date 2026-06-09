<template>
  <div class="result-box">
    <div v-if="loading" class="result-status">
      <span class="spinner"></span> Recherche en cours...
    </div>

    <div v-else-if="items.length === 0" class="result-status empty-state">
      Aucun résultat trouvé pour "{{ searchQuery }}"
    </div>

    <ul v-else class="result-list">
      <li 
        v-for="item in items" 
        :key="item.id" 
        class="result-item"
        @click="$emit('select', item)"
      >
        <div class="item-icon" v-if="item.icon">
          {{ item.icon }}
        </div>
        <div class="item-content">
          <p class="item-title">{{ item.title }}</p>
          <p v-if="item.description" class="item-description">{{ item.description }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ResultBox',
  props: {
    items: {
      type: Array,
      required: true,
      default: () => []
    },
    searchQuery: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['select']
}
</script>

<style scoped>
.result-box {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
  width: 100%;
  font-family: sans-serif;
  margin-top: 0.5rem;
  z-index: 50;
}

.result-status {
  padding: 1.5rem;
  text-align: center;
  color: #6b7280;
  font-size: 0.9rem;
}

.empty-state {
  font-style: italic;
}

.result-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.15s;
  border-bottom: 1px solid #f3f4f6;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background-color: #f3f4f6;
}

.item-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.item-content {
  display: flex;
  flex-direction: column;
}

.item-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 500;
  color: #1f2937;
}

.item-description {
  margin: 2px 0 0 0;
  font-size: 0.8rem;
  color: #6b7280;
}

/* Petit Spinner de chargement CSS */
.spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid #d1d5db;
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s linear infinite;
  margin-right: 6px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>