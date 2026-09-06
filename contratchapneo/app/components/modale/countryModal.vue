<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content-manage">
      <div class="modal-header">
        <div class="modal-header-title-group">
          <component :is="GlobeAltIcon" class="icon-md text-blue" />
          <div>
            <h3 class="modal-title">Gestion des Pays</h3>
            <p class="modal-subtitle">{{ countries.length }} pays configuré(s)</p>
          </div>
        </div>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <div class="modal-body-scrollable">
        <!-- Notification d'erreur ou de succès -->
        <div v-if="countryError" class="alert-box alert-error">
          <span>{{ countryError }}</span>
          <button @click="countryError = null" class="alert-close">✕</button>
        </div>
        <div v-if="countrySuccess" class="alert-box alert-success">
          <span>{{ countrySuccess }}</span>
          <button @click="countrySuccess = null" class="alert-close">✕</button>
        </div>

        <!-- Formulaire d'ajout rapide -->
        <div class="quick-add-panel">
          <h4 class="panel-subtitle">Ajouter un nouveau pays</h4>
          <div class="quick-add-grid">
            <div class="input-wrapper">
              <label class="input-label">Nom du pays *</label>
              <input 
                type="text" 
                v-model="newCountry.name" 
                class="form-input" 
                placeholder="Ex: Sénégal" 
                @keydown.enter="saveCountry" 
              />
            </div>
            <div class="input-wrapper">
              <label class="input-label">Code ISO *</label>
              <input 
                type="text" 
                v-model="newCountry.code" 
                class="form-input text-uppercase" 
                placeholder="Ex: SN" 
                maxlength="3" 
                @keydown.enter="saveCountry" 
              />
            </div>
          </div>
          <div class="quick-add-actions">
            <label class="checkbox-label">
              <input type="checkbox" v-model="newCountry.is_ohada_member" class="form-checkbox">
              <span class="checkbox-text">Membre de l'espace OHADA</span>
            </label>
            <button class="btn-primary-custom btn-sm" @click="saveCountry" :disabled="isLoading">
              <component :is="PlusIcon" class="icon-xs" /> Ajouter
            </button>
          </div>
        </div>

        <!-- Liste des pays existants -->
        <div class="items-list-section">
          <div class="list-header-row">
            <h4 class="panel-subtitle">Liste des pays</h4>
            <div class="mini-search-box">
              <component :is="MagnifyingGlassIcon" class="icon-xs icon-gray" />
              <input type="text" v-model="countrySearch" placeholder="Rechercher..." class="mini-search-input" />
            </div>
          </div>

          <div class="items-list-container">
            <div v-if="filteredCountries.length === 0" class="empty-list-notice">
              Aucun pays trouvé
            </div>
            <div 
              v-for="country in filteredCountries" 
              :key="country.id" 
              class="item-row"
            >
              <div class="item-info">
                <span class="country-badge">{{ country.code }}</span>
                <span class="item-name">{{ country.name }}</span>
                <span v-if="country.is_ohada_member" class="ohada-tag">OHADA</span>
              </div>
              <button 
                class="action-icon-btn delete-btn" 
                title="Supprimer ce pays" 
                @click="removeCountry(country)"
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
  GlobeAltIcon, 
  PlusIcon, 
  MagnifyingGlassIcon, 
  TrashIcon 
} from '@heroicons/vue/24/outline';

export default {
  name: 'CountryModal',
  emits: ['close'],
  setup() {
    const adminProStore = useAdminProStore();

    const newCountry = ref({ name: '', code: '', is_ohada_member: true });
    const countrySearch = ref('');
    const countryError = ref<string | null>(null);
    const countrySuccess = ref<string | null>(null);

    const countries = computed(() => adminProStore.countries);
    const isLoading = computed(() => adminProStore.isLoading);

    const filteredCountries = computed(() => {
      const q = countrySearch.value.trim().toLowerCase();
      if (!q) return countries.value;
      return countries.value.filter(c => 
        c.name.toLowerCase().includes(q) || c.code.toLowerCase().includes(q)
      );
    });

    const saveCountry = async () => {
      countryError.value = null;
      countrySuccess.value = null;
      if (!newCountry.value.name.trim() || !newCountry.value.code.trim()) {
        countryError.value = "Le nom et le code du pays sont obligatoires.";
        return;
      }
      try {
        await adminProStore.addCountry({
          name: newCountry.value.name.trim(),
          code: newCountry.value.code.trim().toUpperCase(),
          is_ohada_member: newCountry.value.is_ohada_member
        });
        countrySuccess.value = `Pays "${newCountry.value.name}" ajouté avec succès !`;
        newCountry.value = { name: '', code: '', is_ohada_member: true };
      } catch(e: any) {
        countryError.value = e.message || "Erreur lors de l'ajout du pays.";
      }
    };

    const removeCountry = async (country: any) => {
      countryError.value = null;
      countrySuccess.value = null;
      if (!confirm(`Êtes-vous sûr de vouloir supprimer le pays "${country.name}" ?`)) return;
      try {
        await adminProStore.deleteCountry(country.id);
        countrySuccess.value = `Pays "${country.name}" supprimé avec succès.`;
      } catch(e: any) {
        countryError.value = e.message || "Impossible de supprimer ce pays.";
      }
    };

    return {
      newCountry,
      countrySearch,
      countryError,
      countrySuccess,
      countries,
      isLoading,
      filteredCountries,
      saveCountry,
      removeCountry,
      GlobeAltIcon: markRaw(GlobeAltIcon),
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
.quick-add-grid { 
  display: grid; 
  grid-template-columns: 2fr 1fr; 
  gap: 0.8rem; 
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
.text-uppercase { 
  text-transform: uppercase; 
}
.quick-add-actions { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  gap: 1rem; 
  flex-wrap: wrap; 
}
.checkbox-label { 
  display: flex; 
  align-items: center; 
  gap: 0.6rem; 
  cursor: pointer; 
}
.form-checkbox { 
  width: 1.1rem; 
  height: 1.1rem; 
  accent-color: #2563eb; 
}
.checkbox-text { 
  font-size: 0.9rem; 
  color: #475569; 
  font-weight: 500; 
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
.country-badge { 
  background: #e0f2fe; 
  color: #0284c7; 
  font-weight: 700; 
  font-size: 0.75rem; 
  padding: 3px 8px; 
  border-radius: 6px; 
  letter-spacing: 0.5px; 
}
.item-name { 
  font-weight: 600; 
  font-size: 0.9rem; 
  color: #1e293b; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
}
.ohada-tag { 
  font-size: 0.7rem; 
  font-weight: 700; 
  color: #059669; 
  background: #d1fae5; 
  padding: 2px 7px; 
  border-radius: 4px; 
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
.text-blue { color: #3b82f6; }
.icon-gray { color: #94a3b8; }
</style>
