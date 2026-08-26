<template>
    <header :class="['main-header', `theme-${theme}`, { 'is-scrolled': isScrolled }]">
        <nav class="nav-container">
            <NuxtLink to="/" class="pic__container" @click="closeMenu">
                <img :src="'/LOGO_CONTRATCHAP.png'" alt="ContratchapNeo">
            </NuxtLink>

            <DesktopMenu :theme="theme" :isScrolled="isScrolled" />

            <div class="cta-container desktop-only">
                <!-- Si l'utilisateur n'est PAS connecté -->
                <NuxtLink v-if="!isAuthenticated" to="/auth/login" class="cta-desktop">
                    Connexion
                </NuxtLink>

                <!-- Si l'utilisateur EST connecté -->
                <NuxtLink v-else to="/profile/dashboard" class="cta-desktop user-dashboard-btn">
                    <span class="user-initials">{{ userInitials }}</span>
                    <span>Dashboard</span>
                </NuxtLink>
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import Hamburger from '../buttons/hamburger.vue';
import DesktopMenu from './navDesktop.vue';  
import MobileMenu from './navMobile.vue';    

import { useContratStore } from '../../stores/contratStore'; 
import { useProStore } from '../../stores/proStore';
import { useAuthStore } from '../../stores/authStore'; 

export default {
    name: 'MainHeader',
    components: { Hamburger, DesktopMenu, MobileMenu },
    props: {
        theme: { type: String, default: 'dark' }
    },

    setup() {
        const contratStore = useContratStore();
        const proStore = useProStore();
        const authStore = useAuthStore(); 

        const isMenuOpen = ref<boolean>(false);
        const isScrolled = ref<boolean>(false);

        const toggleMenu = () => { isMenuOpen.value = !isMenuOpen.value; };
        const closeMenu = () => { isMenuOpen.value = false; };

        // Robust scroll detection: check multiple scroll sources and
        // listen at document level with capture to catch scrolling in
        // any overflowed container (works for pages using internal scroll).
        const getScrollTop = () => {
            try {
                if (typeof window !== 'undefined' && window.scrollY !== undefined) return window.scrollY;
                if (document.scrollingElement) return document.scrollingElement.scrollTop || 0;
                return document.documentElement?.scrollTop || 0;
            } catch (e) {
                return 0;
            }
        };

        const handleScroll = () => { isScrolled.value = getScrollTop() > 20; };

        // ── NOUVEAU : Fonction utilitaire pour extraire l'utilisateur proprement ──
        const getSafeUser = () => {
            // Si l'API a imbriqué l'utilisateur dans une clé "user" (ex: { user: { email: ... } })
            if (authStore.user && authStore.user.user) {
                return authStore.user.user;
            }
            // Sinon on retourne l'objet standard
            return authStore.user || {};
        };

        // ── LOGIQUE D'AUTHENTIFICATION CORRIGÉE ──
        const isAuthenticated = computed(() => {
            const u = getSafeUser();
            // On vérifie l'email ou le username plutôt que l'ID (car ton backend l'appelle parfois 'user' au lieu de 'id')
            return !!u.email || !!u.username;
        });

        const userInitials = computed(() => {
            const u = getSafeUser();
            
            if (u.first_name && u.last_name) {
                return (u.first_name.charAt(0) + u.last_name.charAt(0)).toUpperCase();
            } 
            else if (u.username) {
                return u.username.substring(0, 2).toUpperCase();
            }
            return 'DB'; 
        });

        onMounted(async () => {
            // Capture scroll events from any bubbling/capturing target
            document.addEventListener('scroll', handleScroll, { passive: true, capture: true } as any);
            // Also keep a window listener as a fallback
            window.addEventListener('scroll', handleScroll, { passive: true } as any);
            handleScroll();

            try {
                if (!isAuthenticated.value) {
                    await authStore.getProfile();
                }
            } catch (e) {
                // Silencieux
            }

            if (contratStore.categories.length === 0) {
                await contratStore.getCategories();
            }
            if (proStore.domains.length === 0) {
                await proStore.getFilters(); 
            }
        });

        onUnmounted(() => {
            document.removeEventListener('scroll', handleScroll as EventListener);
            window.removeEventListener('scroll', handleScroll as EventListener);
        });

        return { 
            isMenuOpen, 
            isScrolled, 
            toggleMenu, 
            closeMenu,
            isAuthenticated, 
            userInitials  
        };
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
.pic__container img { width: 200px; height: 90px; }
.cta-desktop { display: none; }
.mobile-only { display: flex; }

/* Thèmes de base pour le logo */
.theme-dark .logo { color: white; }
.theme-light .logo, .main-header.is-scrolled .logo { color: var(--primary-color) !important; }

@media (min-width: 1180px) {
    .main-header {
        top: 16px; left: 50%; transform: translateX(-50%); width: 100%; max-width: 1200px; border-radius: 50px ; background: transparent; border: 1px solid rgba(255, 255, 255, 0); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0);
    }
    .main-header.is-scrolled {
        top: 8px; background: rgba(255, 255, 255, 0.65); border: 1px solid rgba(255, 255, 255, 0.45); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.06);
    }
    .pic__container img { width: 180px; height: 70px; margin-bottom:5px }
    .nav-container { padding: 0 2rem; width: 100%; gap: 1rem; flex: 1; }
    
    .desktop-only { display: block; flex-shrink: 0; }
    
    .cta-desktop {
        display: block; white-space: nowrap; background:var(--primary-color); color: white ; padding: 0.55rem 1.15rem; border-radius: 50px; font-weight: 800; font-size: 0.85rem; text-decoration: none; transition: opacity 0.2s, transform 0.2s;
    }
    .cta-desktop:hover { opacity: 0.85; transform: scale(1.02); }

    /* ── NOUVEAU : Bouton Dashboard connecté ── */
    .user-dashboard-btn {
        display: flex !important;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 1rem 0.35rem 0.4rem !important; 
    }

    .user-initials {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background-color: white;
        color: var(--primary-color);
        border-radius: 50%;
        font-size: 0.75rem;
        font-weight: 800;
    }

    .mobile-only { display: none !important; }
}
</style>