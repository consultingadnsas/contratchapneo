<template>
  <header class="admin-header">
    <div class="header-titles">
      <h1 class="page-title">{{ title }}</h1>
      <p class="page-subtitle">{{ subtitle }}</p>
    </div>
    
    <div class="header-actions">
      <!-- Le bouton d'ajout global -->
      <button class="btn-primary" @click="$emit('add-contract')">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Nouveau Contrat
      </button>
    </div>
  </header>
</template>

<script lang="ts">
export default {
  name: 'AdminHeader',
  props: {
    title: { type: String, required: true },
    subtitle: { type: String, required: true }
  },
  emits: ['add-contract']
}
</script>

<style scoped>
.admin-header {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffffff; /* Texte blanc sur fond sombre */
  margin: 0 0 0.2rem 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: #94a3b8; /* Gris clair */
  margin: 0;
  font-size: 0.95rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #34d399; /* Vert ContratChap */
  color: #064e3b; /* Vert très foncé pour le texte */
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary svg { width: 20px; height: 20px; }
.btn-primary:hover { filter: brightness(1.1); transform: translateY(-2px); }

@media (min-width: 768px) {
  .admin-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
</style>