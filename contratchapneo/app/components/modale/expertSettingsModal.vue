<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content-manage">
      <div class="modal-header">
        <div class="modal-header-title-group">
          <component :is="Cog6ToothIcon" class="icon-md text-gray-700" />
          <div>
            <h3 class="modal-title">Paramètres</h3>
            <p class="modal-subtitle">Gérer les pays et les domaines</p>
          </div>
        </div>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- TABS -->
      <div class="tabs-container">
        <button 
          class="tab-btn" 
          :class="{ 'active-tab': activeTab === 'countries' }"
          @click="activeTab = 'countries'"
        >
          Pays ({{ countries.length }})
        </button>
        <button 
          class="tab-btn" 
          :class="{ 'active-tab': activeTab === 'domains' }"
          @click="activeTab = 'domains'"
        >
          Domaines ({{ domains.length }})
        </button>
      </div>
      <CountryModal v-if="activeTab === 'countries'" />

      <DomainModal v-if="activeTab === 'domains'" />

      <div class="modal-footer">
        <button class="btn-secondary-custom" @click="$emit('close')">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw } from 'vue';
import { useAdminProStore } from '../../stores/adminProStore';
import CountryModal from './countryModal.vue';
import DomainModal from './domainModal.vue';
import { Cog6ToothIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'ExpertSettingsModal',
  components: { CountryModal, DomainModal },
  emits: ['close'],
  setup() {
    const adminProStore = useAdminProStore();
    const activeTab = ref('countries');
    
    const countries = computed(() => adminProStore.countries);
    const domains = computed(() => adminProStore.domains);

    return {
      activeTab,
      countries,
      domains,
      Cog6ToothIcon: markRaw(Cog6ToothIcon)
    };
  }
};
</script>

<style scoped>
.modal-overlay { 
  position: fixed; 
  top: 0; 
  left: 0; 
  right: 0; 
  bottom: 0; 
  background: rgba(15, 23, 42, 0.4); 
  backdrop-filter: blur(4px); 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  z-index: 1000; 
  padding: 1rem; 
  box-sizing: border-box;
}

.modal-content-manage { 
  background: #ffffff; 
  border-radius: 20px; 
  width: 100%; 
  max-width: 580px; 
  max-height: 88vh; 
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); 
  display: flex; 
  flex-direction: column; 
  overflow: hidden; 
  box-sizing: border-box;
  animation: modalScaleIn 0.25s ease-out;
}

@keyframes modalScaleIn {
  from { opacity: 0; transform: scale(0.96) translateY(-10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 1.25rem 1.5rem; 
  border-bottom: 1px solid #f1f5f9; 
  flex-shrink: 0;
}

.modal-header-title-group { 
  display: flex; 
  align-items: center; 
  gap: 0.8rem; 
}

.modal-title { 
  margin: 0; 
  font-size: 1.25rem; 
  font-weight: 700; 
  color: #0f172a; 
}

.modal-subtitle { 
  margin: 0.15rem 0 0 0; 
  font-size: 0.8rem; 
  color: #94a3b8; 
  font-weight: 500; 
}

.close-btn { 
  background: #f1f5f9; 
  border: none; 
  width: 32px; 
  height: 32px; 
  border-radius: 50%; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  color: #64748b; 
  cursor: pointer; 
  transition: 0.2s; 
  flex-shrink: 0;
}

.close-btn:hover { 
  background: #fee2e2; 
  color: #ef4444; 
}

.tabs-container {
  display: flex;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.tab-btn {
  flex: 1;
  padding: 0.9rem 0.5rem;
  text-align: center;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  font-weight: 600;
  font-size: 0.9rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #0f172a;
}
.tab-btn.active-tab {
  color: #2563eb;
  background: #ffffff;
}

.modal-footer { 
  padding: 1.2rem 1.5rem; 
  border-top: 1px solid #f1f5f9; 
  background: #fafaf9; 
  border-bottom-left-radius: 20px; 
  border-bottom-right-radius: 20px; 
  display: flex; 
  justify-content: center; 
  gap: 1rem; 
  flex-shrink: 0;
}

.btn-secondary-custom { 
  background: #f1f5f9; 
  color: #475569; 
  border: 1px solid #e2e8f0; 
  font-weight: 600; 
  border-radius: 999px; 
  padding: 10px 24px; 
  font-size: 0.95rem; 
  transition: 0.2s ease; 
  display: flex; 
  align-items: center; 
  justify-content: center;
  gap: 0.5rem; 
  cursor: pointer; 
}

.btn-secondary-custom:hover { 
  background: #e2e8f0; 
  color: #0f172a; 
}

.icon-xs { width: 16px; height: 16px; }
.icon-sm { width: 20px; height: 20px; }
.icon-md { width: 24px; height: 24px; }
.text-gray-700 { color: #374151; }

/* ========================================================
   RESPONSIVE : TABLETTES ET SMARTPHONES (<= 640px)
   ======================================================== */
@media (max-width: 640px) {
  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-content-manage {
    max-height: 92vh;
    border-radius: 18px;
  }

  .modal-header {
    padding: 1rem 1.25rem;
  }

  .modal-title {
    font-size: 1.15rem;
  }

  .tabs-container .tab-btn {
    padding: 0.8rem 0.4rem;
    font-size: 0.85rem;
  }

  .modal-footer {
    padding: 1rem;
    border-bottom-left-radius: 18px;
    border-bottom-right-radius: 18px;
  }

  .btn-secondary-custom {
    width: 100%;
    justify-content: center;
  }
}
</style>