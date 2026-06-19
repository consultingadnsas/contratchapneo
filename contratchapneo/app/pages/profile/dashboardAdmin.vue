<template>
  <!-- Le fond global est géré ici -->
  <div class="admin-layout">
    
    <!-- 1. LA SIDEBAR (Transmet la liste et écoute les clics) -->
    <AdminSidebar 
      :menuItems="adminMenu" 
      @navigate="changePage" 
      @logout="handleLogout" 
    />

    <!-- 2. L'ESPACE DE TRAVAIL BLEU NUIT -->
    <main class="main-workspace">
        <!-- L'en-tête dynamique -->
        <AdminHeader 
          :title="currentPageTitle" 
          :subtitle="currentPageSubtitle"
          @add-contract="openAddContractModal"
        />

        <!-- Le contenu (A terme, ce sera un <router-view />) -->
        <div class="workspace-content">
          <adminHome v-if="activePageId === 'overview'" />
          <adminContrats v-if="activePageId === 'contracts'"/>
          <adminHistory v-if="activePageId === 'history'"/>
          
          <!-- Exemple d'espace vide pour les autres pages en attendant -->
          <div v-else class="placeholder-page">
            <h2>Module "{{ currentPageTitle }}" en cours de développement...</h2>
          </div>
        </div>
    </main>

  </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import AdminSidebar, { MenuItem } from '../../components/navigation/adminSidebar.vue' // Ajustez vos chemins
import AdminHeader from '../../components/heroSection/adminHeader.vue';
import adminHome from '../../components/sections/adminSection/adminHome.vue';
import adminContrats from '../../components/sections/adminSection/adminContrats.vue';
import adminHistory from '../../components/sections/adminSection/adminHistory.vue'
import { 
  HomeIcon, 
  BookOpenIcon, 
  InboxIcon, 
  DocumentTextIcon, 
  TrashIcon,
  Cog8ToothIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminLayout',
  components: { AdminSidebar, AdminHeader, adminHome, adminContrats, adminHistory },
  setup() {
    // La liste stricte des rubriques demandées
   // La liste stricte des rubriques demandées

    const adminMenu = ref<MenuItem[]>([
      { id: 'overview', label: "Tableau de bord", isActive: true, icon: HomeIcon },
      { id: 'history', label: 'Historiques', isActive: false, icon: BookOpenIcon },
      { id: 'inbox', label: 'Boîte de réception', isActive: false, icon: InboxIcon },
      { id: 'contracts', label: 'Contrats', isActive: false, icon: DocumentTextIcon },
      { id: 'trash', label: 'Corbeille', isActive: false, icon: TrashIcon },
      {id: 'settings', label: 'Paramètre', isActive:false, icon: Cog8ToothIcon },
    ]);

    const activePageId = ref('overview');

    // Mettre à jour les titres de l'en-tête dynamiquement
    const currentPageTitle = computed(() => adminMenu.value.find(m => m.id === activePageId.value)?.label || '');
    const currentPageSubtitle = computed(() => {
      if (activePageId.value === 'overview') return "Dernières actions et notifications de la plateforme.";
      if (activePageId.value === 'inbox') return "Gestion des demandes de contrats sur mesure.";
      if (activePageId.value === 'contracts') return "Ajoutez, modifiez ou supprimez des modèles du catalogue.";
      return "Gérez vos données administratives.";
    });

    const changePage = (id: string) => {
      activePageId.value = id;
      adminMenu.value.forEach(item => item.isActive = (item.id === id));
    };

    const handleLogout = () => console.log("Fermeture de la session Admin");
    const openAddContractModal = () => console.log("Ouverture de la modale d'ajout de contrat !");

    return { adminMenu, activePageId, currentPageTitle, currentPageSubtitle, changePage, handleLogout, openAddContractModal };
  }
}
</script>

<style scoped>
/* LE FOND BLEU NUIT SE TROUVE ICI */
.admin-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #0f172a; /* Bleu Nuit ContratChap */
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
  padding-bottom: calc(80px + env(safe-area-inset-bottom)); /* Laisse la place à la navbar mobile */
}

@media (min-width: 1024px) {
  .main-workspace { padding: 2.5rem 3rem; }
}

/* Style de remplacement pour les pages non créées */
.placeholder-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  border: 2px dashed rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  color: #64748b;
  text-align: center;
}
</style>