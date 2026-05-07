<template>
    <header class="main-header">
        <nav class="nav-container">
            <!-- Logo -->
            <h3 class="logo">
            <span class="logo-accent">Contrat</span>ChapNeo
            </h3>

            <!-- Bouton Hamburger avec état -->
            <Hamburger 
                :isOpen="isMenuOpen"
                @toggle="toggleMenu" 
                :class="{'is-active': isMenuOpen}"
            />
        </nav>

        <!-- Menu Mobile avec Transition -->
        <transition name="slide-down">
            <div v-if="isMenuOpen" class="nav-layout">
                <ul class="nav-links">
                    <li><a href="#">Accueil</a></li>
                    <li><a href="#">Contrats</a></li>
                    <li><a href="#">À propos</a></li>
                </ul>
            </div>
        </transition>
    </header>
</template>

<script lang="ts">
import { ref } from 'vue';
import Hamburger from '../buttons/hamburger.vue';

export default{
    
    components:{
        Hamburger
    },

    setup(props, {emit}) {
        
        const isMenuOpen = ref<boolean>(false);
        const toggleMenu = () => {
            isMenuOpen.value = !isMenuOpen.value;
        };

        return{
            isMenuOpen,
            toggleMenu
        }
    }
}

</script>

<style scoped>
.main-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(var(--primary-rgb), 0.1);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px; /* Hauteur plus standard */
  padding: 0 1.5rem;
}

.logo {
  font-family: 'Instrument Sans', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}

.logo-accent {
  background: var(--primary-color);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  margin-right: 2px;
}

.nav-layout {
  position: absolute;
  top: 70px;
  left: 0;
  width: 100%;
  background: white;
  height: auto;
  padding: 2rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Animations */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease-out;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

.nav-links {
  list-style: none;
  padding: 0;
}

.nav-links li {
  font-size: 1.1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f0f0f0;
}

/* --- DESIGN DESKTOP (Ordinateurs) --- */
@media (min-width: 1024px) {
    .main-header {
        top: 20px; /* Décalage du haut */
        left: 50%;
        transform: translateX(-50%);
        width: 95%; /* Ne prend pas toute la largeur */
        max-width: 1200px;
        border-radius: 50px; /* Bords très arrondis */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid var(--tertiary-color);
    }

    .nav-links-desktop {
        display: flex; /* Affiche les liens sur desktop */
    }

    .mobile-only {
        display: none !important; /* Cache le hamburger sur desktop */
    }
}
</style>