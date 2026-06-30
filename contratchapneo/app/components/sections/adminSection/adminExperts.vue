<template>
  <div class="experts-wrapper">
    
    <!-- EN-TÊTE & BARRE DE RECHERCHE -->
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Experts Juridiques</h3>
        <button class="btn-primary" @click="openAddModal">
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

    <!-- GRILLE DES PROFILS -->
    <div class="experts-grid">
      <div class="expert-card" v-for="expert in filteredExperts" :key="expert.id" :class="{'card-suspended': !expert.isActive}">
        
        <!-- Haut de la carte : Avatar & Statut -->
        <div class="card-header">
          <div class="status-indicator" :class="expert.isActive ? 'bg-green' : 'bg-red'" :title="expert.isActive ? 'Actif' : 'Suspendu'"></div>
          <button class="action-icon-btn delete-btn" title="Suspendre/Supprimer">
            <component :is="NoSymbolIcon" class="icon-sm" />
          </button>
        </div>

        <!-- Corps : Info de l'expert -->
        <div class="card-body">
          <div class="avatar-container">
            <img v-if="expert.avatar" :src="expert.avatar" alt="Avatar" class="avatar-img" />
            <div v-else class="avatar-placeholder" :class="getRoleColor(expert.role)">
              {{ getInitials(expert.name) }}
            </div>
            <!-- Badge Vérifié -->
            <div v-if="expert.isVerified" class="verified-badge" title="Profil vérifié">
              <component :is="CheckBadgeIcon" class="icon-xs text-blue" />
            </div>
          </div>
          
          <h4 class="expert-name">{{ expert.name }}</h4>
          <span class="expert-role">{{ expert.role }} &bull; {{ expert.specialty }}</span>
          
          <div class="rating-box">
            <component :is="StarIcon" class="icon-xs text-yellow" />
            <span class="dark-text font-bold text-sm">{{ expert.rating }}</span>
            <span class="gray-text text-xs">({{ expert.reviews }} avis)</span>
          </div>
        </div>

        <!-- Bas : Statistiques & Actions -->
        <div class="card-footer">
          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-val">{{ expert.contractsSold }}</span>
              <span class="stat-label">Contrats</span>
            </div>
            <div class="stat-item">
              <span class="stat-val">{{ expert.consultations }}</span>
              <span class="stat-label">Consultations</span>
            </div>
          </div>
          
          <div class="actions-row">
            <button class="btn-secondary-outline w-full" @click="viewProfile(expert)">Voir le profil</button>
            <button class="icon-btn-outline" title="Envoyer un email">
              <component :is="EnvelopeIcon" class="icon-sm" />
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Message si aucun résultat -->
    <div v-if="filteredExperts.length === 0" class="empty-state">
      <div class="icon-box-light bg-gray-light mb-3">
        <component :is="MagnifyingGlassIcon" class="icon-lg text-gray" />
      </div>
      <h4 class="dark-text">Aucun expert trouvé</h4>
      <p class="gray-text">Essayez de modifier vos termes de recherche ou vos filtres.</p>
    </div>

  </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import { 
  UserPlusIcon, 
  MagnifyingGlassIcon, 
  CheckBadgeIcon, 
  StarIcon, 
  EnvelopeIcon,
  NoSymbolIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminExperts',
  setup() {
    const searchQuery = ref('');
    const activeTab = ref('Tous');

    // Données factices contextualisées OHADA
    const experts = ref([
      { id: 1, name: 'Me. Bamba Souleymane', role: 'Avocat', specialty: 'Droit des Affaires', avatar: '', isVerified: true, isActive: true, rating: 4.8, reviews: 124, contractsSold: 45, consultations: 89 },
      { id: 2, name: 'Me. Sylla Awa', role: 'Notaire', specialty: 'Droit Immobilier', avatar: '', isVerified: true, isActive: true, rating: 4.9, reviews: 56, contractsSold: 12, consultations: 34 },
      { id: 3, name: 'Kouassi Jean', role: 'Juriste', specialty: 'Droit Social', avatar: '', isVerified: false, isActive: true, rating: 4.2, reviews: 18, contractsSold: 8, consultations: 15 },
      { id: 4, name: 'Me. Touré Fatou', role: 'Avocat', specialty: 'Droit Pénal des Affaires', avatar: '', isVerified: true, isActive: false, rating: 4.5, reviews: 92, contractsSold: 30, consultations: 41 },
    ]);

    // Filtrage dynamique selon la recherche et l'onglet actif
    const filteredExperts = computed(() => {
      return experts.value.filter(expert => {
        const matchesSearch = expert.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                              expert.specialty.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesTab = activeTab.value === 'Tous' || expert.role === activeTab.value;
        return matchesSearch && matchesTab;
      });
    });

    const getInitials = (name: string) => {
      const parts = name.replace('Me. ', '').split(' ');
      return parts.length > 1 ? parts[0][0] + parts[1][0] : parts[0][0];
    };

    const getRoleColor = (role: string) => {
      if (role === 'Avocat') return 'bg-blue-light text-blue';
      if (role === 'Notaire') return 'bg-purple-light text-purple';
      return 'bg-orange-light text-orange';
    };

    const openAddModal = () => console.log('Ouvrir modale ajout expert');
    const viewProfile = (expert: any) => console.log('Voir profil:', expert.name);

    return {
      searchQuery,
      activeTab,
      filteredExperts,
      getInitials,
      getRoleColor,
      openAddModal,
      viewProfile,
      UserPlusIcon, MagnifyingGlassIcon, CheckBadgeIcon, StarIcon, EnvelopeIcon, NoSymbolIcon
    };
  }
}
</script>

<style scoped>
/* ==============================================================
   VARIABLES & STRUCTURE
   ============================================================== */
.experts-wrapper {
  --bg-main: #f8fafc;
  --bg-panel: #ffffff;
  --bg-panel-light: #f1f5f9;
  --text-dark: #1e293b;
  --text-gray: #94a3b8;
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

/* UTILITAIRES */
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); }
.font-bold { font-weight: 700; }
.text-sm { font-size: 0.85rem; }
.text-xs { font-size: 0.75rem; }
.text-blue { color: #3b82f6; }
.text-purple { color: #a855f7; }
.text-orange { color: #f97316; }
.text-yellow { color: #eab308; fill: #eab308; }
.text-gray { color: #94a3b8; }
.bg-blue-light { background: #eff6ff; }
.bg-purple-light { background: #faf5ff; }
.bg-orange-light { background: #fff7ed; }
.bg-gray-light { background: #f1f5f9; }
.bg-green { background: #10b981; }
.bg-red { background: #ef4444; }
.mb-3 { margin-bottom: 1rem; }
.w-full { width: 100%; }

/* ICÔNES */
.icon-xs { width: 16px; height: 16px; }
.icon-sm { width: 20px; height: 20px; }
.icon-lg { width: 32px; height: 32px; }
.icon-gray { color: var(--text-gray); }

/* ==============================================================
   EN-TÊTE & FILTRES
   ============================================================== */
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

/* ONGLETS */
.tabs-group { display: flex; background: var(--bg-panel-light); border-radius: 50px; padding: 0.3rem; }
.tab-btn { background: transparent; border: none; color: var(--text-gray); font-size: 0.85rem; font-weight: 600; padding: 0.5rem 1.2rem; border-radius: 50px; cursor: pointer; transition: all 0.2s ease; }
.tab-btn.active { background: var(--bg-panel); color: var(--text-dark); box-shadow: 0px 2px 10px rgba(0,0,0,0.05); }

/* BOUTONS */
.btn-primary { background: var(--accent-blue); color: white; border: none; padding: 0.7rem 1.2rem; border-radius: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: 0.2s; }
.btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); }

.btn-secondary-outline { background: transparent; border: 1px solid #e2e8f0; color: var(--text-dark); padding: 0.6rem 1rem; border-radius: 10px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-secondary-outline:hover { background: #f8fafc; border-color: #cbd5e1; }

.icon-btn-outline { background: transparent; border: 1px solid #e2e8f0; color: var(--text-gray); padding: 0.6rem; border-radius: 10px; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; }
.icon-btn-outline:hover { background: #f8fafc; color: var(--text-dark); }

.action-icon-btn { background: transparent; border: none; color: #cbd5e1; cursor: pointer; transition: 0.2s; padding: 0.2rem; }
.delete-btn:hover { color: #ef4444; }

/* ==============================================================
   GRILLE DES EXPERTS
   ============================================================== */
.experts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }

.expert-card {
  background: var(--bg-panel); border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #f8fafc;
  display: flex; flex-direction: column; transition: 0.3s ease; position: relative;
}
.expert-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.06); }
.card-suspended { opacity: 0.7; filter: grayscale(30%); }

/* HAUT CARTE */
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.status-indicator { width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 3px rgba(255,255,255,0.8); }

/* CORPS CARTE (Avatar & Textes) */
.card-body { display: flex; flex-direction: column; align-items: center; text-align: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 1.2rem; margin-bottom: 1.2rem; }
.avatar-container { position: relative; width: 80px; height: 80px; margin-bottom: 1rem; }
.avatar-placeholder { width: 100%; height: 100%; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; letter-spacing: 1px; }
.avatar-img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
.verified-badge { position: absolute; bottom: 0; right: 0; background: white; border-radius: 50%; padding: 2px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

.expert-name { margin: 0 0 0.2rem 0; font-size: 1.1rem; font-weight: 700; color: var(--text-dark); }
.expert-role { font-size: 0.85rem; color: var(--text-gray); margin-bottom: 0.6rem; }

.rating-box { display: flex; align-items: center; justify-content: center; gap: 0.3rem; background: #fffbeb; padding: 0.3rem 0.8rem; border-radius: 50px; }

/* BAS CARTE (Stats & Boutons) */
.card-footer { display: flex; flex-direction: column; gap: 1rem; }
.stats-row { display: flex; justify-content: space-around; }
.stat-item { display: flex; flex-direction: column; align-items: center; }
.stat-val { font-size: 1.1rem; font-weight: 800; color: var(--text-dark); }
.stat-label { font-size: 0.7rem; color: var(--text-gray); text-transform: uppercase; letter-spacing: 0.5px; }

.actions-row { display: flex; gap: 0.5rem; }

/* EMPTY STATE */
.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; background: var(--bg-panel); border-radius: 24px; text-align: center; border: 1px dashed #cbd5e1; }
.icon-box-light { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

/* RESPONSIVE */
@media (max-width: 640px) {
  .title-row { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .btn-primary { width: 100%; justify-content: center; }
  .search-box { max-width: 100%; }
  .tabs-group { width: 100%; overflow-x: auto; }
}
</style>