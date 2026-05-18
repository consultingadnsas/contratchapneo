<template>
    <section class="main-section">
        <div class="wrapper-content">
            <div class="flex flex-col items-center justify-center gap-2">
                <h3>
                    Trouvez des contrats qui vous correspondent
                    <span>conformes aux lois en vigueur</span>
                </h3>
            </div>

            <!-- SECTION CONTRATS (inchangée : carrousel mobile / grille desktop) -->
            <div class="green-dark-section w-full flex justify-center items-center flex-col gap-4">
                <div class="subtitle-wrapper">
                    <h4 class="subtitle">Nos contrats les plus téléchargés</h4>
                    <div class="divider"></div>
                </div>
                
                <!-- Conteneur original avec sa classe "cards-container" -->
                <div class="cards-container">
                    <contratCards 
                        v-for="(card, index) in legalContrat" 
                        :key="index"
                        :title="card.title"
                        :description="card.description"
                        :subtitle="card.subtitle"
                    />
                </div>

                <mainButton label="voir tous nos contrats" />
            </div>

            <!-- SECTION CATÉGORIES (CARROUSEL AJOUTÉ) -->
            <div class="green-dark-section w-full flex justify-center items-center flex-col gap-4">
                <div class="subtitle-wrapper carousel-header">
                    <h4 class="subtitle">Nos catégories les plus vues</h4>
                    <div class="divider"></div>
                    <!-- Boutons de navigation du carrousel (uniquement pour catégories) -->
                    <div class="carousel-controls">
                        <button class="carousel-btn prev" @click="scrollPrev" aria-label="Précédent">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                            </svg>
                        </button>
                        <button class="carousel-btn next" @click="scrollNext" aria-label="Suivant">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                            </svg>
                        </button>
                    </div>
                </div>
                
                <!-- NOUVEAU carrousel pour les catégories (classes spécifiques) -->
                <div class="category-carousel-container" ref="carouselRef">
                    <div class="category-carousel-track">
                        <contratCategoryCards 
                            v-for="i in 8" 
                            :key="i"
                            :title="'Exemple ' + i"
                        />
                    </div>
                </div>

                <mainButton label="voir toutes nos catégories" />
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import contratCards from '../cards/contratCards.vue';
import contratCategoryCards from '../cards/contratCategoryCards.vue';

export default {
    name: 'OrdinarySection',
    components: { 
        mainButton, 
        contratCards,
        contratCategoryCards
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
    background: none;
}

.wrapper-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    width: 100%;
}

/* --- STYLES ORIGINAUX DES CONTRATS (carrousel mobile / grille desktop) --- */
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 2rem;
    padding: 0.5rem 1rem;
    width: 100%;
    scrollbar-width: thin;
}

.cards-container > * {
    flex: 0 0 85%;
    scroll-snap-align: start;
}

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

/* --- STYLES DU CARROUSEL POUR CATÉGORIES (NOUVEAU, sans impact sur les contrats) --- */
.subtitle-wrapper.carousel-header {
    display: flex;
    align-items: center;
    width: 100%;
    gap: 1rem;
    flex-wrap: wrap;
}

.carousel-controls {
    display: flex;
    gap: 0.5rem;
    margin-left: auto;
}

.carousel-btn {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    color: var(--primary-color, #4ade80);
}

.carousel-btn svg {
    width: 20px;
    height: 20px;
}

.carousel-btn:hover {
    background: var(--primary-color, #4ade80);
    color: white;
    border-color: var(--primary-color, #4ade80);
    transform: scale(1.05);
}

.category-carousel-container {
    width: 100%;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    scrollbar-width: thin;
}

.category-carousel-container::-webkit-scrollbar {
    height: 6px;
}

.category-carousel-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.category-carousel-container::-webkit-scrollbar-thumb {
    background: var(--primary-color, #4ade80);
    border-radius: 10px;
}

.category-carousel-track {
    display: flex;
    gap: 1.5rem;
    width: max-content;
    padding: 0.5rem 0;
}

.category-carousel-track > * {
    flex-shrink: 0;
    scroll-snap-align: start;
    width: 240px;
}

/* Responsive du carrousel catégories */
@media (max-width: 767px) {
    .category-carousel-track > * {
        width: 85vw;
        max-width: 280px;
    }
    .carousel-controls {
        margin-left: 0;
        width: 100%;
        justify-content: flex-end;
    }
}

@media (min-width: 768px) {
    .category-carousel-track > * {
        width: 220px;
    }
}

/* --- Autres styles partagés (inchangés) --- */
.subtitle-wrapper {
    display: flex;
    align-items: center;
    width: 100%;
    gap: 1rem;
    padding: 0 1rem;
}

.subtitle {
    font-size: 1.1rem;
    font-weight: 600;
    color: currentColor;
    white-space: nowrap;
}

.divider {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--primary-color, #4ade80), transparent);
    opacity: 0.6;
}

@media (min-width: 768px) {
    .subtitle-wrapper {
        padding: 0;
    }
    .subtitle {
        font-size: 1.3rem;
    }
}
</style>