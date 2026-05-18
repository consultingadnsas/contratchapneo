<template>
    <section class="main-section" data-aos="fade-up" data-aos-duration="3000" >

        <h3>
            Nos solutions pour les entreprises
        </h3>

        <div class="business-pic-wrapper">
            <div class="description flex flex-col gap-4">
                <h4>
                    Nous avons aussi pensé aux entreprises 
                </h4>
                <p>
                    Nos packs business adaptés aux différents types d'entreprises.
                    Achetez nos packs et bénéficier d'un avantage sur tout le reste
                </p>
                <mainButton label="Ouvrir un compte"/>
            </div>
            
            <div class="pic-container">
                <img src="../../assets/pictures/ContratChap/black-people.jpg" alt="Solutions Business">
            </div>
        </div>

        <div class="cards-container">
            <packCards
                v-for="(card, index) in contratPack" 
                :key="index"
                :title="card.title"
            />
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import companyPic from '../../assets/pictures/partners/PROPARCO_Logo_RVB-1.png'
import packCards from '../cards/packCards.vue';
import mainButton from '../buttons/mainButton.vue';

export default {
    name: 'CompanySection',
    components: {
        packCards,
        mainButton
    },
    setup() {
        const mypic = companyPic;
        const logos = Array(12).fill(mypic)

         const contratPack = ref([
            {title: 'Pack basic'},
            {title: 'Pack business'},
            {title: 'Pack business pro'}
        ])

        return {
            logos,
            contratPack
        }
    }
}
</script>

<style lang="css" scoped>
.main-section {
    width: 100%;
    overflow: hidden;
}

.main-section h3 {
    text-align: center;
    font-size: 1.6rem; 
    padding: 2rem 1rem 1rem 1rem;
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
    height: 240px; /* Hauteur maîtrisée sur mobile */
    border-radius: 1.25rem;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.pic-container img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* L'image remplit l'espace sans se déformer */
}

/* Le dégradé qui vient se poser au-dessus de l'image */
.pic-container::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* Dégradé sombre de bas en haut pour donner du contraste */
    background: linear-gradient(to top, rgba(0, 0, 0, 0.4) 0%, transparent 70%);
    pointer-events: none; /* Laisse passer les clics et le scroll tactile */
}


/* --- CONTENEUR DES CARTES (Mobile) --- */
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1rem;
    padding: 1.5rem 1rem;
    width: 100%;
    scrollbar-width: none; /* Cache la barre de défilement sur Firefox */
    border-radius: 1rem;
    background: var(--background-color);
}
.cards-container::-webkit-scrollbar {
    display: none; /* Cache la barre de défilement sur Chrome/Safari */
}


/* --- RESPONSIVE : TABLETTE & DESKTOP (A partir de 768px) --- */
@media (min-width: 768px) {
    .main-section h3 { 
        font-size: 2.2rem; 
        padding: 3rem 1rem 2rem 1rem;
    }

    /* On passe d'un affichage vertical à un affichage côte à côte */
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
        height: 360px; /* L'image prend de l'envergure sur grand écran */
    }
    
    /* Changement de direction du dégradé pour le desktop si nécessaire */
    .pic-container::after {
        background: linear-gradient(to top, rgba(0, 0, 0, 0.3), transparent);
    }

    .cards-container {
        padding: 2rem 3rem;
        justify-content: center; /* Centre les 3 packs sur grand écran */
        overflow-x: visible;
    }
}

@media (min-width: 1024px) {
    .business-pic-wrapper {
        max-width: 1200px;
        margin: 0 auto; /* Centre le bloc de contenu sur les très grands écrans */
    }
    .description h4 {
        font-size: 2.2rem;
    }
}
</style>