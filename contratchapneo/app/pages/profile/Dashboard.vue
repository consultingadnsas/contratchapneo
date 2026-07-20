<template>
  
  <div class="dashboard-container">
    
    <sidebar />
    
    <main class="main-content">
      
      <header class="dashboard-header">
        
        <div v-if="authStore.user">
          <h1 class="greeting">Bonjour, {{ authStore.user.user?.username ?? 'invité' }}</h1>
          <p class="subtitle">Voici un résumé de votre activité juridique.</p>
        </div>
        
        <div v-else>
          <p>Chargement...</p>
        </div>
        
        <dashboard-btn/>

      </header>
      
      <div class="dashboard-grid">

        <profile-section/>

      </div>

    </main>
    
  </div>

</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import sidebar from '../../components/navigation/sidebar.vue'; 
import cardSection from '../../components/sections/bankContratSections/cardSection.vue'
import mainButton from '../../components/buttons/secondButton.vue';
import dashboardBtn from '../../components/buttons/dashboardBtn.vue'
import profileSection from '../../components/sections/userSection/profileSection.vue'
import BaseResearchInput from '../../components/input/BaseResearchInput.vue'
import {useAuthStore} from '../../stores/authStore'

export default {
  name: 'DashboardLayout',
  components: {
    sidebar,
    cardSection,
    mainButton,
    profileSection,
    dashboardBtn,
    BaseResearchInput
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
  
  /* C'EST ICI LA MAGIE : On met flex en colonne pour le mobile... */
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--bg-pearl);
  color: var(--text-night);
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden; 
}

/* ... ET ON PASSE EN LIGNE (CÔTE À CÔTE) SUR PC ! */
@media (min-width: 1024px) {
  .dashboard-container {
    flex-direction: row;
  }
}

/* =========================================
   CONTENU PRINCIPAL (ZONE BLANCHE)
========================================= */
.main-content {
  flex: 1; /* Prend toute la place restante à côté de la sidebar */
  padding: 0.5rem;
  overflow-y: auto; 
  overflow-x: hidden; 
}

@media (min-width: 1024px) {
  .main-content {
    padding: 2.5rem;
  }
}

/* Bouton menu temporaire sur mobile */
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

/* =========================================
   LE RESTE DU DESIGN (Header, Widgets, etc.)
========================================= */
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
.subtitle { 
  color: var(--text-muted); 
  font-size: 1rem; 
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
  display: grid; 
  grid-template-columns: 1fr; 
  gap: 1.5rem; 
  width: 100%; 
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
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
    grid-template-columns: 2fr 1fr; 
    gap: 2rem; 
  }
}

.left-column, .right-column { 
  display: flex; 
  flex-direction: column; 
  gap: 1.5rem; 
}

.glass-widget {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
}

.section-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 1.5rem; 
  padding-bottom: 0.75rem; 
  border-bottom: 1px solid rgba(15, 23, 42, 0.06); 
}
.title-wrapper { display: flex; align-items: center; gap: 0.75rem; }
.section-header h2 { font-size: 1.15rem; font-weight: 600; margin: 0; }

.status-badge { font-size: 0.7rem; font-weight: 600; color: #3b82f6; background: rgba(59, 130, 246, 0.1); padding: 0.2rem 0.6rem; border-radius: 50px; }
.notification-dot { background: #ef4444; color: white; font-size: 0.75rem; font-weight: 700; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

.list-layout { display: flex; flex-direction: column; gap: 1rem; }
.contract-item, .action-item { display: flex; align-items: center; gap: 1rem; padding: 0.75rem; border-radius: 12px; background: rgba(255, 255, 255, 0.5); }
.action-item { justify-content: space-between; border-bottom: 1px solid rgba(15, 23, 42, 0.05); padding-bottom: 0.75rem; background: none; border-radius: 0; }
.contract-details h3, .action-text h4 { font-size: 0.95rem; font-weight: 600; margin: 0 0 0.2rem 0; }
.contract-details p, .action-text p { font-size: 0.8rem; color: var(--text-muted); margin: 0; }
.badge-draft { background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 50px; }
.action-btn { background: white; border: 1px solid rgba(15, 23, 42, 0.1); color: var(--text-night); padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.8rem; cursor: pointer; }
</style>