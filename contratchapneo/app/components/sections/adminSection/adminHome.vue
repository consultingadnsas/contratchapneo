<template>
  <div class="dashboard-wrapper">
    
    <div class="top-section">
      <div class="overview-section">
        <h3 class="section-title">Aperçu financier</h3>
        <div class="overview-grid">
          
          <!-- ⚡️ CARTE 1 : REVENUS GLOBAUX -->
          <div class="gradient-card">
            <div class="card-header">
              <div class="icon-white"><svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg></div>
            </div>
            <div class="card-body">
              <h2>Revenus Globaux</h2>
              <p>Chiffre d'affaires total</p>
            </div>
            <div class="card-footer">
              <div class="stat-block">
                <span>Total</span>
                <!-- ⚡️ Affichage dynamique du chiffre d'affaires -->
                <strong>{{ formatCurrency(transactStore.accountancy?.global?.total_revenue) }} FCFA</strong>
              </div>
            </div>
          </div>

          <!-- ⚡️ CARTE 2 : CONTRATS VENDUS -->
          <div class="white-card">
            <div class="card-header">
              <div class="icon-purple">
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </div>
            <div class="card-body">
              <!-- ⚡️ Nouveaux textes plus inclusifs -->
              <h2 class="dark-text">Ventes Globales</h2>
              <p class="gray-text">Tous services et produits confondus</p>
            </div>
            <div class="card-footer">
              <div class="stat-block-dark">
                <span>Total Cumulé</span>
                <!-- ⚡️ Le compteur affiche maintenant TOUT -->
                <strong>{{ totalContractsSold }}</strong>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- ⚡️ DERNIÈRES ACTIVITÉS (Inchangé) -->
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
import { computed, onMounted, markRaw } from 'vue';
import folderCards from '../../cards/folderCards.vue';
import { 
  ArrowDownTrayIcon, 
  ArrowUpTrayIcon, 
  CreditCardIcon 
} from '@heroicons/vue/24/outline';
import { useAdminTransactStore } from '../../../stores/adminTransactStore';

export default {
  name: 'AdminOverview',
  components: {
    folderCards
  },
  emits: ['open-catalogue'],
  setup() {
    const transactStore = useAdminTransactStore();

    // 1. Déclenchement des appels API au montage
    onMounted(async () => {
     await transactStore.fetchTransact(1, 'all');
     await transactStore.fetchAccountancy();
    });

    // 2. Helper : Formatage monétaire (ex: 2300000 -> 2 300 000)
    const formatCurrency = (amount: number | string | undefined) => {
      const num = Number(amount) || 0;
      return new Intl.NumberFormat('fr-FR').format(num);
    };

    // 3. Helper : Formatage des dates
    const formatDate = (dateString: string) => {
      if (!dateString) return 'Date inconnue';
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
    };

    // 4. Helper : Couleurs de statuts
    const getStatusStyles = (status: string) => {
      const safeStatus = status?.toLowerCase() || '';
      if (['success', 'payé', 'paid', 'successful'].includes(safeStatus)) {
        return { color: 'dot-green', text: 'Succès' };
      } else if (['pending', 'en attente'].includes(safeStatus)) {
        return { color: 'dot-yellow', text: 'En attente' };
      } else if (['failed', 'échoué', 'error', 'canceled'].includes(safeStatus)) {
        return { color: 'dot-red', text: 'Échoué' };
      }
      return { color: 'dot-gray', text: status || 'Inconnu' };
    };

    // 5. CALCUL DYNAMIQUE : Toutes les ventes réussies de la plateforme
    const totalContractsSold = computed(() => {
      // Au lieu de compter les éléments de la page 1, 
      // on utilise la statistique globale renvoyée par le backend (AccountingSummary)
      return transactStore.accountancy?.transactions_status?.successful || 0;
    });

    // 6. Tableau des dernières activités
    const recentActivities = computed(() => {
      const sortedTransactions = [...transactStore.transactions].sort((a, b) => {
        const dateA = new Date(a.created_at || a.order?.created_at).getTime();
        const dateB = new Date(b.created_at || b.order?.created_at).getTime();
        return dateB - dateA;
      });

      return sortedTransactions.slice(0, 7).map((tx) => {
        const styles = getStatusStyles(tx.status);
        const order = tx.order || {};
        const orderItems = order.order_items || order.items || tx.order_items || [];
        
        let actionType = 'Achat de contrat';
        
        // ⚡️ DÉTECTION ROBUSTE UNIQUEMENT
        const hasPack = order.pack || tx.pack || order.order_type === 'pack' || orderItems.some((i: any) => i.pack || i.pack_title || i.pack_id);
        const hasCustom = order.custom_contract || tx.custom_contract || order.order_type === 'custom' || orderItems.some((i: any) => i.customised_contract || i.contrat_customed || i.contract_revision ||i.contract_revision_id);
        const hasRevision = orderItems.some((i: any) => i.contract_revision || i.contract_revision_id);
        const hasPro = orderItems.some((i: any) => i.pro || i.pro_name || i.pro_id);

        if (hasPack) {
          actionType = 'Achat de pack';
        } else if (hasRevision) {
          actionType = 'Révision de contrat';
        } else if (hasCustom) {
          actionType = 'Demande sur-mesure';
        }  else if (hasPro) {
          actionType = 'Sollicitation Expert';
        }
        
        const clientEmail = order.buyer_email || order.guest?.email || order.user?.email || 'Email non renseigné';

        return {
          id: tx.id || Math.random().toString(),
          action: actionType, 
          status: styles.text,
          statusColor: styles.color,
          client: clientEmail,
          date: formatDate(tx.created_at || order.created_at),
          amount: new Intl.NumberFormat('fr-FR').format(tx.amount || order.total_amount || 0), 
          icon: markRaw(CreditCardIcon), 
          colorClass: 'bg-gray-light' 
        };
      });
    });

    return { 
      transactStore,         // Exporté pour accéder aux données dans le template
      formatCurrency,        // Exporté pour formater le prix
      totalContractsSold,    // Exporté pour le compteur
      recentActivities,
      isLoading: computed(() => transactStore.isLoading)
    };
  }
}
</script>

<style scoped>
/* Ton CSS original reste inchangé */
.dashboard-wrapper {
  --bg-main: #f8fafc;        
  --bg-panel: #ffffff;       
  --text-dark: #1e293b;      
  --text-gray: #94a3b8;      
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2.5rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}
.section-title { font-size: 1.1rem; color: var(--text-dark); font-weight: 700; margin: 0 0 1rem 0; }
.section-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1rem; }
.top-section { display: grid; grid-template-columns: 1fr; gap: 2rem; }
@media (min-width: 1024px) { .top-section { grid-template-columns: 1.5fr 1fr; } }
.overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; }
.gradient-card {
  background: var(--primary-color);
  border-radius: 24px; padding: 1.5rem; color: white;
  display: flex; flex-direction: column; justify-content: space-between;
  min-height: 180px;
}
.icon-white { background: var(--secondary-light-color); color:#ffffff; padding: 0.5rem; border-radius: 12px; display: inline-flex; }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
.card-body h2 { margin: 0; font-size: 1.1rem; font-weight: 700; }
.card-body p { margin: 0.2rem 0 0 0; font-size: 0.8rem; opacity: 0.9; }
.card-footer { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 1.5rem; }
.stat-block { display: flex; flex-direction: column; }
.stat-block span { font-size: 0.7rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px; }
.stat-block strong { font-size: 1.2rem; }
.white-card {
  background: rgba(255,255,255,0.2); border-radius: 24px; padding: 1.5rem;
  display: flex; flex-direction: column; justify-content: space-between;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; min-height: 180px;
}
.icon-purple { background:var(--secondary-light-color); color: #ffffff; padding: 0.5rem; border-radius: 12px; display: inline-flex; }
.dark-text { color: black; }
.gray-text { color: var(--text-gray); font-size: 0.85rem; }
.stat-block-dark { display: flex; flex-direction: column; }
.stat-block-dark span { font-size: 0.7rem; color: var(--text-gray); text-transform: uppercase; letter-spacing: 1px; }
.stat-block-dark strong { font-size: 1.2rem; color: black; }
.folders-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
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
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.status-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 0.4rem; vertical-align: middle; }
.dot-green { background-color: #10b981; }
.dot-yellow { background-color: #f59e0b; }
.dot-red { background-color: #ef4444; }
.dot-gray { background-color: #94a3b8; }
@media (min-width: 1200px){ .gradient-card { min-height: 300px; } }
</style>