<template>
    <section class="main-section">

        

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
import companyPic from '../../assets/pictures/partners/PROPARCO_Logo_RVB-1.png'

export default {
    name: 'CompanySection',
    setup() {
        const mypic = companyPic;
        // On garde 10 ou plus pour bien remplir l'écran
        const logos = Array(12).fill(mypic)

        return {
            logos
        }
    }
}
</script>

<style lang="css" scoped>
.main-section {
    width: 100%;
    overflow: hidden; /* Sécurité supplémentaire */
}

.main-section h3 {
    text-align: center;
    font-size: 1.8rem; /* Plus petit pour mobile */
    padding: 2rem 1rem;
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
    height: 40px; /* Plus petit pour les écrans de téléphone */
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