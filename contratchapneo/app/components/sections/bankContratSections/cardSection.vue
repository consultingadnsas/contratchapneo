<template>
    <div class="contrat-card-section">
        
        <header>
            <h2>Découvrez tous nos contrats</h2>
            <p>Nos contrats sont conformes aux lois en vigueur dans l'espace OHADA.</p>
        </header>

        
        <div class="toolbar">
            <Basefilter class="toolbar__filter" />
            <BaseSearchInput class="toolbar__search" placeholder="Rechercher un article ou un produit..."/>
        </div>

        <contractCardSkeleton v-if="contratStore.isLoading" />

        <emptyState
            v-else-if="contratStore.contracts.length === 0" 
            title = "Contrat non disponibile pour l'instant"
            description="Le contrat démandé n'est pas disponible pour l'instant. Faire un contrat sur mesure "
            @go-to="()=>router.push('contractBank/customContrat')"
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

import { ref, onMounted } from 'vue'
import {useContratStore} from '../../../stores/contratStore'
import { useRouter } from 'vue-router'

export default {
    components: {
        contratCards,
        Basefilter,
        Paginator,
        BaseSearchInput,
        contractCardSkeleton,
        emptyState,
        cartModale,
        viewModale
    },
    setup() {

        const router = useRouter();

        const contratStore = useContratStore();

        const activeCategoryId = ref('');

        const handlePageChange = (page: number) => {
            contratStore.getContracts(page, activeCategoryId.value);
        };

        // About cart view
        const isOpen = ref<boolean>(false);
        
        const openModal = () => {
            isOpen.value = true;
        }

        // About modalView
        const isViewOpen = ref<boolean>(false) // Votre deuxième booléen
        
        const openViewModal = async(contratId:string) => {
            await contratStore.getSpecificContract(contratId)
            isViewOpen.value = true; // On ouvre la deuxième modale
            console.log('The item selected', contratId)
        }

        onMounted(()=>{
            contratStore.getContracts(1);
        })

        return {
            router,
            activeCategoryId,
            handlePageChange,
            contratStore,

            // modale
            isOpen,
            openModal,
            isViewOpen,
            openViewModal
        }
    }
}
</script>

<style scoped>
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
    font-size: 2rem;
    font-weight: 500;
    line-height: 1.5;
    color: var(--primary-color);
}

header{
    margin-top: 2rem;
    margin-bottom: 1rem;
}

header p{
    font-size: 1.2rem;
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

/* Sur mobile : le select prend sa place naturelle (auto),
   la loupe est un bouton rond fixe → rien ne disparaît */
.toolbar__filter {
    min-width: 0;     /* évite le débordement flex */
    margin: 0;        /* retire le margin: 1rem 0 du composant */
}

.toolbar__search {
    flex: 0 0 auto;   /* taille naturelle (bouton rond) par défaut */
}

/* Quand la recherche s'étend sur mobile, elle ne chasse pas le filtre :
   on lui donne une largeur fixe max plutôt que 100% */
:deep(.search-container.is-mobile.is-expanded) {
    width: auto;
    flex: 1 1 auto;
    min-width: 0;
}

/* ==========================================
   TABLETTE (>= 768px) : recherche toujours visible
========================================== */
@media (min-width: 768px) {
    .toolbar__filter {
        
    }

    .toolbar__search {
        max-width: 360px;
        margin-left: auto; /* pousse la recherche à droite */
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