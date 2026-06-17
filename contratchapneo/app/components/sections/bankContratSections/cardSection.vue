<template>
    <div class="contrat-card-section">
        
        <header class="w-full flex flex-col justify-center items-center gap-4">
            <h2>Découvrez tous nos contrats</h2>
            <p>Nos contrats sont conformes aux lois en vigueur dans l'espace OHADA.</p>
            <mainButton label="contrat sur mesure"/>
        </header>

        
        <div class="toolbar">
            <Basefilter class="toolbar__filter" />
            <BaseSearchInput 
                class="toolbar__search" 
                placeholder="Trouver un contrat..."
                v-model="searchQuery"
                theme="dark"
            />
        </div>

        <contractCardSkeleton v-if="contratStore.isLoading" />

        <emptyState
            v-else-if="contratStore.contracts.length === 0" 
            title = "Contrat non disponibile pour l'instant"
            description="Le contrat démandé n'est pas disponible pour l'instant. Faire un contrat sur mesure "
            @go-to="() => router.push('contractBank/customContrat')"
        />

        <template v-else>
            
         <div class="cards-container">
                <contratCards 
                    v-for="(contrat, index) in contratStore.contracts" 
                    :key="contrat.id || index"
                    :title="contrat.title"
                    :description="contrat.description"
                    :price="contrat.prix"
                    :image="contrat.picture || undefined"
                    @view="openViewModal(contrat.id)"
                    @buy="()=>{addTocart(contrat.id)}"
                />
            </div>
            
            <Paginator 
                :currentPage="contratStore.currentPage"
                :totalCount="contratStore.totalCount"
                :pageSize="contratStore.pageSize"
                @page-change="handlePageChange"
            />

        </template>

        <Teleport to="body">
            
            <cartModale
                :isOpen="isOpen" 
                @close="isOpen = false"
            />
            
            <viewModale
                :file="contratStore.contrat?.pdf_preview"
                v-if="isViewOpen" 
                @close="isViewOpen = false"
            />

            <cartBubble @open-cart="openModal()" />
        </Teleport>
    </div>
</template>

<script lang="ts">
import contratCards from '../../cards/contratCards.vue'
import contractCardSkeleton from '../../cards/contractCardSkeleton.vue'
import emptyState from '../../tools/emptyState.vue'
import Basefilter from '../../tools/Basefilter.vue'
import Paginator from '../../tools/Paginator.vue'
import BaseSearchInput from '../../input/BaseSearchInput.vue'
import cartModale from '../../modale/cartModale.vue'
import viewModale from '../../modale/viewModale.vue'
import cartBubble from '../../modale/cartBubble.vue'
import notifications from '../../tools/notifications.vue'
import mainButton from '../../buttons/mainButton.vue'

import { ref, onMounted, watch } from 'vue'
import {useContratStore} from '../../../stores/contratStore'
import {useCartStore} from '../../../stores/cartStore'
import { useRouter, useRoute } from 'vue-router'
import type { Contrat } from '../../../stores/contratStore'

export default {
    
    components: {
        contratCards,
        Basefilter,
        Paginator,
        BaseSearchInput,
        contractCardSkeleton,
        emptyState,
        cartModale,
        viewModale,
        cartBubble,
        notifications,
        mainButton
    },
    
    setup() {

        const router = useRouter();
        const route = useRoute();

        const contratStore = useContratStore();

        const cartStore = useCartStore();

        const activeCategoryId = ref((route.query.category as string) || '');

        const handlePageChange = (page: number) => {
            contratStore.getContracts(page, activeCategoryId.value);
        };

        // Make a query 
        const searchQuery = ref<string>('');

        let debounceTimeout: NodeJS.Timeout;

        // About cart view
        const isOpen = ref<boolean>(false);
        
        const openModal = ()=> {
            isOpen.value = true;
        }

        const addTocart = async (contratId: string) => {
            try {
                await cartStore.addToCart(contratId);
            } catch (error: any) {
                console.error("Erreur lors de l'ajout au panier", error)
            }
        }

        // About modalView
        const isViewOpen = ref<boolean>(false) // Votre deuxième booléen
        
        const openViewModal = async(contratId:string) => {
            await contratStore.getSpecificContract(contratId)
            isViewOpen.value = true; // On ouvre la deuxième modale
            console.log('The item selected', contratId)
        }

        onMounted(()=>{
            // On charge la première page de contrats
            contratStore.getContracts(1, activeCategoryId.value);
        })
        watch(
            () => route.query.category,
            (newCategoryId) => {
                activeCategoryId.value = (newCategoryId as string) || '';
                // On relance la recherche depuis la page 1 avec le nouveau filtre
                contratStore.getContracts(1, activeCategoryId.value);
            }
        );

        watch(searchQuery, (newQuery) => {
            
            clearTimeout(debounceTimeout);

            // On attends 600ms d'inactivité avant de lancer la requête
            debounceTimeout = setTimeout(()=> {
                // On va dans le store pour réccupérer le contrat concerné
                // paramètres: page=1, categorie, mot-clé
                contratStore.fetchContracts(1, activeCategoryId.value, newQuery),
                // Debug
                console.log("Recherche lancée pour :", newQuery)
            }, 500)
        })

        return {
            router,
            activeCategoryId,
            handlePageChange,
            searchQuery,
            debounceTimeout,
            contratStore,
            cartStore,

            // modale
            isOpen,
            openModal,
            isViewOpen,
            openViewModal,
            addTocart
        }
    }
}
</script>

<style scoped>

/* ==========================================
   1. STRUCTURE GLOBALE ET ZONE DE TRAVAIL
========================================== */
.contrat-card-section {
    position: relative;
    width: 100%;
    max-width: 1400px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    padding: 4rem 1rem 1rem 1rem;
    overflow: hidden; 
    background-color: #fdfcfc; 
}

/* ==========================================
   2. LE COFFRE NUMÉRIQUE (Arrière-plan)
========================================== */
.contrat-card-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 440px; 
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-bottom-left-radius: 48px;
    border-bottom-right-radius: 48px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
    z-index: 0;
}

/* ==========================================
   3. LES CONTRATS FLOTTANTS (Effet Verre)
========================================== */
.contrat-card-section::after {
    content: '';
    position: absolute;
    top: 20px;
    right: 8%;
    width: 280px;
    height: 380px;
    background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.01) 100%);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    transform: rotate(12deg);
    z-index: 0;
    pointer-events: none;
    transition: all 0.3s ease;
}

/* On force le contenu textuel et les cartes au premier plan */
.contrat-card-section > * {
    position: relative;
    z-index: 2;
}

/* ==========================================
   4. TYPOGRAPHIE ET EN-TÊTE
========================================== */
header {
    margin-top: 2rem;
    margin-bottom: 2rem;
    text-align: center;
    width: 100%;
}

header::before {
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    color: #34d399; 
    background: rgba(52, 211, 153, 0.1);
    padding: 0.4rem 1rem;
    border-radius: 50px;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(52, 211, 153, 0.2);
}

.contrat-card-section h2 {
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 1rem;
}

header p {
    font-size: 1.15rem;
    color: #cbd5e1;
    max-width: 550px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ==========================================
   5. TOOLBAR (Filtres & Recherche)
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
   6. GRILLE DE CARTES (Base Mobile)
========================================== */
.cards-container {
    width: 100%;
    max-width: 1400px;
    display: grid;
    grid-template-columns: 1fr;
    place-items: center;
    gap: 1.5rem;
}


/* ==========================================
   === MEDIA QUERIES (RESPONSIVE DESIGN) ===
========================================== */

/* 📱 SMARTPHONES (Max 767px) */
@media (max-width: 767px) {
    header {
        margin-bottom: 0.2rem !important; 
    }

    header.flex {
        gap: 0.75rem !important; 
    }

    .toolbar {
        margin-top: 0; 
        justify-content: center; 
        gap: 1rem; 
        width: 100%;
        max-width: 92%; 
        margin-left: auto; 
        margin-right: auto;
        position: relative;
        z-index: 3;
    }

    /* On réduit l'effet de verre pour ne pas polluer l'écran mobile */
    .contrat-card-section::after {
        right: -50px;
        top: -20px;
        transform: scale(0.6) rotate(15deg);
    }
}

/* 💊 TABLETTES (De 768px à 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
    .cards-container {
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }

    .toolbar {
        padding: 0.5rem 1rem;
    }

    .toolbar__search {
        max-width: 320px;
        margin-left: auto;
    }

    /* On réduit légèrement l'effet de verre pour qu'il ne chevauche pas le titre sur un iPad */
    .contrat-card-section::after {
        right: -20px;
        transform: scale(0.8) rotate(12deg);
    }
}

/* 💻 PETITS ÉCRANS & ORDINATEURS PORTABLES (De 1024px à 1279px) */
@media (min-width: 1024px) {
    /* 3 colonnes au lieu de 4 pour éviter des cartes trop écrasées sur petits PC */
    .cards-container {
        grid-template-columns: repeat(3, 1fr);
    }

    .toolbar__search {
        max-width: 360px;
        margin-left: auto;
    }
    .toolbar{
        padding:0%;
    }
}

/* 🖥️ GRANDS ÉCRANS (1280px et plus) */
@media (min-width: 1280px) {
    .cards-container {
        grid-template-columns: repeat(4, 1fr);
    }
}
</style>