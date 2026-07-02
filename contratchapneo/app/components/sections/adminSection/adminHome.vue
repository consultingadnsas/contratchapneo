<template>
  <div class="dashboard-wrapper">
    
    <div class="top-section">
      
      <div class="overview-section">
        <h3 class="section-title">Aperçu financier</h3>
        <div class="overview-grid">
          
          <div class="gradient-card">
            <div class="card-header">
              <div class="icon-white"><svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg></div>
            </div>
            <div class="card-body">
              <h2>Revenus Globaux</h2>
              <p>Chiffre d'affaires total du mois</p>
            </div>
            <div class="card-footer">
              <div class="stat-block">
                <span>Total</span>
                <strong>2.3M FCFA</strong>
              </div>
            </div>
          </div>

          <div class="white-card">
            <div class="card-header">
              <div class="icon-purple"><svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg></div>
            </div>
            <div class="card-body">
              <h2 class="dark-text">Contrats Vendus</h2>
              <p class="gray-text">Modèles et packs téléchargés</p>
            </div>
            <div class="card-footer">
              <div class="stat-block-dark">
                <span>Ce mois</span>
                <strong>342</strong>
              </div>
            </div>
          </div>

        </div>
      </div>

      <div class="folders-section">
        <div class="section-header">
          <h3 class="section-title">Catalogue</h3>
        </div>
        <!-- Grille de dossiers -->
        <div class="folders-grid">
          
          <!-- 1. Dossier Rempli (Bleu) -->
          <folderCards 
            title="Sur-Mesure" 
            subtitle="12 demandes" 
            color="blue"
            :hasItems="true"
          />

          <!-- 2. Dossier Rempli (Orange) -->
          <folderCards
            title="Packs Création" 
            subtitle="Modifié le 14 Jul" 
            color="blue"
          />

          <!-- 3. Dossier Rempli (Violet) -->
          <folderCards 
            title="Modèles OHADA" 
            subtitle="Modifié le 2 Oct" 
            color="blue"
          />

          <!-- 4. L'ÉTAT VIDE (Bouton d'ajout) -->
          <folderCards 
            title="Voir plus..." 
            subtitle="Gérer les catégories" 
            color="gray" 
            :hasItems="true" 
            @action="$emit('open-catalogue')"
          />

        </div>
      </div>

    </div>

    <div class="activities-section">
      <div class="section-header">
        <h3 class="section-title">Dernières Activités</h3>
      </div>

      <div class="clean-list-container">
        <table class="minimal-table">
          <thead>
            <tr>
              <th>Type d'Action</th>
              <th>Statut</th>
              <th>Client</th>
              <th>Date</th>
              <th class="text-right">Montant</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in recentActivities" :key="item.id">
              <td>
                <div class="action-cell">
                  <span class="dark-text font-bold">{{ item.action }}</span>
                </div>
              </td>
              <td>
                <span class="status-dot" :class="item.statusColor"></span> 
                <span class="gray-text">{{ item.status }}</span>
              </td>
              <td class="gray-text">{{ item.client }}</td>
              <td class="gray-text">{{ item.date }}</td>
              <td class="text-right dark-text font-bold">{{ item.amount }} FCFA</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
// 1. On importe markRaw ET les vraies icônes de Heroicons
import { ref, markRaw } from 'vue';
import folderCards from '../../cards/folderCards.vue';
import { 
  ArrowDownTrayIcon, 
  ArrowUpTrayIcon, 
  CreditCardIcon 
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminOverview',
  components:{
    folderCards
  },
  emits: ['open-catalogue'],
  setup() {
    // 2. On utilise les vraies icônes enveloppées de markRaw()
    const recentActivities = ref([
      { 
        id: 1, 
        action: "Achat Modèle SARL", 
        status: "Succès", 
        statusColor: "dot-green", 
        client: "TechAfrica", 
        date: "05 Oct 2026", 
        amount: "15 000", 
        icon: markRaw(ArrowDownTrayIcon), 
        colorClass: 'bg-blue-light' 
      },
      { 
        id: 2, 
        action: "Demande Sur-Mesure", 
        status: "En attente", 
        statusColor: "dot-yellow", 
        client: "Bamba L.", 
        date: "12 Sep 2026", 
        amount: "250 000", 
        icon: markRaw(ArrowUpTrayIcon), 
        colorClass: 'bg-orange-light' 
      },
      { 
        id: 3, 
        action: "Achat Pack Création", 
        status: "Succès", 
        statusColor: "dot-green", 
        client: "Startup Z", 
        date: "15 Jul 2026", 
        amount: "45 000", 
        icon: markRaw(CreditCardIcon), 
        colorClass: 'bg-purple-light' 
      },
      { 
        id: 4, 
        action: "Achat Contrat Bail", 
        status: "Succès", 
        statusColor: "dot-green", 
        client: "Sylla Awa", 
        date: "07 May 2026", 
        amount: "15 000", 
        icon: markRaw(ArrowDownTrayIcon), 
        colorClass: 'bg-blue-light' 
      },
    ]);

    return { recentActivities };
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  --bg-main: #f8fafc;        /* Fond général très clair */
  --bg-panel: #ffffff;       /* Blanc pur pour les cartes */
  --text-dark: #1e293b;      /* Bleu nuit très foncé */
  --text-gray: #94a3b8;      /* Gris doux */
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2.5rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

.section-title { font-size: 1.1rem; color: var(--text-dark); font-weight: 700; margin: 0 0 1rem 0; }
.section-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1rem; }

/* LIGNE DU HAUT */
.top-section { display: grid; grid-template-columns: 1fr; gap: 2rem; }
@media (min-width: 1024px) { .top-section { grid-template-columns: 1.5fr 1fr; } }

/* GRILLE APERÇU (My Insurances) */
.overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; }

/* Carte Dégradée (Health Protection) */
.gradient-card {
  background: var(--primary-color);
  border-radius: 24px; padding: 1.5rem; color: white;
  display: flex; flex-direction: column; justify-content: space-between;
  min-height: 180px;
}
.icon-white { background: rgba(255,255,255,0.2); color:#32f459; padding: 0.5rem; border-radius: 12px; display: inline-flex; }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
.card-body h2 { margin: 0; font-size: 1.1rem; font-weight: 700; }
.card-body p { margin: 0.2rem 0 0 0; font-size: 0.8rem; opacity: 0.9; }
.card-footer { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 1.5rem; }
.stat-block { display: flex; flex-direction: column; }
.stat-block span { font-size: 0.7rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px; }
.stat-block strong { font-size: 1.2rem; }
.avatar { width: 28px; height: 28px; border-radius: 50%; background: white; color: #f43f5e; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: bold; border: 2px solid #f97316; margin-left: -8px; }

/* Carte Blanche (Auto Insurance) */
.white-card {
  background: rgba(255,255,255,0.2); border-radius: 24px; padding: 1.5rem;
  display: flex; flex-direction: column; justify-content: space-between;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; min-height: 180px;
}
.icon-purple { background:rgba(255,255,255,0.2); color: #32f459; padding: 0.5rem; border-radius: 12px; display: inline-flex; }
.dark-text { color: black; }
.gray-text { color: var(--text-gray); font-size: 0.85rem; }
.stat-block-dark { display: flex; flex-direction: column; }
.stat-block-dark span { font-size: 0.7rem; color: var(--text-gray); text-transform: uppercase; letter-spacing: 1px; }
.stat-block-dark strong { font-size: 1.2rem; color: black; }

/* DOSSIERS (Documents) */
.folders-grid { 
  display: grid; 
  /* minmax(140px) au lieu de 200px permet aux dossiers de s'afficher sur 2 colonnes même sur un petit écran iPhone ! */
  grid-template-columns: repeat(2, 1fr); 
  gap: 1rem; 
}

/* LIGNE DU BAS : TABLEAU ÉPURÉ (Last Activities) */
.clean-list-container {
  background: var(--bg-panel); border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9;
  overflow-x: auto;
}
.minimal-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 600px; }
.minimal-table th { color: #cbd5e1; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding-bottom: 1.5rem; }
.minimal-table td { padding: 1rem 0; border-bottom: 1px solid #f8fafc; vertical-align: middle; }
.minimal-table tr:last-child td { border-bottom: none; }

.action-cell { display: flex; align-items: center; gap: 1rem; }
.icon-box-light { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.bg-blue-light { background: #eff6ff; color: #3b82f6; }
.bg-orange-light { background: #fff7ed; color: #f97316; }
.bg-purple-light { background: #faf5ff; color: #a855f7; }

.font-bold { font-weight: 600; }
.text-right { text-align: right; }

.status-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 0.4rem; vertical-align: middle; }
.dot-green { background-color: #10b981; }
.dot-yellow { background-color: #f59e0b; }

.pill-btn {
  background: white; border: 1px solid #e2e8f0; color: var(--text-dark);
  padding: 0.4rem 1rem; border-radius: 50px; font-size: 0.8rem; font-weight: 600; cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}
@media (min-width: 1200px){
  .gradient-card {
  min-height: 300px;
}
}
</style>