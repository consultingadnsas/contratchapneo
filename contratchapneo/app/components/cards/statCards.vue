<template>
    <div class="features-cards">
        <h4 class="features-title">
            {{ title }}
        </h4>

        <div class="btn-container">
            <button>
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                    </svg>
                </span>
            </button>
        </div>
    </div>
</template>

<script lang="ts">

export default{

    name:'features-cards',
    props:{
        title:{
            type:String,
            default:"Création et cession"
        }
    }

}

</script>

<style scoped>
.features-cards {
    z-index: 1;
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;
    height: 200px;
    border-radius: 1.5rem;
    padding: 1.2rem;
    
    /* EFFET GLASSMORPHISM */
    background: rgba(255, 255, 255, 0.1); /* Fond blanc très transparent */
    backdrop-filter: blur(15px); /* Flou de l'image de fond */
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2); /* Bordure façon verre */
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    
    /* On retire l'arrondi manquant pour garder un look moderne */
    /* border-bottom-right-radius: 0; */ 
}

.features-cards h4 {
    font-size: 1.1rem;
    line-height: 1.3;
    font-weight: 600;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-container {
    z-index: 2;
    position: absolute;
    bottom: -5px; /* On le fait dépasser légèrement pour le style */
    right: -5px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* Rappel de la couleur secondaire mais avec un peu de transparence */
    background: none;
    border-top-left-radius: 2rem;
    border-bottom-right-radius: 1.5rem; /* Aligné avec la carte */
    width: 60px;
    height: 60px;
}

.features-cards button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    color: #ffffff;
    background: var(--secondary-light-color);
    transition: transform 0.3s ease;
}

.features-cards button:hover {
    transform: scale(1.1) rotate(5deg);
}

.size-6 {
    width: 20px;
    height: 20px;
}

@media(min-width: 768px){
    .features-cards {
        padding: 2rem;
        height: 300px;
        max-width: 300px;
    }

    .features-cards h4 {
        font-size: 1.8rem;
    }

    .btn-container {
        width: 80px;
        height: 80px;
    }

    .features-cards button {
        width: 60px;
        height: 60px;
    }
}

@media (min-width: 1200px){
    .features-cards {
        padding: 2rem;
        height: 250px;
    }
}
</style>