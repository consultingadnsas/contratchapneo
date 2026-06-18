<template>
  <aside class="sidebar" :class="{ 'is-reduced': isReduced }">
    <div class="logo hidden-mobile">
      <span class="logo-text" v-if="!isReduced">ContratChap</span>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="toggle-icon" @click="toggleReduce">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
      </svg>
    </div>

    <nav class="nav-menu">
      <button 
        v-for="item in menuItems" 
        :key="item.id"
        class="nav-item" 
        :class="{ 'active': item.isActive }"
        @click="$emit('navigate', item.id)"
      >
        <component :is="item.icon" class="icon" />
        <span class="nav-label" v-if="!isReduced">{{ item.label }}</span>
      </button>

      <div class="logout">
        <button class="nav-item btn-logout" @click="$emit('logout')">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
          </svg>
          <span class="nav-label" v-if="!isReduced">Déconnexion</span>
        </button>
      </div>
    </nav>
  </aside>
</template>

<script lang="ts">
import { ref, PropType, Component } from 'vue';

export interface MenuItem {
  id: string;
  label: string;
  icon: Component;  
  isActive: boolean;
}

export default {
  name: 'AdminSidebar',
  props: {
    menuItems: { type: Array as PropType<MenuItem[]>, required: true }
  },
  emits: ['navigate', 'logout'],
  setup() {
    const isReduced = ref(false);
    const toggleReduce = () => isReduced.value = !isReduced.value;
    return { isReduced, toggleReduce };
  }
}
</script>

<style scoped>
/* COULEURS SIDEBAR BLANCHE */
.sidebar {
  --sb-bg: #ffffff;           /* Fond Blanc */
  --sb-text: #64748b;         /* Gris ardoise clair */
  --sb-text-active: #0f172a;  /* Bleu nuit foncé au survol */
  --sb-accent: #34d399;       /* Vert émeraude */
  --sb-border: #e2e8f0;       /* Bordure grise très légère */
  --sb-hover-bg: #f8fafc;     /* Gris perle au survol */
}

/* Le reste du CSS (structure) est identique à celui validé précédemment */
.sidebar {
  position: fixed; bottom: 0; left: 0; width: 100%; height: calc(65px + env(safe-area-inset-bottom));
  background-color: var(--sb-bg); border-top: 1px solid var(--sb-border);
  display: flex; justify-content: space-around; align-items: center; z-index: 100;
}
.nav-menu { display: flex; width: 100%; justify-content: flex-start; align-items: center; overflow-x: auto; -webkit-overflow-scrolling: touch; gap: 0.5rem; padding: 0 1rem; scrollbar-width: none; }
.nav-menu::-webkit-scrollbar{ display: none; }
/* =========================================
   CORRECTION SÉCURITÉ COULEUR DES ICÔNES
   ========================================= */

.icon {
  width: 24px;
  height: 24px;
  margin-bottom: 0.2rem;
  transition: transform 0.2s ease;
  
  /* On force l'icône à utiliser le gris de la sidebar, jamais le blanc global */
  stroke: var(--sb-text) !important; 
  fill: none;
}

/* Quand le menu est actif : l'icône devient verte */
.nav-item.active .icon {
  stroke: var(--sb-accent) !important;
}

/* Au survol : l'icône devient anthracite/noire */
.nav-item:hover:not(.active) .icon {
  stroke: var(--sb-text-active) !important;
}

/* On applique la même logique de sécurité pour le texte des boutons */
.nav-item {
  background: none;
  border: none;
  color: var(--sb-text) !important; /* Force le texte en gris */
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  width: 100px;
  min-height: 50px;
  font-size: 0.65rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.nav-item.active {
  color: var(--sb-accent) !important; /* Texte actif en vert */
}

.nav-item:hover:not(.active) {
  color: var(--sb-text-active) !important; /* Texte survolé en sombre */
}

.hidden-mobile { display: none; }
.logout span{
    color:#ef4444
}
.logout .nav-item{
    color: #ef4444;
}


@media (min-width: 1024px) {
  .hidden-mobile { display: flex; }
  .sidebar { position: relative; width: 260px; height: 100vh; flex-direction: column; padding: 1.5rem 1rem; border-top: none; border-right: 1px solid var(--sb-border); }
  .sidebar.is-reduced { width: 88px; padding: 1.5rem 0.5rem; }
  .logo { display: flex; align-items: center; justify-content: space-between; padding: 0 0.5rem; gap: 1.5rem; }
  .sidebar.is-reduced .logo { justify-content: center; padding: 0; }
  .logo-text { font-weight: 800; font-size: 1.3rem; color: #0f172a; }
  .toggle-icon { width: 26px; height: 26px; color: var(--sb-text); cursor: pointer; }
  .toggle-icon:hover { color: var(--sb-accent); }
  .nav-menu { flex-direction: column; width: 100%; gap: 0.5rem; }
  .nav-item { width: 100%; flex-direction: row; justify-content: flex-start; gap: 1rem; padding: 0.8rem 1rem; border-radius: 12px; font-size: 0.95rem; }
  .nav-item:hover { background-color: var(--sb-hover-bg); color: var(--sb-text-active); }
  .nav-item.active { background-color: rgba(52, 211, 153, 0.1); color: var(--sb-accent); }
  .nav-item.active .icon { transform: none; }
  .sidebar.is-reduced .nav-item { justify-content: center; padding: 0.8rem 0; }
  .nav-label { white-space: nowrap; }
  .logout { margin-top: auto; width: 100%; border-top: 1px solid var(--sb-border); padding-top: 1rem; }
  .logout .btn-logout:hover { background-color: rgba(239, 68, 68, 0.05) !important; color:#ef4444 !important; }
}
</style>