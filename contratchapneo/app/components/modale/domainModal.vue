<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content-manage">
      <div class="modal-header">
        <div class="modal-header-title-group">
          <component :is="BriefcaseIcon" class="icon-md text-purple" />
          <div>
            <h3 class="modal-title">Gestion des Domaines Juridiques</h3>
            <p class="modal-subtitle">{{ domains.length }} domaine(s) configuré(s)</p>
          </div>
        </div>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <div class="modal-body-scrollable">
        <!-- Notification d'erreur ou de succès -->
        <div v-if="domainError" class="alert-box alert-error">
          <span>{{ domainError }}</span>
          <button @click="domainError = null" class="alert-close">✕</button>
        </div>
        <div v-if="domainSuccess" class="alert-box alert-success">
          <span>{{ domainSuccess }}</span>
          <button @click="domainSuccess = null" class="alert-close">✕</button>
        </div>

        <!-- Formulaire d'ajout rapide -->
        <div class="quick-add-panel">
          <h4 class="panel-subtitle">Ajouter un nouveau domaine</h4>
          <div class="input-wrapper mb-2">
            <label class="input-label">Nom du domaine / Acte uniforme *</label>
            <input 
              type="text" 
              v-model="newDomain.name" 
              class="form-input" 
              placeholder="Ex: Droit des sociétés" 
              @keydown.enter="saveDomain" 
            />
          </div>
          <div class="input-wrapper mb-2">
            <label class="input-label">Description (Optionnelle)</label>
            <input 
              type="text" 
              v-model="newDomain.description" 
              class="form-input" 
              placeholder="Brève description..." 
              @keydown.enter="saveDomain" 
            />
          </div>
          <div class="quick-add-actions justify-end">
            <button class="btn-primary-custom btn-sm" @click="saveDomain" :disabled="isLoading">
              <component :is="PlusIcon" class="icon-xs" /> Ajouter
            </button>
          </div>
        </div>

        <!-- Liste des domaines existants -->
        <div class="items-list-section">
          <div class="list-header-row">
            <h4 class="panel-subtitle">Liste des domaines</h4>
            <div class="mini-search-box">
              <component :is="MagnifyingGlassIcon" class="icon-xs icon-gray" />
              <input type="text" v-model="domainSearch" placeholder="Rechercher..." class="mini-search-input" />
            </div>
          </div>

          <div class="items-list-container">
            <div v-if="filteredDomains.length === 0" class="empty-list-notice">
              Aucun domaine trouvé
            </div>
            <div 
              v-for="domain in filteredDomains" 
              :key="domain.id" 
              class="item-row"
            >
              <div class="item-info">
                <div class="domain-main-info">
                  <span class="item-name">{{ domain.name }}</span>
                  <span v-if="domain.description" class="domain-description">{{ domain.description }}</span>
                </div>
              </div>
              <button 
                class="action-icon-btn delete-btn" 
                title="Supprimer ce domaine" 
                @click="removeDomain(domain)"
                :disabled="isLoading"
              >
                <component :is="TrashIcon" class="icon-sm" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn-secondary-custom" @click="$emit('close')">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw } from 'vue';
import { useAdminProStore } from '../../stores/adminProStore';
import { 
  BriefcaseIcon, 
  PlusIcon, 
  MagnifyingGlassIcon, 
  TrashIcon 
} from '@heroicons/vue/24/outline';

export default {
  name: 'DomainModal',
  emits: ['close'],
  setup() {
    const adminProStore = useAdminProStore();

    const newDomain = ref({ name: '', description: '' });
    const domainSearch = ref('');
    const domainError = ref<string | null>(null);
    const domainSuccess = ref<string | null>(null);

    const domains = computed(() => adminProStore.domains);
    const isLoading = computed(() => adminProStore.isLoading);

    const filteredDomains = computed(() => {
      const q = domainSearch.value.trim().toLowerCase();
      if (!q) return domains.value;
      return domains.value.filter((d: any) => 
        d.name.toLowerCase().includes(q) || (d.description && d.description.toLowerCase().includes(q))
      );
    });

    const saveDomain = async () => {
      domainError.value = null;
      domainSuccess.value = null;
      if (!newDomain.value.name.trim()) {
        domainError.value = "Le nom du domaine est obligatoire.";
        return;
      }
      try {
        await adminProStore.addDomain({
          name: newDomain.value.name.trim(),
          description: newDomain.value.description ? newDomain.value.description.trim() : ''
        });
        domainSuccess.value = `Domaine "${newDomain.value.name}" ajouté avec succès !`;
        newDomain.value = { name: '', description: '' };
      } catch(e: any) {
        domainError.value = e.message || "Erreur lors de l'ajout du domaine.";
      }
    };

    const removeDomain = async (domain: any) => {
      domainError.value = null;
      domainSuccess.value = null;
      if (!confirm(`Êtes-vous sûr de vouloir supprimer le domaine "${domain.name}" ?`)) return;
      try {
        await adminProStore.deleteDomain(domain.id);
        domainSuccess.value = `Domaine "${domain.name}" supprimé avec succès.`;
      } catch(e: any) {
        domainError.value = e.message || "Impossible de supprimer ce domaine.";
      }
    };

    return {
      newDomain,
      domainSearch,
      domainError,
      domainSuccess,
      domains,
      isLoading,
      filteredDomains,
      saveDomain,
      removeDomain,
      BriefcaseIcon: markRaw(BriefcaseIcon),
      PlusIcon: markRaw(PlusIcon),
      MagnifyingGlassIcon: markRaw(MagnifyingGlassIcon),
      TrashIcon: markRaw(TrashIcon)
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
}
.modal-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 1.5rem; 
  border-bottom: 1px solid #f1f5f9; 
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
}
.close-btn:hover { 
  background: #e2e8f0; 
  color: #0f172a; 
}
.modal-body-scrollable { 
  padding: 1.2rem 1.5rem; 
  overflow-y: auto; 
  display: flex; 
  flex-direction: column; 
  gap: 1.2rem; 
}
.quick-add-panel { 
  background: #f8fafc; 
  border: 1px solid #e2e8f0; 
  border-radius: 16px; 
  padding: 1.2rem; 
  display: flex; 
  flex-direction: column; 
  gap: 0.8rem; 
}
.panel-subtitle { 
  font-size: 0.85rem; 
  font-weight: 700; 
  color: #334155; 
  margin: 0; 
  text-transform: uppercase; 
  letter-spacing: 0.5px; 
}
.input-wrapper { 
  display: flex; 
  flex-direction: column; 
}
.input-label { 
  display: block; 
  font-size: 0.85rem; 
  font-weight: 600; 
  color: #475569; 
  margin-bottom: 0.4rem; 
}
.form-input { 
  width: 100%; 
  padding: 0.7rem 1rem; 
  border-radius: 12px; 
  border: 1px solid #cbd5e1; 
  outline: none; 
  font-size: 0.95rem; 
}
.form-input:focus { 
  border-color: #2563eb; 
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); 
}
.quick-add-actions { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  gap: 1rem; 
  flex-wrap: wrap; 
}
.justify-end { 
  justify-content: flex-end; 
}
.btn-primary-custom { 
  background: var(--primary-color-dark, #0f172a); 
  color: #ffffff; 
  font-weight: 600; 
  border-radius: 999px; 
  padding: 10px 20px; 
  font-size: 0.95rem; 
  border: none; 
  transition: background 0.2s ease; 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
  cursor: pointer; 
}
.btn-primary-custom:hover { 
  background: #1f2937; 
}
.btn-secondary-custom { 
  background: #f1f5f9; 
  color: #475569; 
  border: 1px solid #e2e8f0; 
  font-weight: 600; 
  border-radius: 999px; 
  padding: 10px 20px; 
  font-size: 0.95rem; 
  transition: 0.2s ease; 
  display: flex; 
  align-items: center; 
  gap: 0.5rem; 
  cursor: pointer; 
}
.btn-secondary-custom:hover { 
  background: #e2e8f0; 
  color: #0f172a; 
}
.btn-sm { 
  padding: 8px 18px; 
  font-size: 0.85rem; 
}
.items-list-section { 
  display: flex; 
  flex-direction: column; 
  gap: 0.7rem; 
}
.list-header-row { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  gap: 1rem; 
}
.mini-search-box { 
  display: flex; 
  align-items: center; 
  gap: 0.4rem; 
  background: #ffffff; 
  border: 1px solid #cbd5e1; 
  border-radius: 999px; 
  padding: 0.35rem 0.8rem; 
  width: 200px; 
}
.mini-search-box:focus-within { 
  border-color: #2563eb; 
}
.mini-search-input { 
  border: none; 
  outline: none; 
  background: transparent; 
  font-size: 0.8rem; 
  width: 100%; 
  color: #1e293b; 
}
.items-list-container { 
  max-height: 250px; 
  overflow-y: auto; 
  border: 1px solid #e2e8f0; 
  border-radius: 14px; 
  background: #ffffff; 
}
.item-row { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 0.75rem 1rem; 
  border-bottom: 1px solid #f1f5f9; 
  transition: background 0.15s ease; 
}
.item-row:last-child { 
  border-bottom: none; 
}
.item-row:hover { 
  background: #f8fafc; 
}
.item-info { 
  display: flex; 
  align-items: center; 
  gap: 0.7rem; 
  min-width: 0; 
  flex: 1; 
}
.domain-main-info { 
  display: flex; 
  flex-direction: column; 
  gap: 0.15rem; 
  min-width: 0; 
}
.item-name { 
  font-weight: 600; 
  font-size: 0.9rem; 
  color: #1e293b; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
}
.domain-description { 
  font-size: 0.75rem; 
  color: #64748b; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
  max-width: 360px; 
}
.action-icon-btn { 
  background: transparent; 
  border: none; 
  color: #cbd5e1; 
  cursor: pointer; 
  transition: 0.2s; 
  padding: 0.2rem; 
}
.action-icon-btn:hover { 
  color: #1e293b; 
}
.delete-btn:hover { 
  color: #ef4444; 
}
.empty-list-notice { 
  padding: 2rem; 
  text-align: center; 
  color: #94a3b8; 
  font-size: 0.85rem; 
  font-style: italic; 
}
.alert-box { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 0.7rem 1rem; 
  border-radius: 10px; 
  font-size: 0.85rem; 
}
.alert-error { 
  background: #fef2f2; 
  border: 1px solid #fecaca; 
  color: #dc2626; 
}
.alert-success { 
  background: #f0fdf4; 
  border: 1px solid #bbf7d0; 
  color: #16a34a; 
}
.alert-close { 
  background: transparent; 
  border: none; 
  font-weight: bold; 
  cursor: pointer; 
  color: inherit; 
  padding: 0 4px; 
  font-size: 0.9rem; 
}
.modal-footer { 
  padding: 1.2rem 1.5rem; 
  border-top: 1px solid #f1f5f9; 
  background: #fafaf9; 
  border-bottom-left-radius: 20px; 
  border-bottom-right-radius: 20px; 
  display: flex; 
  justify-content: flex-end; 
  gap: 1rem; 
}
.icon-xs { width: 16px; height: 16px; }
.icon-sm { width: 20px; height: 20px; }
.icon-md { width: 24px; height: 24px; }
.text-purple { color: #a855f7; }
.icon-gray { color: #94a3b8; }
.mb-2 { margin-bottom: 0.5rem; }
</style>
