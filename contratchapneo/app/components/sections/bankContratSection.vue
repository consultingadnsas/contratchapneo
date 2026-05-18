<template>
    <section class="main-section">
        <div class="wrapper-content">
            <div class="flex flex-col items-center justify-center gap-2">
                <h3>
                    Trouvez des contrats qui vous correspondent
                    <span>conformes aux lois en vigueur</span>
                </h3>
                <mainButton label="consulter un pro" />
            </div>

            <div class="green-dark-section w-full flex justify-center items-center flex-col gap-4">
                <!-- Conteneur responsive : carrousel mobile, grille desktop -->
                <div class="cards-container">
                    <contratCards 
                        v-for="(card, index) in legalContrat" 
                        :key="index"
                        :title="card.title"
                        :description="card.description"
                        :subtitle="card.subtitle"
                    />
                </div>
            </div>

        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import prodCards from '../cards/proCards.vue';
import contratCards from '../cards/contratCards.vue';
import packCards from '../cards/packCards.vue';

export default {
    name: 'OrdinarySection',
    components: { 
        mainButton, 
        prodCards, 
        contratCards,
        packCards
    },
    setup() {
        const legalContrat = ref([
            { title: 'Contrat de travail' , subtitle: '100% Gratuit', description: 'Un contrat de travail est un accord entre un employeur et un employé qui définit les termes et conditions de l\'emploi.'},
            { title: 'Contrat de freelance', subtitle: '15000 FCFA' },
            { title: 'contrat de vente', subtitle: '100% Gratuit' },
            { title: 'contrat de bail', subtitle: '5000 FCFA' },
        ]);

        return { legalContrat, };
    }
}
</script>

<style scoped>
.main-section {
    padding: 2rem 0;
    background: #e4e4e4;
}

.wrapper-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    width: 100%;
}

/* --- Carrousel mobile (par défaut) --- */
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1rem;
    padding: 0.5rem 1rem;
    width: 100%;
    scrollbar-width: thin;
}

.cards-container > * {
    flex: 0 0 85%;
    scroll-snap-align: start;
}

/* --- Grille à partir de 768px (tablette et desktop) --- */
@media (min-width: 768px) {
    .cards-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        overflow-x: visible;
        scroll-snap-type: none;
        padding: 0;
    }

    .cards-container > * {
        flex: auto;
        scroll-snap-align: none;
    }
}
</style>