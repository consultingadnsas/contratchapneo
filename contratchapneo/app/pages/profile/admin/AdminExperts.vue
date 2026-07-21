<template>
  <div class="admin-layout-container">
    
    <!-- Ta barre latérale fixe -->
    <AdminSidebar 
      :menuItems="adminMenu" 
      @logout="handleLogout" 
    />
    
    <!-- La zone dynamique -->
    <main class="admin-main-content">
      <AdminExpertModule />

    </main>
  </div>
</template>

<script lang="ts">
import { ref, markRaw } from 'vue';
import { useRouter } from 'vue-router';
import AdminSidebar, {MenuItem} from '../../../components/navigation/adminSidebar.vue';
import AdminExpertModule from '../../../components/sections/adminSection/adminExperts.vue';
import { HomeIcon, BanknotesIcon, UsersIcon, BookOpenIcon, InboxIcon, DocumentTextIcon, Cog8ToothIcon, TrashIcon, ChatBubbleBottomCenterTextIcon, SwatchIcon } from '@heroicons/vue/24/outline';
export default {
  name: 'AdminHistoryPage', 
  
  components: { 
    AdminSidebar,
    AdminExpertModule // 👈 Un seul composant à charger
  },

  setup() {
    const router = useRouter();

    const adminMenu = ref<MenuItem[]>([
      { id: 'overview', label: "Dashboard", route: '/profile/admin/AdminHome', icon: markRaw(HomeIcon), category: 'General' },
      { id: 'history', label: 'Historiques', route: '/profile/admin/AdminHistory', icon: markRaw(BookOpenIcon), category: 'General' },
      { id: 'finance', label: 'Finances', route: '/profile/admin/AdminFinance', icon: markRaw(BanknotesIcon), category: 'General' },
      { id: 'inbox', label: 'Demandes clients', route: '/profile/admin/AdminInbox', icon: markRaw(InboxIcon), category: 'General' },
      { id: 'contracts', label: 'Contrats', route: '/profile/admin/AdminContrats', icon: markRaw(DocumentTextIcon), category: 'Catalogue' },
      { id: 'experts', label: 'Experts Juridiques', route: '/profile/admin/AdminExperts', icon: markRaw(UsersIcon), category: 'Catalogue' },
      { id: 'settings', label: 'Paramètres', route: '/profile/admin/AdminSettings', icon: markRaw(Cog8ToothIcon), category: 'Tools' },
      { id: 'trash', label: 'Corbeille', route: '/profile/admin/AdminTrash', icon: markRaw(TrashIcon), category: 'Tools' },
      { id: 'temoin', label: 'Témoignages', route: '/profile/admin/AdminTesti', icon: markRaw(ChatBubbleBottomCenterTextIcon), category: 'Catalogue' },
      { id: 'packs', label: 'Packs de contrat', route: '/profile/admin/Adminpacks', icon : markRaw(SwatchIcon), category: 'Catalogue' }
    ]);

    const handleLogout = () => {
      console.log('Déconnexion...');
      // router.push('/auth/login');
    };

    return {
      adminMenu,
      handleLogout
    }
  }
}
</script>

<style scoped>
.admin-layout-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8fafc;
}

.admin-main-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: calc(80px + env(safe-area-inset-bottom)); 
}

@media (max-width: 728px) {
  .admin-main-content {
    margin-left: 0;
    margin-bottom: 80px;
    padding: 1rem;
  }
}
</style>