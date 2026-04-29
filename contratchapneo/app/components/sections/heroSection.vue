<template>

    <section class="">

        <div class="hero-section">
            <h1>
                Tout ce dont vous avez besoin
                pour <span>un bon service juridique</span>
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
            <img src="../../assets/pictures/ContratChap/pexels-kampus-8475168.jpg" class="two" alt="">
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

.hero-section{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    padding: 4rem 1rem 1rem 1rem;
}

.hero-section h1{
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    width: 100%;
    text-align: start;
    font-weight: 500;
}

.hero-section h1 span{
    font-size: 3rem;
    color: var(--primary-color);
    font-weight: 700;
}

.hero-section h4{
    font-size: 1.5rem;
    font-weight: 500;
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

.pic-wrapper{
    display: grid;
    grid-template-columns: 1fr 1fr;
}

.one{
    grid-column: 1/4;
    grid-row: 2/3;
}

.two {
  grid-column: 2 / 4;
  grid-row: 1 / 3;
}

.three {
  grid-column: 3/4;
  grid-row: 1 / 3;
}

.four{
    grid-column: 4/4;
    grid-row: 2/3;
}

</style>