<template>

  <div class="dashboard-container">

    <sidebar />

    <main class="main-content">
        
      <header class="dashboard-header">
      
        <div v-if="authStore.user">
          <h1 class="greeting">Bonjour, {{ authStore.displayName }}</h1>
        </div>
    
        <div v-else>
            <p>Chargement...</p>
        </div>
        
        <dashboard-btn/>

      </header>
        
      <div class="dashboard-grid">
        
        <!-- ⚡️ AJOUT : La barre de recherche -->
        <div class="search-section">
          <dashBoardInput placeholder="Rechercher un contrat dans votre pack..." />
        </div>

        <user-contrat-section/>

      </div>

    </main>

  </div>

</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import {useAuthStore} from '../../stores/authStore'

import sidebar from '../../components/navigation/sidebar.vue'; 
import cardSection from '../../components/sections/bankContratSections/cardSection.vue'
import mainButton from '../../components/buttons/secondButton.vue';
import dashboardBtn from '../../components/buttons/dashboardBtn.vue'
import profileSection from '../../components/sections/userSection/profileSection.vue'
import userContratSection from '../../components/sections/userSection/userContratSection.vue'
// ⚡️ AJOUT : Import de la barre de recherche (Ajustez le chemin si nécessaire)
import dashBoardInput from '../../components/input/dashBoardInput.vue' 

export default {
  name: 'DashboardLayout',
  components: {
    sidebar,
    cardSection,
    mainButton,
    profileSection,
    dashboardBtn,
    userContratSection,
    dashBoardInput // ⚡️ AJOUT
  },
  setup() {

    const authStore = useAuthStore();

    onMounted(()=> {
      authStore.getProfile();
    })

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
  height: 100vh;
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
   CONTENU PRINCIPAL (ZONE BLANCHE)
========================================= */
.main-content {
  flex: 1;
  min-width: 0; 
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
  padding: 0.5rem;
  overflow-y: auto;
  overflow-x: hidden;
  box-sizing: border-box;
}

@media (min-width: 1024px) {
  .main-content {
    padding: 2.5rem;
  }
}

/* ⚡️ AJOUT : Style pour la section de recherche */
.search-section {
  width: 100%;
  max-width: 800px; /* Limite la largeur pour que ce soit élégant sur PC */
  margin: 0 auto 2rem auto;
}

/* ... (Le reste de vos styles existants reste inchangé) ... */
.mobile-menu-btn {
  background: none;
  border: none;
  color: var(--text-night);
  margin-bottom: 1rem;
  cursor: pointer;
}
.d-lg-none {
  display: block;
}
@media (min-width: 1024px) {
  .d-lg-none {
    display: none;
  }
}

.dashboard-header { 
  display: flex; 
  flex-direction: column; 
  gap: 1rem; 
}
.greeting { 
  font-size: 1.8rem; 
  font-weight: 700; 
  color: var(--text-night); 
  margin-bottom: 0.25rem; 
}
.primary-btn { 
  background-color: var(--text-night); 
  color: white; 
  border: none; 
  padding: 0.75rem 1.5rem; 
  border-radius: 8px; 
  font-weight: 500; 
  cursor: pointer; 
  align-self: flex-start; 
}

.dashboard-grid {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  display: flex;           
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  height: 100%;
}

@media (min-width: 1024px) {
  .dashboard-header { 
    flex-direction: row; 
    justify-content: space-between; 
    align-items: center; 
  }
  .primary-btn { 
    align-self: center; 
  }
  .dashboard-grid { 
    /* grid-template-columns retiré car vous voulez tout empiler proprement */
    gap: 2rem; 
  }
}
</style>