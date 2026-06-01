<template>
    <div class="features-cards">
        <h4 class="features-title">
            {{ title }}
        </h4>

        <div :class="['btn-container', btnPosition]">
            <button>
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
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
        },
        btnPosition:{
            type:String,
            default:'bottom-right'
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
    /* hauteur min au lieu de fixe → la carte s'adapte au contenu */
    min-height: 100px;
    height: auto;
    border-radius: 1.5rem;
    padding: 1rem 1.2rem;
    box-sizing: border-box;

    /* EFFET GLASSMORPHISM */
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

.features-cards h4 {
    font-size: clamp(0.85rem, 2.5vw, 1.1rem); /* fluid, jamais trop petit ni trop grand */
    line-height: 1.3;
    font-weight: 600;
    font-size: 0.7rem;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    /* évite que le texte chevauche le bouton */
    padding-right: 3rem;
    margin-left: 3rem;
    margin-bottom: 0.5rem;
}

.btn-container {
    z-index: 2;
    position: absolute;
    bottom: -5px;
    right: -5px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    border-top-left-radius: 2rem;
    border-bottom-right-radius: 1.5rem;
    width: 45px;
    height: 45px;
}

.features-cards button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    color: #ffffff;
    background: var(--secondary-light-color);
    transition: transform 0.3s ease;
    flex-shrink: 0;
}

.features-cards button:hover {
    transform: scale(1.1) rotate(5deg);
}

.size-4 {
    width: 16px;
    height: 16px;
}
.pos-center-bottom {
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    /* On arrondit les coins du haut pour que ça s'encastre bien */
    border-top-left-radius: 1.5rem;
    border-top-right-radius: 1.5rem;
}
.pos-bottom-right {
    bottom: -5px;
    right: -5px;
    border-top-left-radius: 2rem;
    border-bottom-right-radius: 1.5rem;
}

.pos-top-right {
    top: -5px;
    right: -5px;
    border-bottom-left-radius: 2rem;
    border-top-right-radius: 1.5rem;
}

.pos-bottom-left {
    bottom: -5px;
    left: -5px;
    border-top-right-radius: 2rem;
    border-bottom-left-radius: 1.5rem;
}

.pos-top-left {
    top: -5px;
    left: -5px;
    border-bottom-right-radius: 2rem;
    border-top-left-radius: 1.5rem;
}

/* Tablette */
@media (min-width: 768px) {
    .features-cards {
        padding: 1.5rem;
        min-height: 140px;
        /* suppression du max-width qui cassait le layout parent */
    }

    .features-cards h4 {
        font-size: clamp(1.1rem, 2vw, 1.5rem);
    }

    .btn-container {
        width: 50px;
        height: 60px;
    }

    .features-cards button {
        width: 35px;
        height: 35px;
    }

    .size-4 {
        width: 16px;
        height: 16px;
    }
}

/* Desktop */
@media (min-width: 1200px) {
    .features-cards {
        padding: 2rem;
        min-height: 160px;
    }

    .features-cards h4 {
        font-size: 1rem;
        margin-left: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .btn-container {
        width: 60px;
        height: 60px;
    }

    .features-cards button {
        width: 40px;
        height: 40px;
    }
}
</style>