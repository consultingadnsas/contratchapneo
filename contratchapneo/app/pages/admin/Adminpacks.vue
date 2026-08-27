<template>
  <div class="admin-layout-container">
    
    <!-- Ta barre latérale fixe -->
    <AdminSidebar 
      :menuItems="adminMenu" 
      @logout="handleLogout" 
    />
    
    <!-- La zone dynamique -->
    <main class="admin-main-content">
      <AdminPacksModule />

    </main>
  </div>
</template>

<script lang="ts">
import { ref, markRaw } from 'vue';
import { useRouter } from 'vue-router';
import AdminSidebar, {MenuItem} from '../../components/navigation/adminSidebar.vue';
import AdminPacksModule from '../../components/sections/adminSection/adminpacks.vue';
import { HomeIcon, BanknotesIcon, UsersIcon, BookOpenIcon, InboxIcon, DocumentTextIcon, CalculatorIcon, ShoppingBagIcon, SwatchIcon, GiftTopIcon } from '@heroicons/vue/24/outline';
export default {
  name: 'AdminPacksPage', 
  
  components: { 
    AdminSidebar,
    AdminPacksModule
  },

  setup() {
    const router = useRouter();

   const adminMenu = ref<MenuItem[]>([
      { id: 'overview', label: "Dashboard", route: '/admin', icon: markRaw(HomeIcon), category: 'General' },
      { id: 'history', label: 'Historiques', route: '/admin/AdminHistory', icon: markRaw(BookOpenIcon), category: 'General' },
      { id: 'finance', label: 'Finances', route: '/admin/AdminFinance', icon: markRaw(BanknotesIcon), category: 'General' },
      { id: 'inbox', label: 'Demandes clients', route: '/admin/AdminInbox', icon: markRaw(InboxIcon), category: 'General' },
      { id: 'contracts', label: 'Contrats', route: '/admin/AdminContrats', icon: markRaw(DocumentTextIcon), category: 'Catalogue' },
      { id: 'experts', label: 'Experts Juridiques', route: '/admin/AdminExperts', icon: markRaw(UsersIcon), category: 'Catalogue' },
      { id:'promo', label: 'Coupons & promo', route: '/admin/AdminPromo', icon: markRaw(GiftTopIcon), category: 'Tools'},
      { id: 'Cart', label: 'Panier', route: '/admin/AdminCart', icon: markRaw(ShoppingBagIcon), category: 'Catalogue' },
      { id: 'packs', label: 'Packs de contrat', route: '/admin/Adminpacks', icon : markRaw(SwatchIcon), category: 'Catalogue' },
      { id: 'calculator', label: 'Outil de calcul', route: '/admin/AdminCalcul', icon: markRaw(CalculatorIcon), category: 'Tools'}
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

@media (max-width: 728px) {
  .admin-main-content {
    margin-left: 0;
    margin-bottom: 80px;
    padding: 1rem;
  }
}
</style>