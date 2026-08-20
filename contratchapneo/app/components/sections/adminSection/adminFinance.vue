<template>
  <div class="finance-wrapper">
    
    <div class="header-section">
      <div class="title-and-tabs">
        <h3 class="section-title">Analyses Financières</h3>
        <div class="header-links hidden-mobile">
          <span class="active-link">Aperçu</span>
          <span>Rapports</span>
          <span>Revenus</span>
        </div>
      </div>
    </div>

    <div class="kpi-grid">
      
      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-title">
            <div class="icon-box-light bg-blue-light">
              <component :is="BanknotesIcon" class="icon-sm" />
            </div>
            <span class="dark-text font-bold">Chiffre d'Affaires</span>
          </div>
          <div class="mini-bars">
            <div class="bar bar-low"></div><div class="bar bar-mid"></div><div class="bar bar-high bg-blue"></div>
          </div>
        </div>
        <div class="kpi-body">
          <h2 class="amount">
            {{ formatCurrency(financeStore.accountancy?.global?.total_revenue) }} 
            <span class="currency">FCFA</span>
          </h2>
        </div>
        <p class="kpi-footer">Total des commandes payées</p>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-title">
            <div class="icon-box-light bg-green-light" style="background: #d1fae5; color: #059669;">
              <component :is="ChartPieIcon" class="icon-sm" />
            </div>
            <span class="dark-text font-bold">Ventes Réussies</span>
          </div>
          <div class="mini-bars">
            <div class="bar bar-mid"></div><div class="bar bar-low"></div><div class="bar bar-high bg-green" style="background: #059669;"></div>
          </div>
        </div>
        <div class="kpi-body">
          <h2 class="amount">{{ financeStore.accountancy?.transactions_status?.successful || 0 }}</h2>
        </div>
        <p class="kpi-footer">Commandes avec statut "Payé"</p>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-title">
            <div class="icon-box-light bg-orange-light">
              <component :is="ShoppingCartIcon" class="icon-sm" />
            </div>
            <span class="dark-text font-bold">En Attente</span>
          </div>
          <div class="mini-bars">
            <div class="bar bar-high"></div><div class="bar bar-mid"></div><div class="bar bar-low bg-orange"></div>
          </div>
        </div>
        <div class="kpi-body">
          <h2 class="amount">{{ financeStore.accountancy?.transactions_status?.pending || 0 }}</h2>
        </div>
        <p class="kpi-footer">Paiements non finalisés</p>
      </div>

    </div>

    <div class="middle-grid">
      <div class="chart-panel">
        <div class="panel-header">
          <div>
            <h4 class="dark-text font-bold text-lg">Performance des Ventes</h4>
            <p class="gray-text text-sm">Volume mensuel des revenus générés</p>
          </div>
        </div>
        
        <div class="chart-container">
          <div class="chart-tooltip">425 580 FCFA</div>
          <div class="chart-dashed-line"></div>
          
          <svg viewBox="0 0 800 250" class="svg-chart" preserveAspectRatio="none">
            <defs>
              <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10b981" stop-opacity="0.3" />
                <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
              </linearGradient>
            </defs>
            <line x1="0" y1="50" x2="800" y2="50" class="grid-line" />
            <line x1="0" y1="100" x2="800" y2="100" class="grid-line" />
            <line x1="0" y1="150" x2="800" y2="150" class="grid-line" />
            <line x1="0" y1="200" x2="800" y2="200" class="grid-line" />
            <path d="M0,200 C100,180 150,80 250,120 C350,160 400,40 500,40 C600,40 650,160 700,140 C750,120 800,50 800,50 L800,250 L0,250 Z" fill="url(#chartGradient)"/>
            <path d="M0,200 C100,180 150,80 250,120 C350,160 400,40 500,40 C600,40 650,160 700,140 C750,120 800,50 800,50" fill="none" stroke="#10b981" stroke-width="4" stroke-linecap="round"/>
            <circle cx="500" cy="40" r="6" fill="#ffffff" stroke="#10b981" stroke-width="3" />
          </svg>
          
          <div class="chart-labels">
            <span>Jan</span><span>Fév</span><span>Mar</span><span>Avr</span><span>Mai</span><span>Juin</span><span>Juil</span><span>Aoû</span><span>Sep</span>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-section panel-card">
      <div class="panel-header">
        <h4 class="dark-text font-bold text-lg">Transactions Récentes</h4>
      </div>
      
      <div class="table-responsive">
        <p v-if="financeStore.isLoading" class="gray-text text-center py-4">Chargement des transactions...</p>
        
        <table v-else class="minimal-table">
          <thead>
            <tr>
              <th>Réf</th>
              <th>Produit</th>
              <th>Client</th>
              <th>Date</th>
              <th>Prix</th>
              <th class="text-right">Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in financeStore.transactions" :key="tx.id">
              
              <td class="gray-text font-bold">#{{ tx.id.substring(0, 8).toUpperCase() }}</td>
              
              <td class="dark-text font-bold">{{ getProductName(tx) }}</td>
              
              <td class="dark-text">{{ getClientName(tx) }}</td>
              
              <td class="gray-text">{{ formatDate(tx.created_at) }}</td>
              
              <td class="dark-text font-bold">{{ formatCurrency(tx.amount) }} F</td>
              
              <td class="text-right">
                <span class="status-pill" :class="getStatusClass(tx.status)">
                  {{ tx.status_labels || tx.status }}
                </span>
              </td>
            </tr>
            
            <tr v-if="financeStore.transactions.length === 0">
              <td colspan="6" class="text-center gray-text py-4">Aucune transaction trouvée.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { markRaw, onMounted } from 'vue';
import { 
  BanknotesIcon, 
  ChartPieIcon, 
  ShoppingCartIcon,
  DocumentChartBarIcon,
  CalculatorIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline';

// ⚡️ Import de ton store tel que créé précédemment
import { useAdminTransactStore } from '../../../stores/adminTransactStore'; 

export default {
  name: 'AdminFinance',
  setup() {
    
    // Initialisation du store
    const financeStore = useAdminTransactStore();

    onMounted(async () => {
      // ⚡️ On lance les DEUX requêtes API (La liste + La compta)
      await financeStore.fetchTransact();
      await financeStore.fetchAccountancy();
    });

    // ⚡️ FORMATER LES PRIX
    const formatCurrency = (amount: number | string | undefined) => {
      const num = Number(amount) || 0;
      return num.toLocaleString('fr-FR');
    };

    // ⚡️ FORMATER LA DATE (Ex: 24 Août 2026)
    const formatDate = (dateString: string) => {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
    };

    // ⚡️ EXTRAIRE LE NOM DU PRODUIT (Depuis tx.order.order_items)
    const getProductName = (tx: any) => {
      // Vérifier si la commande et ses items existent
      const items = tx.order?.order_items;
      if (!items || items.length === 0) return 'Article inconnu';
      
      // On cherche le nom du contrat ou du pack (ajuste les noms de champs selon ton backend)
      const firstItem = items[0];
      const itemName = firstItem.contrat?.title || firstItem.pack?.nom || 'Produit';

      if (items.length === 1) return itemName;
      return `${itemName} (+${items.length - 1})`;
    };

    // ⚡️ EXTRAIRE LE NOM DU CLIENT (Guest ou User)
    const getClientName = (tx: any) => {
      const order = tx.order;
      if (!order) return 'Client Inconnu';
      
      // Si c'est un invité (guest checkout)
      if (order.guest && order.guest.full_name) {
        return order.guest.full_name;
      }
      
      // Si c'est un utilisateur enregistré
      if (order.user) {
        return `${order.user.first_name || ''} ${order.user.last_name || ''}`.trim() || order.user.email;
      }
      
      return 'Client Inconnu';
    };

    // ⚡️ ATTRIBUER LA COULEUR SELON LE STATUT
    const getStatusClass = (status: string) => {
      // Les statuts viennent de ton TransactionStatus (PENDING, SUCCESSFUL, FAILED, CANCELED)
      const s = status ? status.toUpperCase() : '';
      if (s === 'SUCCESSFUL') return 'pill-green';
      if (s === 'PENDING') return 'pill-yellow';
      if (s === 'FAILED' || s === 'CANCELED') return 'pill-gray';
      return 'pill-gray';
    };

    return {
      financeStore,
      formatCurrency,
      formatDate,
      getProductName,
      getClientName,
      getStatusClass,
      
      // Icônes
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
/* Conserve 100% du CSS de ton code précédent ! */
/* J'ai seulement ajouté de quoi centrer le texte "Aucune transaction" et les loaders dans le template */
.py-4 { padding-top: 1.5rem; padding-bottom: 1.5rem; }

/* ... Ton CSS d'origine ... */
.finance-wrapper {
  --bg-main: #f8fafc;
  --bg-panel: #ffffff;
  --text-dark: #1e293b;
  --text-gray: #94a3b8;
  --accent-green: #10b981; 
  
  display: flex; flex-direction: column; gap: 2rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); }
.font-bold { font-weight: 700; }
.text-lg { font-size: 1.1rem; }
.text-sm { font-size: 0.8rem; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.flex-align { display: flex; align-items: center; gap: 0.8rem; }
.mb-3 { margin-bottom: 1rem; }
.icon-sm { width: 20px; height: 20px; }
.icon-gray { color: var(--text-gray); }
.panel-card { background: var(--bg-panel); border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; }
.panel-header { margin-bottom: 1.5rem; }
.header-section { margin-bottom: 0.5rem; }
.title-and-tabs { display: flex; justify-content: space-between; align-items: center; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 700; margin: 0; }
.header-links { display: flex; gap: 2rem; font-weight: 600; font-size: 0.95rem; color: var(--text-gray); }
.header-links span { cursor: pointer; transition: 0.2s; }
.header-links span:hover { color: var(--text-dark); }
.active-link { color: var(--text-dark); border-bottom: 2px solid var(--text-dark); padding-bottom: 4px; }
@media (max-width: 768px) { .hidden-mobile { display: none; } }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
.kpi-card { background: var(--bg-panel); border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; display: flex; flex-direction: column; justify-content: space-between; }
.kpi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.kpi-title { display: flex; align-items: center; gap: 0.8rem; }
.icon-box-light { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.bg-blue-light { background: #eff6ff; color: #3b82f6; }
.bg-orange-light { background: #fff7ed; color: #f97316; }
.bg-purple-light { background: #faf5ff; color: #a855f7; }
.mini-bars { display: flex; gap: 4px; align-items: flex-end; height: 24px; }
.bar { width: 6px; border-radius: 4px; background: #e2e8f0; }
.bar-low { height: 40%; }
.bar-mid { height: 70%; }
.bar-high { height: 100%; }
.bg-blue { background: #3b82f6; }
.bg-orange { background: #f97316; }
.bg-purple { background: #a855f7; }
.kpi-body { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.amount { margin: 0; font-size: 1.8rem; font-weight: 800; color: var(--text-dark); letter-spacing: -0.5px; }
.currency { font-size: 1rem; color: var(--text-gray); font-weight: 600; }
.badge { padding: 0.3rem 0.6rem; border-radius: 50px; font-size: 0.75rem; font-weight: 700; }
.badge-green { background: #d1fae5; color: #059669; }
.badge-red { background: #fee2e2; color: #dc2626; }
.kpi-footer { margin: 0; font-size: 0.75rem; color: var(--text-gray); }
.middle-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 1024px) { .middle-grid { grid-template-columns: 2fr 1fr; } }
.chart-panel { background: var(--bg-panel); border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; }
.chart-container { position: relative; width: 100%; height: 300px; margin-top: 2rem; display: flex; flex-direction: column; justify-content: flex-end; }
.svg-chart { width: 100%; height: 250px; overflow: visible; }
.grid-line { stroke: #f1f5f9; stroke-width: 1; stroke-dasharray: 4; }
.chart-tooltip { position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #1e293b; color: white; padding: 0.4rem 0.8rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; z-index: 10; }
.chart-tooltip::after { content: ''; position: absolute; bottom: -4px; left: 50%; transform: translateX(-50%); border-width: 5px 5px 0; border-style: solid; border-color: #1e293b transparent transparent transparent; }
.chart-dashed-line { position: absolute; top: 25px; bottom: 30px; left: 50%; width: 1px; border-left: 2px dashed #10b981; z-index: 5; opacity: 0.3; }
.chart-labels { display: flex; justify-content: space-between; width: 100%; margin-top: 10px; color: var(--text-gray); font-size: 0.75rem; font-weight: 500; }
.side-panel { display: flex; flex-direction: column; gap: 1.5rem; }
.insight-btn { display: flex; justify-content: space-between; align-items: center; background: #f8fafc; padding: 1rem; border-radius: 16px; border: 1px solid #f1f5f9; margin-bottom: 0.8rem; cursor: pointer; transition: 0.2s; }
.insight-btn:hover { background: #f1f5f9; }
.promo-box { display: flex; flex-direction: column; align-items: center; background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%); }
.promo-illustration { font-size: 3rem; margin-bottom: 1rem; }
.btn-upgrade { background: var(--accent-green); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 50px; font-weight: 700; width: 100%; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3); }
.btn-upgrade:hover { background: #059669; transform: translateY(-2px); }
.table-responsive { overflow-x: auto; }
.minimal-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 700px; }
.minimal-table th { color: #cbd5e1; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; padding-bottom: 1.5rem; }
.minimal-table td { padding: 1.2rem 0; border-bottom: 1px solid #f8fafc; vertical-align: middle; }
.minimal-table tr:last-child td { border-bottom: none; }
.status-pill { padding: 0.4rem 1rem; border-radius: 50px; font-size: 0.75rem; font-weight: 700; display: inline-block; }
.pill-green { background: #d1fae5; color: #059669; }
.pill-yellow { background: #fef3c7; color: #d97706; }
.pill-gray { background: #f1f5f9; color: #64748b; }
</style>