<template>
    <header :class="['main-header', `theme-${theme}`, { 'is-scrolled': isScrolled }]">
        <nav class="nav-container">
            <NuxtLink to="/" class="pic__container" @click="closeMenu">
                <img src="/CONTRATCHAP.png" alt="ContratchapNeo">
            </NuxtLink>

            <DesktopMenu :theme="theme" :isScrolled="isScrolled" />

            <div class="cta-container desktop-only">
                <a href="/auth/login" class="cta-desktop">Connexion</a>
            </div>

            <Hamburger
                :class="['mobile-only', { 'is-active': isMenuOpen }]"
                :isOpen="isMenuOpen"
                @toggle="toggleMenu"
            />
        </nav>

        <MobileMenu :isOpen="isMenuOpen" @close="closeMenu" />

    </header>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Hamburger from '../buttons/hamburger.vue';
import DesktopMenu from './navDesktop.vue';  // <-- Import du nouveau composant
import MobileMenu from './navMobile.vue';    // <-- Import du nouveau composant

import { useContratStore } from '../../stores/contratStore'; 
import { useProStore } from '../../stores/proStore';

export default {
    name: 'MainHeader',
    components: { Hamburger, DesktopMenu, MobileMenu },
    props: {
        theme: { type: String, default: 'dark' }
    },

    setup() {
        const contratStore = useContratStore();
        const proStore = useProStore();

        const isMenuOpen = ref<boolean>(false);
        const isScrolled = ref<boolean>(false);

        const toggleMenu = () => { isMenuOpen.value = !isMenuOpen.value; };
        const closeMenu = () => { isMenuOpen.value = false; };
        const handleScroll = () => { isScrolled.value = window.scrollY > 20; };

        onMounted(async () => {
            window.addEventListener('scroll', handleScroll);
            handleScroll();

            // On charge les listes pour toute la Navbar en une seule fois
            if (contratStore.categories.length === 0) {
                await contratStore.getCategories();
            }
            if (proStore.domains.length === 0) {
                await proStore.getFilters(); // Filtres (Domaines) pour les Experts
            }
        });

        onUnmounted(() => {
            window.removeEventListener('scroll', handleScroll);
        });

        return { isMenuOpen, isScrolled, toggleMenu, closeMenu };
    },
};
</script>

<style scoped>
/* Il ne reste ici QUE le style global de la Navbar (la barre blanche/bleue, le logo et le bouton connexion) */
.main-header {
    position: fixed; top: 0; left: 0; width: 100%; z-index: 100; background:white; backdrop-filter: blur(0px); -webkit-backdrop-filter: blur(0px); border-bottom: 1px solid rgba(255, 255, 255, 0); box-shadow: 0 4px 30px rgba(0, 0, 0, 0); transition: background 0.3s ease, backdrop-filter 0.3s ease, border 0.3s ease, box-shadow 0.3s ease, top 0.3s ease;
}

.main-header.is-scrolled {
    background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255, 255, 255, 0.80); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
}

.nav-container { display: flex; justify-content: space-between; align-items: center; height: 70px; padding: 0 1.5rem; }
.pic__container img { width: 70px; height: 60px; }
.cta-desktop { display: none; }
.mobile-only { display: flex; }

/* Thèmes de base pour le logo */
.theme-dark .logo { color: white; }
.theme-light .logo, .main-header.is-scrolled .logo { color: var(--primary-color) !important; }

@media (min-width: 1180px) {
    .main-header {
        top: 16px; left: 50%; transform: translateX(-50%); width: 100%; max-width: 1200px; border-radius: 50px ; background: rgba(210, 215, 245, 0.632); border: 1px solid rgba(255, 255, 255, 0); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0);
    }
    .main-header.is-scrolled {
        top: 8px; background: rgba(255, 255, 255, 0.65); border: 1px solid rgba(255, 255, 255, 0.45); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.06);
    }
    .pic__container img { width: 70px; height: 50px; }
    .nav-container { padding: 0 2rem; width: 100%; gap: 1rem; flex: 1; }
    
    .desktop-only { display: block; flex-shrink: 0; }
    .cta-desktop {
        display: block; white-space: nowrap; background: var(--primary-color-dark); color: white; padding: 0.55rem 1.15rem; border-radius: 50px; font-weight: 800; font-size: 0.85rem; text-decoration: none; transition: opacity 0.2s, transform 0.2s;
    }
    .cta-desktop:hover { opacity: 0.85; transform: scale(1.02); }
    .mobile-only { display: none !important; }
}
</style>