<template>
  <div class="admin-layout-container">
    <!-- Ta barre latérale fixe -->
    <AdminSidebar 
      :menuItems="adminMenu" 
      @logout="handleLogout" 
    />
    
    <!-- La zone dynamique où tes pages (Aperçu, Finance, etc.) vont s'afficher -->
    <main class="admin-main-content">
      <AdminHome/>
    </main>
  </div>
</template>

<script lang="ts">
import { ref, markRaw } from 'vue';
import AdminSidebar, {MenuItem} from '../../components/navigation/adminSidebar.vue';
import AdminHome from '../../components/sections/adminSection/adminHome.vue';
import AdminHeader from '../../components/heroSection/adminHeader.vue';
import { useRouter } from 'vue-router';
// Importe tes icônes ici...
import { HomeIcon, BanknotesIcon, UsersIcon, BookOpenIcon, InboxIcon, DocumentTextIcon, Cog8ToothIcon, TrashIcon, ChatBubbleBottomCenterTextIcon, SwatchIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'AdminLayout',
  components: { AdminSidebar, AdminHome, AdminHeader },
  setup() {
    const router = useRouter();

    // On définit le menu directement dans le Layout
    const adminMenu = ref<MenuItem[]>([
      { id: 'overview', label: "Dashboard", route: '/admin', icon: markRaw(HomeIcon), category: 'General' },
      { id: 'history', label: 'Historiques', route: '/admin/AdminHistory', icon: markRaw(BookOpenIcon), category: 'General' },
      { id: 'finance', label: 'Finances', route: '/admin/AdminFinance', icon: markRaw(BanknotesIcon), category: 'General' },
      { id: 'inbox', label: 'Demandes clients', route: '/admin/AdminInbox', icon: markRaw(InboxIcon), category: 'General' },
      { id: 'contracts', label: 'Contrats', route: '/admin/AdminContrats', icon: markRaw(DocumentTextIcon), category: 'Catalogue' },
      { id: 'experts', label: 'Experts Juridiques', route: '/admin/AdminExperts', icon: markRaw(UsersIcon), category: 'Catalogue' },
      { id: 'settings', label: 'Paramètres', route: '/admin/AdminSettings', icon: markRaw(Cog8ToothIcon), category: 'Tools' },
      { id: 'trash', label: 'Corbeille', route: '/admin/AdminTrash', icon: markRaw(TrashIcon), category: 'Tools' },
      { id: 'temoin', label: 'Témoignages', route: '/admin/AdminTesti', icon: markRaw(ChatBubbleBottomCenterTextIcon), category: 'Catalogue' },
      { id: 'packs', label: 'Packs de contrat', route: '/admin/Adminpacks', icon : markRaw(SwatchIcon), category: 'Catalogue' }
    ]);


    const handleLogout = () => {
      console.log('Déconnexion...');
      router.push('/auth/login');
    };

    return { adminMenu, handleLogout };
  }
}
</script>

<style scoped>
.admin-layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: #f8fafc;
}

.admin-main-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: calc(80px + env(safe-area-inset-bottom)); 
}

/* Ajustement pour mobile */
@media (max-width: 728px) {
  .admin-main-content {
    margin-left: 0;
    margin-bottom: 80px; /* Place pour la sidebar en bas sur mobile */
    padding: 1rem;
  }
}
</style>