<template>
  <div class="admin-coupons-wrapper">
    <!-- En-tête de la section -->
    <div class="header-section">
      <div class="title-col">
        <h3 class="section-title">Codes Promo & Réductions</h3>
        <p class="gray-text">Gérez vos campagnes promotionnelles et suivez leur utilisation.</p>
      </div>
      <div class="action-col">
        <button class="btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="icon-sm">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          Nouveau Code Promo
        </button>
      </div>
    </div>

    <!-- Tableau des coupons -->
    <div class="table-container">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Code Promo</th>
            <th>Réduction</th>
            <th>Validité</th>
            <th>Utilisations</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        
        <tbody>
          <!-- On boucle sur nos fausses données en attendant le store -->
          <tr v-for="coupon in coupons" :key="coupon.id">
            
            <!-- Code -->
            <td>
              <span class="font-bold code-badge">{{ coupon.code }}</span>
            </td>

            <!-- Valeur de la réduction -->
            <td>
              <span v-if="coupon.discount_type === 'percentage'" class="discount-val">
                {{ coupon.discount_value }} %
              </span>
              <span v-else class="discount-val">
                {{ coupon.discount_value }} FCFA
              </span>
            </td>

            <!-- Période de validité -->
            <td>
              <div class="date-cell">
                <span class="text-sm">Du : <span class="font-bold">{{ formatDate(coupon.valid_from) }}</span></span>
                <span class="text-sm">Au : <span class="font-bold">{{ formatDate(coupon.valid_to) }}</span></span>
              </div>
            </td>

            <!-- Compteur d'utilisations -->
            <td>
              <div class="usage-bar-container">
                <div class="usage-stats text-sm">
                  <span>{{ coupon.used_count }} / {{ coupon.max_usages }}</span>
                </div>
                <div class="progress-bg">
                  <div class="progress-fill" :style="{ width: getUsagePercentage(coupon.used_count, coupon.max_usages) + '%' }"></div>
                </div>
              </div>
            </td>

            <!-- Statut (Actif/Inactif) -->
            <td>
              <span :class="['status-badge', coupon.active ? 'active' : 'inactive']">
                {{ coupon.active ? 'Actif' : 'Désactivé' }}
              </span>
            </td>

            <!-- Actions (Modifier / Supprimer) -->
            <td>
              <div class="actions-row">
                <button class="btn-icon edit" title="Modifier">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
                  </svg>
                </button>
                <button class="btn-icon delete" title="Supprimer">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                  </svg>
                </button>
              </div>
            </td>

          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, computed } from 'vue';
import { useAdminCouponStore } from '../../../stores/AdminCouponStore'; // Ajuste le chemin

export default defineComponent({
  name: 'AdminCouponSection',
  setup() {
    const couponStore = useAdminCouponStore();

    // On charge les données dès que le composant est monté
    onMounted(async () => {
      await couponStore.fetchCoupons();
    });

    // On rend les données du store réactives pour le template
    const coupons = computed(() => couponStore.coupons);
    const isLoading = computed(() => couponStore.isLoading);
    const error = computed(() => couponStore.error);

    // Utilitaires d'affichage
    const formatDate = (dateString: string) => {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
    };

    const getUsagePercentage = (used: number, max: number) => {
      if (max === 0) return 0;
      const percentage = (used / max) * 100;
      return percentage > 100 ? 100 : percentage;
    };

    return {
      coupons, 
      isLoading,
      error,
      formatDate,
      getUsagePercentage
    };
  }
});
</script>

<style scoped>
.admin-coupons-wrapper {
  display: flex; flex-direction: column; gap: 1.5rem;
  font-family: 'Inter', sans-serif;
}

.header-section { display: flex; justify-content: space-between; align-items: flex-end; }
.title-col { display: flex; flex-direction: column; gap: 0.3rem; }
.section-title { font-size: 1.4rem; color: #1e293b; font-weight: 700; margin: 0; }
.gray-text { color: #64748b; font-size: 0.95rem; margin: 0; }

.btn-primary {
  display: flex; align-items: center; gap: 0.5rem;
  background-color: #0f172a; color: white;
  border: none; padding: 0.6rem 1.2rem;
  border-radius: 8px; font-weight: 600; cursor: pointer;
  transition: 0.2s;
}
.btn-primary:hover { background-color: #334155; }

.table-container { background: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; border: 1px solid #e2e8f0; }
.admin-table { width: 100%; border-collapse: collapse; text-align: left; }
.admin-table th { background: #f8fafc; padding: 1rem 1.2rem; font-size: 0.85rem; font-weight: 600; color: #475569; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; }
.admin-table td { padding: 1rem 1.2rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }

.code-badge { background: #f1f5f9; padding: 0.4rem 0.8rem; border-radius: 6px; color: #0f172a; font-family: monospace; font-size: 1rem; letter-spacing: 1px; }
.discount-val { font-weight: 700; color: #059669; }
.text-sm { font-size: 0.85rem; }
.font-bold { font-weight: 700; }
.date-cell { display: flex; flex-direction: column; gap: 0.2rem; color: #475569; }

.usage-bar-container { width: 120px; display: flex; flex-direction: column; gap: 0.3rem; }
.usage-stats { display: flex; justify-content: space-between; font-weight: 600; color: #334155; }
.progress-bg { height: 6px; background: #e2e8f0; border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; background: #3b82f6; border-radius: 10px; transition: width 0.3s; }

.status-badge { padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.status-badge.active { background: #dcfce7; color: #166534; }
.status-badge.inactive { background: #fee2e2; color: #991b1b; }

.actions-row { display: flex; gap: 0.5rem; }
.btn-icon { background: none; border: none; cursor: pointer; padding: 0.4rem; border-radius: 6px; transition: 0.2s; color: #64748b; }
.btn-icon:hover { background: #f1f5f9; }
.btn-icon.edit:hover { color: #2563eb; }
.btn-icon.delete:hover { color: #dc2626; }
.icon-sm { width: 18px; height: 18px; }
</style>