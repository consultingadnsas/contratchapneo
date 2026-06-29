<template>
  <div class="admin-layout">
    
    <AdminSidebar 
      :menuItems="adminMenu" 
      @navigate="changePage" 
      @logout="handleLogout" 
    />

    <main class="main-workspace">
        <AdminHeader 
          :title="currentPageTitle" 
          :subtitle="currentPageSubtitle"
          @add-contract="openAddContractModal"
        />

        <div class="workspace-content">
          <adminHome v-if="activePageId === 'overview'" />
          <adminContrats v-if="activePageId === 'contracts'" 
          :targetTab="requestedTab"/>
          <adminHistory v-if="activePageId === 'history'"/>
          <adminInbox v-if="activePageId === 'inbox'"/>
          
          <div v-else class="placeholder-page">
            <h2>Module "{{ currentPageTitle }}" en cours de développement...</h2>
          </div>
        </div>
    </main>

  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw } from 'vue';
import AdminSidebar, { MenuItem } from '../../components/navigation/adminSidebar.vue';
import AdminHeader from '../../components/heroSection/adminHeader.vue';
import adminHome from '../../components/sections/adminSection/adminHome.vue';
import adminContrats from '../../components/sections/adminSection/adminContrats.vue';
import adminHistory from '../../components/sections/adminSection/adminHistory.vue';
import adminInbox from '../../components/sections/adminSection/adminInbox.vue';
import { 
  HomeIcon, 
  BookOpenIcon, 
  InboxIcon, 
  DocumentTextIcon, 
  TrashIcon,
  Cog8ToothIcon,
  UsersIcon,
  BanknotesIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminLayout',
  components: { AdminSidebar, AdminHeader, adminHome, adminContrats, adminHistory, adminInbox },
  setup() {
    // Ajout de la propriété 'category' pour reproduire le style de l'image
    const adminMenu = ref<MenuItem[]>([
      { id: 'overview', label: "Dashboard", isActive: true, icon: markRaw(HomeIcon), category: 'General' },
      { id: 'history', label: 'Historiques', isActive: false, icon: markRaw(BookOpenIcon), category: 'General' },
      { id: 'finance', label: 'Finances', isActive: false, icon: markRaw(BanknotesIcon), category: 'General' },
      { id: 'inbox', label: 'Demandes clients', isActive: false, icon: markRaw(InboxIcon), category: 'General' },
      { id: 'contracts', label: 'Catalogue Contrats', isActive: false, icon: markRaw(DocumentTextIcon), category: 'Catalogue' },
      { id: 'experts', label: 'Experts Juridiques', isActive: false, icon: markRaw(UsersIcon), category: 'Catalogue' },
      { id: 'settings', label: 'Paramètres', isActive:false, icon: markRaw(Cog8ToothIcon), category: 'Tools' },
      { id: 'trash', label: 'Corbeille', isActive: false, icon: markRaw(TrashIcon), category: 'Tools' },
    ]);

    const activePageId = ref('overview');
    const requestedTab = ref('contracts'); // Par défaut, onglet normal

    const currentPageTitle = computed(() => adminMenu.value.find(m => m.id === activePageId.value)?.label || '');
    const currentPageSubtitle = computed(() => {
      if (activePageId.value === 'overview') return "Dernières actions et notifications de la plateforme.";
      if (activePageId.value === 'inbox') return "Gestion des demandes de contrats sur mesure.";
      if (activePageId.value === 'contracts') return "Ajoutez, modifiez ou supprimez des modèles du catalogue.";
      return "Gérez vos données administratives.";
    });

    const changePage = (id: string) => {
      activePageId.value = id;
      requestedTab.value = 'contracts';
      adminMenu.value.forEach(item => item.isActive = (item.id === id));
    };

    const goToCatalogueTab = () => {
      activePageId.value = 'contracts';
      requestedTab.value = 'categories'; // On cible spécifiquement les dossiers
      adminMenu.value.forEach(item => item.isActive = (item.id === 'contracts'));
    };

    const handleLogout = () => console.log("Fermeture de la session Admin");
    const openAddContractModal = () => console.log("Ouverture de la modale d'ajout de contrat !");

    return { adminMenu, activePageId, requestedTab, currentPageTitle, currentPageSubtitle, goToCatalogueTab, changePage, handleLogout, openAddContractModal };
  }
}
</script>

<style scoped>
/* LE NOUVEAU FOND GRIS/BLEU TRÈS CLAIR DE L'IMAGE */
.admin-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f4f7fe; /* Fond lumineux */
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden;
}

@media (min-width: 1024px) {
  .admin-layout { flex-direction: row; }
}

.main-workspace {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: calc(80px + env(safe-area-inset-bottom)); 
}

@media (min-width: 1024px) {
  .main-workspace { padding: 2.5rem 3rem; }
}

.placeholder-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  border: 2px dashed #cbd5e1;
  border-radius: 20px;
  color: #64748b;
  text-align: center;
}
</style>