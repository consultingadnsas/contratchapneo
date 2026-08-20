<template>
  <div class="finance-wrapper">
    
    <div class="header-section">
      <div class="title-and-tabs">
        <h3 class="section-title">Analyses Financières</h3>
      </div>
    </div>

    <!-- 1. KPI GRID -->
    <div class="kpi-grid">
      <!-- KPI 1 : Chiffre d'Affaires -->
      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-title">
            <div class="icon-box-light bg-blue-light"><component :is="BanknotesIcon" class="icon-sm" /></div>
            <span class="dark-text font-bold">Chiffre d'Affaires</span>
          </div>
          <div class="mini-bars"><div class="bar bar-low"></div><div class="bar bar-mid"></div><div class="bar bar-high bg-blue"></div></div>
        </div>
        <div class="kpi-body">
          <h2 class="amount">{{ formatCurrency(financeStore.accountancy?.global?.total_revenue) }} <span class="currency">FCFA</span></h2>
        </div>
        <p class="kpi-footer">Total des commandes payées</p>
      </div>

      <!-- KPI 2 : Ventes Réussies -->
      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-title">
            <div class="icon-box-light bg-green-light"><component :is="ChartPieIcon" class="icon-sm" /></div>
            <span class="dark-text font-bold">Ventes Réussies</span>
          </div>
          <div class="mini-bars"><div class="bar bar-mid"></div><div class="bar bar-low"></div><div class="bar bar-high bg-green"></div></div>
        </div>
        <div class="kpi-body"><h2 class="amount">{{ financeStore.accountancy?.transactions_status?.successful || 0 }}</h2></div>
        <p class="kpi-footer">Commandes avec statut "Payé"</p>
      </div>

      <!-- KPI 3 : En Attente -->
      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-title">
            <div class="icon-box-light bg-orange-light"><component :is="ShoppingCartIcon" class="icon-sm" /></div>
            <span class="dark-text font-bold">En Attente</span>
          </div>
          <div class="mini-bars"><div class="bar bar-high"></div><div class="bar bar-mid"></div><div class="bar bar-low bg-orange"></div></div>
        </div>
        <div class="kpi-body"><h2 class="amount">{{ financeStore.accountancy?.transactions_status?.pending || 0 }}</h2></div>
        <p class="kpi-footer">Paiements non finalisés</p>
      </div>
    </div>

    <!-- 2. LIGNE HAUTE : COURBE (2/3) + DONUT (1/3) -->
    <div class="charts-grid-top">
      <div class="chart-panel">
        <div class="panel-header">
          <div>
            <h4 class="dark-text font-bold text-lg">Évolution des revenus</h4>
            <p class="gray-text text-sm">Volume mensuel généré</p>
          </div>
        </div>
        <div class="chart-container" style="height: 280px; position: relative;">
          <RevenueChart :revenue-data="financeStore.computedMonthlyRevenue" />
        </div>
      </div>

      <div class="panel-card flex-col-center">
        <div class="panel-header text-center">
          <h4 class="dark-text font-bold text-lg">Répartition des statuts</h4>
        </div>
        <div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; position: relative; width: 100%;">
          <StatusDonutChart :status-stats="financeStore.accountancy?.transactions_status || { successful: 0, pending: 0, failed: 0 }" />
        </div>
      </div>
    </div>

    <!-- 3. LIGNE MILIEU : DEMANDES (Pleine largeur) -->
    <div class="panel-card">
      <div class="panel-header">
        <div>
          <h4 class="dark-text font-bold text-lg">Demandes de services personnalisés</h4>
          <p class="gray-text text-sm">Comparaison des volumes : Sur-mesure vs Révisions de contrats</p>
        </div>
      </div>
      <div class="chart-container" style="height: 280px; position: relative;">
        <DemandBarChart :demand-data="financeStore.demandStats" />
      </div>
    </div>

    <!-- 4. LIGNE BASSE : PACKS (1/2) + PROS (1/2) -->
    <div class="charts-grid-bottom">
      <div class="chart-panel">
        <div class="panel-header">
          <div>
            <h4 class="dark-text font-bold text-lg">Ventes de Packs</h4>
            <p class="gray-text text-sm">Volume mensuel des packs écoulés</p>
          </div>
        </div>
        <div class="chart-container" style="height: 260px; position: relative;">
          <PackChart :chart-data-array="financeStore.packStats" />
        </div>
      </div>

      <div class="chart-panel">
        <div class="panel-header">
          <div>
            <h4 class="dark-text font-bold text-lg">Sollicitations des Pros</h4>
            <p class="gray-text text-sm">Mises en relation avec les experts</p>
          </div>
        </div>
        <div class="chart-container" style="height: 260px; position: relative;">
          <ProChart :chart-data-array="financeStore.proStats" />
        </div>
      </div>
    </div>

    <!-- 5. LIGNE FINALE : TOP CONTRATS (Pleine largeur) -->
    <div class="panel-card mt-6">
      <div class="panel-header">
        <div>
          <h4 class="dark-text font-bold text-lg">Palmarès des Contrats</h4>
          <p class="gray-text text-sm">Les Contrats les plus téléchargés</p>
        </div>
      </div>
      <div class="chart-container" style="height: 300px; position: relative;">
        <ContratChart :top-data="financeStore.topContractsStats" />
      </div>
    </div>

    <!-- 6. LIGNE FINALE : TOP PACKS (1/2) + TOP PROS (1/2) -->
    <div class="charts-grid-bottom mt-6">
      
      <!-- Classement des Packs (Pie Chart) -->
      <div class="chart-panel">
        <div class="panel-header">
          <div>
            <h4 class="dark-text font-bold text-lg">Palmarès des Packs</h4>
            <p class="gray-text text-sm">Les offres groupées les plus vendues</p>
          </div>
        </div>
        <div class="chart-container" style="height: 300px; position: relative;">
          <TopPacksChart :top-data="financeStore.topPacksStats" />
        </div>
      </div>

      <!-- Classement des Pros (Polar Area Chart) -->
      <div class="chart-panel">
        <div class="panel-header">
          <div>
            <h4 class="dark-text font-bold text-lg">Classement des Experts</h4>
            <p class="gray-text text-sm">Les professionnels les plus sollicités</p>
          </div>
        </div>
        <div class="chart-container" style="height: 300px; position: relative;">
          <TopProChart :top-data="financeStore.topProsStats" />
        </div>
      </div>

    </div>

  </div>
</template>

<script lang="ts">
import { markRaw, onMounted } from 'vue';
import { 
  BanknotesIcon, ChartPieIcon, ShoppingCartIcon, DocumentChartBarIcon, CalculatorIcon, ChevronRightIcon
} from '@heroicons/vue/24/outline';

import { useAdminTransactStore } from '../../../stores/adminTransactStore'; 
import RevenueChart from '../../charts/revenuCharts.vue'; 
import StatusDonutChart from '../../charts/statutCharts.vue';
import DemandBarChart from '../../charts/demandChart.vue';
import PackChart from '../../charts/packChart.vue';
import ProChart from '../../charts/proChart.vue';
import ContratChart from '../../charts/contratChart.vue';
import TopPacksChart from '../../charts/topPackChart.vue';
import TopProChart from '../../charts/topProChart.vue'

export default {
  name: 'AdminFinance',
  components: {
    RevenueChart, StatusDonutChart, DemandBarChart, PackChart, ProChart, ContratChart, TopPacksChart, TopProChart,
  },
  setup() {
    const financeStore = useAdminTransactStore();

    onMounted(async () => {
      await financeStore.fetchTransact();
      await financeStore.fetchAccountancy();
    });

    const formatCurrency = (amount: number | string | undefined) => {
      const num = Number(amount) || 0;
      return num.toLocaleString('fr-FR');
    };

    return {
      financeStore,
      formatCurrency,
      BanknotesIcon: markRaw(BanknotesIcon),
      ChartPieIcon: markRaw(ChartPieIcon),
      ShoppingCartIcon: markRaw(ShoppingCartIcon),
      DocumentChartBarIcon: markRaw(DocumentChartBarIcon),
      CalculatorIcon: markRaw(CalculatorIcon),
      ChevronRightIcon: markRaw(ChevronRightIcon)
    };
  }
}
</script>

<style scoped>
/* STRUCTURE DE BASE */
.finance-wrapper {
  --bg-panel: #ffffff;
  --text-dark: #1e293b;
  --text-gray: #94a3b8;
  display: flex; 
  flex-direction: column; 
  gap: 1.5rem; /* Espace global réduit pour compacter l'interface */
  font-family: 'Inter', sans-serif; 
  padding-bottom: 2rem;
}

/* TYPOGRAPHIE ET UTILITAIRES */
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); }
.font-bold { font-weight: 700; }
.text-lg { font-size: 1.1rem; }
.text-sm { font-size: 0.8rem; }
.text-center { text-align: center; }
.flex-col-center { display: flex; flex-direction: column; height: 100%; }

/* HEADER */
.header-section { margin-bottom: 0.5rem; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 700; margin: 0; }

/* PANNEAUX ET CARTES */
.chart-panel, .panel-card, .kpi-card { 
  background: var(--bg-panel); 
  border-radius: 20px; 
  padding: 1.5rem; 
  box-shadow: 0 4px 20px rgba(0,0,0,0.03); 
  border: 1px solid #f1f5f9; 
}
.panel-header { margin-bottom: 1rem; }

/* GRILLE DES KPIS (3 colonnes) */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
.kpi-card { display: flex; flex-direction: column; justify-content: space-between; }
.kpi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.kpi-title { display: flex; align-items: center; gap: 0.8rem; }
.kpi-body { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; }
.amount { margin: 0; font-size: 1.6rem; font-weight: 800; color: var(--text-dark); }
.currency { font-size: 0.9rem; color: var(--text-gray); font-weight: 600; }
.kpi-footer { margin: 0; font-size: 0.75rem; color: var(--text-gray); }

/* ICONES ET MINI BARRES */
.icon-box-light { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.icon-sm { width: 20px; height: 20px; }
.bg-blue-light { background: #eff6ff; color: #3b82f6; }
.bg-orange-light { background: #fff7ed; color: #f97316; }
.bg-green-light { background: #d1fae5; color: #059669; }
.mini-bars { display: flex; gap: 4px; align-items: flex-end; height: 24px; }
.bar { width: 6px; border-radius: 4px; background: #e2e8f0; }
.bar-low { height: 40%; } .bar-mid { height: 70%; } .bar-high { height: 100%; }
.bg-blue { background: #3b82f6; } .bg-orange { background: #f97316; } .bg-green { background: #059669; }

/* ⚡️ LES NOUVELLES GRILLES D'AGENCEMENT */

/* Ligne Haute : Courbe (66%) + Donut (33%) */
.charts-grid-top { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 1024px) { 
  .charts-grid-top { grid-template-columns: 2fr 1fr; } 
}

/* Ligne Basse : Packs (50%) + Pros (50%) */
.charts-grid-bottom { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 1024px) { 
  .charts-grid-bottom { grid-template-columns: 1fr 1fr; } 
}
</style>