<template>
  <div class="surmesure-container">

    <div class="grid-3-cols">
      <!-- ⚡️ CORRECTION : Utilisation de is_active au lieu de isActive -->
      <div class="contract-card" v-for="contract in filteredContracts" :key="contract.id" :class="{'card-offline': !contract.is_active}">
        
        <div class="card-header">
          <div class="icon-box-purple"><component :is="DocumentTextIcon" class="icon-md" /></div>
          <span class="status-badge" :class="contract.is_active ? 'badge-green' : 'badge-gray'">
            {{ contract.is_active ? 'En ligne' : 'Hors ligne' }}
          </span>
        </div>

        <div class="card-body">
          <!-- ⚡️ CORRECTION : Le backend utilise 'subject' pour le sur-mesure -->
          <h4 class="dark-text">{{ contract.subject || contract.title }}</h4>
          <span class="price-text">{{ contract.price || contract.prix }} FCFA</span>
          <span class="gray-text text-sm block mt-1" v-if="contract.email">{{ contract.email }}</span>
        </div>

        <div class="card-footer">
          <div class="actions-block">
            <label class="switch" title="Mettre en ligne / Hors ligne">
              <input type="checkbox" v-model="contract.is_active" @change="toggleStatus(contract)">
              <span class="slider round"></span>
            </label>
            <button class="action-icon-btn edit-btn" @click="openLocalModal(contract)" title="Modifier">
              <component :is="PencilSquareIcon" class="icon-sm" />
            </button>
            <button class="action-icon-btn delete-btn" @click="handleDelete(contract.id)" title="Supprimer">
              <component :is="TrashIcon" class="icon-sm" />
            </button>
          </div>
        </div>

      </div>
    </div>

    <div v-if="filteredContracts.length === 0" class="empty-state">
      <p class="gray-text">Aucun contrat sur-mesure trouvé.</p>
    </div>

    <transition name="fade">
      <div v-if="isModalOpen" class="folder-modal-overlay" @click.self="closeLocalModal">
        <div class="folder-modal">
          <div class="folder-modal-header bg-purple">
            <h3>{{ editingContract ? 'Modifier le contrat' : 'Nouveau Contrat Sur-Mesure' }}</h3>
            <button class="close-modal-btn" @click="closeLocalModal">&times;</button>
          </div>
          
          <form @submit.prevent="submitContract" class="folder-modal-body">
            <div class="form-group">
              <label for="contractTitle">Sujet du contrat</label>
              <input type="text" id="contractTitle" v-model="formData.title" placeholder="Ex: Pacte d'actionnaires..." required />
            </div>
            
            <div class="form-group">
              <label for="contractPrice">Prix (FCFA)</label>
              <input type="number" id="contractPrice" v-model="formData.price" placeholder="Ex: 150000" required />
            </div>

            <div class="folder-modal-footer">
              <button type="button" class="btn-cancel" @click="closeLocalModal">Annuler</button>
              <button type="submit" class="btn-save bg-purple-btn">{{ editingContract ? 'Enregistrer' : 'Créer' }}</button>
            </div>
          </form>
        </div>
      </div>
    </transition>

  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw, reactive } from 'vue';
import { PlusIcon, TrashIcon, PencilSquareIcon, DocumentTextIcon } from '@heroicons/vue/24/outline';
import { useAdminContratStore } from '../../../../stores/adminContratStore'; // 👈 Ajout du store

export default {
  name: 'AdminSurmesure',
  props: {
    contracts: { type: Array as () => any[], required: true },
    searchQuery: { type: String, default: '' }
  },
  setup(props, { expose }) {
    
    // ⚡️ Initialisation du store
    const adminStore = useAdminContratStore();

    const isModalOpen = ref(false);
    const editingContract = ref<any>(null);
    const formData = reactive({ title: '', price: '' });

    const filteredContracts = computed(() => {
      if (!props.searchQuery) return props.contracts;
      return props.contracts.filter(c => {
        const searchText = c.subject || c.title || '';
        return searchText.toLowerCase().includes(props.searchQuery.toLowerCase());
      });
    });

    const openLocalModal = (contract: any = null) => {
      if (contract && (contract.title || contract.subject)) {
        editingContract.value = contract;
        formData.title = contract.subject || contract.title;
        formData.price = contract.price || contract.prix;
      } else {
        editingContract.value = null;
        formData.title = '';
        formData.price = '';
      }
      isModalOpen.value = true;
    };

    const closeLocalModal = () => { isModalOpen.value = false; };

    expose({ openLocalModal });

    const submitContract = () => {
      if (editingContract.value) {
        editingContract.value.subject = formData.title;
        editingContract.value.price = formData.price;
      } else {
        // En attendant que ton collègue crée la route POST pour le sur-mesure
        props.contracts.unshift({
          id: Date.now().toString(),
          subject: formData.title,
          price: formData.price,
          is_active: true,
          email: 'Nouveau'
        });
      }
      closeLocalModal();
    };

    const handleDelete = (id: string | number) => {
      if (confirm('Voulez-vous vraiment supprimer ce contrat sur-mesure définitivement ?')) {
        const index = props.contracts.findIndex(c => c.id === id);
        if (index !== -1) props.contracts.splice(index, 1);
      }
    };

    const toggleStatus = (contract: any) => {
      console.log(`Le statut de ${contract.subject || contract.title} est maintenant: ${contract.is_active}`);
    };

    return {
      adminStore,
      filteredContracts,
      isModalOpen, editingContract, formData,
      openLocalModal, closeLocalModal, submitContract, handleDelete, toggleStatus,
      PlusIcon: markRaw(PlusIcon), TrashIcon: markRaw(TrashIcon), 
      PencilSquareIcon: markRaw(PencilSquareIcon), DocumentTextIcon: markRaw(DocumentTextIcon)
    };
  }
}
</script>

<style scoped>
/* Les styles restent identiques, j'ai juste retiré la classe .actions-header et .add-btn[cite: 12] */
.surmesure-container { font-family: 'Inter', sans-serif; }

.grid-3-cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; padding: 1rem 0; }

.contract-card { background: #ffffff; border-radius: 24px; padding: 1.5rem; border: 1px solid #e2e8f0; display: flex; flex-direction: column; gap: 1.2rem; transition: 0.3s ease; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }
.contract-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }
.card-offline { opacity: 0.7; filter: grayscale(40%); }

.card-header { display: flex; justify-content: space-between; align-items: flex-start; }
.icon-box-purple { width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; background: #f3e8ff; color: var(--nathan-blue); }
.status-badge { padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; white-space: nowrap; }
.badge-green { background: #d1fae5; color: #059669; }
.badge-gray { background: #f1f5f9; color: #64748b; }

.dark-text { color: #1e293b; margin: 0; font-size: 1.1rem; font-weight: 700;}
.price-text { color: var(--nathan-blue); font-size: 0.95rem; font-weight: 600; }

.card-footer { display: flex; justify-content: flex-end; border-top: 1px solid #f1f5f9; padding-top: 1.2rem; }
.actions-block { display: flex; align-items: center; gap: 0.5rem; }

.switch { position: relative; display: inline-block; width: 36px; height: 20px; margin-right: 0.5rem; flex-shrink: 0; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: #fff; transition: .4s; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
input:checked + .slider { background-color: #10b981; }
input:checked + .slider:before { transform: translateX(16px); }

.action-icon-btn { background: #f8fafc; border: 1px solid #e2e8f0; color: #64748b; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; flex-shrink: 0; }
.action-icon-btn:hover { background: #e2e8f0; color: #1e293b; }
.delete-btn:hover { background: #fee2e2; border-color: #fecaca; color: #ef4444; }

.folder-modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 100; padding: 1rem;
}
.folder-modal {
  background: white; border-radius: 20px; width: 100%; max-width: 450px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden;
}
.folder-modal-header {
  display: flex; justify-content: space-between; align-items: center; text-align: center; 
  padding: 1.5rem 2rem; border-bottom: 1px solid #e2e8f0;
}
.bg-purple { background: var(--nathan-blue); }
.folder-modal-header h3 { margin: 0; font-size: 1.2rem; color: #ffffff; white-space: nowrap; }
.close-modal-btn { background: transparent; border: none; font-size: 1.5rem; color: #e2e8f0; cursor: pointer }
.close-modal-btn:hover { color: #ffffff; }

.folder-modal-body { padding: 2rem; }
.form-group { margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-weight: 600; font-size: 0.9rem; color: #334155; }
.form-group input {
  width: 100%; padding: 0.8rem; border: 1px solid #cbd5e1; border-radius: 8px;
  background: #f8fafc; font-family: inherit; font-size: 0.95rem; outline: none; box-sizing: border-box;
}
.form-group input:focus { border-color: #7c3aed; background: #fff; }

.folder-modal-footer {
  display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; flex-wrap: nowrap;
}
.btn-cancel { background: transparent; border: 1px solid #cbd5e1; color: #64748b; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; font-weight: 600; white-space: nowrap; }
.btn-cancel:hover { background: #f1f5f9; }
.btn-save { border: none; color: white; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; font-weight: 600; white-space: nowrap; transition: 0.2s; }
.bg-purple-btn { background: #7c3aed; }
.bg-purple-btn:hover { background: #6d28d9; }

.empty-state { padding: 3rem; text-align: center; }
.gray-text { color: #64748b; font-size: 1.1rem; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 1024px) {
  .grid-3-cols { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .grid-3-cols { grid-template-columns: 1fr; }
}
</style>