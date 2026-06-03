<template>
    <article :class="['testimonials-card', { 'is-featured': isFeatured }]">
        <div class="card-body">
            <!-- Icône guillemets SVG inline -->
            <svg class="icon-quote" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M9.983 3v7.391c0 5.704-3.731 9.57-8.983 10.609l-.995-2.151c2.432-.917 3.995-3.638 3.995-5.849h-4v-10h9.983zm14.017 0v7.391c0 5.704-3.748 9.571-9 10.609l-.996-2.151c2.433-.917 3.996-3.638 3.996-5.849h-3.983v-10h9.983z"/>
            </svg>
            <p class="quote-text">
                {{ quote }}
            </p>
        </div>
        
        <div class="card-footer">
            <div class="pic_container">
                <img :src="avatarUrl" :alt="authorName">
            </div>
            <div class="info">
                <span class="company-name">{{ companyName }}</span>
                <p class="author-details">
                    <span class="author-name">{{ authorName }}</span>
                    <span class="separator"> - </span>
                    <span class="author-role">{{ authorRole }}</span>
                </p>
            </div>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import defaultAvatar from '../../assets/pictures/ContratChap/pexels-picha-stock-2210122-3894377.jpg';

export default defineComponent({
    name: 'TestimonialCard',
    props: {
        quote: { 
            type: String, 
            default: 'Legally Always has been an invaluable partner in navigating the complexities of business law.' 
        },
        companyName: { 
            type: String, 
            default: 'FinVision' 
        },
        authorName: { 
            type: String, 
            default: 'Sarah Mitchell' 
        },
        authorRole: { 
            type: String, 
            default: 'Small Business Owner' 
        },
        avatarUrl: { 
            type: String, 
            default: defaultAvatar
        },
        isFeatured: { 
            type: Boolean, 
            default: false 
        }
    }
});
</script>

<style scoped>
/* --- DESIGN DE BASE DE LA CARTE --- */
.testimonials-card {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 2.5rem;
    width: 100%;
    max-width: 380px;
    min-height: 260px;
    border-radius: 1rem;
    box-sizing: border-box;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;

    /* Thème clair par défaut */
    background-color: #ffffff;
    color: #111827;
    box-shadow: 0px 2px 4px 0px #656973;
    cursor: pointer;
}

.testimonials-card:hover {
    transform: translateY(-5px);
    transition: all 0.3s;
}

/* --- DEMI-CERCLE DÉCORATIF EN HAUT À DROITE (cartes non sélectionnées) --- */
.testimonials-card:not(.is-featured)::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 30px;
    height: 30px;
    background-color: #65e17e;
    border-radius: 0 0 0 70px;
    z-index: 0;
}

/* --- THÈME DE LA CARTE SÉLECTIONNÉE (FONCÉE) --- */
.testimonials-card.is-featured {
    background-color: var(--primary-color-dark);
    color: #ffffff;
}

/* --- ICÔNE GUILLEMETS --- */
.icon-quote {
    /* Couleur par défaut pour cartes claires */
    color: #0f172a;
    margin-bottom: 0.5rem;
    display: block;
    position: relative;
    z-index: 1;
}

/* Sur carte sombre, l'icône devient blanche */
.is-featured .icon-quote {
    color: #ffffff;
}

/* --- TEXTE DU TÉMOIGNAGE (CORPS) --- */
.quote-text {
    font-size: 1rem;
    font-weight: 500;
    line-height: 1.4;
    margin: 0;
    text-align: left;
    letter-spacing: -0.02em;
    position: relative;
    z-index: 1;
}

/* --- SECTION DE L'AUTEUR (PIED DE CARTE) --- */
.card-footer {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    position: relative;
    z-index: 1;
}

.pic_container {
    flex-shrink: 0;
}

.pic_container img {
    height: 42px;
    width: 42px;
    border-radius: 50%;
    object-fit: cover;
    display: block;
}

.info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    text-align: left;
}

.company-name {
    font-size: 0.9rem;
    font-weight: 700;
}

.author-details {
    font-size: 0.8rem;
    margin: 0;
    font-weight: 400;
}

/* Adaptation des couleurs des métadonnées */
.testimonials-card:not(.is-featured) .author-details {
    color: #6b7280;
}

.testimonials-card.is-featured .author-details {
    color: #94a3b8;
}
</style>