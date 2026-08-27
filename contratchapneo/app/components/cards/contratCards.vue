<template>
    <!-- Ajout du clic sur toute la carte -->
    <article class="pro-card" @click="viewContrat">
        <div 
            class="card-bg" 
            :style="{ backgroundImage: `url(${image})` }"
        ></div>

        <div class="overlay"></div>

        <div class="card-info">
            <h4 class="pro-name">{{ title }}</h4>
            
            <!-- ⚡️ NOUVEAU : Logique d'affichage du prix avec ou sans promotion -->
            <div v-if="promoPrice && Number(promoPrice) > 0" class="pro-specialty price-wrapper">
                <span class="old-price">{{ price }} FCFA</span>
                <span class="new-price">{{ promoPrice }} FCFA</span>
            </div>
            <p v-else class="pro-specialty">{{ price }} FCFA</p>
            <!-- ============================================================= -->

        </div>

        <div class="btn-container">
            <!-- ⚡️ NOUVEAU : On émet 'contrat-checkout' directement, comme dans proCards -->
            <button @click.stop="()=>{$emit('contrat-checkout')}">
                <span v-if="!isloading">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                    </svg>
                </span>
                <span class="loading loading-spinner loading-md" v-else></span>
            </button>
        </div>

        <div class="btn_container2">
            <!-- .stop ici aussi -->
            <button @click.stop="viewContrat">
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                </span>
            </button>
            <span class="tooltip">Aperçu</span>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import defaultImg from '../../assets/pictures/ContratChap/pexels-thirdman-5060819.jpg';

export default defineComponent({
    name: 'ContratCards',
    props: {
        title: {
            type: String,
            default: 'James Benjamin'
        },
        price: {
            type: [Number, String],
            default: 4000
        },
        promoPrice: {
            type: [Number, String],
            default: null
        },
        description: {
            type: String,
            default: 'bienvenue au pays mon fils'
        },
        image: {
            type: String,
            default: defaultImg
        },
        // ⚡️ NOUVEAU : Ajout de la prop isloading calquée sur ProCards
        isloading: {
            type: Boolean,
            default: false
        }
    },
    // ⚡️ NOUVEAU : On remplace 'buy' par 'contrat-checkout'
    emits: ['contrat-checkout', 'view'],
    setup(props, { emit }) {
        
        function viewContrat() {
            emit('view'); 
        }

        return {
            viewContrat
        };
    }
});
</script>

<style scoped>
.pro-card {
    position: relative;
    width: 100%;
    height: 350px;
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    background-color: #1a1a1a;
    flex-shrink: 0;
    border-radius: 28px;
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

/* Overlay : totalement transparent en haut, devient très noir en bas */
.overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to bottom, 
        transparent 0%, 
        transparent 40%, 
        rgba(0, 0, 0, 0.7) 65%, 
        rgba(0, 0, 0, 0.95) 70%
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
    /* On ajoute un padding droit pour que le texte n'écrase pas les boutons */
    padding-right: 70px;
}

.pro-name {
    margin: 0;
    font-size: 0.93rem;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
}

.pro-info {
    font-size: 0.80rem;
    font-weight: 500;
    color: #999999;
}

.pro-specialty {
    margin: 0.5rem 0 0 0;
    font-size: 0.9rem;
    font-weight: 700;
    background: var(--primary-color);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    width: fit-content;
    max-width: 100%;
    color: #ffffff;
}

/* ⚡️ NOUVEAU : Styles pour la promotion sur fond sombre */
.price-wrapper {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.old-price {
    color: #cbd5e1; /* Gris clair pour bien ressortir sur le fond */
    font-size: 0.75rem;
    text-decoration: line-through;
    font-weight: 500;
    opacity: 0.8;
}

.new-price {
    color: #ffffff;
    font-weight: 700;
    font-size: 0.9rem;
}

/* Barre d'accentuation au survol */
.pro-name::after {
    content: '';
    display: block;
    width: 0;
    height: 2px;
    background: #34d399;
    margin-top: 4px;
    transition: width 0.3s ease;
}

.pro-card:hover .pro-name::after {
    width: 40px;
}

/* Bouton d'achat */
.btn-container {
    z-index: 4;
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

/* Bouton de vue */
.btn_container2 {
    z-index: 3;
    position: absolute;
    bottom: 9px;
    right: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.075);
    border: 1px solid rgba(255, 255, 255, 0.089);
    border-radius: 999px;
    width: 45px;
    height: 45px;
    transition: all ease-in-out 0.4s;
}

.btn_container2:hover {
    background: rgba(255, 255, 255, 0.315);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

/* Style du tooltip */
.tooltip {
    position: absolute;
    bottom: 50px; 
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0, 0, 0, 0.8);
    color: #fff;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.2s ease, visibility 0.2s ease;
    pointer-events: none; 
}

/* Petite flèche sous le tooltip */
.tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: rgba(0, 0, 0, 0.8);
}

/* Affichage du tooltip au survol du conteneur */
.btn_container2:hover .tooltip {
    opacity: 1;
    visibility: visible;
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
    background: transparent;
    transition: transform 0.3s ease;
    flex-shrink: 0;
}

.pro-card button:hover {
    transform: scale(1.1) rotate(5deg);
}

.pro-card button svg {
    width: 20px;
    height: 20px;
}

.size-6 {
    width: 18px;
    height: 18px;
}
</style>