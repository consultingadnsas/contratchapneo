<template>
  <div class="experts-wrapper">
    
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Experts Juridiques</h3>
        
        <!-- ⚡️ NOUVEAU : Groupe de boutons -->
        <div class="header-buttons">
          <button class="btn-secondary-custom" @click="openCountryModal()">
            <component :is="GlobeAltIcon" class="icon-sm" /> Gérer les pays ({{ countriesList.length }})
          </button>

          <button class="btn-secondary-custom" @click="openDomainModal()">
            <component :is="BriefcaseIcon" class="icon-sm" /> Gérer les domaines ({{ domainsList.length }})
          </button>
          
          <button class="btn-primary-custom" @click="openModal()">
            <component :is="UserPlusIcon" class="icon-sm" /> Ajouter un expert
          </button>
        </div>
      </div>

      <div class="filters-row">
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-gray icon-sm" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher par nom, spécialité..." />
        </div>
        
        <div class="filters-row">      
        <div class="domain-filter-box">
          <select v-model="activeDomainFilter" class="custom-filter-select">
            <option value="Tous">Tous les domaines</option>
            <option v-for="domain in domainsList" :key="domain.id" :value="domain.id">
              {{ domain.name }}
            </option>
          </select>
        </div>
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

    <!-- Modale Expert -->
    <ExpertModal 
      v-if="isModalOpen"
      :expert="selectedExpert"
      :domains="domainsList"
      :countries="countriesList"
      @close="closeModal"
      @save="saveExpert"
    />

    <!-- ⚡️ Modale Gestion des Pays -->
    <CountryModal 
      v-if="isCountryModalOpen" 
      @close="closeCountryModal" 
    />

    <!-- ⚡️ Modale Gestion des Domaines -->
    <DomainModal 
      v-if="isDomainModalOpen" 
      @close="closeDomainModal" 
    />

  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw, onMounted } from 'vue';
import ExpertModal from '../../modale/expertModal.vue';
import CountryModal from '../../modale/countryModal.vue';
import DomainModal from '../../modale/domainModal.vue';
import { useAdminProStore } from '../../../stores/adminProStore'; 
import { 
  UserPlusIcon, 
  MagnifyingGlassIcon, 
  CheckBadgeIcon, 
  TrashIcon, 
  BriefcaseIcon,
  PencilSquareIcon,
  GlobeAltIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminExperts',
  components: { ExpertModal, CountryModal, DomainModal },
  setup() {
    const adminProStore = useAdminProStore();
    
    const searchQuery = ref('');
    const activeDomainFilter = ref('Tous');

    const experts = computed(() => {
      return adminProStore.pros.map(pro => ({
        id: pro.id,
        name: `${pro.first_name || ''} ${pro.last_name || ''}`.trim(),
        roleDisplay: pro.title_display || pro.title || 'Expert',
        role: pro.title,
        email: pro.email,
        phone_number: pro.phone_number,
        city: pro.city,
        
        // ⚡️ LES 3 LIGNES MANQUANTES SONT ICI :
        country: pro.country, 
        years_of_experience: pro.years_of_experience,
        domains: pro.domains,
        
        bio: pro.bio,
        specialty: pro.domains && pro.domains.length > 0 ? pro.domains.map((d: any) => d.name).join(', ') : 'Généraliste',
        avatar: pro.profile_picture,
        visiting_card: pro.visiting_card,
        isVerified: pro.is_verified,
        isActive: pro.is_active,
        consultations: pro.consultations ?? pro.downloads_count ?? 0
      }));
    });

    const filteredExperts = computed(() => {
      return experts.value.filter(expert => {
        // Recherche textuelle
        const matchesSearch = expert.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                              expert.specialty.toLowerCase().includes(searchQuery.value.toLowerCase());
        
        // ⚡️ Filtrage strict par ID de domaine
        const matchesDomain = activeDomainFilter.value === 'Tous' || 
                              (expert.domains && expert.domains.some((d: any) => d.id === activeDomainFilter.value));
        
        return matchesSearch && matchesDomain;
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

    const isModalOpen = ref(false);
    const selectedExpert = ref<any>(null);

    const openModal = (expert: any = null) => {
      selectedExpert.value = expert && expert.id ? { ...expert } : null;
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
      
      // ⚡️ CORRECTION 1 : Le Pays
      if (expertData.country) {
          formData.append('country', expertData.country);
      }
      
      // ⚡️ CORRECTION 2 : Les années d'expérience
      if (expertData.years_of_experience !== undefined) {
          formData.append('years_of_experience', expertData.years_of_experience.toString());
      }

      // ⚡️ CORRECTION 3 : La boucle indispensable pour les domaines (ManyToMany)
      if (expertData.domains && expertData.domains.length > 0) {
          expertData.domains.forEach((domainId: string | number) => {
              formData.append('domains', domainId.toString());
          });
      }
      
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
        alert(adminProStore.error || "Une erreur est survenue lors de l'enregistrement.");
      }
    };

    const deleteExpert = async (id: string) => {
      if (confirm('Supprimer définitivement cet expert ?')) {
        try {
          await adminProStore.deletePro(id);
        } catch(e) {
          alert(adminProStore.error || "Impossible de supprimer l'expert.");
        }
      }
    };

    // ⚡️ Gestion des modales Pays & Domaines
    const isCountryModalOpen = ref(false);
    const openCountryModal = () => { isCountryModalOpen.value = true; };
    const closeCountryModal = () => { isCountryModalOpen.value = false; };

    const isDomainModalOpen = ref(false);
    const openDomainModal = () => { isDomainModalOpen.value = true; };
    const closeDomainModal = () => { isDomainModalOpen.value = false; };

    onMounted(async () => {
      await adminProStore.fetchCountries(); // Charge les pays
      await adminProStore.fetchPros();      // Charge les experts
      await adminProStore.fetchDomains();   // Charge les domaines
    });

    return {
      searchQuery,
      activeDomainFilter,
      filteredExperts,
      getInitials,
      getRoleColor,
      isModalOpen,
      selectedExpert,
      openModal,
      closeModal,
      saveExpert,
      deleteExpert,
      isCountryModalOpen,
      openCountryModal,
      closeCountryModal,
      isDomainModalOpen,
      openDomainModal,
      closeDomainModal,
      countriesList: computed(() => adminProStore.countries),
      domainsList: computed(() => adminProStore.domains),
      isLoading: computed(() => adminProStore.isLoading),
      UserPlusIcon: markRaw(UserPlusIcon), 
      MagnifyingGlassIcon: markRaw(MagnifyingGlassIcon), 
      CheckBadgeIcon: markRaw(CheckBadgeIcon),
      TrashIcon: markRaw(TrashIcon),
      PencilSquareIcon: markRaw(PencilSquareIcon),
      GlobeAltIcon: markRaw(GlobeAltIcon),
      BriefcaseIcon: markRaw(BriefcaseIcon)
    };
  }
}
</script>

<style scoped>
/* Styles existants... */
.experts-wrapper { --bg-panel: #ffffff; --bg-panel-light: #f1f5f9; --text-dark: #1e293b; --text-gray: #94a3b8; --accent-blue: #2563eb; display: flex; flex-direction: column; gap: 2rem; font-family: 'Inter', sans-serif; padding-bottom: 2rem; }
.dark-text { color: var(--text-dark); } .gray-text { color: var(--text-gray); } .font-bold { font-weight: 700; } .text-sm { font-size: 0.85rem; } .text-xs { font-size: 0.75rem; } .text-blue { color: #3b82f6; } .text-purple { color: #a855f7; } .text-orange { color: #f97316; } .bg-blue-light { background: #eff6ff; } .bg-purple-light { background: #faf5ff; } .bg-orange-light { background: #fff7ed; } .bg-gray-light { background: #f1f5f9; } .bg-green { background: #10b981; } .bg-red { background: #ef4444; } .mb-3 { margin-bottom: 1rem; } .mt-3 { margin-top: 1rem; } .w-full { width: 100%; } .icon-xs { width: 16px; height: 16px; } .icon-sm { width: 20px; height: 20px; } .icon-lg { width: 32px; height: 32px; } .icon-gray { color: var(--text-gray); }
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-row { display: flex; justify-content: space-between; align-items: center; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 700; margin: 0; }
.filters-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.search-box { display: flex; align-items: center; gap: 0.5rem; background: var(--bg-panel); border: 1px solid #e2e8f0; padding: 0.6rem 1rem; border-radius: 50px; width: 100%; max-width: 350px; transition: 0.2s; }
.search-box:focus-within { border-color: var(--accent-blue); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.search-box input { border: none; outline: none; background: transparent; width: 100%; font-size: 0.9rem; color: var(--text-dark); }

/* ⚡️ NOUVEAU : Header Buttons */
.header-buttons { display: flex; gap: 1rem; }
.btn-primary-custom { background: var(--primary-color-dark); color: #ffffff; font-weight: 600; border-radius: 999px; padding: 10px 20px; font-size: 0.95rem; border: none; transition: background 0.2s ease; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.btn-primary-custom:hover { background: #1f2937; }
.btn-secondary-custom { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; font-weight: 600; border-radius: 999px; padding: 10px 20px; font-size: 0.95rem; transition: 0.2s ease; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
.btn-secondary-custom:hover { background: #e2e8f0; color: #0f172a; }

.experts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
.expert-card { background: var(--bg-panel); border-radius: 24px; padding: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #f8fafc; display: flex; flex-direction: column; transition: 0.3s ease; position: relative; }
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
.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; background: var(--bg-panel); border-radius: 24px; text-align: center; border: 1px dashed #cbd5e1; }
.icon-box-light { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

.domain-filter-box {
  min-width: 220px;
}
.custom-filter-select {
  width: 100%;
  padding: 0.6rem 1.2rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-dark);
  background-color: var(--bg-panel);
  border: 1px solid #e2e8f0;
  border-radius: 50px;
  cursor: pointer;
  outline: none;
  transition: 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.2em;
  padding-right: 2.5rem;
}
.custom-filter-select:focus {
  border-color: var(--accent-blue);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

@media (max-width: 640px) {
  .title-row { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .header-buttons { width: 100%; flex-direction: column; gap: 0.8rem; }
  .btn-primary-custom, .btn-secondary-custom { width: 100%; justify-content: center; }
  .search-box { max-width: 100%; }
}
</style>