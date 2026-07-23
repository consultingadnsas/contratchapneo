<template>
    <div class="contrat-card-section">
        
        <header class="hero-header">
            <h2>Découvrez tous nos contrats</h2>
            <p>Télécharger vos contrats en un clic !</p>
            <div class="search-container-large">
                <BaseSearchInput 
                    class="large-search" 
                    placeholder="Rechercher un modèle de contrat..."
                    v-model="searchQuery"
                    theme="light"
                />
            </div>

            <div class="action-buttons">
                <button class="btn-primary btn-inline" @click="router.push('/contractBank/customContrat')">
                    Contrat sur mesure
                </button>
                
                <button class="btn-secondary btn-inline" @click="router.push('/etudeContrat')">
                    Révision de contrat
                </button>
            </div>
        </header>

        <div v-if="searchQuery.trim() !== '' || activeCategoryId !== ''" class="search-results-section">
            
            <div class="filter-toolbar">
                <Basefilter class="toolbar__filter" />
            </div>

            <contractCardSkeleton v-if="contratStore.isLoading" />

            <emptyState
                v-else-if="contratStore.contracts.length === 0" 
                title="Aucun contrat trouvé"
                description="Aucun modèle ne correspond à votre recherche actuelle."
                textAction="Faire un contrat sur mesure"
                type="contrat"
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

        </div>

        <div v-else class="packages-section">
            <div class="packages-header">
                <h3>Nos offres de contrats</h3>
                <p>Choisissez le pack qui correspond le mieux à vos besoins pour économiser.</p>
            </div>
            
            <div class="packages-grid">
                <packCards 
                    v-for="(pack, index) in packagesList" 
                    :key="index"
                    :planType="pack.planType"
                    :title="pack.title"
                    :price="pack.price"
                    :description="pack.description"
                    :features="pack.features"
                    :buttonLabel="pack.buttonLabel"
                />
            </div>
        </div>

        <Teleport to="body">
            <cartModale
                :isOpen="isOpen" 
                @close="isOpen = false"
            />
            
            <viewModale
                v-if="isViewOpen" 
                :contract="contratStore.contrat"
                @close="isViewOpen = false"
                @buy="(id) => { addTocart(id); isViewOpen = false; }"
            />

            <cartBubble @open-cart="openModal()" />
        </Teleport>
    </div>
</template>

<script lang="ts">
// 👈 IMPORT DU COMPOSANT PACKCARDS
import packCards from '../../cards/packCards.vue' 

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
import { useContratStore } from '../../../stores/contratStore'
import { useCartStore } from '../../../stores/cartStore'
import { useRouter, useRoute } from 'vue-router'

export default {
    components: {
        packCards, // 👈 Ajout dans les composants déclarés
        contratCards, Basefilter, Paginator, BaseSearchInput,
        contractCardSkeleton, emptyState, cartModale, viewModale,
        cartBubble, notifications, mainButton
    },
    
    setup() {
        const router = useRouter();
        const route = useRoute();
        const contratStore = useContratStore();
        const cartStore = useCartStore();

        const activeCategoryId = ref((route.query.category as string) || '');
        const searchQuery = ref((route.query.q as string) || '');
        let debounceTimeout: NodeJS.Timeout;

        // 📦 DONNÉES DES PACKAGES 
        // Tu peux modifier ces informations pour qu'elles correspondent à tes vraies offres
        const packagesList = ref([
            {
                title: 'Pack basic',
                price: '29 000 FCFA',
                oldPrice: '400 000 FCFA',
                features: [
                    'Accès à 10 documents juridiques payants',
                    'Très petites entreprises ou consultants individuels'
                ],
                planType: 'basique',
                description: 'Packs idéal pour les petites entreprises'
            },
            {
                title: 'Pack business',
                price: '49 000 FCFA',
                oldPrice: '1 000 000 FCFA',
                features: [
                    'Accès à 12 documents juridiques payants',
                    'Rédaction sur-mesure d\'un document juridique',
                    'PME et startups de moins de 10 employés avec un volume de tache juridique modéré'
                ],
                planType: 'business',
                description: 'Accédez à une fourniture de contrat bien plus épurée et d\'autres avantages intéressant'
            },
            {
                title: 'Pack business pro',
                price: '99 000 FCFA',
                oldPrice: '1 500 000 FCFA',
                features: [
                    'Accès à 25 documents juridiques payants',
                    'Rédaction sur-mesure de 3 documents juridiques',
                    'Suivi par une équipe de juriste(appui & conseils personnalisés)',
                    'PME et startups de plus de 10 employés avec un volume de tache juridique important'
                ],
                planType: 'business-pro',
                description: 'Profitez de la pleine puissance de Contratchap. Accédez à une panoplie de contrats, de service, de conseil, et de nos outils de calcules'
            }
        ]);

        const handlePageChange = (page: number) => {
            if (searchQuery.value) {
                contratStore.fetchContracts(page, activeCategoryId.value, searchQuery.value);
            } else {
                contratStore.getContracts(page, activeCategoryId.value);
            }
        };

        const isOpen = ref<boolean>(false);
        const openModal = () => { isOpen.value = true; }

        const addTocart = async (contratId: string) => {
            try {
                await cartStore.addToCart(contratId);
            } catch (error: any) {
                console.error("Erreur lors de l'ajout au panier", error)
            }
        }

        const isViewOpen = ref<boolean>(false);
        const textToShow = ref<string | null>(null);
        
        const openViewModal = async(contratId:string) => {
            await contratStore.getSpecificContract(contratId);
            textToShow.value = contratStore.contrat?.document_preview;
            isViewOpen.value = true; 
        }

        watch(() => route.query.category, (newCategoryId) => {
            activeCategoryId.value = (newCategoryId as string) || '';
            if (searchQuery.value) {
                contratStore.fetchContracts(1, activeCategoryId.value, searchQuery.value);
            } else {
                contratStore.getContracts(1, activeCategoryId.value);
            }
        });

        watch(searchQuery, (newQuery) => {
            clearTimeout(debounceTimeout);
            debounceTimeout = setTimeout(() => {
                if (newQuery.trim() !== '') {
                    contratStore.fetchContracts(1, activeCategoryId.value, newQuery);
                }
            }, 500);
        });

        onMounted(() => {
            if (searchQuery.value) {
                contratStore.fetchContracts(1, activeCategoryId.value, searchQuery.value);
            } else {
                contratStore.getContracts(1, activeCategoryId.value);
            }
        });

        return {
            router, activeCategoryId, handlePageChange, searchQuery,
            contratStore, cartStore, textToShow, isOpen, openModal,
            isViewOpen, openViewModal, addTocart,
            packagesList // 👈 Exposer la liste au template
        }
    }
}
</script>

<style scoped>
/* ==========================================
   1. STRUCTURE GLOBALE
========================================== */
.contrat-card-section {
    position: relative;
    width: 100%;
    max-width: 1400px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding: 10rem 1rem 1rem 1rem;
    overflow: hidden; 
    background:linear-gradient(to bottom, #000000, #61a2d7); 
}

.contrat-card-section > * {
    position: relative;
    z-index: 2;
}

/* ==========================================
   ANIMATIONS DES TRANSITIONS
========================================== */
.search-results-section,
.packages-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: fadeIn 0.5s ease-out forwards;
}

.search-results-section { gap: 1.5rem; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ==========================================
   NOUVEAU : ZONE DES PACKAGES
========================================== */
.packages-header {
    text-align: center;
    margin: 2rem 0;
}

.packages-header h3 {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.packages-header p {
    color: #cbd5e1;
    font-size: 1.05rem;
}

.packages-grid {
    width: 100%;
    max-width: 1300px;
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
    place-items: center;
    margin-top: 1rem;
}

/* ==========================================
   2. EN-TÊTE STYLE GOOGLE (Recherche + Boutons)
========================================== */
.hero-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
    max-width: 1000px;
    margin: 0 auto 0.5rem auto;
    gap: 1.2rem;
}

.hero-header h2 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: #ffffff; 
    margin-bottom: 0.5rem;
}

.hero-header p {
    font-size: 1.1rem;
    color: #cbd5e1; 
    max-width: 550px;
    margin: 0 auto;
    line-height: 1.5;
}

.search-container-large {
    min-width: 70%;
    display: flex;
    align-items: center;
}

.search-container-large :deep(.search-container),
.search-container-large :deep(input) {
    height: 75px; 
    border-radius: 50px;
    width: 100%;
}

/* Styles spécifiques à la boîte englobante */
.search-container-large :deep(.search-container) {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    background: #ffffff;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

/* Styles spécifiques au champ de texte */
.search-container-large :deep(input) {
    font-size: 1.2rem;
    background: transparent;
    border: none;
    outline: none;
    /* ⚡️ C'EST ICI QUE LA MAGIE OPÈRE : On pousse le texte vers la droite */
    padding-left: 4rem; /* Ajuste cette valeur (ex: 3.5rem ou 4.5rem) selon la taille de l'icône */
}

.search-container-large :deep(input:focus) {
    box-shadow: 0 4px 20px rgba(52, 211, 153, 0.3);
    border-color: #34d399;
}

.action-buttons {
    display: flex;
    flex-direction: row; 
    gap: 0.5rem;
    justify-content: center;
    align-items: center;
    width: 100%;
    max-width: 850px;
    margin-top: 2.5rem
}

.btn-inline {
    flex: 1; 
    max-width: 250px; 
    font-weight: 600;
}
.btn-primary{
    background: transparent;
    color: var(--primary-color);
    padding: 0 24px;
    height: 48px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    backdrop-filter: blur(10px);
    white-space: nowrap;
}

.btn-primary:hover{
    color:#ffffff;
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(52, 211, 153, 0.2);
}

.btn-secondary {
    background: transparent; 
    color: #ffffff;
    padding: 0 24px;
    height: 48px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    backdrop-filter: blur(10px);
    white-space: nowrap; 
}

.btn-secondary:hover {
    border-color: #34d399;
    color: #10b981;
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(52, 211, 153, 0.2);
}

/* ==========================================
   3. BARRE DE FILTRES
========================================== */
.filter-toolbar {
    width: 100%;
    max-width: 1400px;
    display: flex;
    justify-content: flex-start;
    padding: 0 0.5rem;
    margin-bottom: 0.5rem;
}

.toolbar__filter { min-width: 0; margin: 0; }

/* ==========================================
   4. GRILLE DE CARTES (CONTRATS)
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
    .hero-header { padding: 0 1rem; }
    
    /* ⚡️ NOUVEAU : On réduit la hauteur et la police de la barre de recherche */
    .search-container-large {
        min-width: 100%; /* S'assure qu'elle prend toute la largeur dispo sur mobile */
    }
    
    .search-container-large :deep(.search-container),
    .search-container-large :deep(input) {
        height: 55px; /* Hauteur beaucoup moins massive */
    }

    .search-container-large :deep(input) {
        font-size: 1rem; /* Texte légèrement plus petit */
        padding-left: 3.5rem; /* On réduit aussi un peu le décalage sur mobile */
    }

    .action-buttons {
        gap: 0.5rem; 
    }

    .btn-secondary, :deep(.main-btn) {
        font-size: 0.85rem;
        padding: 0 10px;
        height: 44px;
        max-width: none;
    }

    .filter-toolbar { justify-content: center; }

    .btn-inline {
        flex: 1; 
        width: 50px; 
        font-weight: 600;
    }
}


/* 💊 TABLETTES (De 768px à 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
    .cards-container { grid-template-columns: repeat(2, 1fr); }
    .packages-grid { grid-template-columns: repeat(2, 1fr); align-items: stretch; }
}

/* 💻 PETITS ÉCRANS & ORDINATEURS PORTABLES (De 1024px à 1279px) */
@media (min-width: 1024px) {
    .cards-container { grid-template-columns: repeat(3, 1fr); }
    .packages-grid { grid-template-columns: repeat(3, 1fr); align-items: stretch; }
}

/* 🖥️ GRANDS ÉCRANS (1280px et plus) */
@media (min-width: 1280px) {
    .cards-container { grid-template-columns: repeat(4, 1fr); }
}
</style>