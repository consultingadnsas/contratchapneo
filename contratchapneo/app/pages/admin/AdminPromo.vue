<template>
  <div class="admin-page-container">
    
    <AdminSidebar 
      :menuItems="adminMenu" 
      @logout="handleLogout" 
    />    
    <main class="admin-content">
      <AdminCouponSection />
    </main>

  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ref, markRaw } from 'vue';
import { useRouter } from 'vue-router';
import AdminSidebar, {MenuItem} from '../../components/navigation/adminSidebar.vue';
import AdminCouponSection from '../../components/sections/adminSection/AdminCoupon.vue';
import { HomeIcon, BanknotesIcon, UsersIcon, BookOpenIcon, InboxIcon, DocumentTextIcon, Cog8ToothIcon, TrashIcon, ShoppingBagIcon, SwatchIcon, GiftTopIcon } from '@heroicons/vue/24/outline';

export default defineComponent({
  name: 'AdminCouponsPage',
  components: {
    AdminSidebar,
    AdminCouponSection
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
      { id: 'settings', label: 'Paramètres', route: '/admin/AdminSettings', icon: markRaw(Cog8ToothIcon), category: 'Tools' },
      { id: 'trash', label: 'Corbeille', route: '/admin/AdminTrash', icon: markRaw(TrashIcon), category: 'Tools' },
      { id: 'Cart', label: 'Panier', route: '/admin/AdminCart', icon: markRaw(ShoppingBagIcon), category: 'Catalogue' },
      { id: 'packs', label: 'Packs de contrat', route: '/admin/Adminpacks', icon : markRaw(SwatchIcon), category: 'Catalogue' },
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
});
</script>

<style scoped>
.admin-page-container {
  min-height: 100vh;
  background-color: #f8fafc;
  display: flex;
}

.admin-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>