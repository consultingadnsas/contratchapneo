<template>
    <section class="main-section pack-section">
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
                :planType="card.planType"
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
    top: -90px;
    bottom: 10px;
    overflow: hidden;
    background: #98f7abdd;
    padding-bottom: 3rem;
}

/* Flaque décorative qui borde tout le bas de la section */
.puddle-bg {
    position: absolute;
    bottom: -20px;
    left: -5%;
    width: 110%;
    height: 250px;
    background: #32f459;
    border-radius: 50% 50% 0 0 / 60% 60% 0 0;
    filter: blur(30px);
    opacity: 0.15;
    z-index: 0;
    pointer-events: none;
}

.main-section h3 {
    text-align: center;
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    padding: 2rem 1rem 1rem 1rem;
    font-weight: 700;
    color: #111827;
}

/* --- CONTENEUR DES CARTES (Scroll horizontal forcé) --- */
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1.5rem;
    padding: 1.5rem 1rem 3rem 1rem; 
    width: 100%;
    box-sizing: border-box;
    scrollbar-width: none; 
    -webkit-overflow-scrolling: touch; 
}

.cards-container::-webkit-scrollbar {
    display: none;
}

/* Taille de base des cartes (Mobile) */
.cards-container > * {
    flex: 0 0 280px; 
    scroll-snap-align: center; 
}

/* ── 📐 TABLETTES (A partir de 768px) ── */
@media (min-width: 768px) {
    .cards-container {
        padding: 2rem 2rem 3rem 2rem;
        gap: 2rem;
    }
    
    .cards-container > * {
        flex: 0 0 340px; 
    }
}

/* ── 💻 PETITS DESKTOP & IPAD PRO (A partir de 1024px) ── */
@media (min-width: 1024px) {
    .main-section h3 {
        font-size: 2.2rem;
        padding: 3rem 1rem 2rem 1rem;
    }

    .cards-container {
        max-width: 1300px;
        margin: 0 auto;
        /* 👈 SUPPRESSION DU justify-content: center ICI */
    }

    .cards-container > * {
        flex: 0 0 380px; 
    }
}

/* ── 🖥️ GRANDS ÉCRANS (A partir de 1280px) ── */
@media (min-width: 1280px) {
    .cards-container {
        /* 👈 On ne centre les cartes QUE lorsqu'on est absolument 
           sûr qu'elles rentrent toutes sans déborder de l'écran ! */
        justify-content: center; 
    }
}
</style>