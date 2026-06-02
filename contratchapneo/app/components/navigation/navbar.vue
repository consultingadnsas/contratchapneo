<template>
    <header :class="['main-header', `theme-${theme}`, { 'is-scrolled': isScrolled }]">
        <nav class="nav-container">

            <!-- Logo -->
            <h3 class="logo">
                <span class="logo-accent">Contrat</span>ChapNeo
            </h3>

            <!-- Liens desktop (cachés sur mobile) -->
            <ul class="nav-links-desktop">
                <li><a href="/">Accueil</a></li>

                <li 
                    class="dropdown-item"
                    @mouseenter="isDropdownOpen = true"
                    @mouseleave="isDropdownOpen = false"
                >
                    <a href="contractbank" class="dropdown-trigger">
                        Banque de contrats
                        <svg :class="['chevron', { 'is-open': isDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="6 9 12 15 18 9"/>
                        </svg>

                    </a>
                    <transition name="dropdown-fade">
                        <ul v-if="isDropdownOpen" class="dropdown-menu">
                            <li><a href="#">Création & Cession</a></li>
                            <li><a href="#">Partenariat & Investissement</a></li>
                            <li><a href="#">Prestation de service & vente</a></li>
                            <li><a href="#">Technologie & Digital</a></li>
                        </ul>
                    </transition>
                </li>

                <li><a href="#">Conseils juridiques</a></li>
                <!-- Dropdown Nos professionnels -->
                <li 
                    class="dropdown-item"
                    @mouseenter="isProDropdownOpen = true"
                    @mouseleave="isProDropdownOpen = false"
                >
                    <a href="#" class="dropdown-trigger">
                        Nos professionnels
                        <svg :class="['chevron', { 'is-open': isProDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="6 9 12 15 18 9"/>
                        </svg>
                    </a>

                    <transition name="dropdown-fade">
                        <!-- J'ai ajouté la classe 'simple-menu' pour ajuster la largeur en CSS plus bas -->
                        <ul v-if="isProDropdownOpen" class="dropdown-menu simple-menu">
                            <li><a href="#">Commissaire de justice</a></li>
                            <li><a href="#">Avocat</a></li>
                            <li><a href="#">Notaire</a></li>
                            <li><a href="#">Comptable</a></li>
                        </ul>
                    </transition>
                </li>
                <li><a href="#">Outil de calcul</a></li>
                <li><a href="/about">A propos</a></li>
            </ul>

            <!-- CTA desktop -->
           <div class="cta-container desktop-only">
                <a href="#" class="cta-desktop">Connexion</a>
            </div>

            <!-- Hamburger -->
            <Hamburger
                :class="['mobile-only', { 'is-active': isMenuOpen }]"
                :isOpen="isMenuOpen"
                @toggle="toggleMenu"
            />
        </nav>

        <!-- Menu mobile -->
        <transition name="slide-down">
            <div v-if="isMenuOpen" class="nav-mobile-menu">
                <ul class="nav-links-mobile">
                    <li><a href="/" @click="toggleMenu">Accueil</a></li>

                    <!-- Accordion Banque de contrats sur mobile -->
                    <li class="mobile-accordion">
                        <button 
                            class="mobile-accordion__trigger"
                            @click="isMobileDropdownOpen = !isMobileDropdownOpen"
                        >
                            Banque de contrats
                            <svg :class="['chevron', { 'is-open': isMobileDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="6 9 12 15 18 9"/>
                            </svg>
                        </button>

                        <transition name="accordion">
                            <ul v-if="isMobileDropdownOpen" class="mobile-accordion__list">
                                <li><a href="#" @click="toggleMenu">Création & Cession</a></li>
                                <li><a href="#" @click="toggleMenu">Partenariat & Investissement</a></li>
                                <li><a href="#" @click="toggleMenu">Prestation de service & vente</a></li>
                                <li><a href="#" @click="toggleMenu">Technologie & Digital</a></li>
                                <li><a href="#" @click="toggleMenu">Evènementiel, Restauration & Logistique</a></li>
                            </ul>
                        </transition>
                    </li>

                    <li><a href="#" @click="toggleMenu">Conseils juridiques</a></li>
                    <!-- Accordion Nos professionnels sur mobile -->
                    <li class="mobile-accordion">
                        <button 
                            class="mobile-accordion__trigger"
                            @click="isMobileProDropdownOpen = !isMobileProDropdownOpen"
                        >
                            Nos professionnels
                            <svg :class="['chevron', { 'is-open': isMobileProDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="6 9 12 15 18 9"/>
                            </svg>
                        </button>

                        <transition name="accordion">
                            <ul v-if="isMobileProDropdownOpen" class="mobile-accordion__list">
                                <li><a href="#" @click="toggleMenu">Commissaire de justice</a></li>
                                <li><a href="#" @click="toggleMenu">Avocat</a></li>
                                <li><a href="#" @click="toggleMenu">Notaire</a></li>
                                <li><a href="#" @click="toggleMenu">Comptable</a></li>
                            </ul>
                        </transition>
                    </li>
                    <li><a href="#" @click="toggleMenu">Outil de calcul</a></li>
                    <li><a href="/about" @click="toggleMenu">A propos</a></li>
                </ul>
                <a href="#" class="cta-mobile" @click="toggleMenu">Connexion</a>
            </div>
        </transition>
    </header>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Hamburger from '../buttons/hamburger.vue';

export default {
    name: 'MainHeader',
    components: { Hamburger },
    props: {
        theme: {
            type: String,
            default: 'dark'
        }
    },

    setup(props) {
        const isMenuOpen = ref<boolean>(false);
        const isScrolled = ref<boolean>(false);
        const isDropdownOpen = ref<boolean>(false);
        const isMobileDropdownOpen = ref<boolean>(false);
        const isProDropdownOpen = ref<boolean>(false);
        const isMobileProDropdownOpen = ref<boolean>(false);

        const toggleMenu = () => {
            isMenuOpen.value = !isMenuOpen.value;
            if (!isMenuOpen.value) {
                isMobileDropdownOpen.value = false;
                isProDropdownOpen.value = false;
                isMobileProDropdownOpen.value = false;
            }
        };

        const handleScroll = () => {
            isScrolled.value = window.scrollY > 20;
        };

        onMounted(() => {
            window.addEventListener('scroll', handleScroll);
            handleScroll();
        });

        onUnmounted(() => {
            window.removeEventListener('scroll', handleScroll);
        });

        return { isMenuOpen, isScrolled, isDropdownOpen, isMobileDropdownOpen, isProDropdownOpen, isMobileProDropdownOpen, toggleMenu };
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
    background: rgba(255, 255, 255, 0);
    backdrop-filter: blur(0px);
    -webkit-backdrop-filter: blur(0px);
    border-bottom: 1px solid rgba(255, 255, 255, 0);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0);
    transition: background 0.3s ease, backdrop-filter 0.3s ease,
                border 0.3s ease, box-shadow 0.3s ease, top 0.3s ease;
}

.main-header.is-scrolled {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.80);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
    padding: 0 1.5rem;
}

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

.nav-links-desktop {
    display: none;
}

.cta-desktop {
    display: none;
}

.mobile-only {
    display: flex;
}

/* =============================================
   MENU MOBILE
   ============================================= */
.nav-mobile-menu {
    position: absolute;
    top: 70px;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem 1.5rem 2rem;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.nav-links-mobile li a {
    display: block;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.04);
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

/* Accordion mobile */
.mobile-accordion {
    border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.mobile-accordion__trigger {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 1rem 0;
    color: var(--primary-color);
    background: none;
    border: none;
    cursor: pointer;
}

.mobile-accordion__list {
    list-style: none;
    padding: 0 0 0.5rem 1rem;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.mobile-accordion__list li a {
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    padding: 0.6rem 0 !important;
    border-bottom: none !important;
    opacity: 0.8;
    color: var(--primary-color);
    text-decoration: none;
    display: block;
    transition: opacity 0.2s;
}

.mobile-accordion__list li a:hover {
    opacity: 1;
}

/* Chevron animé */
.chevron {
    transition: transform 0.25s ease;
    flex-shrink: 0;
}

.chevron.is-open {
    transform: rotate(180deg);
}

/* Animation accordion mobile */
.accordion-enter-active,
.accordion-leave-active {
    transition: all 0.25s ease;
    overflow: hidden;
    max-height: 200px;
}

.accordion-enter-from,
.accordion-leave-to {
    max-height: 0;
    opacity: 0;
}

.nav-mobile-menu .cta-mobile {
    align-self: center;
}

.cta-mobile {
    display: block;
    text-align: center;
    background: var(--primary-color);
    width: 70%;
    color: white;
    padding: 0.85rem 1.5rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    transition: opacity 0.2s;
}

.cta-mobile:hover {
    opacity: 0.85;
}

/* Animation menu mobile */
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
   DESKTOP — ≥ 1024px
   ============================================= */
@media (min-width: 1024px) {
    .main-header {
        top: 16px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1200px;
        border-radius: 50px;
        background: rgba(255, 255, 255, 0);
        backdrop-filter: blur(0px);
        -webkit-backdrop-filter: blur(0px);
        border: 1px solid rgba(255, 255, 255, 0);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0);
    }

    .main-header.is-scrolled {
        top: 16px;
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.45);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.06);
    }

    .nav-container {
        padding: 0 2rem;
        width: 100%;
        gap: 1rem;
        flex: 1;
        justify-content: space-between;
        align-items: center;
    }

    .nav-links-desktop {
        display: flex;
        list-style: none;
        padding: 0;
        margin: 0;
        gap: 0.2rem;
        flex: 1;
        justify-content: center;
    }

    .nav-links-desktop li a,
    .nav-links-desktop li .dropdown-trigger {
        display: flex;
        align-items: center;
        white-space: nowrap;
        font-size: clamp(0.8rem, 0.9vw, 0.9rem);
        gap: 0.3rem;
        font-weight: 500;
        padding: 0.5rem 0.6rem;
        border-radius: 50px;
        color: var(--tertiary-color);
        text-decoration: none;
        transition: background 0.2s, opacity 0.2s;
        cursor: pointer;
    }

    .nav-links-desktop li a:hover,
    .nav-links-desktop li .dropdown-trigger:hover {
        background: rgba(255, 255, 255, 0.4);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    .cta-container.desktop-only {
        display: block;
        /* Empêche le bouton d'être écrasé par les liens s'il manque de place */
        flex-shrink: 0; 
    }

    /* Dropdown desktop */
    .dropdown-item {
        position: relative;
    }

    .dropdown-menu {
        position: absolute;
        top: calc(100% + 12px);
        left: 50%;
        transform: translateX(-50%);
        width: 260px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
        padding: 0.5rem;
        list-style: none;
        margin: 0;
        z-index: 200;
    }

    /* Petit pont invisible pour ne pas perdre le hover entre trigger et menu */
    .dropdown-menu::before {
        content: '';
        position: absolute;
        top: -12px;
        left: 0;
        width: 100%;
        height: 12px;
    }

    .dropdown-menu li a {
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        font-size: 0.875rem !important;
        color: var(--primary-color) !important;
        text-decoration: none;
        transition: background 0.15s !important;
        white-space: normal !important;
    }

    .dropdown-menu li a:hover {
        background: rgba(0, 0, 0, 0.04) !important;
        box-shadow: none !important;
    }

    .dropdown-icon {
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    .dropdown-menu li a span:last-child {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
    }

    .dropdown-menu li a strong {
        font-weight: 600;
        font-size: 0.875rem;
        line-height: 1.2;
    }

    .dropdown-menu li a small {
        font-size: 0.75rem;
        opacity: 0.55;
        font-weight: 400;
    }

    /* Animation dropdown desktop */
    .dropdown-fade-enter-active,
    .dropdown-fade-leave-active {
        transition: all 0.2s ease;
    }

    .dropdown-fade-enter-from,
    .dropdown-fade-leave-to {
        opacity: 0;
        transform: translateX(-50%) translateY(-6px);
    }

    .cta-desktop {
        display: block;
        white-space: nowrap;
        background: var(--primary-color);
        color: white;
        padding: 0.55rem 1.15rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.88rem;
        text-decoration: none;
        transition: opacity 0.2s, transform 0.2s;
    }

    .cta-desktop:hover {
        opacity: 0.85;
        transform: scale(1.02);
    }

    .mobile-only {
        display: none !important;
    }

    .nav-mobile-menu {
        display: none !important;
    }
    .dropdown-menu.simple-menu {
        width: 200px; /* Plus fin que l'autre menu */
    }

    .dropdown-menu.simple-menu li a {
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1rem !important; /* Un peu moins haut que les gros boutons de l'autre menu */
    }
}

.main-header.is-scrolled .nav-links-desktop li a,
.main-header.is-scrolled .nav-links-desktop li .dropdown-trigger {
    color: var(--primary-color);
}

/* ── THÈME SOMBRE (Fond bleu/noir -> Texte blanc) ── */
    .theme-dark .logo { color: white; }
    .theme-dark .nav-links-desktop li a { color: white; }
    .theme-dark .nav-links-desktop li .dropdown-trigger { color: white; }

    /* ── THÈME CLAIR (Fond blanc -> Texte bleu) ── */
    .theme-light .logo { color: var(--primary-color); }
    .theme-light .nav-links-desktop li a { color: var(--primary-color); }
    .theme-light .nav-links-desktop li .dropdown-trigger { color: var(--primary-color); }
    .theme-light .nav-links-desktop li a:hover,
    .nav-links-desktop li .dropdown-trigger:hover {
        background: rgba(97, 96, 96, 0.4);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    /* ── AU SCROLL (Le fond devient blanc opaque -> On force le texte en bleu) ── */
    .main-header.is-scrolled .logo,
    .main-header.is-scrolled .nav-links-desktop li a,
    .main-header.is-scrolled .nav-links-desktop li .dropdown-trigger {
        color: var(--primary-color) !important;
    }
</style>