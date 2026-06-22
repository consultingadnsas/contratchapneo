<template>
    <ul :class="['nav-links-desktop', `theme-${theme}`, { 'is-scrolled': isScrolled }]">
        <li><NuxtLink to="/">Accueil</NuxtLink></li>

        <li class="dropdown-item" @mouseenter="isDropdownOpen = true" @mouseleave="isDropdownOpen = false">
            <NuxtLink to="/contractbank" class="dropdown-trigger">
                Banque de contrats
                <svg :class="['chevron', { 'is-open': isDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"/>
                </svg>
            </NuxtLink>
            <transition name="dropdown-fade">
                <ul v-if="isDropdownOpen" class="dropdown-menu">
                    <li v-for="category in contratStore.categories" :key="category.id">
                        <NuxtLink :to="{ path: '/contractbank', query: { category: category.id } }">
                            {{ category.title }}
                        </NuxtLink>
                    </li>
                    <li v-if="contratStore.isLoading"><span class="muted-text pl-3 text-sm">Chargement...</span></li>
                </ul>
            </transition>
        </li>

        <li class="dropdown-item" @mouseenter="isProDropdownOpen = true" @mouseleave="isProDropdownOpen = false">
            <NuxtLink to="/pro" class="dropdown-trigger">
                Experts
                <svg :class="['chevron', { 'is-open': isProDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"/>
                </svg>
            </NuxtLink>
            <transition name="dropdown-fade">
                <ul v-if="isProDropdownOpen" class="dropdown-menu">
                    <li v-for="domain in proStore.domains" :key="domain.id">
                        <NuxtLink :to="{ path: '/pro', query: { domaine: domain.slug } }">
                            {{ domain.name }}
                        </NuxtLink>
                    </li>
                    <li v-if="proStore.isLoading"><span class="muted-text pl-3 text-sm">Chargement...</span></li>
                </ul>
            </transition>
        </li>

        <li><NuxtLink to="/lawCalcul">Calcul de droits</NuxtLink></li>

        <li class="dropdown-item" @mouseenter="isServicesDropdownOpen = true" @mouseleave="isServicesDropdownOpen = false">
            <NuxtLink to="/services" class="dropdown-trigger">
                Services juridiques
                <svg :class="['chevron', { 'is-open': isServicesDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"/>
                </svg>
            </NuxtLink>
            <transition name="dropdown-fade">
                <ul v-if="isServicesDropdownOpen" class="dropdown-menu">
                    <li><NuxtLink to="/services#diag">Diagnostic juridique</NuxtLink></li>
                    <li><NuxtLink to="/services#domicile">Domiciliation d'entreprise</NuxtLink></li>
                    <li><NuxtLink to="/services#crea">Créations d'entreprises</NuxtLink></li>
                    <li><NuxtLink to="/services#assistance">Assistance juridique</NuxtLink></li>
                    <li><NuxtLink to="/services#programmes">Programmes juridiques</NuxtLink></li>
                    <li><NuxtLink to="/services#noms">Enregistrement Noms Commerciaux</NuxtLink></li>
                    <li><NuxtLink to="/services#marques">Dépôt de Marque</NuxtLink></li>
                    <li><NuxtLink to="/services#brevets">Brevet d'Invention</NuxtLink></li>
                    <li><NuxtLink to="/services#tech">Legaltech</NuxtLink></li>
                </ul>
            </transition>
        </li>

        <li><NuxtLink to="/etudeContrat">Etude de contrats</NuxtLink></li>
        <li><NuxtLink to="/about"> À propos</NuxtLink></li>
    </ul>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useContratStore } from '../../stores/contratStore'; 
import { useProStore } from '../../stores/proStore';

export default {
    name: 'DesktopMenu',
    props: {
        theme: { type: String, default: 'dark' },
        isScrolled: { type: Boolean, default: false }
    },
    setup() {
        const contratStore = useContratStore();
        const proStore = useProStore();

        const isDropdownOpen = ref<boolean>(false);
        const isServicesDropdownOpen = ref<boolean>(false);
        const isProDropdownOpen = ref<boolean>(false);

        return { 
            contratStore, proStore, 
            isDropdownOpen, isServicesDropdownOpen, isProDropdownOpen 
        };
    }
}
</script>

<style scoped>
.nav-links-desktop { display: none; }

@media (min-width: 1180px) {
    .nav-links-desktop { display: flex; list-style: none; padding: 0; margin: 0; gap: 0.2rem; flex: 1; justify-content: center; }
    
    .nav-links-desktop li a, .nav-links-desktop li .dropdown-trigger {
        position: relative; display: flex; align-items: center; white-space: nowrap; font-size: clamp(0.85rem, 0.9vw, 0.9rem); gap: 0.3rem; font-weight: 500; padding: 0.5rem 0.6rem; border-radius: 50px; color: var(--tertiary-color); text-decoration: none; transition: background 0.2s, opacity 0.2s; cursor: pointer;
    }

    .nav-links-desktop li a::after, .nav-links-desktop li .dropdown-trigger::after {
        content: ''; position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 0; height: 2px; background-color: currentColor; border-radius: 2px; transition: width 0.3s ease;
    }

    .nav-links-desktop > li > a.router-link-active::after, .nav-links-desktop > li > a.router-link-exact-active::after, .nav-links-desktop > li > .dropdown-trigger.router-link-active::after { width: 60%; }
    .nav-links-desktop > li > a.router-link-active:hover::after, .nav-links-desktop > li > .dropdown-trigger.router-link-active:hover::after { width: 75%; }
    .dropdown-menu li a::after { display: none !important; }

    .nav-links-desktop li a:hover, .nav-links-desktop li .dropdown-trigger:hover {
        background: rgba(255, 255, 255, 0.15) !important; backdrop-filter: blur(12px) !important; -webkit-backdrop-filter: blur(12px) !important; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important; transform: translateY(-1px);
    }

    .dropdown-item { position: relative; }
    .dropdown-menu {
        position: absolute; top: calc(100% + 12px); left: 50%; transform: translateX(-50%); width: 260px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 16px; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1); padding: 0.5rem; list-style: none; margin: 0; z-index: 200;
    }
    .dropdown-menu::before { content: ''; position: absolute; top: -12px; left: 0; width: 100%; height: 12px; }

    .dropdown-menu li a {
        display: flex !important; align-items: center !important; gap: 0.75rem !important; padding: 0.75rem 1rem !important; border-radius: 10px !important; font-size: 0.875rem !important; color: var(--primary-color) !important; text-decoration: none; transition: background 0.15s !important; white-space: normal !important;
    }
    .dropdown-menu li a:hover { background: rgba(0, 0, 0, 0.04) !important; box-shadow: none !important; }
    .chevron { transition: transform 0.25s ease; flex-shrink: 0; }
    .chevron.is-open { transform: rotate(180deg); }

    .dropdown-fade-enter-active, .dropdown-fade-leave-active { transition: all 0.2s ease; }
    .dropdown-fade-enter-from, .dropdown-fade-leave-to { opacity: 0; transform: translateX(-50%) translateY(-6px); }

    /* Thèmes et Scroll (Adaptés pour cibler le wrapper nav-links-desktop directement) */
    .nav-links-desktop.theme-dark li a, .nav-links-desktop.theme-dark li .dropdown-trigger { color: white; }
    .nav-links-desktop.theme-light li a, .nav-links-desktop.theme-light li .dropdown-trigger { color: var(--primary-color); }
    .nav-links-desktop.theme-light li a:hover, .nav-links-desktop.theme-light li .dropdown-trigger:hover {
        background: rgba(97, 96, 96, 0.4) !important; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    .nav-links-desktop.is-scrolled li a, .nav-links-desktop.is-scrolled li .dropdown-trigger {
        color: var(--primary-color) !important;
    }
}
</style>