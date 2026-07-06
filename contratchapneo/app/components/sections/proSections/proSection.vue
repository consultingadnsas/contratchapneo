<template>
    <div class="contrat-card-section">
        
        <header>
            <h2>Découvrez tous nos professionnels</h2>
            <p>Pour un suivi plus personnalisé concernant vos besoins.</p>
        </header>

       <div class="toolbar">
            <baseProFilter 
                class="toolbar__filter" 
                :domains="proStore.domains"
                :activeDomain="activeDomainSlug" @filter="handleDomainFilter"
            />
            
            <BaseCountrySelect 
                class="toolbar__select" 
                placeholder="Choisir le pays" 
                :options="proStore.countries"
                @select="handleCountryFilter"
            />
            
            <BaseSearchInput 
                class="toolbar__search" 
                placeholder="Trouver un professionnel"
                v-model="searchQuery"
                @search="handleSearch"
            />
        </div>

        <contractCardSkeleton v-if="proStore.isLoading" />

        <emptyState
            v-else-if="proStore.professionals.length === 0" 
            title="Aucun professionnel disponible pour cette recherche"
            description="Le professionnel que vous cherchez n'est pas encore disponible. Essayez de modifier vos filtres ou contactez-nous pour plus d'informations."
            @go-to="() => router.push('/')"
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
                @pay-consultation="()=>{addToCart}"
            />

        </Teleport>

    </div>
</template>

<script lang="ts">
import ProCards from '../../cards/proCards.vue'
import contractCardSkeleton from '../../cards/contractCardSkeleton.vue'
import emptyState from '../../tools/emptyState.vue'
import baseProFilter from '../../tools/baseProFilter.vue'
import BaseCountrySelect from '../../input/BaseCountrySelect.vue'
import BaseSearchInput from '../../input/BaseSearchInput.vue'
import Paginator from '../../tools/Paginator.vue'
import cartModale from '../../modale/cartModale.vue'
import viewModale from '../../modale/viewModale.vue'
import proModale from '../../modale/proModale.vue'

import { ref, onMounted, watch } from 'vue' // 👈 Ajout de "watch"
import { useRouter, useRoute } from 'vue-router' // 👈 Ajout de "useRoute"
import { useProStore } from '../../../stores/proStore'
import { useCartStore } from '../../../stores/cartStore'

export default {
    components: {
        ProCards, Paginator, BaseSearchInput, BaseCountrySelect,
        contractCardSkeleton, emptyState, cartModale, viewModale,
        baseProFilter, proModale
    },
    
    setup() {
        const router = useRouter();
        const route = useRoute(); // 👈 Accès à l'URL
        const proStore = useProStore();
        const cartStore = useCartStore();

        // 1. Initialiser avec ce qui se trouve dans l'URL (si présent)
        const activeDomainSlug = ref((route.query.domaine as string) || '');
        const activeCountryCode = ref('');
        const searchQuery = ref('');

        // Fonction centralisée pour la recherche
        const fetchPros = () => {
            proStore.getProfessionals(activeDomainSlug.value, activeCountryCode.value, searchQuery.value);
        }

        // 2. Gestionnaires de filtres
        const handleSearch = (query: string) => {
            searchQuery.value = query;
            fetchPros();
        };

        const handleDomainFilter = (slug: string) => {
            activeDomainSlug.value = slug;
            // 🪄 Met à jour l'URL dynamiquement quand on clique sur un bouton de baseProFilter
            router.push({ path: '/pro', query: { ...route.query, domaine: slug || undefined } });
            fetchPros();
        };

        const handleCountryFilter = (code: string) => {
            activeCountryCode.value = code;
            fetchPros();
        };

        // 3. 🪄 SURVEILLANCE : Si l'utilisateur clique sur la NavBox depuis CETTE page
        watch(() => route.query.domaine, (newDomain) => {
            const newSlug = (newDomain as string) || '';
            if (activeDomainSlug.value !== newSlug) {
                activeDomainSlug.value = newSlug;
                fetchPros(); // On relance la recherche instantanément
            }
        });

        // 4. Modales (inchangées)
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
            await proStore.getFilters();
            // On lance la recherche initiale en prenant en compte l'URL
            fetchPros(); 
        });

        return {
            router, cartStore, proStore, searchQuery, activeDomainSlug,
            handleSearch, handleDomainFilter, handleCountryFilter,
            isOpen, openModal, isViewOpen, openViewModal, addToCart
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
   TOOLBAR : filtre + recherche côte à côte
========================================== */
.toolbar {
    width: 100%;
    max-width: 1200px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    gap: 0.75rem;
    padding: 0.5rem;
}

.toolbar__filter {
    min-width: 0; 
    margin: 0; 
}

.toolbar__search {
    flex: 0 0 auto; 
}

:deep(.search-container.is-mobile.is-expanded) {
    width: auto;
    flex: 1 1 auto;
    min-width: 0;
}

/* ==========================================
   TABLETTE (>= 768px)
========================================== */
@media (min-width: 768px) {

    .toolbar__search {
        max-width: 360px;
        margin-left: auto; 
    }
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
</style>