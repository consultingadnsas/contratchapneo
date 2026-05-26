<template>
  <div class="contrat-card-section">
    <h2>Trouve le contrat qui te correspond</h2>

    <Basefilter/>

    <div class="cards-container">
        <contratCards 
          v-for="(contrat, index) in legalContrat" 
          :key="index"
          :contrat="contrat"
        />
    </div>

    <Paginator/>
  </div>
</template>

<script lang="ts">
import contratCards from '../../cards/contratCards.vue'
import Basefilter from '../../tools/Basefilter.vue'
import Paginator from '../../tools/Paginator.vue'
import { ref } from 'vue'

export default {
    components: {
        contratCards,
        Basefilter,
        Paginator
    },
    setup() {
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

        return {
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
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 6rem 1rem 1rem 1rem;
}

.contrat-card-section h2 {
    font-size: 2rem;
    font-weight: 500;
    line-height: 1.5;
}

.contrat-card-section p {
    font-size: 1.2rem;
    font-weight: 400;
}

/* 📱 MOBILE (Par défaut) : 1 colonne verticale */
.cards-container {
    width: 100%;
    max-width: 1400px;
    display: grid;
    grid-template-columns: 1fr;
    place-items: center;
    gap: 1rem; /* Un peu d'espace entre les cartes */
}

/* TABLETTE / IPAD (Écrans >= 768px) : 2 colonnes */
@media (min-width: 768px) {
    .cards-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* LAPTOP (Écrans >= 1024px) : 3 colonnes */
@media (min-width: 1024px) {
    .cards-container {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* DESKTOP (Écrans >= 1280px) : 4 colonnes */
@media (min-width: 1300px) {
    .cards-container {
        grid-template-columns: repeat(4, 1fr);
    }
}
</style>