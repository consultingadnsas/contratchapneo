<template>
  <div class="dashboard-container">
    
    <sidebar />
    
    <main class="main-content">
      
      <header class="dashboard-header">
        <div v-if="authStore.user">
          <h1 class="greeting">Bonjour, {{ authStore.user.user?.username ?? 'invité' }}</h1>
        </div>
        <div v-else>
          <p>Chargement...</p>
        </div>       
        <dashboard-btn/>
      </header>
      
      <div class="dashboard-grid">
        <!-- Ta section profil complètement gérée ici -->
        <profile-section/>
      </div>

    </main>
    
  </div>
</template>

<script lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from '../../stores/authStore'

// ⚡️ CORRECTION : J'ai nettoyé les imports inutilisés (cardSection, BaseResearchInput, etc.)
import sidebar from '../../components/navigation/sidebar.vue'; 
import dashboardBtn from '../../components/buttons/dashboardBtn.vue';
import profileSection from '../../components/sections/userSection/profileSection.vue';

export default {
  name: 'DashboardLayout',
  components: {
    sidebar,
    profileSection,
    dashboardBtn
  },
  setup() {
    const authStore = useAuthStore();

    onMounted(() => {
      authStore.getProfile();
    });

    return {
      authStore
    };
  }
};
</script>

<style scoped>
/* =========================================
  STRUCTURE GLOBALE DU DASHBOARD
========================================= */
.dashboard-container {
  --bg-pearl: #f8fafc;        
  --text-night: #0f172a;      
  --text-muted: #64748b;      
  
  display: flex;
  flex-direction: column;
  /* ⚡️ CORRECTION : 100dvh s'adapte à la vraie taille de l'écran mobile */
  height: 100dvh; 
  background-color: var(--bg-pearl);
  color: var(--text-night);
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden; 
}

@media (min-width: 1024px) {
  .dashboard-container {
    flex-direction: row;
  }
}

/* =========================================
   CONTENU PRINCIPAL (ZONE DE SCROLL)
========================================= */
.main-content {
  flex: 1; 
  padding: 1rem;
  /* ⚡️ CORRECTION CRUCIALE : Ajoute de l'espace en bas pour que la sidebar mobile ne cache pas les cartes */
  padding-bottom: 85px; 
  overflow-y: auto; 
  overflow-x: hidden; 
}

@media (min-width: 1024px) {
  .main-content {
    padding: 2.5rem;
    /* Sur PC, la sidebar est à gauche, donc on retire le padding en bas */
    padding-bottom: 2.5rem; 
  }
}

/* =========================================
   HEADER ET CONTENU
========================================= */
.dashboard-header { 
  display: flex; 
  flex-direction: row; 
  justify-content: space-between;
}

.greeting { 
  font-size: 1.8rem; 
  font-weight: 700; 
  color: var(--text-night); 
  margin-bottom: 0.25rem; 
}

.subtitle { 
  color: var(--text-muted); 
  font-size: 1rem; 
}

.dashboard-grid { 
  display: block; 
  width: 100%; 
  margin-top: 1.5rem; 
}

@media (min-width: 1024px) {
  .dashboard-header { 
    display: flex;
    flex-direction: row; 
    justify-content: space-between; 
    align-items: center; 
  }
  
  /* ⚡️ CORRECTION : J'ai retiré le display: grid erroné qui cassait ton design. 
     Ta profileSection gère déjà sa propre grille ! */
  .dashboard-grid { 
    margin-top: 2rem; 
  }
}
</style>