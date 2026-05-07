<template>

    <section class="main-Section">

        <div class="hero-section">
            <h1>
                Tout ce dont vous avez besoin
                pour <span>un bon service juridique de qualité</span>
            </h1>

            <h4>
                Besoin de contrat, de conseil juridique, 
                d'assistance juridique ou tout autre produit
                juridique.
            </h4>

            <div class="btn-wrap">
                <MainButton @click="()=>{console.log('Bienvenu au pays mon fils')}"/>
            </div>
        </div>

        <div class="pic-wrapper">
            <img src="../../assets/pictures/ContratChap/pexels-kampus-8475168.jpg" class="one" alt="">
            <img src="../../assets/pictures/ContratChap/pexels-gustavo-fring-6720580.jpg" class="two" alt="">
            <img src="../../assets/pictures/ContratChap/pexels-kampus-8475168.jpg" class="three" alt="">
            <img src="../../assets/pictures/ContratChap/pexels-kampus-8475168.jpg" class="four" alt="">
        </div>

    </section>
    
</template>

<script lang="ts">
import MainButton from '../buttons/mainButton.vue';


export default {
    name: 'HeroSection',
    components:{
        MainButton
    }
}

</script>

<style scoped>

/* Mobile first */

.main-Section{
    padding: 6rem 1rem 1rem 1rem;
    border-radius: 1rem;
}

.hero-section{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

.hero-section h1{
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    width: 100%;
    text-align: start;
    font-weight: 700;
    line-height: 1.2;
}

.hero-section h1 span{
    font-size: 3rem;
    color: var(--primary-color);
    font-weight: 700;
}

.hero-section h4{
    font-size: 1.5rem;
    font-weight: 400;
    color: gray;
    text-align: start;
}

.btn-wrap{
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: space-between;
}

.btn-wrap span{
    font-size: 1.2rem;
    font-weight: 500;
    color: var(--primary-color);
}

/* 1. On définit la structure globale */
.pic-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Deux colonnes de largeur égale */
    grid-template-rows: repeat(10, 1fr); /* On divise la hauteur en 10 unités */
    gap: 0.5rem;
    height: 500px; /* IMPORTANT : il faut une hauteur pour que les ratios s'appliquent */
    padding: 0.5rem;
}

.pic-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px; /* Optionnel : pour le style */
}

/* 2. Placement de la première colonne (Ratio 0.7 / 0.3) */
.one {
    grid-column: 1;    /* Colonne de gauche */
    grid-row: 1 / 8;   /* De la ligne 1 à 8 (soit 7 unités) */
}

.two {
    grid-column: 1;    /* Colonne de gauche */
    grid-row: 8 / 11;  /* De la ligne 8 à 11 (soit 3 unités) */
}

/* 3. Placement de la deuxième colonne (Ratio 50 / 50) */
.three {
    grid-column: 2;    /* Colonne de droite */
    grid-row: 1 / 6;   /* De la ligne 1 à 6 (soit 5 unités) */
}

.four {
    grid-column: 2;    /* Colonne de droite */
    grid-row: 6 / 11;  /* De la ligne 6 à 11 (soit 5 unités) */
}

/* Tablet */

@media (min-width: 768px){
    .main-Section{
        display: grid;
        grid-template-columns: 1fr 1fr;
    }
}
</style>