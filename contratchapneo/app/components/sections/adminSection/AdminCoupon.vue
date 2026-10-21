<template>
  <div class="admin-coupons-wrapper">
    <!-- Header Section -->
    <div class="header-section">
      <div class="title-col">
        <h3 class="section-title">Codes Promo & Réductions</h3>
        <p class="gray-text">Gérez vos campagnes promotionnelles et suivez leur utilisation.</p>
      </div>
      <div class="action-col">
        <button type="button" class="btn-primary" @click="openAddModal">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="icon-sm">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          <span>Nouveau Code Promo</span>
        </button>
      </div>
    </div>

    <!-- Alert Error -->
    <div v-if="error" class="alert-error">
      {{ error }}
    </div>

    <!-- Vue Tableau (Desktop & Tablette) -->
    <div class="table-container desktop-table-view">
      <div class="table-scroll-container">
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
          
          <tbody v-if="isLoading && coupons.length === 0">
            <tr>
              <td colspan="6" class="text-center py-6">
                <div class="state-indicator">
                  <div class="spinner-sm"></div>
                  <span>Chargement des coupons...</span>
                </div>
              </td>
            </tr>
          </tbody>
          <tbody v-else-if="coupons.length === 0">
            <tr>
              <td colspan="6" class="text-center py-6 gray-text">
                Aucun code promo trouvé.
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr v-for="coupon in coupons" :key="coupon.id">
              <td>
                <div class="code-cell">
                  <span class="font-bold code-badge">{{ coupon.code }}</span>
                  <button 
                    type="button" 
                    class="btn-copy-sm" 
                    @click="copyCode(coupon.code)" 
                    :title="copiedCode === coupon.code ? 'Copié !' : 'Copier le code'"
                  >
                    <svg v-if="copiedCode === coupon.code" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="icon-xs text-green">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-xs">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                    </svg>
                  </button>
                  <span v-if="copiedCode === coupon.code" class="copy-tooltip">Copié !</span>
                </div>
              </td>
              <td>
                <span v-if="coupon.discount_type === 'percentage'" class="discount-val">{{ coupon.discount_value }} %</span>
                <span v-else class="discount-val">{{ formatCurrency(coupon.discount_value) }}</span>
              </td>
              <td>
                <div class="date-cell">
                  <span class="text-sm"><span class="text-muted">Du :</span> <span class="font-semibold">{{ formatDate(coupon.valid_from) }}</span></span>
                  <span class="text-sm"><span class="text-muted">Au :</span> <span class="font-semibold">{{ formatDate(coupon.valid_to) }}</span></span>
                </div>
              </td>
              <td>
                <div class="usage-bar-container">
                  <div class="usage-stats text-sm">
                    <span>{{ coupon.used_count || 0 }} / {{ coupon.max_usages }}</span>
                    <span class="text-muted text-xs">({{ Math.round(getUsagePercentage(coupon.used_count || 0, coupon.max_usages)) }}%)</span>
                  </div>
                  <div class="progress-bg">
                    <div class="progress-fill" :style="{ width: getUsagePercentage(coupon.used_count || 0, coupon.max_usages) + '%' }"></div>
                  </div>
                </div>
              </td>
              <td>
                <span :class="['status-badge', coupon.active ? 'active' : 'inactive']">
                  <span class="status-dot"></span>
                  {{ coupon.active ? 'Actif' : 'Désactivé' }}
                </span>
              </td>
              <td>
                <div class="actions-row">
                  <button type="button" class="btn-icon edit" title="Modifier" @click="openEditModal(coupon)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" /></svg>
                  </button>
                  <button type="button" class="btn-icon delete" title="Supprimer" @click="openDeleteModal(coupon.id!)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Vue Cartes (Smartphones <= 768px) -->
    <div class="mobile-cards-view">
      <div v-if="isLoading && coupons.length === 0" class="empty-state-card">
        <div class="spinner-sm"></div>
        <p class="gray-text">Chargement des coupons...</p>
      </div>

      <div v-else-if="coupons.length === 0" class="empty-state-card">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="empty-icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 11.25v8.25a1.5 1.5 0 0 1-1.5 1.5H4.5a1.5 1.5 0 0 1-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1 0 9.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1 1 14.625 7.5H12m0 0V21m-8.625-9.75h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
        </svg>
        <p class="font-bold text-slate-800">Aucun code promo trouvé</p>
        <p class="gray-text text-sm">Créez votre première offre promotionnelle.</p>
        <button type="button" class="btn-primary mt-2" @click="openAddModal">
          Nouveau Code Promo
        </button>
      </div>

      <div v-else class="cards-list">
        <div v-for="coupon in coupons" :key="coupon.id" class="coupon-card">
          <!-- Entête Carte : Code badge + Statut -->
          <div class="card-header">
            <div class="code-wrapper">
              <span class="code-badge">{{ coupon.code }}</span>
              <button 
                type="button" 
                class="btn-copy-sm" 
                @click="copyCode(coupon.code)" 
                :title="copiedCode === coupon.code ? 'Copié !' : 'Copier le code'"
              >
                <svg v-if="copiedCode === coupon.code" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="icon-xs text-green">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-xs">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                </svg>
              </button>
              <span v-if="copiedCode === coupon.code" class="copy-feedback">Copié !</span>
            </div>

            <span :class="['status-badge', coupon.active ? 'active' : 'inactive']">
              <span class="status-dot"></span>
              {{ coupon.active ? 'Actif' : 'Désactivé' }}
            </span>
          </div>

          <!-- Corps Carte -->
          <div class="card-body">
            <!-- Réduction -->
            <div class="card-row">
              <span class="card-label">Réduction</span>
              <span class="discount-val highlight">
                {{ coupon.discount_type === 'percentage' ? `${coupon.discount_value} %` : formatCurrency(coupon.discount_value) }}
              </span>
            </div>

            <!-- Validité -->
            <div class="card-row">
              <span class="card-label">Validité</span>
              <div class="validity-dates">
                <div class="validity-item">
                  <span class="date-prefix">Du</span>
                  <span class="date-val">{{ formatDate(coupon.valid_from) }}</span>
                </div>
                <div class="validity-item">
                  <span class="date-prefix">Au</span>
                  <span class="date-val">{{ formatDate(coupon.valid_to) }}</span>
                </div>
              </div>
            </div>

            <!-- Utilisations & Barre -->
            <div class="card-row usage-block">
              <div class="usage-title-row">
                <span class="card-label">Utilisations</span>
                <span class="usage-count">
                  {{ coupon.used_count || 0 }} / {{ coupon.max_usages }}
                  <span class="text-muted text-xs">({{ Math.round(getUsagePercentage(coupon.used_count || 0, coupon.max_usages)) }}%)</span>
                </span>
              </div>
              <div class="progress-bg">
                <div class="progress-fill" :style="{ width: getUsagePercentage(coupon.used_count || 0, coupon.max_usages) + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- Actions Carte -->
          <div class="card-actions">
            <button type="button" class="btn-card-action edit" @click="openEditModal(coupon)">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm">
                <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
              </svg>
              <span>Modifier</span>
            </button>
            <button type="button" class="btn-card-action delete" @click="openDeleteModal(coupon.id!)">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon-sm">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
              <span>Supprimer</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modale d'ajout / modification -->
    <AdminCouponFormModal 
      v-if="showFormModal"
      :mode="modalMode"
      :initialData="formData"
      :isSubmitting="isSubmitting"
      @close="closeModals"
      @submit="handleFormSubmit"
    />

    <!-- Modale de confirmation de suppression -->
    <AdminCouponDeleteModal
      v-if="showDeleteModal"
      :isSubmitting="isSubmitting"
      @close="closeModals"
      @confirm="handleConfirmDelete"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, computed, ref } from 'vue';
import { useAdminCouponStore, type Coupon } from '../../../stores/AdminCouponStore'; 
import AdminCouponFormModal from '../../modale/adminCouponModale.vue';
import AdminCouponDeleteModal from '../../modale/deleteModale.vue';

export default defineComponent({
  name: 'AdminCouponSection',
  components: {
    AdminCouponFormModal,
    AdminCouponDeleteModal
  },
  setup() {
    const couponStore = useAdminCouponStore();

    const coupons = computed(() => couponStore.coupons);
    const isLoading = computed(() => couponStore.isLoading);
    const error = computed(() => couponStore.error);
    const isSubmitting = ref(false);

    const showFormModal = ref(false);
    const showDeleteModal = ref(false);
    const modalMode = ref<'add' | 'edit'>('add');
    const selectedCouponId = ref<number | null>(null);

    const copiedCode = ref<string | null>(null);

    const formData = ref<Coupon>({
      code: '',
      discount_type: 'percentage',
      discount_value: 0,
      valid_from: '',
      valid_to: '',
      max_usages: 100,
      active: true,
      used_count: 0
    });

    onMounted(async () => {
      await couponStore.fetchCoupons();
    });

    const formatForDatetimeLocal = (isoString: string) => {
      if (!isoString) return '';
      const date = new Date(isoString);
      return new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().slice(0, 16);
    };

    const copyCode = async (code: string) => {
      try {
        if (navigator && navigator.clipboard) {
          await navigator.clipboard.writeText(code);
        } else {
          // Fallback pour navigateurs plus anciens / contextes non-sécurisés
          const textArea = document.createElement('textarea');
          textArea.value = code;
          textArea.style.position = 'fixed';
          textArea.style.left = '-9999px';
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);
        }
        copiedCode.value = code;
        setTimeout(() => {
          if (copiedCode.value === code) {
            copiedCode.value = null;
          }
        }, 2000);
      } catch (err) {
        console.error("Erreur lors de la copie du code promo :", err);
      }
    };

    const openAddModal = () => {
      modalMode.value = 'add';
      formData.value = { 
        code: '', 
        discount_type: 'percentage', 
        discount_value: 0, 
        valid_from: '', 
        valid_to: '', 
        max_usages: 100, 
        active: true, 
        used_count: 0 
      };
      showFormModal.value = true;
    };

    const openEditModal = (coupon: Coupon) => {
      modalMode.value = 'edit';
      selectedCouponId.value = coupon.id as number;
      formData.value = { 
        ...coupon, 
        valid_from: formatForDatetimeLocal(coupon.valid_from), 
        valid_to: formatForDatetimeLocal(coupon.valid_to) 
      };
      showFormModal.value = true;
    };

    const openDeleteModal = (id: number) => {
      selectedCouponId.value = id;
      showDeleteModal.value = true;
    };

    const closeModals = () => {
      showFormModal.value = false;
      showDeleteModal.value = false;
      selectedCouponId.value = null;
    };

    const handleFormSubmit = async (submittedData: Coupon) => {
      isSubmitting.value = true;
      try {
        if (modalMode.value === 'add') {
          await couponStore.createCoupon(submittedData);
        } else if (modalMode.value === 'edit' && selectedCouponId.value) {
          await couponStore.updateCoupon(selectedCouponId.value, submittedData);
        }
        closeModals();
      } catch (err) {
        console.error("Erreur de soumission :", err);
      } finally {
        isSubmitting.value = false;
      }
    };

    const handleConfirmDelete = async () => {
      if (!selectedCouponId.value) return;
      isSubmitting.value = true;
      try {
        await couponStore.deleteCoupon(selectedCouponId.value);
        closeModals();
      } catch (err) {
        console.error("Erreur de suppression :", err);
      } finally {
        isSubmitting.value = false;
      }
    };

    const formatDate = (dateString: string) => {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    };

    const formatCurrency = (amount: number | string | null | undefined) => {
      if (amount === null || amount === undefined || amount === '') return '0 FCFA';
      const num = Number(amount);
      if (isNaN(num)) return '0 FCFA';
      return new Intl.NumberFormat('fr-FR').format(Math.round(num)) + ' FCFA';
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
      isSubmitting,
      showFormModal,
      showDeleteModal,
      modalMode,
      formData,
      copiedCode,
      copyCode,
      openAddModal,
      openEditModal,
      openDeleteModal,
      closeModals,
      handleFormSubmit,
      handleConfirmDelete,
      formatDate,
      formatCurrency,
      getUsagePercentage
    };
  }
});
</script>

<style scoped>
/* ========================================================
   CONTENEUR PRINCIPAL & EN-TÊTE
   ======================================================== */
.admin-coupons-wrapper { 
  display: flex; 
  flex-direction: column; 
  gap: 1.5rem; 
  font-family: 'Inter', sans-serif; 
  position: relative; 
  width: 100%;
  box-sizing: border-box;
}

.header-section { 
  display: flex; 
  justify-content: space-between; 
  align-items: flex-end;
  gap: 1rem;
}

.title-col { 
  display: flex; 
  flex-direction: column; 
  gap: 0.3rem; 
}

.section-title { 
  font-size: 1.4rem; 
  color: #1e293b; 
  font-weight: 700; 
  margin: 0; 
  letter-spacing: -0.3px;
}

.gray-text { 
  color: #64748b; 
  font-size: 0.95rem; 
  margin: 0; 
}

.btn-primary { 
  display: inline-flex; 
  align-items: center; 
  justify-content: center;
  gap: 0.5rem; 
  background-color: #0f172a; 
  color: white; 
  border: none; 
  padding: 0.65rem 1.25rem; 
  border-radius: 10px; 
  font-weight: 600; 
  font-size: 0.95rem;
  cursor: pointer; 
  transition: all 0.2s ease; 
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(15, 23, 42, 0.1);
}

.btn-primary:hover:not(:disabled) { 
  background-color: #334155; 
  transform: translateY(-1px);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.icon-sm { 
  width: 18px; 
  height: 18px; 
  flex-shrink: 0;
}

.icon-xs { 
  width: 15px; 
  height: 15px; 
  flex-shrink: 0;
}

.text-green { 
  color: #16a34a; 
}

.mt-2 { 
  margin-top: 0.5rem; 
}

.alert-error { 
  background: #fee2e2; 
  color: #991b1b; 
  padding: 1rem 1.25rem; 
  border-radius: 10px; 
  font-weight: 500; 
  font-size: 0.9rem; 
  border: 1px solid #f87171; 
  word-break: break-word;
}

/* ========================================================
   VUE TABLEAU (DESKTOP & TABLETTE >= 769px)
   ======================================================== */
.table-container { 
  background: #ffffff; 
  border-radius: 14px; 
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); 
  border: 1px solid #e2e8f0; 
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.table-scroll-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  width: 100%;
}

.table-scroll-container::-webkit-scrollbar {
  height: 6px;
}
.table-scroll-container::-webkit-scrollbar-track {
  background: #f8fafc;
}
.table-scroll-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.table-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.admin-table { 
  width: 100%; 
  border-collapse: collapse; 
  text-align: left; 
  min-width: 720px;
}

.admin-table th { 
  background: #f8fafc; 
  padding: 1rem 1.2rem; 
  font-size: 0.85rem; 
  font-weight: 600; 
  color: #475569; 
  text-transform: uppercase; 
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e2e8f0; 
  white-space: nowrap;
}

.admin-table td { 
  padding: 1rem 1.2rem; 
  border-bottom: 1px solid #f1f5f9; 
  vertical-align: middle; 
}

.admin-table tbody tr {
  transition: background-color 0.15s ease;
}

.admin-table tbody tr:hover {
  background-color: #f8fafc;
}

/* Éléments de cellules */
.code-cell {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  position: relative;
}

.code-badge { 
  background: #f1f5f9; 
  padding: 0.4rem 0.75rem; 
  border-radius: 6px; 
  color: #0f172a; 
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; 
  font-size: 0.95rem; 
  letter-spacing: 0.8px; 
  border: 1px solid #e2e8f0;
}

.btn-copy-sm {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 4px;
  color: #94a3b8;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-copy-sm:hover {
  background: #f1f5f9;
  color: #3b82f6;
}

.copy-tooltip {
  position: absolute;
  top: -24px;
  left: 30px;
  background: #1e293b;
  color: white;
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
  pointer-events: none;
  animation: fadeIn 0.2s ease-out;
}

.discount-val { 
  font-weight: 700; 
  color: #059669; 
  white-space: nowrap;
}

.text-sm { font-size: 0.85rem; }
.text-xs { font-size: 0.75rem; }
.text-muted { color: #64748b; }
.font-bold { font-weight: 700; }
.font-semibold { font-weight: 600; }

.date-cell { 
  display: flex; 
  flex-direction: column; 
  gap: 0.2rem; 
  color: #475569; 
  white-space: nowrap;
}

.usage-bar-container { 
  width: 140px; 
  display: flex; 
  flex-direction: column; 
  gap: 0.35rem; 
}

.usage-stats { 
  display: flex; 
  justify-content: space-between; 
  align-items: baseline;
  font-weight: 600; 
  color: #334155; 
}

.progress-bg { 
  height: 6px; 
  background: #e2e8f0; 
  border-radius: 10px; 
  overflow: hidden; 
}

.progress-fill { 
  height: 100%; 
  background: #3b82f6; 
  border-radius: 10px; 
  transition: width 0.3s ease; 
}

.status-badge { 
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.8rem; 
  border-radius: 50px; 
  font-size: 0.75rem; 
  font-weight: 700; 
  text-transform: uppercase; 
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-badge.active { 
  background: #dcfce7; 
  color: #166534; 
}
.status-badge.active .status-dot {
  background: #16a34a;
}

.status-badge.inactive { 
  background: #fee2e2; 
  color: #991b1b; 
}
.status-badge.inactive .status-dot {
  background: #dc2626;
}

.actions-row { 
  display: flex; 
  gap: 0.4rem; 
}

.btn-icon { 
  background: none; 
  border: none; 
  cursor: pointer; 
  padding: 0.5rem; 
  border-radius: 8px; 
  transition: all 0.2s; 
  color: #64748b; 
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover { 
  background: #f1f5f9; 
}
.btn-icon.edit:hover { 
  color: #2563eb; 
  background: #eff6ff;
}
.btn-icon.delete:hover { 
  color: #dc2626; 
  background: #fef2f2;
}

.text-center { text-align: center; }
.py-6 { padding: 2.5rem 0; }

.state-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.spinner-sm {
  width: 18px;
  height: 18px;
  border: 2px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ========================================================
   VUE CARTES MOBILES (PAR DÉFAUT CACHÉE SUR GRAND ÉCRAN)
   ======================================================== */
.mobile-cards-view {
  display: none;
  width: 100%;
}

.empty-state-card {
  background: #ffffff;
  border-radius: 14px;
  border: 1px dashed #cbd5e1;
  padding: 2.5rem 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.empty-icon {
  width: 44px;
  height: 44px;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.cards-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.coupon-card {
  background: #ffffff;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.code-wrapper {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  position: relative;
}

.copy-feedback {
  font-size: 0.75rem;
  color: #16a34a;
  font-weight: 600;
  background: #dcfce7;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  padding: 0.85rem 0;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
}

.card-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.card-label {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
}

.discount-val.highlight {
  font-size: 1.1rem;
  font-weight: 800;
  color: #059669;
}

.validity-dates {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.2rem;
}

.validity-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
}

.date-prefix {
  color: #94a3b8;
  font-weight: 500;
  font-size: 0.75rem;
}

.date-val {
  color: #1e293b;
  font-weight: 600;
}

.card-row.usage-block {
  flex-direction: column;
  align-items: stretch;
  gap: 0.4rem;
}

.usage-title-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.usage-count {
  font-size: 0.85rem;
  font-weight: 700;
  color: #1e293b;
}

.card-actions {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

.btn-card-action {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.65rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 42px;
}

.btn-card-action.edit {
  background: #eff6ff;
  color: #2563eb;
  border: 1px solid #bfdbfe;
}
.btn-card-action.edit:hover {
  background: #dbeafe;
}

.btn-card-action.delete {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}
.btn-card-action.delete:hover {
  background: #fee2e2;
}

/* ========================================================
   RESPONSIVE : TABLETTES (769px <= écran <= 1024px)
   ======================================================== */
@media (max-width: 1024px) {
  .admin-coupons-wrapper {
    gap: 1.25rem;
    padding-bottom: calc(80px + env(safe-area-inset-bottom));
  }

  .header-section {
    flex-wrap: wrap;
    align-items: center;
  }

  .admin-table th,
  .admin-table td {
    padding: 0.85rem 1rem;
    font-size: 0.85rem;
  }

  .usage-bar-container {
    width: 110px;
  }
}

/* ========================================================
   RESPONSIVE : SMARTPHONES (<= 768px)
   ======================================================== */
@media (max-width: 768px) {
  .admin-coupons-wrapper {
    gap: 1.2rem;
    padding-bottom: calc(85px + env(safe-area-inset-bottom));
  }

  .header-section {
    flex-direction: column;
    align-items: stretch;
    gap: 0.9rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .gray-text {
    font-size: 0.85rem;
  }

  .action-col {
    width: 100%;
  }

  .btn-primary {
    width: 100%;
    min-height: 44px;
    padding: 0.75rem 1rem;
    border-radius: 10px;
  }

  /* Bascule : Cacher le tableau, afficher les cartes */
  .desktop-table-view {
    display: none !important;
  }

  .mobile-cards-view {
    display: block !important;
  }
}

/* ========================================================
   RESPONSIVE : TRÈS PETITS ÉCRANS (<= 380px)
   ======================================================== */
@media (max-width: 380px) {
  .card-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .validity-dates {
    align-items: flex-start;
  }

  .btn-card-action {
    font-size: 0.8rem;
    padding: 0.55rem;
  }
}
</style>