<template>
  <div class="experts-wrapper">
    
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Experts Juridiques</h3>
        
        <button class="btn-primary-custom" @click="openModal()">
          <component :is="UserPlusIcon" class="icon-sm" /> Ajouter un expert
        </button>
      </div>

      <div class="filters-row">
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-gray icon-sm" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher par nom, spécialité..." />
        </div>
        
        <div class="tabs-group">
          <button class="tab-btn" :class="{ active: activeTab === 'Tous' }" @click="activeTab = 'Tous'">Tous</button>
          <button class="tab-btn" :class="{ active: activeTab === 'Avocat' }" @click="activeTab = 'Avocat'">Avocats</button>
          <button class="tab-btn" :class="{ active: activeTab === 'Notaire' }" @click="activeTab = 'Notaire'">Notaires</button>
          <button class="tab-btn" :class="{ active: activeTab === 'Juriste' }" @click="activeTab = 'Juriste'">Juristes</button>
        </div>
      </div>
    </div>

    <div class="experts-grid">
      <div class="expert-card" v-for="expert in filteredExperts" :key="expert.id" :class="{'card-suspended': !expert.isActive}">
        
        <div class="card-header">
          <div class="status-indicator" :class="expert.isActive ? 'bg-green' : 'bg-red'" :title="expert.isActive ? 'Actif' : 'Inactif'"></div>
          <div class="actions-group-top">
            <button class="action-icon-btn edit-btn" title="Modifier" @click="openModal(expert)">
               <component :is="PencilSquareIcon" class="icon-sm" />
            </button>
            <button class="action-icon-btn delete-btn" title="Supprimer" @click="deleteExpert(expert.id)">
              <component :is="TrashIcon" class="icon-sm" />
            </button>
          </div>
        </div>

        <div class="card-body">
          <div class="avatar-container">
            <img v-if="expert.avatar" :src="expert.avatar" alt="Avatar" class="avatar-img" />
            <div v-else class="avatar-placeholder" :class="getRoleColor(expert.role)">
              {{ getInitials(expert.name) }}
            </div>
            <div v-if="expert.isVerified" class="verified-badge" title="Profil vérifié">
              <component :is="CheckBadgeIcon" class="icon-xs text-blue" />
            </div>
          </div>
          
          <h4 class="expert-name">{{ expert.name }}</h4>
          <span class="expert-role">{{ expert.roleDisplay }} &bull; {{ expert.specialty }}</span>
        </div>

        <div class="card-footer">
          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-val">{{ expert.consultations }}</span>
              <span class="stat-label">Consultations</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div v-if="filteredExperts.length === 0" class="empty-state">
      <div class="icon-box-light bg-gray-light mb-3">
        <component :is="MagnifyingGlassIcon" class="icon-lg text-gray" />
      </div>
      <h4 class="dark-text">Aucun expert trouvé</h4>
      <p class="gray-text">Essayez de modifier vos termes de recherche ou vos filtres.</p>
    </div>

    <ExpertModal 
      v-if="isModalOpen"
      :expert="selectedExpert"
      @close="closeModal"
      @save="saveExpert"
    />

  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw, onMounted } from 'vue';
import ExpertModal from '../../modale/expertModal.vue';
import secondButton from '../../buttons/secondButton.vue';
import { useAdminProStore } from '../../../stores/adminProStore'; 
import { 
  UserPlusIcon, 
  MagnifyingGlassIcon, 
  CheckBadgeIcon, 
  TrashIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminExperts',
  components: { ExpertModal, secondButton },
  setup() {
    const adminProStore = useAdminProStore();
    
    const searchQuery = ref('');
    const activeTab = ref('Tous');

    // Mappage complet des données pour l'affichage ET la modale
    const experts = computed(() => {
      return adminProStore.pros.map(pro => ({
        id: pro.id,
        name: `${pro.first_name || ''} ${pro.last_name || ''}`.trim(),
        roleDisplay: pro.title_display || pro.title || 'Expert',
        role: pro.title,
        email: pro.email,
        phone_number: pro.phone_number,
        city: pro.city,
        bio: pro.bio,
        specialty: pro.domains && pro.domains.length > 0 ? pro.domains.map((d: any) => d.name).join(', ') : 'Généraliste',
        avatar: pro.profile_picture,
        visiting_card: pro.visiting_card,
        isVerified: pro.is_verified,
        isActive: pro.is_active,
        consultations: 0
      }));
    });

    const filteredExperts = computed(() => {
      return experts.value.filter(expert => {
        const matchesSearch = expert.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                              expert.specialty.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesTab = activeTab.value === 'Tous' || expert.roleDisplay.toLowerCase().includes(activeTab.value.toLowerCase());
        return matchesSearch && matchesTab;
      });
    });

    const getInitials = (name: string) => {
      const cleanName = name.replace(/^(Me\.|Dr\.|Maître)\s+/i, '').trim();
      const parts = cleanName.split(' ');
      return parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : parts[0][0].toUpperCase();
    };

    const getRoleColor = (role: string) => {
      if (!role) return 'bg-gray-light text-gray';
      const roleLower = role.toLowerCase();
      if (roleLower.includes('avocat')) return 'bg-blue-light text-blue';
      if (roleLower.includes('notaire')) return 'bg-purple-light text-purple';
      return 'bg-orange-light text-orange';
    };

    // --- CRUD LOGIQUE ---
    const isModalOpen = ref(false);
    const selectedExpert = ref<any>(null);

    // ⚡️ Ultra-simple : on prend l'expert tel quel ou on vide
    const openModal = (expert: any = null) => {
      if (expert && expert.id) {
        selectedExpert.value = { ...expert }; 
      } else {
        selectedExpert.value = null;
      }
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
      selectedExpert.value = null;
    };

    const saveExpert = async (expertData: any) => {
      const nameParts = expertData.name.trim().split(' ');
      const firstName = nameParts.shift() || 'Prénom';
      const lastName = nameParts.join(' ') || 'Nom'; 

      const formData = new FormData();
      formData.append('first_name', firstName);
      formData.append('last_name', lastName);
      formData.append('title', expertData.role);
      
      if (expertData.email) formData.append('email', expertData.email);
      if (expertData.phone_number) formData.append('phone_number', expertData.phone_number);
      if (expertData.city) formData.append('city', expertData.city);
      if (expertData.bio) formData.append('bio', expertData.bio);
      
      formData.append('is_active', expertData.isActive ? 'true' : 'false');
      formData.append('is_verified', expertData.isVerified ? 'true' : 'false');

      if (expertData.avatarFile) formData.append('profile_picture', expertData.avatarFile);
      if (expertData.visitingCardFile) formData.append('visiting_card', expertData.visitingCardFile);

      try {
        if (expertData.id) {
          await adminProStore.updatePro(expertData.id, formData);
        } else {
          await adminProStore.addPro(formData);
        }
        closeModal();
      } catch (e: any) {
        alert(adminProStore.error || "Une erreur est survenue lors de l'enregistrement. Vérifiez que tous les champs sont valides.");
      }
    };

    const deleteExpert = async (id: string) => {
      if (confirm('Supprimer définitivement cet expert ? Cette action est irréversible.')) {
        try {
          await adminProStore.deletePro(id);
        } catch(e) {
          alert(adminProStore.error || "Impossible de supprimer l'expert.");
        }
      }
    };

    const viewProfile = (expert: any) => console.log('Voir profil complet:', expert.name);

    onMounted(async () => {
      await adminProStore.fetchPros(); 
    });

    return {
      searchQuery,
      activeTab,
      filteredExperts,
      getInitials,
      getRoleColor,
      isModalOpen,
      selectedExpert,
      openModal,
      closeModal,
      saveExpert,
      deleteExpert,
      viewProfile,
      isLoading: computed(() => adminProStore.isLoading),
      UserPlusIcon: markRaw(UserPlusIcon), 
      MagnifyingGlassIcon: markRaw(MagnifyingGlassIcon), 
      CheckBadgeIcon: markRaw(CheckBadgeIcon),
      TrashIcon: markRaw(TrashIcon),
      PencilSquareIcon: markRaw(PencilSquareIcon)
    };
  }
}
</script>

<style scoped>
/* Conservez exactement vos styles existants... */
.experts-wrapper {
  --bg-panel: #ffffff;
  --bg-panel-light: #f1f5f9;
  --text-dark: #1e293b;
  --text-gray: #94a3b8;
  --accent-blue: #2563eb;
  display: flex; flex-direction: column; gap: 2rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); }
.font-bold { font-weight: 700; }
.text-sm { font-size: 0.85rem; }
.text-xs { font-size: 0.75rem; }
.text-blue { color: #3b82f6; }
.text-purple { color: #a855f7; }
.text-orange { color: #f97316; }
.bg-blue-light { background: #eff6ff; }
.bg-purple-light { background: #faf5ff; }
.bg-orange-light { background: #fff7ed; }
.bg-gray-light { background: #f1f5f9; }
.bg-green { background: #10b981; }
.bg-red { background: #ef4444; }
.mb-3 { margin-bottom: 1rem; }
.mt-3 { margin-top: 1rem; }
.w-full { width: 100%; }

.icon-xs { width: 16px; height: 16px; }
.icon-sm { width: 20px; height: 20px; }
.icon-lg { width: 32px; height: 32px; }
.icon-gray { color: var(--text-gray); }

.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-row { display: flex; justify-content: space-between; align-items: center; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 700; margin: 0; }

.filters-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }

.search-box {
  display: flex; align-items: center; gap: 0.5rem;
  background: var(--bg-panel); border: 1px solid #e2e8f0;
  padding: 0.6rem 1rem; border-radius: 50px; width: 100%; max-width: 350px;
  transition: 0.2s;
}
.search-box:focus-within { border-color: var(--accent-blue); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.search-box input { border: none; outline: none; background: transparent; width: 100%; font-size: 0.9rem; color: var(--text-dark); }

.tabs-group { display: flex; background: var(--primary-color); border-radius: 50px; padding: 0.3rem; }
.tab-btn { background: transparent; border: none; color: #ffffff; font-size: 0.85rem; font-weight: 600; padding: 0.5rem 1.2rem; border-radius: 50px; cursor: pointer; transition: all 0.2s ease; }
.tab-btn.active { background: var(--secondary-light-color); color: #ffffff; box-shadow: 0px 2px 10px rgba(0,0,0,0.05); }

.btn-primary-custom { 
  background: var(--primary-color-dark); color: #ffffff; font-weight: 600; 
  border-radius: 999px; padding: 12px 24px; font-size: 1rem; 
  border: none; transition: background 0.2s ease; 
  display: flex; align-items: center; gap: 0.5rem; cursor: pointer;
}
.btn-primary-custom:hover { background: #1f2937; }

.experts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }

.expert-card {
  background: var(--bg-panel); border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #f8fafc;
  display: flex; flex-direction: column; transition: 0.3s ease; position: relative;
}
.expert-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }
.card-suspended { opacity: 0.7; filter: grayscale(30%); }

.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.status-indicator { width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 3px rgba(255,255,255,0.8); }
.actions-group-top { display: flex; gap: 0.4rem; }
.action-icon-btn { background: transparent; border: none; color: #cbd5e1; cursor: pointer; transition: 0.2s; padding: 0.2rem; }
.action-icon-btn:hover { color: var(--text-dark); }
.delete-btn:hover { color: #ef4444; }

.card-body { display: flex; flex-direction: column; align-items: center; text-align: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 1.2rem; margin-bottom: 1.2rem; }
.avatar-container { position: relative; width: 80px; height: 80px; margin-bottom: 1rem; }
.avatar-placeholder { width: 100%; height: 100%; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; letter-spacing: 1px; }
.avatar-img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
.verified-badge { position: absolute; bottom: 0; right: 0; background: white; border-radius: 50%; padding: 2px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

.expert-name { margin: 0 0 0.2rem 0; font-size: 1.1rem; font-weight: 700; color: var(--text-dark); }
.expert-role { font-size: 0.85rem; color: var(--text-gray); }

.card-footer { display: flex; flex-direction: column; gap: 1rem; }
.stats-row { display: flex; justify-content: space-around; }
.stat-item { display: flex; flex-direction: column; align-items: center; }
.stat-val { font-size: 1.1rem; font-weight: 800; color: var(--text-dark); }
.stat-label { font-size: 0.7rem; color: var(--text-gray); text-transform: uppercase; letter-spacing: 0.5px; }

.actions-row { display: flex; width: 100%; }

.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; background: var(--bg-panel); border-radius: 24px; text-align: center; border: 1px dashed #cbd5e1; }
.icon-box-light { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

@media (max-width: 640px) {
  .title-row { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .btn-primary-custom { width: 100%; justify-content: center; }
  .search-box { max-width: 100%; }
  .tabs-group { width: 100%; overflow-x: auto; }
}
</style>