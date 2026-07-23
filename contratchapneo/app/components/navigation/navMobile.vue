<template>
    <transition name="slide-down">
        <div v-if="isOpen" class="nav-mobile-menu">
            <ul class="nav-links-mobile">
                <li><NuxtLink to="/" @click="close">Accueil</NuxtLink></li>

                <li class="mobile-accordion">
                    <div class="mobile-accordion__trigger-wrapper">
                        <NuxtLink to="/contractbank" class="mobile-accordion__main-link" @click="close">Contrats</NuxtLink>
                        <button class="mobile-accordion__icon-btn" @click="isMobileDropdownOpen = !isMobileDropdownOpen">
                            <svg :class="['chevron', { 'is-open': isMobileDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                        </button>
                    </div>
                    <transition name="accordion">
                        <ul v-if="isMobileDropdownOpen" class="mobile-accordion__list">
                            <li v-for="category in contratStore.categories" :key="category.id">
                                <NuxtLink :to="{ path: '/contractbank', query: { category: category.id } }" @click="close">{{ category.title }}</NuxtLink>
                            </li>
                            <li v-if="contratStore.isLoading" class="pl-2 opacity-50 text-sm">Chargement...</li>
                        </ul>
                    </transition>
                </li>

                <li class="mobile-accordion">
                    <div class="mobile-accordion__trigger-wrapper">
                        <NuxtLink to="/pro" class="mobile-accordion__main-link" @click="close">Experts</NuxtLink>
                        <button class="mobile-accordion__icon-btn" @click="isMobileProDropdownOpen = !isMobileProDropdownOpen">
                            <svg :class="['chevron', { 'is-open': isMobileProDropdownOpen }]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                        </button>
                    </div>
                    <transition name="accordion">
                        <ul v-if="isMobileProDropdownOpen" class="mobile-accordion__list">
                            <li v-for="domain in proStore.domains" :key="domain.id">
                                <NuxtLink :to="{ path: '/pro', query: { domaine: domain.slug } }" @click="close">{{ domain.name }}</NuxtLink>
                            </li>
                            <li v-if="proStore.isLoading" class="pl-2 opacity-50 text-sm">Chargement...</li>
                        </ul>
                    </transition>
                </li>

                <li><NuxtLink to="/lawCalcul" @click="close">Calcul de droits</NuxtLink></li>

                <li class="mobile-accordion">
                    <div class="mobile-accordion__trigger-wrapper">
                        <NuxtLink to="/services" @click="close">Centre d'appel</NuxtLink>
                    </div>
                </li>
                <li><NuxtLink to="/etudeContrat" @click="close">Revise ton contrat</NuxtLink></li>
                <li><NuxtLink to="/about" @click="close">À propos</NuxtLink></li>
            </ul>
            <a href="#" class="cta-mobile" @click="close">Connexion</a>
        </div>
    </transition>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import { useContratStore } from '../../stores/contratStore'; 
import { useProStore } from '../../stores/proStore';

export default {
    name: 'MobileMenu',
    props: {
        isOpen: { type: Boolean, required: true }
    },
    emits: ['close'],
    setup(props, { emit }) {
        const contratStore = useContratStore();
        const proStore = useProStore();

        const isMobileDropdownOpen = ref<boolean>(false);
        const isMobileProDropdownOpen = ref<boolean>(false);
        const isMobileServicesDropdownOpen = ref<boolean>(false);

        onMounted(() => {
            if (proStore.domains.length === 0) {
                proStore.getFilters();
            }
            if (contratStore.categories.length === 0) {
                contratStore.fetchContracts();
            }
        });

        const close = () => { emit('close'); };

        return { 
            contratStore, proStore, 
            isMobileDropdownOpen, isMobileProDropdownOpen, isMobileServicesDropdownOpen, close 
        };
    }
}
</script>

<style scoped>
.nav-mobile-menu {
    position: absolute; top: 70px; left: 0; width: 100%; background: rgba(255, 255, 255); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); display: flex; flex-direction: column; gap: 1.5rem; padding: 1.5rem 1.5rem 2rem; border-top: 1px solid rgba(0, 0, 0, 0.06); max-height: calc(100vh - 70px); overflow-y: auto;
}
.nav-links-mobile { list-style: none; padding: 0; margin: 0; }
.nav-links-mobile li a { display: block; font-size: 1.1rem; font-weight: 500; padding: 1rem 0; border-bottom: 1px solid rgba(0, 0, 0, 0.04); color: var(--primary-color); text-decoration: none; transition: opacity 0.2s; }
.nav-links-mobile li:last-child a { border-bottom: none; }
.nav-links-mobile li a:hover { opacity: 0.6; }

.mobile-accordion { border-bottom: 1px solid rgba(0, 0, 0, 0.04); }
.mobile-accordion__trigger-wrapper { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; }
.mobile-accordion__list { list-style: none; padding: 0 0 0.5rem 1rem; margin: 0; display: flex; flex-direction: column; gap: 0.25rem; }
.mobile-accordion__icon-btn { background: none; border: none; color: var(--primary-color); margin-right: -7rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }

.mobile-accordion__list li a { font-size: 0.95rem !important; font-weight: 400 !important; padding: 0.6rem 0 !important; border-bottom: none !important; opacity: 0.8; color: var(--primary-color); text-decoration: none; display: block; transition: opacity 0.2s; }
.mobile-accordion__list li a:hover { opacity: 1; }

.chevron { transition: transform 0.25s ease; flex-shrink: 0; }
.chevron.is-open { transform: rotate(180deg); }

.accordion-enter-active, .accordion-leave-active { transition: all 0.25s ease; overflow: hidden; max-height: 400px; }
.accordion-enter-from, .accordion-leave-to { max-height: 0; opacity: 0; }

.cta-mobile { align-self: center; display: block; text-align: center; background: var(--primary-color); width: 70%; color: white; padding: 0.8rem 1.5rem; border-radius: 50px; font-weight: 600; font-size: 0.95rem; text-decoration: none; transition: opacity 0.2s; }
.cta-mobile:hover { opacity: 0.85; }

.slide-down-enter-active, .slide-down-leave-active { transition: all 0.28s ease-out; }
.slide-down-enter-from, .slide-down-leave-to { transform: translateY(-12px); opacity: 0; }

@media (min-width: 1180px) {
    .nav-mobile-menu { display: none !important; }
}
</style>