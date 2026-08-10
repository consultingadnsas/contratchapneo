<template>
  <aside class="sidebar" :class="{ 'is-reduced': isReduced }">
    <div class="logo hidden-mobile">
      <span class="logo-text" v-if="!isReduced">ContratChap</span>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="toggle-icon" @click="toggleReduce">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
      </svg>
    </div>

    <nav class="nav-menu">
      <template v-for="(group, category) in groupedMenu" :key="category">
        <div class="menu-category hidden-mobile" v-if="!isReduced">{{ category }}</div>
        
        <button 
          v-for="item in group" 
          :key="item.id"
          class="nav-item" 
          :class="{ 'active': route.path === item.route }"
          @click="navigate(item.route)"
        >
          <component :is="item.icon" class="icon" />
          <span class="nav-label" v-if="!isReduced">{{ item.label }}</span>
        </button>
      </template>

      <div class="logout">
        <button class="nav-item btn-logout" @click="$emit('logout')">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
          </svg>
          <span class="nav-label" v-if="!isReduced">Se déconnecter</span>
        </button>
      </div>
    </nav>
  </aside>
</template>

<script lang="ts">
import { ref, computed, PropType, Component } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// 🔥 MODIFICATION : On remplace isActive par route
export interface MenuItem {
  id: string;
  label: string;
  icon: Component;  
  route: string; 
  category?: string;
}

export default {
  name: 'AdminSidebar',
  props: {
    menuItems: { type: Array as PropType<MenuItem[]>, required: true }
  },
  emits: ['logout'],
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const isReduced = ref(false);
    
    const toggleReduce = () => isReduced.value = !isReduced.value;

    const navigate = (path: string) => {
      router.push(path);
    };

    const groupedMenu = computed(() => {
      const groups: Record<string, MenuItem[]> = {};
      props.menuItems.forEach(item => {
        const cat = item.category || 'Menu';
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push(item);
      });
      return groups;
    });

    return { 
      isReduced, 
      toggleReduce, 
      groupedMenu, 
      route, 
      navigate 
    };
  }
}
</script>

<style scoped>
.sidebar {
  --sb-bg: #ffffff;           
  --sb-text: #ffffff;         
  --sb-text-active: #ffffff;  
  --sb-accent: var(--secondary-light-color);       
  --sb-hover: var(--secondary-light-color);
}

.sidebar {
  position: fixed; bottom: 0; left: 0; width: 100%; height: calc(65px + env(safe-area-inset-bottom));
  background-color:var(--primary-color);
  display: flex; justify-content: space-around; align-items: center; z-index: 100;
  box-shadow: 0px -4px 20px rgba(0, 0, 0, 0.02);
}

/* Scroll mobile (horizontal) invisible par défaut */
.nav-menu { 
  display: flex; width: 100%; justify-content: flex-start; align-items: center; 
  overflow-x: auto; gap: 0.5rem; padding: 0 1rem; 
  scrollbar-width: none; 
}
.nav-menu::-webkit-scrollbar{ display: none; }

.icon {
  width: 20px; height: 20px; transition: all 0.2s ease;
  stroke: var(--sb-text) !important; fill: none;
}

.nav-item {
  background: none; border: none; color: var(--sb-text) !important; 
  cursor: pointer; padding: 0.5rem; display: flex; flex-direction: column; justify-content: center; align-items: center;
  flex-shrink: 0; width: 100px; min-height: 50px; font-size: 0.65rem; font-weight: 600;
  transition: all 0.3s ease; border-radius: 14px;
}

.nav-item.active {
  background-color: var(--sb-accent);
  color: var(--sb-text-active) !important;
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
}
.nav-item.active .icon { stroke: var(--sb-text-active) !important; }

.nav-item:hover:not(.active) { background-color: var(--sb-hover); color: #475569 !important; }
.nav-item:hover:not(.active) .icon { stroke: #475569 !important; }

.hidden-mobile { display: none; }

@media (min-width: 1030px) {
  .hidden-mobile { display: flex; }
  .sidebar { 
    position: relative; width: 270px; height: auto; flex-direction: column; 
    padding: 1rem 1.5rem; box-shadow: 10px 0 30px rgba(0,0,0,0.01);
  }
  .sidebar.is-reduced { width: 90px; height: auto; padding: 5rem 0.2rem; }
  
  .logo { display: flex; align-items: center; justify-content: space-between; padding: 0 0.5rem; margin-bottom: 2rem; width: 100%; flex-shrink: 0; }
  .sidebar.is-reduced .logo { justify-content: center; }
  .logo-text { font-weight: 800; font-size: 1.4rem; color: #ffffff; letter-spacing: -0.5px; }
  
  .toggle-icon { width: 24px; height: 24px; color: var(--sb-text); cursor: pointer; }
  .toggle-icon:hover { color: var(--sb-accent); }
  
  /* --- GESTION DU SCROLL VERTICAL (BUREAU) --- */
  .nav-menu { 
    flex-direction: column; width: 100%; gap: 0.4rem; align-items: flex-start; padding: 0; 
    overflow-y: auto; 
    overflow-x: hidden;
    
    /* Firefox : Scrollbar transparente par défaut */
    scrollbar-width: thin;
    scrollbar-color: transparent transparent;
  }

  /* Firefox : Apparition de la scrollbar au survol de la sidebar */
  .sidebar:hover .nav-menu {
    scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  }

  /* Chrome, Edge, Safari : Annulation du display: none mobile */
  .nav-menu::-webkit-scrollbar {
    display: block; 
    width: 6px;
  }
  .nav-menu::-webkit-scrollbar-track {
    background: transparent;
  }
  
  /* Thumb (barre de défilement) transparente par défaut */
  .nav-menu::-webkit-scrollbar-thumb {
    background-color: transparent;
    border-radius: 10px;
  }
  
  /* Apparition du Thumb au survol de la sidebar */
  .sidebar:hover .nav-menu::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.2);
  }
  /* ------------------------------------------- */
  
  .menu-category {
    display: block; width: 100%; padding: 1.5rem 1rem 0.5rem 0.8rem;
    font-size: 0.75rem; font-weight: 500; color: #cbd5e1; flex-shrink: 0;
  }

  .nav-item { 
    width: 100%; flex-direction: row; justify-content: flex-start; gap: 1rem; 
    padding: 0.8rem 1rem; border-radius: 12px; font-size: 0.9rem; font-weight: 500;
  }

  .sidebar.is-reduced .nav-item { justify-content: center; padding: 1rem 0; }
  .nav-label { white-space: nowrap; }
  
  .logout { margin-top: auto; width: 100%; padding-top: 1rem; flex-shrink: 0; }
  .logout .btn-logout { color: #ffffff !important; }
  .btn-logout:hover { color: red !important; }
  .logout .btn-logout .icon { stroke: rgb(241, 22, 22) !important; }
}
</style>