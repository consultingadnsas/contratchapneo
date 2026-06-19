<template>
  <div class="dashboard-wrapper">
    
    <!-- LIGNE 1 : REVENUS & STATS RAPIDES (Comme "Total Holding" & "My Portfolio") -->
    <div class="top-row">
      <!-- Carte Revenus Globaux -->
      <div class="panel main-stat-panel">
        <div class="panel-header-simple">
          <span class="text-gray">Revenus Globaux</span>
          <div class="pill-select">
            <span>Ce mois</span>
            <svg class="icon-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
          </div>
        </div>
        <div class="main-stat-body">
          <h1 class="amount">2 350 000 <span class="currency">FCFA</span></h1>
          <p class="return-positive">Return <span>+3.5% (82 000)</span></p>
        </div>
      </div>

      <!-- Cartes Mini-Stats (Comme "My Portfolio") -->
      <div class="panel mini-stats-panel">
        <div class="panel-header-simple">
          <span class="text-gray">Vue d'ensemble</span>
          <div class="pill-btn">Voir tout <svg class="icon-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg></div>
        </div>
        <div class="mini-cards-grid">
          <div class="mini-card" v-for="stat in quickStats" :key="stat.id">
            <div class="mini-card-top">
              <span class="mini-value">{{ stat.value }}</span>
              <span class="mini-trend" :class="stat.up ? 'text-green' : 'text-red'">{{ stat.trend }}</span>
            </div>
            <div class="mini-card-bottom">
              <span class="mini-label">{{ stat.label }}</span>
              <span class="mini-sub">{{ stat.sub }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- LIGNE 2 : HISTORIQUE DES TÉLÉCHARGEMENTS (À la place du grand graphique) -->
    <div class="panel history-panel">
      <div class="panel-header-flex">
        <span class="text-gray">Historique des Téléchargements</span>
        <div class="tabs-group">
          <button class="tab-btn active">Tous</button>
          <button class="tab-btn">Modèles</button>
          <button class="tab-btn">Packs</button>
        </div>
      </div>
      
      <!-- Tableau épuré (Style "Portfolio Overview") -->
      <table class="clean-table">
        <thead>
          <tr>
            <th>Document</th>
            <th>Client</th>
            <th>Prix</th>
            <th>Date</th>
            <th class="text-right">Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in downloadHistory" :key="item.id">
            <td class="font-bold text-white flex-align">
              <span class="doc-icon">📄</span> {{ item.doc }}
            </td>
            <td class="text-gray">{{ item.client }}</td>
            <td class="font-bold">{{ item.price }} FCFA</td>
            <td class="text-gray">{{ item.date }}</td>
            <td class="text-right text-green flex-align-right">
              {{ item.status }} <span class="dot-green"></span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- LIGNE 3 : PACKS & SUR-MESURE (Comme le bas de l'image) -->
    <div class="bottom-row">
      <!-- Derniers Packs -->
      <div class="panel">
        <div class="panel-header-simple">
          <span class="text-gray">Derniers Packs Achetés</span>
          <div class="tabs-group">
            <button class="tab-btn active">Gros succès</button>
            <button class="tab-btn">Nouveaux</button>
          </div>
        </div>
        <table class="clean-table no-header">
          <tbody>
            <tr v-for="pack in recentPacks" :key="pack.id">
              <td class="font-bold text-white flex-align"><span class="doc-icon">📦</span> {{ pack.name }}</td>
              <td class="text-gray">{{ pack.client }}</td>
              <td class="text-right font-bold text-blue">{{ pack.price }} FCFA</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Alertes / Sur-Mesure -->
      <div class="panel">
        <div class="panel-header-simple">
          <span class="text-gray">Demandes Sur-Mesure</span>
          <div class="pill-btn active-pill">Urgent</div>
        </div>
        <ul class="simple-list">
          <li v-for="task in urgentTasks" :key="task.id">
            <div class="list-info">
              <h4 class="text-white font-bold">{{ task.title }}</h4>
              <p class="text-gray text-xs">{{ task.client }}</p>
            </div>
            <span class="text-green text-sm font-bold">+{{ task.budget }} F</span>
          </li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
  name: 'AdminOverview',
  setup() {
    const quickStats = ref([
      { id: 1, value: "342", trend: "+12.5%", up: true, label: "Téléchargements", sub: "Modèles" },
      { id: 2, value: "28", trend: "+5.2%", up: true, label: "Packs Vendus", sub: "Premium" },
      { id: 3, value: "45", trend: "-1.5%", up: false, label: "Nouveaux Clients", sub: "Inscrits" },
      { id: 4, value: "8", trend: "+2.0%", up: true, label: "Sur-Mesure", sub: "Demandes" },
    ]);

    const downloadHistory = ref([
      { id: 1, doc: "Statuts SARL OHADA", client: "TechAfrica", price: "15 000", date: "Aujourd'hui, 10:45", status: "Payé" },
      { id: 2, doc: "Contrat de Prestation", client: "Konan M.", price: "10 000", date: "Aujourd'hui, 09:12", status: "Payé" },
      { id: 3, doc: "Pacte d'Associés", client: "Startup Z", price: "25 000", date: "Hier", status: "Payé" },
      { id: 4, doc: "Contrat de Travail", client: "Sylla Awa", price: "15 000", date: "Hier", status: "Payé" },
    ]);

    const recentPacks = ref([
      { id: 1, name: "Pack Création Entreprise", client: "Bamba L.", price: "45 000" },
      { id: 2, name: "Pack RH & Embauche", client: "ImmoTech", price: "30 000" },
      { id: 3, name: "Pack Freelance", client: "Koffi A.", price: "20 000" },
    ]);

    const urgentTasks = ref([
      { id: 1, title: "Contrat de Fusion", client: "Groupe EBOMAF", budget: "150k" },
      { id: 2, title: "Audit Juridique", client: "FinTech CI", budget: "300k" },
    ]);

    return { quickStats, downloadHistory, recentPacks, urgentTasks };
  }
}
</script>

<style scoped>
/* COULEURS ET VARIABLES INSPIRÉES DE L'IMAGE */
.dashboard-wrapper {
  --bg-panel: #161618; /* Gris très sombre presque noir */
  --bg-panel-light: #1e1e20; /* Pour les mini-cartes */
  --border-color: #2a2a2c;
  --text-main: #ffffff;
  --text-muted: #8a8a8e;
  --accent-blue: #0A84FF;
  --accent-green: #30D158;
  --accent-red: #FF453A;
  
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  font-family: 'Inter', sans-serif;
  padding-bottom: 2rem;
}

/* PANNEAUX GLOBAUX */
.panel {
  background-color: var(--bg-panel);
  border: 1px solid var(--border-color);
  border-radius: 20px; /* Bords bien arrondis comme l'image */
  padding: 1.5rem;
}

/* LIGNE 1 */
.top-row { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 1024px) { .top-row { grid-template-columns: 1fr 2fr; } }

/* CARTE REVENUS (Avec un fond subtil de vague si possible, ici simulé par un dégradé) */
.main-stat-panel {
  background: linear-gradient(135deg, #161618 0%, #1a1a1d 100%);
  display: flex; flex-direction: column; justify-content: space-between;
}
.panel-header-simple { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.text-gray { color: var(--text-muted); font-size: 0.9rem; font-weight: 500; }

.pill-select, .pill-btn {
  display: flex; align-items: center; gap: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 50px; padding: 0.3rem 0.8rem;
  font-size: 0.8rem; color: var(--text-main); cursor: pointer;
}
.active-pill { background-color: var(--accent-blue); border-color: var(--accent-blue); }

.amount { font-size: 2.5rem; font-weight: 600; color: var(--text-main); margin: 1rem 0 0.5rem 0; letter-spacing: -1px; }
.currency { font-size: 1.2rem; color: var(--text-muted); }
.return-positive { font-size: 0.9rem; color: var(--text-muted); }
.return-positive span { color: var(--accent-green); background: rgba(48, 209, 88, 0.1); padding: 0.2rem 0.5rem; border-radius: 10px; margin-left: 0.5rem; }

/* MINI CARTES STATS */
.mini-cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1rem; }
.mini-card {
  background-color: var(--bg-panel-light); border: 1px solid var(--border-color);
  border-radius: 16px; padding: 1rem; display: flex; flex-direction: column; justify-content: space-between;
}
.mini-card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.mini-value { font-size: 1.2rem; font-weight: 600; color: var(--text-main); }
.mini-trend { font-size: 0.75rem; font-weight: 600; }
.text-green { color: var(--accent-green); }
.text-red { color: var(--accent-red); }
.text-blue { color: var(--accent-blue); }
.mini-card-bottom { display: flex; justify-content: space-between; align-items: center; }
.mini-label { font-size: 0.8rem; color: var(--text-muted); }
.mini-sub { font-size: 0.7rem; color: #555; }

/* LIGNE 2 & TABS (Pilules) */
.panel-header-flex { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.tabs-group { display: flex; background: var(--bg-panel-light); border-radius: 50px; padding: 0.2rem; border: 1px solid var(--border-color); }
.tab-btn {
  background: transparent; border: none; color: var(--text-muted); font-size: 0.8rem;
  padding: 0.4rem 1rem; border-radius: 50px; cursor: pointer; transition: all 0.2s;
}
.tab-btn.active { background: var(--accent-blue); color: var(--text-main); }

/* TABLEAUX ÉPURÉS */
.clean-table { width: 100%; border-collapse: collapse; text-align: left; }
.clean-table th { color: var(--text-muted); font-size: 0.8rem; font-weight: 500; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }
.clean-table td { padding: 1rem 0; font-size: 0.9rem; border-bottom: 1px solid rgba(255,255,255,0.02); }
.clean-table tr:last-child td { border-bottom: none; }
.no-header th { display: none; }
.text-white { color: var(--text-main); }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.flex-align { display: flex; align-items: center; gap: 0.8rem; }
.flex-align-right { display: flex; justify-content: flex-end; align-items: center; gap: 0.5rem; }
.doc-icon { background: var(--bg-panel-light); padding: 0.4rem; border-radius: 8px; font-size: 1.1rem; }
.dot-green { width: 8px; height: 8px; background-color: var(--accent-green); border-radius: 50%; box-shadow: 0 0 8px var(--accent-green); }

/* LIGNE 3 */
.bottom-row { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 1024px) { .bottom-row { grid-template-columns: 2fr 1fr; } }

/* LISTE SIMPLE */
.simple-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 1rem; }
.simple-list li { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.02); }
.text-xs { font-size: 0.75rem; margin-top: 0.2rem; }
.text-sm { font-size: 0.85rem; }
.icon-sm { width: 16px; height: 16px; }
</style>