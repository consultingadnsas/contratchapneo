<template>
    <div class="services-showcase" ref="showcaseRef">
        <article 
            v-for="(service, index) in services" 
            :key="index"
            :id="service.id"
            :class="['expanding-card', { 'is-active': activeIndex === index }]"
            :data-index="index"
            @mouseenter="handleMouseEnter(index)"
        >
            <div class="card-inactive" v-show="activeIndex !== index">
                <span class="big-number">{{ formatNumber(index + 1) }}.</span>
                <div class="inactive-footer">
                    <div class="mini-icon" v-html="service.icon"></div>
                    <span class="mini-title">{{ service.shortTitle || service.title }}</span>
                </div>
            </div>

            <div class="card-active" v-show="activeIndex === index">
                <div class="card-image-wrapper" :style="{ background: service.gradient || 'linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%)' }">
                    <div class="glass-overlay"></div>
                </div>
                
                <div class="card-content">
                    <div class="icon-wrapper" v-html="service.icon"></div>
                    <h3>{{ service.title }}</h3>
                    <p class="muted-text">{{ service.description }}</p>
                </div>
            </div>
        </article>
    </div>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import {useRoute} from 'vue-router';

export default {
    name: 'ServicesCards',
    props: {
        services: {
            type: Array,
            required: true,
            default: () => []
        }
    },
    setup(props) {
        const route = useRoute();
        const activeIndex = ref(0);
        const showcaseRef = ref<HTMLElement | null>(null);
        let observer: IntersectionObserver | null = null;

        // Formater le numéro en "01", "02", etc.
        const formatNumber = (num: number) => {
            return num < 10 ? `0${num}` : num;
        };

        // --- GESTION DES INTERACTIONS ---

        // Desktop : Ouverture au survol
        const handleMouseEnter = (index: number) => {
            if (window.innerWidth >= 768) {
                activeIndex.value = index;
            }
        };

        // --- NOUVEAU : GESTION DU SCROLL AUTOMATIQUE (Mobile) ---

        const initIntersectionObserver = () => {
            // On ne l'active que sur mobile
            if (window.innerWidth >= 768) return;

            const options = {
                root: null, // Utilise le viewport
                // rootMargin : On définit une zone "cible" au centre de l'écran. 
                // '-40% 0px' signifie que l'élément doit être dans les 20% centraux de la hauteur de l'écran.
                rootMargin: '-40% 0px -40% 0px', 
                threshold: 0 // Dès qu'un pixel entre dans la zone cible
            };

            const callback = (entries: IntersectionObserverEntry[]) => {
                entries.forEach(entry => {
                    // Si la carte entre dans la zone centrale
                    if (entry.isIntersecting) {
                        const indexStr = entry.target.getAttribute('data-index');
                        if (indexStr !== null) {
                            // On ouvre cette carte automatiquement
                            activeIndex.value = parseInt(indexStr, 10);
                        }
                    }
                });
            };

            observer = new IntersectionObserver(callback, options);

            // On observe toutes les cartes
            const cards = showcaseRef.value?.querySelectorAll('.expanding-card');
            cards?.forEach(card => observer?.observe(card));
        };

        const scrollToService = () =>{
            if (route.hash){
                const targetId=route.hash.replace('#','');
                const targetIndex=props.services.findIndex((s:any)=>s.id===targetId);
                if (targetIndex!==-1){
                    activeIndex.value = targetIndex;
                    // Scroll vers la carte ciblée
                    nextTick(()=>{
                        const element=document.getElementById(targetId);
                        if(element){
                            const y=element.getBoundingClientRect().top + window.scrollY - 120;
                            window.scrollTo({ top: y, behavior: 'smooth' });
                        }
                    })
                }
            }
        }

        onMounted(() => {
            initIntersectionObserver();
            scrollToService();
            // Optionnel : Ré-initialiser si on redimensionne la fenêtre
            window.addEventListener('resize', () => {
                observer?.disconnect();
                if (window.innerWidth < 768) initIntersectionObserver();
            });
            watch(()=>route.hash, ()=>{scrollToService();})
        });

        onUnmounted(() => {
            observer?.disconnect();
            window.removeEventListener('resize', initIntersectionObserver);
        });

        return {
            activeIndex,
            showcaseRef,
            formatNumber,
            handleMouseEnter,
        };
    }
}
</script>

<style scoped>
/* --- TYPOGRAPHIE GLOBALE --- */
.muted-text {
    color: #64748b;
}

/* --- DESIGN SOMBRE & BLANC (D.A. About.vue) --- */
.services-showcase {
    display: flex;
    gap: 1rem;
    height: 440px; /* Hauteur fixe pour l'effet accordéon */
    width: 100%;
    margin-top: 2rem;
}

/* Base de la carte (Blanche avec ombre douces) */
.expanding-card {
    position: relative;
    flex: 1; /* Carte étroite par défaut */
    background-color: #ffffff;
    border-radius: 20px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
    border: 1px solid #f1f5f9;
    transition: flex 0.6s cubic-bezier(0.2, 1, 0.2, 1), 
                box-shadow 0.3s ease,
                height 0.4s ease; /* Pour mobile vertical */
    display: flex;
    flex-direction: column;
}

/* État actif (carte élargie) */
.expanding-card.is-active {
    flex: 3; /* Prend 3 fois plus de place que les autres sur desktop */
    box-shadow: 0 20px 40px rgba(52, 211, 153, 0.1); /* Ombre douce avec accent vert */
    border-color: rgba(52, 211, 153, 0.2);
    cursor: default;
}

/* ── CONTENU INACTIF (Carte étroite) ── */
.card-inactive {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 1.5rem 0.5rem;
    animation: fadeIn 0.4s ease forwards;
}

.big-number {
    font-size: clamp(2.5rem, 3.5vw, 3.5rem);
    font-weight: 200;
    color: #e2e8f0; /* Gris très clair, technique */
    margin-top: 1rem;
}

.inactive-footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.8rem;
    text-align: center;
}

.mini-icon {
    width: 24px;
    height: 24px;
    color: #0f172a; /* Icône foncée sur fond blanc */
}

.mini-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #0f172a;
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    letter-spacing: 1px;
    white-space: nowrap;
}

/* ── CONTENU ACTIF (Carte élargie) ── */
.card-active {
    display: flex;
    flex-direction: column;
    height: 100%;
    animation: fadeIn 0.6s ease forwards;
}

.card-image-wrapper {
    height: 40%;
    width: 100%;
    position: relative;
    overflow: hidden;
}

.glass-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50px;
    background: linear-gradient(to top, #ffffff, transparent); /* Dégradé vers le blanc */
}

.card-content {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    flex: 1;
}

.icon-wrapper {
    width: 40px;
    height: 40px;
    background: #0f172a; /* Rond sombre */
    color: #ffffff; /* Icône blanche */
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px;
    margin-top: -40px; /* Chevauche l'image sur desktop */
    position: relative;
    z-index: 2;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
}

.card-content h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
    margin: 0 0 1rem 0;
}

.card-content p {
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* ── RESPONSIVE TABLETTE ── */
@media (max-width: 1024px) {
    .mini-title {
        writing-mode: horizontal-tb;
        transform: none;
        font-size: 0.75rem;
    }
}

/* ── RESPONSIVE MOBILE OPTIMISÉ (≤ 768px) ── */
@media (max-width: 768px) {
    /* Sur mobile, on passe en affichage vertical */
    .services-showcase {
        flex-direction: column;
        height: auto;
        gap: 1rem; /* Espacement réduit pour mobile */
        padding: 0 1rem; /* Marge sur les côtés */
    }

    .expanding-card {
        flex: none !important; /* Désactive le flex proportionnel desktop */
        height: 100px; /* Hauteur fermée */
        border-radius: 20px; /* Coins un peu moins arrondis */
    }

    /* GESTION DU SCROLL : La carte active s'ouvre verticalement */
    .expanding-card.is-active {
        height: auto; /* S'adapte au contenu */
        min-height: 400px; /* Assure une bonne hauteur pour le contenu */
    }

    /* Ajustement contenu INACTIF sur mobile (devient horizontal) */
    .card-inactive {
        flex-direction: row;
        padding: 1rem 2rem;
    }

    .big-number {
        margin-top: 0;
        font-size: 2.5rem;
    }

    .inactive-footer {
        flex-direction: row;
    }

    .mini-icon {
        width: 20px;
        height: 20px;
    }

    /* ── CORRECTION DEMANDÉE : Design de l'Icône sur mobile actif ── */
    
    .card-image-wrapper {
        height: 120px; /* Hauteur fixe réduite pour l'image area sur mobile */
    }

    .icon-wrapper {
        /* On retire les styles desktop gênants */
        margin-top: 1rem !important; /* On annule le chevauchement négatif */
        align-self: center; /* On centre l'icône proprement */
        margin-bottom: 1.5rem;
        
        /* Optionnel : On peut rendre le rond un peu plus gros/fluide sur mobile */
        width: 48px;
        height: 48px;
        padding: 10px;
    }

    .card-content {
        padding: 1.5rem; /* Padding réduit */
        align-items: center; /* Centre le texte sur mobile (cohérent avec l'icône) */
        text-align: center;
    }

    .card-content h3 {
        font-size: 1.5rem; /* Titre plus petit */
    }

    .card-content p {
        font-size: 0.95rem;
    }
}
</style>