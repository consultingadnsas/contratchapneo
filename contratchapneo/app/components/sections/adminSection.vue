<template>
  <div class="overview-content">
    <!-- Exemple de tableau de bord rapide -->
    <div class="cards-grid">
      <div class="stat-card">
        <h4>Contrats Actifs</h4>
        <p class="value">124</p>
      </div>
      <div class="stat-card">
        <h4>Demandes en attente</h4>
        <p class="value text-warning">5</p>
      </div>
    </div>

    <!-- Dernières Actions / Activité -->
    <section class="recent-actions">
      <h2>Dernières actions</h2>
      <div class="action-list">
        <div class="action-item">
          <div class="action-icon bg-green">✓</div>
          <div class="action-details">
            <p><strong>Contrat de Bail</strong> ajouté au catalogue</p>
            <span>Aujourd'hui, 10:42</span>
          </div>
        </div>
        <div class="action-item">
          <div class="action-icon bg-blue">↻</div>
          <div class="action-details">
            <p>Mise à jour du modèle <strong>Statuts SARL</strong></p>
            <span>Hier, 16:15</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.overview-content { display: flex; flex-direction: column; gap: 2rem; }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; }

/* Cartes sur fond sombre */
.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 12px;
}
.stat-card h4 { color: #94a3b8; font-size: 0.9rem; font-weight: 500; margin: 0 0 0.5rem 0; }
.stat-card .value { color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0; }
.text-warning { color: #facc15 !important; }

/* Liste d'actions */
.recent-actions h2 { color: #ffffff; font-size: 1.2rem; margin-bottom: 1rem; }
.action-list { display: flex; flex-direction: column; gap: 1rem; }
.action-item { display: flex; align-items: center; gap: 1rem; background: rgba(255, 255, 255, 0.03); padding: 1rem; border-radius: 12px; }
.action-icon { width: 36px; height: 36px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; }
.bg-green { background: rgba(52, 211, 153, 0.2); color: #34d399; }
.bg-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.action-details p { color: #e2e8f0; margin: 0 0 0.2rem 0; font-size: 0.95rem; }
.action-details span { color: #64748b; font-size: 0.8rem; }
</style>