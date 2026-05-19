<template>
    <header class="main-header">
        <nav class="nav-container">

            <!-- Logo -->
            <h3 class="logo">
                <span class="logo-accent">Contrat</span>ChapNeo
            </h3>

            <!-- Liens desktop (cachés sur mobile) -->
            <ul class="nav-links-desktop">
                <li><a href="#">Accueil</a></li>
                <li><a href="#">Contrats</a></li>
                <li><a href="#">À propos</a></li>
            </ul>

            <!-- CTA desktop -->
            <a href="#" class="cta-desktop">Parcourir les contrats</a>

            <!-- Hamburger (caché sur desktop) -->
            <Hamburger
                :class="['mobile-only', { 'is-active': isMenuOpen }]"
                :isOpen="isMenuOpen"
                @toggle="toggleMenu"
            />
        </nav>

        <!-- Menu mobile avec transition -->
        <transition name="slide-down">
            <div v-if="isMenuOpen" class="nav-mobile-menu">
                <ul class="nav-links-mobile">
                    <li><a href="#" @click="toggleMenu">Accueil</a></li>
                    <li><a href="#" @click="toggleMenu">Contrats</a></li>
                    <li><a href="#" @click="toggleMenu">À propos</a></li>
                </ul>
                <a href="#" class="cta-mobile" @click="toggleMenu">Parcourir les contrats</a>
            </div>
        </transition>
    </header>
</template>

<script lang="ts">
import { ref } from 'vue';
import Hamburger from '../buttons/hamburger.vue';

export default {
    name: 'MainHeader',
    components: { Hamburger },

    setup() {
        const isMenuOpen = ref<boolean>(false);

        const toggleMenu = () => {
            isMenuOpen.value = !isMenuOpen.value;
        };

        return { isMenuOpen, toggleMenu };
    },
};
</script>

<style scoped>

/* =============================================
   BASE — Mobile first
   ============================================= */
.main-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px); /* Safari */
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
    padding: 0 1.5rem;
}

/* --- Logo --- */
.logo {
    font-family: 'Instrument Sans', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary-color);
    white-space: nowrap;
}

.logo-accent {
    background: var(--primary-color);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    margin-right: 2px;
}

/* --- Liens desktop : cachés par défaut (mobile first) --- */
.nav-links-desktop {
    display: none;
}

.cta-desktop {
    display: none;
}

/* --- Hamburger : visible sur mobile --- */
.mobile-only {
    display: flex; /* ou block selon ton composant Hamburger */
}

/* =============================================
   MENU MOBILE
   ============================================= */
.nav-mobile-menu {
    position: absolute; /* relatif à .main-header qui est fixed */
    top: 70px;
    left: 0;
    width: 100%;
    background: white;
    padding: 1.5rem 1.5rem 2rem;
    box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    border-top: 1px solid #f0f0f0;
}

.nav-links-mobile {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
}

.nav-links-mobile li a {
    display: block;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 1rem 0;
    border-bottom: 1px solid #f0f0f0;
    color: var(--primary-color);
    text-decoration: none;
    transition: opacity 0.2s;
}

.nav-links-mobile li:last-child a {
    border-bottom: none;
}

.nav-links-mobile li a:hover {
    opacity: 0.6;
}

.cta-mobile {
    display: block;
    text-align: center;
    background: var(--primary-color);
    color: white;
    padding: 0.85rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    transition: opacity 0.2s;
}

.cta-mobile:hover {
    opacity: 0.85;
}

/* =============================================
   ANIMATIONS MENU MOBILE
   ============================================= */
.slide-down-enter-active,
.slide-down-leave-active {
    transition: all 0.28s ease-out;
}

.slide-down-enter-from,
.slide-down-leave-to {
    transform: translateY(-12px);
    opacity: 0;
}

/* =============================================
   BREAKPOINT DESKTOP — ≥ 1024px
   Navbar floating pill + liens inline
   ============================================= */
@media (min-width: 1024px) {
    .main-header {
        top: 16px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 1200px;
        border-radius: 50px;
        border: 1px solid var(--tertiary-color, rgba(0,0,0,0.08));
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.07);
        /* Pas de border-bottom sur desktop, la pill a sa propre bordure */
        border-bottom: 1px solid var(--tertiary-color, rgba(0,0,0,0.08));
    }

    .nav-container {
        padding: 0 2rem;
        gap: 2rem;
    }

    /* Affiche les liens desktop */
    .nav-links-desktop {
        display: flex;
        list-style: none;
        padding: 0;
        margin: 0;
        gap: 0.25rem;
        flex: 1; /* prend l'espace disponible entre le logo et le CTA */
        justify-content: center;
    }

    .nav-links-desktop li a {
        display: block;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        color: var(--primary-color);
        text-decoration: none;
        transition: background 0.2s, opacity 0.2s;
    }

    .nav-links-desktop li a:hover {
        background: rgba(0, 0, 0, 0.05);
    }

    /* Affiche le CTA desktop */
    .cta-desktop {
        display: block;
        white-space: nowrap;
        background: var(--primary-color);
        color: white;
        padding: 0.6rem 1.25rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.88rem;
        text-decoration: none;
        transition: opacity 0.2s, transform 0.2s;
    }

    .cta-desktop:hover {
        opacity: 0.85;
        transform: scale(1.02);
    }

    /* Cache le hamburger sur desktop */
    .mobile-only {
        display: none !important;
    }

    /* Le menu mobile ne doit JAMAIS s'afficher sur desktop */
    .nav-mobile-menu {
        display: none !important;
    }
}
</style>