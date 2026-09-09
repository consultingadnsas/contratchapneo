<template>
    <div class="contrat-card-section">
        
        <header>
            <h2>Découvrez tous nos Expert</h2>
            <p>Pour un suivi plus personnalisé concernant vos besoins.</p>
        </header>

       <div class="toolbar">
            <BaseSearchInput 
                class="toolbar__search" 
                placeholder="Trouver un professionnel"
                v-model="searchQuery"
                @update:modelValue="handleSearch"
            />

            <div class="toolbar__filters-row">
                <baseProFilter 
                    class="toolbar__filter" 
                    :titles="proStore.titles"
                    :activeTitle="activeTitle" 
                    @filter="handleTitleFilter"
                />
                
                <BaseDomainSelect 
                    class="toolbar__select" 
                    placeholder="Choisir le domaine" 
                    :options="proStore.domains"
                    v-model="activeDomainSlug"
                    @update:modelValue="handleDomainFilter"
                />

                <BaseCountrySelect 
                    class="toolbar__select" 
                    placeholder="Choisir le pays" 
                    :options="proStore.countries"
                    v-model="activeCountryCode"
                    @update:modelValue="handleCountryFilter"
                />
            </div>
            
        </div>

        <contractCardSkeleton v-if="proStore.isLoading" />

        <emptyState
            v-else-if="proStore.professionals.length === 0" 
            title="Aucun expert trouvé"
            description="Aucun professionnel ne correspond à vos critères."
            textAction="Contactez nos services juridiques"
            type="pro"
        />

        <template v-else>
            
            <div class="cards-container">                
                <ProCards 
                    v-for="pro in proStore.professionals" 
                    :key="pro.id"
                    :title="`${pro.first_name} ${pro.last_name}`"
                    :subtitle="pro.title_display"
                    :image="pro.profile_picture || undefined"
                    :isloading="cartStore.isLoading"
                    @view="openViewModal(pro.id)"
                    @pro-checkout="addToCart(pro.id)"
                />
            </div>
            <Paginator 
                :currentPage="proStore.currentPage" 
                :totalCount="proStore.totalCount" 
                :pageSize="proStore.pageSize" 
                @page-changed="handlePageChange"
            />
            
        </template>

        <Teleport to="body">
            
            <cartModale
                :isOpen="isOpen" 
                @close="isOpen = false"
            />
            
            <proModale
                v-if="isViewOpen"
                :isOpen="isViewOpen"
                :professional="proStore.professional"
                @close="isViewOpen = false"
                @pro-checkout="addToCart($event)"
            />
        </Teleport>

    </div>
</template>

<script lang="ts">
import ProCards from '../../cards/proCards.vue'
import contractCardSkeleton from '../../cards/contractCardSkeleton.vue'
import emptyState from '../../tools/emptyState.vue'
import baseProFilter from '../../tools/baseProFilter.vue'
import BaseDomainSelect from '../../input/BaseDomainSelect.vue'
import BaseCountrySelect from '../../input/BaseCountrySelect.vue'
import BaseSearchInput from '../../input/BaseSearchInput.vue'
import Paginator from '../../tools/Paginator.vue'
import cartModale from '../../modale/cartModale.vue'
import viewModale from '../../modale/viewModale.vue'
import proModale from '../../modale/proModale.vue'

import { ref, onMounted, watch } from 'vue' 
import { useRouter, useRoute } from 'vue-router' 
import { useProStore } from '../../../stores/proStore'
import { useCartStore } from '../../../stores/cartStore'

export default {
    components: {
        ProCards, Paginator, BaseSearchInput, BaseCountrySelect, BaseDomainSelect,
        contractCardSkeleton, emptyState, cartModale, viewModale,
        baseProFilter, proModale
    },
    
    setup() {
        const router = useRouter();
        const route = useRoute(); 
        const proStore = useProStore();
        const cartStore = useCartStore();

        // 1. Initialiser avec ce qui se trouve dans l'URL (si présent)
        const activeTitle = ref((route.query.titre as string) || (route.query.title as string) || '');
        const activeDomainSlug = ref((route.query.domaine as string) || (route.query.domain as string) || '');
        const activeCountryCode = ref((route.query.pays as string) || (route.query.country as string) || '');
        const searchQuery = ref((route.query.q as string) || '');
        const currentPage = ref(Number(route.query.page) || 1);

        // Fonction centralisée pour la recherche (avec la pagination)
        const fetchPros = (page = 1) => {
            currentPage.value = page;
            proStore.getProfessionals(
                page, 
                activeTitle.value, 
                activeCountryCode.value, 
                searchQuery.value,
                activeDomainSlug.value
            );
        }

        // 2. Gestionnaires de filtres
        let searchTimeout: ReturnType<typeof setTimeout>;

        const handleSearch = (query: string) => {
            searchQuery.value = query; 
            if (searchTimeout) clearTimeout(searchTimeout);
            
            searchTimeout = setTimeout(() => {
                fetchPros(1);
            }, 300);
        };

        const handleTitleFilter = (title: string) => {
            activeTitle.value = title;
            router.push({ path: '/pro', query: { ...route.query, titre: title || undefined } });
            fetchPros(1);
        };

        const handleDomainFilter = (slug: string) => {
            activeDomainSlug.value = slug;
            router.push({ path: '/pro', query: { ...route.query, domaine: slug || undefined } });
            fetchPros(1);
        };

        const handleCountryFilter = (code: string) => {
            activeCountryCode.value = code;
            router.push({ path: '/pro', query: { ...route.query, pays: code || undefined } });
            fetchPros(1);
        };

        const handlePageChange = (page: number) => {
            fetchPros(page);
        };

        // 3. Surveillance URL
        watch(() => route.query.titre || route.query.title, (newTitle) => {
            const title = (newTitle as string) || '';
            if (activeTitle.value !== title) {
                activeTitle.value = title;
                fetchPros(1);
            }
        });

        watch(() => route.query.domaine || route.query.domain, (newDomain) => {
            const domain = (newDomain as string) || '';
            if (activeDomainSlug.value !== domain) {
                activeDomainSlug.value = domain;
                fetchPros(1);
            }
        });

        watch(() => route.query.pays || route.query.country, (newCountry) => {
            const country = (newCountry as string) || '';
            if (activeCountryCode.value !== country) {
                activeCountryCode.value = country;
                fetchPros(1);
            }
        });

        // 4. Modales
        const isOpen = ref<boolean>(false);
        const openModal = () => { isOpen.value = true; }

        const isViewOpen = ref<boolean>(false);
        const openViewModal = async (proId: string) => {
            proStore.getSpecificProfessional(proId);  
            isViewOpen.value = true;
        }

        const addToCart = async (proId:string) => {
            try{
                await cartStore.addProToCart(proId);
                router.push('/order/checkout/');
            } catch (error: any) {
                console.error("Erreur lors de l'ajout", error)
            }
        }

        // 5. Chargement initial
        onMounted(async () => {
            if (proStore.titles.length === 0 || proStore.countries.length === 0 || proStore.domains.length === 0) {
                await proStore.getFilters();
            }
            
            fetchPros(currentPage.value || 1);
        });

        return {
            router, cartStore, proStore, searchQuery, activeTitle, activeDomainSlug, activeCountryCode,
            handleSearch, handleTitleFilter, handleDomainFilter, handleCountryFilter,
            isOpen, openModal, isViewOpen, openViewModal, addToCart, handlePageChange
        }
    }
}
</script>

<style scoped>
/* J'ai gardé exactement ton style d'origine intact */
.contrat-card-section {
    width: 100%;
    max-width: 1400px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-items: center;
    gap: 2rem;
    padding: 4rem 1rem 1rem 1rem;
    background: #FDFCFC;
}

.contrat-card-section h2 {
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: var(--primary-color-dark);
    margin-bottom: 1rem;
}

header{
    margin-top: 2rem;
    margin-bottom: 1rem;
}

header p{
    font-size: 1.15rem;
    color: var(--primary-color-dark);
    max-width: 550px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ==========================================
   TOOLBAR : Recherche en haut, filtres alignés
========================================== */
.toolbar {
    width: 100%;
    max-width: 1200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.25rem;
    padding: 0.5rem;
}

.toolbar__search {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

.toolbar__filters-row {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.toolbar__filter {
    flex: 1 1 auto;
    min-width: 0; 
    margin: 0; 
}

.toolbar__select {
    flex: 0 0 auto;
    width: 190px;
    min-width: 160px;
}

:deep(.search-container) {
    width: 100%;
    max-width: 100%;
}

:deep(.search-container.is-mobile.is-expanded) {
    width: auto;
    flex: 1 1 auto;
    min-width: 0;
}

/* ==========================================
   GRILLE DE CARTES
========================================== */
.cards-container {
    width: 100%;
    max-width: 1400px;
    display: grid;
    grid-template-columns: 1fr;
    place-items: center;
    gap: 1rem;
}

@media (min-width: 768px) {
    .cards-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .cards-container {
        grid-template-columns: repeat(4, 1fr);
    }
}

@media (min-width: 1300px) {
    .cards-container {
        grid-template-columns: repeat(4, 1fr);
    }
}
@media (max-width: 767px) {
    .toolbar {
        flex-direction: column;
        align-items: stretch;
        gap: 1rem;
        padding: 1rem;
    }

    .toolbar__filters-row {
        flex-direction: column;
        align-items: stretch;
        gap: 0.75rem;
        width: 100%;
    }
    
    .toolbar__filter,
    .toolbar__select,
    .toolbar__search {
        width: 100%;
        max-width: 100%;
        margin: 0;
    }
}
</style>