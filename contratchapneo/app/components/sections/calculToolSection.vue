<template>
    <section class="main-section">
        <div class="">

            <div class=" flex flex-col items-center justify-center gap-2">
                <h3>
                    Et si on calculait vos droits en quelques clics ?
                </h3>
            </div>

        </div>

        <div class="blue-section w-full flex justify-center items-center flex-col">
            <div class="section-overlay"></div>
            
            <div class="content-wrapper">
                <h3 class="section-title">Notre outil calcul vos droits pour que vous puissiez les faires valoir en toute sérénité</h3>

                <div class="cards-grid">
                   
                </div>
            </div>
        </div>
        <mainButton label="Outil de calcul"/>
    </section>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
// Importation de l'image par défaut (tu pourras la changer pour une liste)
import defaultImage from '../../assets/pictures/ContratChap/konkapo-home-office-10207248_1920.jpg';
import mainButton from '../buttons/mainButton.vue';
import featuresCards from '../cards/featuresCards.vue';
import statCards from '../cards/statCards.vue';

export default {
    name: 'OrdinarySection',
    props: {
        titleHead: {
            type: String,
            default: 'Outil de calcul'
        }
    },
    components:{
        mainButton,
        featuresCards,
        statCards
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

        const legalPro = [
            {title:'Droit de licenciement'},
            {title: 'Commissaire de justice'},
            {title: 'Notaire'},
            {title: 'Juriste droit des affaires'}
        ]

        return {
            carouselImages,
            currentIndex,
            next,
            prev,
            getItemClass,
            legalPro
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
    background: rgba(0,0,0,0.5);
    color: white;
    border: none;
    font-size: 2rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    z-index: 20; /* Toujours au-dessus */
    border-radius: 50%;
}

.nav-btn.prev { left: 5%; }
.nav-btn.next { right: 5%; }

.blue-section {
    position: relative;
    min-height: 500px;
    background: var(--background-color);
    padding: 4rem 1rem;
    overflow: hidden;
    border-radius: 1rem;
}

.content-wrapper {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 1200px;
}

.section-title {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1rem;
    letter-spacing: 2px;
    text-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

/* Grille Responsive Dynamique */
.cards-grid {
    display: grid;
    grid-template-columns: 1fr; /* Mobile-first */
    gap: 1.5rem;
    padding: 0 1rem;
}

@media(min-width:768px){
    .cards-grid{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
}
</style>