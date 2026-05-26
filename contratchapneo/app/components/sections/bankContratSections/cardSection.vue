<template>
  
    <div class="contrat-card-section">

        <contratCards v-for="i in 4" :key="i"/>

    </div>

</template>

<script lang="ts">
import contratCards from '../../cards/contratCards.vue'
import {ref} from 'vue'

export default {
    components:{
        contratCards
    },
    setup(){

        const legalContrat = ref([
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
.contrat-card-section{

    width: 100%;
    max-width: 1400px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 1rem;
}
</style>