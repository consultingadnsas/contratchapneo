<template>
  <div class="categories-wrapper">
    
    <div v-if="!openedCategory">
      
      <div class="folders-section">
        <h3 class="section-title text-md mb-3">Modèles de Contrats (Boutique)</h3>
        <div class="add-input-group">
          <input type="text" v-model="newStdCat" placeholder="Ajouter une catégorie..." @keyup.enter="handleAddStd" />
          <button class="btn-primary-small" @click="handleAddStd"><component :is="PlusIcon" class="icon-sm"/></button>
        </div>
        
        <div class="folders-grid">
          <div class="folder-wrapper" v-for="(cat, index) in standardCategories" :key="'std'+index" @click="openCategory(cat)">
            <folderCards 
              :title="cat"
              subtitle="Modèles OHADA"
              color="blue"
              :hasItems="true"
            />
            <button class="delete-folder-btn" @click.stop="$emit('delete-std', index)" title="Supprimer ce dossier">
              <component :is="TrashIcon" class="icon-xs" />
            </button>
          </div>
        </div>
      </div>

      <div class="folders-section mt-4">
        <h3 class="section-title text-md mb-3">Services Sur-Mesure</h3>
        <div class="add-input-group">
          <input type="text" v-model="newCustomCat" placeholder="Ajouter une catégorie..." @keyup.enter="handleAddCustom" />
          <button class="btn-primary-small" @click="handleAddCustom"><component :is="PlusIcon" class="icon-sm"/></button>
        </div>
        
        <div class="folders-grid">
          <div class="folder-wrapper" v-for="(cat, index) in customCategories" :key="'cus'+index" @click="openCategory(cat)">
            <folderCards 
              :title="cat"
              subtitle="Expertise juridique"
              color="purple"
              :hasItems="true"
            />
            <button class="delete-folder-btn" @click.stop="$emit('delete-custom', index)" title="Supprimer ce dossier">
              <component :is="TrashIcon" class="icon-xs" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="opened-folder-view">
      
      <div class="opened-folder-header">
        <button class="btn-secondary" @click="closeCategory">
          <component :is="ArrowLeftIcon" class="icon-sm" /> Retour
        </button>
        <div class="folder-title-box">
          <span class="gray-text text-sm">Contenu du dossier</span>
          <h3 class="section-title">{{ openedCategory }}</h3>
        </div>
      </div>

      <div class="contracts-grid mt-4">
        <div class="contract-card" v-for="contract in contractsInCategory" :key="contract.id" :class="{'card-offline': !contract.isActive}">
          <div class="card-header">
            <div class="icon-box-light">
              <component :is="DocumentTextIcon" class="icon-md" />
            </div>
            <span class="status-badge" :class="contract.isActive ? 'badge-green' : 'badge-gray'">
              {{ contract.isActive ? 'En ligne' : 'Hors ligne' }}
            </span>
          </div>

          <div class="card-body">
            <h4 class="dark-text">{{ contract.title }}</h4>
            <span class="gray-text text-sm">{{ contract.category }}</span>
          </div>

          <div class="card-footer">
            <div class="price-block">
              <strong class="dark-text">{{ contract.price }} FCFA</strong>
            </div>
            <div class="actions-block">
              <button class="action-icon-btn edit-btn" @click="$emit('edit-contract', contract)">
                <component :is="PencilSquareIcon" class="icon-sm" />
              </button>
            </div>
          </div>
        </div>

        <div v-if="contractsInCategory.length === 0" class="empty-folder-state">
          <div class="icon-box-light bg-gray-light mx-auto mb-3">
            <component :is="DocumentTextIcon" class="icon-lg gray-text" />
          </div>
          <h4 class="dark-text">Ce dossier est vide</h4>
          <p class="gray-text text-sm">Aucun contrat n'est actuellement associé à cette catégorie.</p>
        </div>
      </div>

    </div>

  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw } from 'vue';
import { PlusIcon, TrashIcon, PencilSquareIcon, DocumentTextIcon, ArrowLeftIcon } from '@heroicons/vue/24/outline';
import folderCards from '../../../cards/folderCards.vue'; // Ajuste le chemin si nécessaire

export default {
  name: 'AdminCategories',
  components: { folderCards },
  props: {
    standardCategories: { type: Array, required: true },
    customCategories: { type: Array, required: true },
    contracts: { type: Array, required: true }
  },
  emits: ['add-std', 'add-custom', 'delete-std', 'delete-custom', 'edit-contract'],
  setup(props, { emit }) {
    const openedCategory = ref<string | null>(null);
    const newStdCat = ref('');
    const newCustomCat = ref('');

    const openCategory = (cat: string) => openedCategory.value = cat;
    const closeCategory = () => openedCategory.value = null;

    // Filtre les contrats pour n'afficher que ceux du dossier ouvert
    const contractsInCategory = computed(() => {
      return props.contracts.filter((c: any) => c.category === openedCategory.value);
    });

    const handleAddStd = () => {
      if (newStdCat.value.trim() !== '') {
        emit('add-std', newStdCat.value.trim());
        newStdCat.value = '';
      }
    };

    const handleAddCustom = () => {
      if (newCustomCat.value.trim() !== '') {
        emit('add-custom', newCustomCat.value.trim());
        newCustomCat.value = '';
      }
    };

    return {
      openedCategory, openCategory, closeCategory, contractsInCategory,
      newStdCat, newCustomCat, handleAddStd, handleAddCustom,
      PlusIcon: markRaw(PlusIcon), TrashIcon: markRaw(TrashIcon), 
      PencilSquareIcon: markRaw(PencilSquareIcon), DocumentTextIcon: markRaw(DocumentTextIcon), 
      ArrowLeftIcon: markRaw(ArrowLeftIcon)
    };
  }
}
</script>

<style scoped>
/* Copie ici toutes les classes CSS liées aux catégories, aux dossiers et aux petites cartes contrats de ton fichier précédent */
.folders-section { background: #ffffff; border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
.section-title { font-size: 1.1rem; color: #1e293b; font-weight: 700; margin: 0; }
.add-input-group { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; max-width: 400px; }
.add-input-group input { flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; padding: 0.6rem 1rem; border-radius: 12px; outline: none; }
.add-input-group input:focus { border-color: #2563eb; }

.btn-primary-small { background: #2563eb; color: white; border: none; padding: 0.6rem; border-radius: 12px; cursor: pointer; transition: 0.2s; }
.btn-primary-small:hover { background: #1d4ed8; }

.folders-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
.folder-wrapper { position: relative; cursor: pointer; transition: 0.2s; border-radius: 16px; }
.folder-wrapper:hover { transform: translateY(-3px); }

.delete-folder-btn { position: absolute; top: -10px; right: -10px; z-index: 10; background: #ffffff; border: 1px solid #fee2e2; color: #ef4444; border-radius: 8px; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; opacity: 0; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.1); }
.folder-wrapper:hover .delete-folder-btn { opacity: 1; }
.delete-folder-btn:hover { background: #fee2e2; transform: scale(1.1); }

.opened-folder-view { background: #ffffff; border-radius: 24px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
.opened-folder-header { display: flex; align-items: center; gap: 1.5rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 1.5rem; margin-bottom: 1rem; }
.btn-secondary { background: #ffffff; border: 1px solid #cbd5e1; padding: 0.6rem 1rem; border-radius: 10px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: 0.2s; color: #1e293b; }
.btn-secondary:hover { background: #f8fafc; border-color: #94a3b8; }
.folder-title-box { display: flex; flex-direction: column; }

.contracts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
.contract-card { background: #ffffff; border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #f8fafc; display: flex; flex-direction: column; gap: 1.2rem; transition: 0.3s ease; }
.contract-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; }
.icon-box-light { width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; background: #eff6ff; color: #3b82f6; }
.status-badge { padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
.badge-green { background: #d1fae5; color: #059669; }
.badge-gray { background: #f1f5f9; color: #64748b; }
.card-body h4 { margin: 0 0 0.2rem 0; font-size: 1.05rem; font-weight: 700; color: #1e293b; }
.card-footer { display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid #f1f5f9; padding-top: 1.2rem; }
.price-block strong { color: #1e293b; font-size: 1.1rem; }
.action-icon-btn { background: #f8fafc; border: 1px solid #e2e8f0; color: #64748b; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }
.action-icon-btn:hover { background: #e2e8f0; color: #1e293b; }

.empty-folder-state { grid-column: 1 / -1; text-align: center; padding: 4rem 2rem; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 20px; }
.bg-gray-light { background: #f1f5f9; }

/* Utilitaires */
.mt-4 { margin-top: 1.5rem; } .mb-3 { margin-bottom: 1rem; } .mx-auto { margin-left: auto; margin-right: auto; }
.icon-xs { width: 16px; height: 16px; } .icon-sm { width: 18px; height: 18px; } .icon-md { width: 22px; height: 22px; } .icon-lg { width: 28px; height: 28px; }
.dark-text { color: #1e293b; } .gray-text { color: #94a3b8; } .text-sm { font-size: 0.8rem; }
</style>