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
                        v-for="(card, index) in legalPro" 
                        :key="index"
                        :title="card.title"
                    />
                </div>

                <div class="cards-container">
                    <packCards 
                        v-for="(card, index) in contratPack" 
                        :key="index"
                        :title="card.title"
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
        const legalPro = ref([
            { title: 'Contrat de travail' },
            { title: 'Contrat de freelance' },
            { title: 'Notaire' },
            { title: 'Juriste droit des affaires' }
        ]);

        const contratPack = ref([
            {title: 'Pack basic'},
            {title: 'Pack business'},
            {title: 'Pack business pro'}
        ])

        return { legalPro, contratPack };
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