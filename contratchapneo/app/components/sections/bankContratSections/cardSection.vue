<template>
    <div class="contrat-card-section">
        
        <header>
            <h2>
                Découvrez tous nos contrats
            </h2>
            <p>Nos contrats sont conformes aux lois en vigeur dans l'espace OHADA.</p>
        </header>
        
        <div class="toolbar">
            <Basefilter class="toolbar__filter"/>
            <BaseSearchInput class="toolbar__search" placeholder="Rechercher un article ou un produit..."/>
        </div>

        <div class="cards-container" v-if="!contratStore.isLoading">
            <contratCards 
                v-for="(contrat, index) in contratStore.contracts" 
                :key="index"
                :title="contrat.title"
                :description="contrat.description"
                :image="contrat.picture ? contrat.picture : undefined"
            />
        </div>

        <contractCardSkeleton v-if="contratStore.isLoading"/>

        <Paginator/>
    </div>
</template>

<script lang="ts">
import contratCards from '../../cards/contratCards.vue'
import contractCardSkeleton from '../../cards/contractCardSkeleton.vue'
import Basefilter from '../../tools/Basefilter.vue'
import Paginator from '../../tools/Paginator.vue'
import BaseSearchInput from '../../input/BaseSearchInput.vue'
import { ref, onMounted } from 'vue'

import {useContratStore} from '../../../stores/contratStore'

export default {
    components: {
        contratCards,
        Basefilter,
        Paginator,
        BaseSearchInput,
        contractCardSkeleton
    },
    setup() {

        const contratStore = useContratStore();

        const legalContrat = ref([
            { title: 'Contrat de travail' , subtitle: '100% Gratuit', description: 'Un contrat de travail est un accord entre un employeur et son employé.'},
            { title: 'Contrat de freelance', subtitle: '15 000 FCFA', description: 'Un contrat de freelance est un accord entre un travailleur indépendant et un client.'},
            { title: 'contrat de vente', subtitle: '40 000 FCFA', description: 'Un contrat de vente est un accord entre un vendeur et un acheteur.'},
            { title: 'contrat de bail', subtitle: '5 000 FCFA', description: 'Un contrat de bail est un accord entre un propriétaire et un locataire.'},
            { title: 'Contrat de travail' , subtitle: '100% Gratuit', description: 'Un contrat de travail est un accord entre un employeur et son employé.'},
            { title: 'Contrat de freelance', subtitle: '15 000 FCFA', description: 'Un contrat de freelance est un accord entre un travailleur indépendant et un client.'},
            { title: 'contrat de vente', subtitle: '40 000 FCFA', description: 'Un contrat de vente est un accord entre un vendeur et un acheteur.'},
            { title: 'contrat de bail', subtitle: '5 000 FCFA', description: 'Un contrat de bail est un accord entre un propriétaire et un locataire.'},
        ]);

        onMounted(()=>{
            contratStore.getContracts();
        })

        return {
            contratStore,
            legalContrat
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
    padding: 6rem 1rem 1rem 1rem;
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