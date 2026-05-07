<template>
    <section class="main-section">
        <div class="head">
            <h3>{{ titleHead }}</h3>
        </div>

        <div class="">

            <div class="carousel-wrapper">
                <!-- Boutons de navigation (Optionnels mais pratiques) -->
                <button @click="prev" class="nav-btn prev">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                    </svg>
                </button>
                
                <div class="carousel-container">
                    <div 
                        v-for="(image, index) in carouselImages" 
                        :key="index"
                        class="carousel-item"
                        :class="getItemClass(index)"
                    >
                        <img :src="image" alt="Slider image">
                    </div>
                </div>

                <button @click="next" class="nav-btn next"> 
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                    </svg>
                </button>
            </div>

            <div class="flex flex-col items-center justify-center gap-2">
                <h3>
                    Une panoplie de contrats vous attend
                    <span>
                        téléchargez-les ici
                    </span>
                </h3>
                <mainButton label="télécharger contrats"/>
            </div>

        </div>

        <div class="green-section w-full flex justify-center items-center flex-col">
            <h3>Nos différents types de contrats</h3>

            <div class="green-body flex flex-col justify-center items-center gap-4">
                <div class="card-container">
                    <featuresCards 
                        v-for="(card, index) in contratCards" :key="index"
                        :title="card.title"
                    />
                </div>
                <h3>Nos contrats s'adaptent à tout type de situations en accord avec les règles de l'OHADA</h3>
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
// Importation de l'image par défaut (tu pourras la changer pour une liste)
import defaultImage from '../../assets/pictures/ContratChap/pexels-thirdman-5060819.jpg';
import mainButton from '../buttons/mainButton.vue';
import featuresCards from '../cards/featuresCards.vue';

export default {
    name: 'OrdinarySection',
    props: {
        titleHead: {
            type: String,
            default: 'Banque de contrats'
        }
    },
    components:{
        mainButton,
        featuresCards
    },
    setup() {
        // 1. Les données : Une liste d'images.
        // Ici je répète la même image pour la démo, mais tu mettras ton tableau d'images.
        const carouselImages = ref([
            defaultImage,
            defaultImage,
            defaultImage,
            defaultImage,
            defaultImage
        ]);

        // 2. L'état : L'index de l'image actuellement au centre
        const currentIndex = ref(2); // On commence au milieu pour la démo

        // 3. Logique : Fonctions de navigation
        const next = () => {
            if (currentIndex.value < carouselImages.value.length - 1) {
                currentIndex.value++;
            } else {
                currentIndex.value = 0; // Boucle au début
            }
        };

        const prev = () => {
            if (currentIndex.value > 0) {
                currentIndex.value--;
            } else {
                currentIndex.value = carouselImages.value.length - 1; // Boucle à la fin
            }
        };

        // 4. Style Dynamique : Calculer la classe de chaque item
        const getItemClass = (index: number) => {
            if (index === currentIndex.value) {
                return 'active'; // Image principale
            } else if (index === currentIndex.value - 1) {
                return 'prev-item'; // Image juste à gauche
            } else if (index === currentIndex.value + 1) {
                return 'next-item'; // Image juste à droite
            } else {
                return 'hidden-item'; // Autres images (éloignées)
            }
        };

        const contratCards = [
            {title:"Création et cession"},
            {title: "Prestation de services"},
            {title:"Contrat de freelance"},
            {title: "Contrat de bénévolat"}
        ]

        return {
            carouselImages,
            currentIndex,
            contratCards,
            next,
            prev,
            getItemClass
        };
    }
}
</script>

<style scoped>
/* --- Structure --- */
.main-section {
    padding: 2rem 0;
    overflow: hidden; /* Important pour ne pas voir dépasser les images latérales */
}

.head h3 {
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 2rem;
    font-family: sans-serif;
}

.carousel-wrapper {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.carousel-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    /* La hauteur doit être définie pour le scale */
    height: 350px; 
    position: relative;
    perspective: 1000px; /* Ajoute un effet 3D lors des transformations */
}

/* --- Les Items (Images) --- */
.carousel-item {
    position: absolute; /* Superpose toutes les images au centre */
    width: 66%; /* <--- TES 2/3 DE LA DIV */
    height: 100%;
    transition: all 0.5s ease-in-out; /* Animation fluide */
    z-index: 1;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.carousel-item img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* L'image remplit son conteneur sans déformer */
}

/* --- LE STYLE PARTICULIER (Classes dynamiques) --- */

/* 1. L'image ACTIVE (Principale) */
.carousel-item.active {
    z-index: 10; /* Au premier plan */
    transform: translateX(0) scale(1); /* Taille normale (qui est déjà 2/3) */
    opacity: 1;
}

/* 2. L'image PRÉCÉDENTE (Juste à gauche) */
.carousel-item.prev-item {
    z-index: 5;
    /* On la décale à gauche ET on la rétrécit */
    transform: translateX(-40%) scale(0.75); 
    opacity: 0.6; /* Un peu transparente */
}

/* 3. L'image SUIVANTE (Juste à droite) */
.carousel-item.next-item {
    z-index: 5;
    /* On la décale à droite ET on la rétrécit */
    transform: translateX(40%) scale(0.75);
    opacity: 0.6;
}

/* 4. Les images ÉLOIGNÉES (Cachées ou très petites) */
.carousel-item.hidden-item {
    z-index: 1;
    transform: translateX(0) scale(0.5); /* Cachées derrière la principale */
    opacity: 0;
}


/* --- Boutons de Navigation (Style basique) --- */
.nav-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: var(--primary-color);
    color: white;
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    z-index: 20; /* Toujours au-dessus */
}

.nav-btn.prev { left: 5%; }
.nav-btn.next { right: 5%; }

.green-section{
    background: var(--secondary-color);
    margin: 0 1rem;
    border-radius: 1rem;
}

.green-section h3{
    color: var(--my-white);
}

.green-body{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

.card-container{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

@media(min-width:768px){
    
    .green-body{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .card-container{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
}

@media(min-width: 1048px){
    .card-container{

    }
}

</style>