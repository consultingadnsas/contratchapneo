<template>
    <section class="main-section" >

        <h3>
            Ces entreprises nous <span>ont fait confiance</span>
        </h3>

        <!-- Changement de classe ici pour correspondre au CSS -->
        <div class="carousel-container">
            <div class="carousel-track">
                <img v-for="(pic, index) in logos" :key="index" :src="pic" alt="Logo partenaire">
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import companyPic from '../../assets/pictures/partners/PROPARCO_Logo_RVB-1.png';
import companyPic2 from '../../assets/pictures/partners/6324bc47b4b22-millenium-fdfp-cote-ivoire.png';
import companyPic3 from '../../assets/pictures/partners/millennium-challenge-corporation-logo-png_seeklogo-245301.png';
import companyPic4 from '../../assets/pictures/partners/OIP.webp';
import companyPic5 from '../../assets/pictures/partners/OIP (4).webp';
import companyPic6 from '../../assets/pictures/partners/OIP (2).webp';
import companyPic7 from '../../assets/pictures/partners/OIP (1).webp';
import companyPic8 from '../../assets/pictures/partners/giz-logo-01.jpg';
import companyPic9 from '../../assets/pictures/partners/LOGO ROND.png';
import packCards from '../cards/packCards.vue';
export default {
    name: 'CompanySection',
    components: {
        packCards,
    },
    setup() {
        const mypic = companyPic;
        const mypic2 = companyPic2;
        const mypic3 = companyPic3;
        const mypic4 = companyPic4;
        const mypic5 = companyPic5;
        const mypic6 = companyPic6;
        const mypic7 = companyPic7;
        const mypic8 = companyPic8;
        const mypic9 = companyPic9;
        // On garde 10 ou plus pour bien remplir l'écran
        const logos = ref([
            mypic, mypic2, mypic3, mypic4, mypic5, mypic6, mypic7, mypic8, mypic9,
            mypic2, mypic3, mypic4, mypic5, mypic6, mypic7, mypic8, mypic9,
            // Ajoutez-en plus si nécessaire
        ])

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
    position: relative;
    top: -120px;
    overflow: hidden; /* Sécurité supplémentaire */
}

.main-section h3 {
    text-align: center;
    font-size: 1.8rem; /* Plus petit pour mobile */
    padding: 1rem;
    font-weight: 600;
}

.main-section h3 span{
    color: var(--primary-color);
}

.carousel-container {
    width: 100%;
    overflow: hidden; 
    position: relative;
    padding: 1rem 0;
}
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1rem;
    padding: 0.5rem 1rem;
    width: 100%;
    scrollbar-width: thin;
}

/* Dégradés sur les côtés */
.carousel-container::before,
.carousel-container::after {
    content: "";
    position: absolute;
    top: 0;
    width: 50px; /* Réduit pour mobile */
    height: 100%;
    z-index: 2;
    pointer-events: none; /* TRÈS IMPORTANT : permet de cliquer à travers */
}

.carousel-container::before { 
    left: 0; 
    background: linear-gradient(to right, white, transparent); 
}
.carousel-container::after { 
    right: 0; 
    background: linear-gradient(to left, white, transparent); 
}

.carousel-track {
    display: flex;
    width: max-content;
    gap: 2rem; /* Gap réduit pour mobile */
    animation: scroll 15s linear infinite; /* Un peu plus rapide pour le dynamisme */
}

.carousel-track img {
    height: 50px; /* Plus petit pour les écrans de téléphone */
    width: auto;
    flex-shrink: 0; /* Empêche les logos de s'écraser */
}

@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* Tablette et Desktop */
@media (min-width: 768px) {
    .main-section h3 { font-size: 2rem; }
    .carousel-track img { height: 60px; }
    .carousel-track { gap: 4rem; }
    .carousel-container::before, .carousel-container::after { width: 100px; }
}
</style>