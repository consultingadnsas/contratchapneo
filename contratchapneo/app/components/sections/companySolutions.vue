<template>
    <section class="main-section" data-aos="fade-up" data-aos-duration="3000">
        <!-- Flaque décorative étendue en bas -->
        <div class="puddle-bg"></div>
        <h3>
            Découvrez nos packs adaptés à
            <span>vos besoins</span>
        </h3>
        <div class="cards-container">
            <packCards
                v-for="(card, index) in contratPack"
                :key="index"
                :title="card.title"
                :price="card.price"
                :oldPrice="card.oldPrice"
                :features="card.features"
                :planType="card.plan"
                :description="card.description"
            />
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import packCards from '../cards/packCards.vue';
import mainButton from '../buttons/mainButton.vue';

export default {
    name: 'CompanySection',
    components: {
        packCards,
        mainButton
    },
    setup() {
        const contratPack = ref([
            {
                title: 'Pack basic',
                price: '29 000 FCFA',
                oldPrice: '400 000 FCFA',
                features: [
                    'Accès à 10 documents juridiques payants',
                    'Très petites entreprises ou consultants individuels'
                ],
                plan: 'basique',
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
                plan: 'business',
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
                plan: 'business-pro',
                description: 'Profitez de la pleine puissance de Contratchap. Accédez à une panoplie de contrats, de service, de conseil, et de nos outils de calcules'
            }
        ]);

        return {
            contratPack
        };
    }
};
</script>

<style lang="css" scoped>
.main-section {
    width: 100%;
    position: relative;
    top: -130px;
    overflow: hidden;
    position: relative;
}

/* Flaque décorative qui borde tout le bas de la section */
.puddle-bg {
    position: absolute;
    bottom: -20px;
    left: -5%;
    width: 110%;
    height: 250px;
    background: #32f459;
    /* Forme de vague qui s'étale horizontalement */
    border-radius: 50% 50% 0 0 / 60% 60% 0 0;
    filter: blur(30px);
    opacity: 0.15;
    z-index: 0;
    pointer-events: none;
}

.main-section h3 {
    text-align: center;
    font-size: 1.6rem;
    padding: 1rem;
    font-weight: 700;
    color: #111827;
}

/* --- SECTION DESCRIPTION & IMAGE (Mobile First) --- */
.business-pic-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1rem;
    width: 100%;
    box-sizing: border-box;
}

.description h4 {
    font-size: 1.2rem;
    font-weight: 600;
    line-height: 1.4;
    color: #1f2937;
    margin-bottom: 0.5rem;
}

.description p {
    font-size: 0.95rem;
    line-height: 1.5;
    color: #4b5563;
    margin: 0;
}

/* Le conteneur de l'image qui porte le dégradé */
.pic-container {
    position: relative;
    width: 100%;
    height: 240px;
    border-radius: 1.25rem;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.pic-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.pic-container::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.4) 0%, transparent 70%);
    pointer-events: none;
}

/* --- CONTENEUR DES CARTES (Mobile) --- */
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1rem;
    padding: 0.5rem;
    width: 100%;
    scrollbar-width: none;
    border-radius: 1rem;
}

.cards-container::-webkit-scrollbar {
    display: none;
}

/* --- RESPONSIVE --- */
@media (min-width: 768px) {
    .main-section h3 {
        font-size: 2.2rem;
        padding: 3rem 1rem 2rem 1rem;
    }

    .business-pic-wrapper {
        flex-direction: row;
        align-items: center;
        gap: 3rem;
        padding: 2rem 3rem;
    }

    .description {
        flex: 1;
    }

    .description h4 {
        font-size: 1.8rem;
    }

    .description p {
        font-size: 1.1rem;
    }

    .pic-container {
        flex: 1;
        height: 360px;
    }

    .pic-container::after {
        background: linear-gradient(to top, rgba(0, 0, 0, 0.3), transparent);
    }

    .cards-container {
        padding: 2rem 3rem;
        justify-content: center;
        overflow-x: visible;
    }
}

@media (min-width: 1024px) {
    .business-pic-wrapper {
        max-width: 1200px;
        margin: 0 auto;
    }

    .description h4 {
        font-size: 2.2rem;
    }
}
</style>