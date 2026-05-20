<template>
    <article class="pro-card">
        <div 
            class="card-bg" 
            :style="{ backgroundImage: `url(${image})` }"
        ></div>

        <div class="overlay"></div>

        <div class="card-info">
            <h4 class="pro-name">{{ title }}</h4>
            <p class="pro-specialty">{{ subtitle }}</p>
        </div>

        <div class="btn-container">
            <button>
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                    </svg>
                </span>
            </button>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import defaultImg from '@/assets/pictures/ContratChap/pexels-thirdman-5060819.jpg';
export default defineComponent({
    name: 'ProCards',
    props: {
        title: {
            type: String,
            default: 'James Benjamin'
        },
        subtitle: {
            type: String,
            default: 'CEO @ Framify'
        },
        image: {
            type: String,
            default: defaultImg
        }
    }
});
</script>

<style scoped>
.pro-card {
    position: relative;
    width: 100%;
    /* On garde un ratio vertical élégant */
    aspect-ratio: 1 / 1.25; 
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    background-color: #1a1a1a;
}

/* Image de fond avec effet de zoom au survol */
.card-bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    transition: transform 0.7s cubic-bezier(0.25, 1, 0.5, 1);
    z-index: 1;
}

.pro-card:hover .card-bg {
    transform: scale(1.1);
}

/* Overlay : sombre en bas (pour le texte) et transparent en haut */
.overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to top, 
        rgba(0, 0, 0, 0.8) 0%, 
        rgba(0, 0, 0, 0.4) 40%, 
        transparent 100%
    );
    z-index: 2;
}

/* Positionnement du texte */
.card-info {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 1.5rem;
    z-index: 3;
    color: #ffffff;
}

.pro-name {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
}

.pro-specialty {
    margin: 0.25rem 0 0 0;
    font-size: 0.9rem;
    font-weight: 400;
    opacity: 0.85; /* Légèrement plus discret que le nom */
}

/* Optionnel : petite barre d'accentuation au survol */
.pro-name::after {
    content: '';
    display: block;
    width: 0;
    height: 2px;
    background: #34d399; /* Ton vert d'accentuation */
    margin-top: 4px;
    transition: width 0.3s ease;
}

.pro-card:hover .pro-name::after {
    width: 40px;
}

.btn-container {
    z-index: 2;
    position: absolute;
    bottom: 9px;
    right: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-color);
    border-radius: 999px;
    width: 45px;
    height: 45px;
}

.pro-card button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    color: #ffffff;
    background: var(--primary-color);
    transition: transform 0.3s ease;
    flex-shrink: 0;
}

.pro-card button:hover {
    transform: scale(1.1) rotate(5deg);
}

.size-6 {
    width: 18px;
    height: 18px;
}
</style>