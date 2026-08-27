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
                <!-- Groupe : Contrat sur mesure -->
                <div class="action-wrapper">
                    <div class="icon-bubble bubble-primary" @click="router.push('/contractBank/customContrat')">
                        <!-- Icône : Document avec stylo -->
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                        </svg>
                    </div>
                    <button class="btn-primary btn-inline" @click="router.push('/contractBank/customContrat')">
                        Contrat sur mesure
                    </button>
                </div>
                
                <!-- Groupe : Révision de contrat -->
                <div class="action-wrapper">
                    <div class="icon-bubble bubble-secondary" @click="router.push('/etudeContrat')">
                        <!-- Icône : Document avec loupe -->
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 0 1 9 9v.375M10.125 2.25A3.375 3.375 0 0 1 13.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 0 1 3.375 3.375M9 15l2.25 2.25L15 12" />
                        </svg>
                    </div>
                    <button class="btn-secondary btn-inline" @click="router.push('/etudeContrat')">
                        Révision de contrat
                    </button>
                </div>
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
                    <contratCardsDynamic 
                        v-for="(contrat, index) in contratStore.contracts" 
                        :key="contrat.id || index"
                        :title="contrat.title"
                        :description="contrat.description"
                        :price="contrat.prix"
                        :promoPrice="contrat.promo_price"
                        :image="contrat.picture || undefined"
                        @view="openViewModal(contrat.id)" 
                        @contrat-checkout="addTocart(contrat.id)"
                        @generate="fillContract(contrat.id)"
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
                v-for="pack in packStore.packs" 
                :key="pack.id"
                :title="pack.title"
                :description="pack.description"
                :price="pack.prix"
                :promoPrice="pack.prix_promo" 
                :nombreCredits="pack.nombre_credits"
                :nombreCustomedContract="pack.nombre_customed_contract"
                :nombreCartesPro="pack.nombre_cartes_pro"
                :dureeValiditeJours="pack.duree_validite_jours"
                :planType="pack.prix < 30000 ? 'basique' : (pack.prix < 60000 ? 'business' : 'business-pro')"
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
import contratCardsDynamic from '../../cards/contratCardsDynamic.vue'

import { ref, onMounted, watch } from 'vue'
import { useContratStore } from '../../../stores/contratStore'
import { useCartStore } from '../../../stores/cartStore'
import { useProfileStore } from '../../../stores/profileStore'
import { useRouter, useRoute } from 'vue-router'
import { usePackStore } from '../../../stores/packStore'

export default {
    components: {
        packCards, contratCardsDynamic,
        contratCards, Basefilter, Paginator, BaseSearchInput,
        contractCardSkeleton, emptyState, cartModale, viewModale,
        cartBubble, notifications, mainButton
    },
    
    setup() {
        const router = useRouter();
        const route = useRoute();
        const contratStore = useContratStore();
        const cartStore = useCartStore();
        const profileStore = useProfileStore();
        const packStore = usePackStore();

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
                // 1. On ajoute au panier
                await cartStore.addToCart(contratId);
                
                // 2. ⚡️ NOUVEAU : On redirige immédiatement vers la page de checkout
                router.push('/order/checkout/'); 
                
            } catch (error: any) {
                console.error("Erreur lors de l'ajout au panier", error);
            }
        }

        const fillContract = async (contractId: string) => {
            try {
                router.push(`/contractwritter/${contractId}`);
                console.log("Redirection directe vers la génération :", contractId);
            } catch (err: any) {
                console.warn("Erreur lors de la redirection :", err);
            }
        }

        const isViewOpen = ref<boolean>(false);
        const textToShow = ref<string | null>(null);
        
       const openViewModal = async(contratId:string) => {
            
            // ⚡️ CORRECTION : On vérifie s'il possède au moins un pack actif
            if (profileStore.activePacks && profileStore.activePacks.length > 0) {
                
                // Il a un abonnement valide -> Go au remplissage !
                fillContract(contratId);

            } else {
                
                // Il n'a pas d'abonnement (ou est déconnecté) -> Modale d'aperçu
                await contratStore.getSpecificContract(contratId);
                textToShow.value = contratStore.contrat?.document_preview;
                isViewOpen.value = true; 
                
            }
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
            // ⚡️ AJOUT INDISPENSABLE : On charge les packs de l'utilisateur s'ils ne sont pas en mémoire
            if (profileStore.userPacks.length === 0) {
                profileStore.getPacks();
            }

            // Ton code de recherche existant :
            if (searchQuery.value) {
                contratStore.fetchContracts(1, activeCategoryId.value, searchQuery.value);
            } else {
                contratStore.getContracts(1, activeCategoryId.value);
            }

            if (packStore.packs.length === 0) {
                packStore.fetchPacks();
            }
        });

        return {
            router, activeCategoryId, handlePageChange, searchQuery,
            contratStore, cartStore, profileStore, textToShow, isOpen, openModal,
            isViewOpen, openViewModal, addTocart, fillContract,
            packagesList, packStore // 👈 Exposer la liste au template
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
    justify-content: center;
    align-items: flex-end; /* Aligne les boutons vers le bas */
    gap: 0.5rem; /* Espace entre les deux blocs */
    width: 100%;
    max-width: 850px;
    margin-top: 2.5rem;
}

.action-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    flex: 1;
    max-width: 280px; 
}

/* ⚡️ STYLE DES BULLES */
.icon-bubble {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.15); /* Fond transparent léger */
    backdrop-filter: blur(10px); /* Effet verre */
    border: 1px solid rgba(255, 255, 255, 0.15);
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

.icon-bubble svg {
    width: 32px;
    height: 32px;
    transition: all 0.3s ease;
}

.bubble-primary svg { color: #39acff; }
.bubble-secondary svg { color: #ffffff; }

/* Animations au survol du groupe complet */
.action-wrapper:hover .icon-bubble {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.15);
}

.action-wrapper:hover .bubble-secondary svg {
    color: #10b981; /* Devient vert comme la bordure du bouton */
}

.btn-inline {
    flex: 1; 
    max-width: none; 
    font-weight: 600;
}
.btn-primary{
    background: transparent;
    color: #39acff;
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
    font-weight: 400;
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
        gap: 1rem; /* Moins d'espace sur mobile */
        margin-top: 1.5rem;
    }

    .icon-bubble {
        width: 50px;
        height: 50px;
    }

    .icon-bubble svg {
        width: 24px;
        height: 24px;
    }

    .action-wrapper {
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