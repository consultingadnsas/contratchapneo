<template>
    <section class="hero-section">
        <div class="flex flex-col gap-4">
            <span>
                {{ displayText }}<span class="cursor">|</span>
            </span>
            <h1>
                Téléchargez librement vos contrats
            </h1>
            <base-research-input/>
        </div>
        <div class="pic-wrapper">
            <div class="pic-container">
                <img src="../../assets/pictures/ContratChap/pexels-picha-stock-2210122-3894377.jpg" alt="Contrats OHADA">

                <!-- HAUT -->
                <stat-cards class="floating-card card-top-left"    title="Modèles OHADA" />
                <stat-cards class="floating-card card-top-right"   title="Conformes OHADA" />
                
                <!-- MILIEU (Nouvelles cartes) -->
                <stat-cards class="floating-card card-mid-left"    title="Mise à jour 2026" />
                <stat-cards class="floating-card card-mid-right"   title="Assistance 24/7" />
                
                <!-- BAS -->
                <stat-cards class="floating-card card-bottom-left"  title="100% Gratuit" />
                <stat-cards class="floating-card card-bottom-right" title="Sécurisez vos affaires" />
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { onMounted, ref, defineComponent } from 'vue'
import mainButton from '../buttons/mainButton.vue'
import BaseResearchInput from '../input/BaseResearchInput.vue'
import statCards from '../cards/statCards.vue'

export default defineComponent({
    name: 'HeroSecondSection',
    components: { 
        mainButton, 
        BaseResearchInput, 
        statCards 
    },

    setup() {
        const phrases = [
            'Profitez de nos contrats gratuits.',
            'Sécurisez juridiquement vos affaires.',
            'Accédez à des modèles conformes à l\'OHADA.'
        ]

        const displayText = ref<string>('');
        const phraseIndex = ref<number>(0);
        const charIndex = ref<number>(0);
        const isDeleting = ref<boolean>(false);
        const typeSpeed = ref<number>(100);

        const handleType = () => {
            const currentPhrase = phrases[phraseIndex.value];

            if(isDeleting.value){
                displayText.value = currentPhrase.substring(0, charIndex.value - 1);
                charIndex.value--;
                typeSpeed.value = 50;
            } else {
                displayText.value = currentPhrase.substring(0, charIndex.value + 1);
                charIndex.value++;
                typeSpeed.value = 100;
            }

            if (!isDeleting.value && charIndex.value === currentPhrase.length) {
                isDeleting.value = true;
                typeSpeed.value = 3000;
            } else if (isDeleting.value && charIndex.value === 0) {
                isDeleting.value = false;
                phraseIndex.value = (phraseIndex.value + 1) % phrases.length;
                typeSpeed.value = 500;
            }

            setTimeout(handleType, typeSpeed.value);
        };

        onMounted(() => {
            handleType();
        })

        return {
            displayText
        }
    }
})
</script>

<style scoped>
/* ── Mobile first ────────────────────────────────────────────── */
.hero-section {
    background: var(--background-color);
    width: 100%;
    min-height: 100vh;
    /* empêche le débordement horizontal causé par les cartes absolues */
    overflow-x: hidden;
    border-bottom-left-radius: 1rem;
    border-bottom-right-radius: 1rem;
    display: flex;
    flex-direction: column;   /* empilé sur mobile */
    align-items: center;
    gap: 2.5rem;
    padding: 2rem 1.25rem;
    box-sizing: border-box;
}

/* Bloc texte */
.hero-section > div:first-child {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    position: relative;
    top:3rem;
}

.hero-section h1 {
    font-size: clamp(1.8rem, 6vw, 3rem); /* fluide, pas de rupture brutale */
    font-weight: 600;
    color: var(--my-white);
    line-height: 1.2;
    margin: 0;
}

.hero-section span {
    color: var(--secondary-light-color);
    font-size: clamp(1rem, 3.5vw, 1.5rem);
    font-weight: 600;
    line-height: 1.2;
}

.cursor {
    color: var(--secondary-light-color);
    animation: blink 0.7s infinite;
    margin-left: 4px;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

/* ── Conteneur image + cartes ────────────────────────────────── */

/* Wrapper externe : centre le bloc et absorbe le débordement des cartes */
.pic-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    /* padding = espace laissé pour les cartes qui débordent de l'image */
    padding: 80px 100px;
    box-sizing: border-box;
    width: 100%;
}

/* pic-container = référentiel de positionnement, taille = taille de l'image */
.pic-container {
    position: relative;
    max-width: 300px;
    display: inline-flex;   /* se réduit à la taille de l'image */
    justify-content: center;
    align-items: center;
}

.pic-container img {
    /* Étape 1 : On force l'image à faire la même largeur sur mobile */
     width: 300px;
    min-width: 300px;
    
    /* Étape 2 : On force un ratio 1:1 (un carré parfait) */
    aspect-ratio: 1 / 1; 
    height: auto; /* Laisse le navigateur gérer la hauteur selon le ratio */
    
    /* Étape 3 : Empêche l'image de se déformer/s'écraser dans son carré */
    object-fit: cover; 
    
    /* Étape 4 : Un rayon de 50% sur un carré parfait donne un cercle parfait */
    border-radius: 50%; 
    
    display: block;
    position: relative;
    z-index: 1;
}
/* ── Cartes flottantes ───────────────────────────────────────── */
/*
  Principe : top/left/right/bottom = 0 correspond aux bords de l'image.
  On utilise translate() pour faire déborder la carte à moitié hors de l'image.
  Chaque carte est à 50% à l'intérieur, 50% à l'extérieur → effet "autour".
*/
.floating-card {
    position: absolute;
    z-index: 10;
    width: 155px !important;
    height: auto !important;
    animation: float 4s ease-in-out infinite;
    transform: translateX(var(--tx)) translateY(var(--ty-base));
    animation: float 4s ease-in-out infinite;
}

.floating-card:hover {
    animation-play-state: paused;
    cursor: pointer;
    /* Conserve la position actuelle, mais applique une transition fluide de zoom (scale) */
    transform: translateX(var(--tx)) translateY(var(--ty-base)) scale(1.05);
    transition: transform 0.2s ease-in-out;
    z-index: 20; /* Passe au-dessus des autres cartes si elles se croisent */
}



/* Haut (Ajusté à 5% pour laisser de la place) */
.card-top-left, .card-top-right {
    --ty-base: -160px;
}
.card-top-left { left: 0; animation-delay: 0s; }
.card-top-right { right: 0; animation-delay: 0.7s; }

/* Milieu (Nouveaux positionnements) */
.card-mid-left, .card-mid-right {
    top: 50%;
    /* On ajuste le translateY initial à -50% pour parfaitement centrer la carte verticalement */
    --ty-base: -50%; 
}
.card-mid-left { left: 0; animation-delay: 1.4s; }
.card-mid-right { right: 0; animation-delay: 2.1s; }

/* Bas (Ajusté à 5% du bas) */
.card-bottom-left, .card-bottom-right {
    --ty-base: 160px;
}
.card-bottom-left { left: 0; animation-delay: 2.8s; }
.card-bottom-right { right: 0; animation-delay: 3.5s; }


/* --- Gestion des décalages sur l'axe X (Gauche / Droite) --- */
.card-top-left,
.card-mid-left,
.card-bottom-left {
    --tx: -70%;
}

.card-top-right,
.card-mid-right,
.card-bottom-right {
    --tx: 70%;
}

@keyframes float {
    0%, 100% { 
        /* var(--ty-base, 0) permet de garder le -50% pour les cartes du milieu, et 0 pour les autres */
        transform: translateX(var(--tx)) translateY(var(--ty-base)); 
    }
    50% { 
        /* On applique l'effet de flottaison de -12px par rapport à la position de base */
        transform: translateX(var(--tx)) translateY(calc(var(--ty-base, 0px) - 6px)); 
    }
}

/* ── Tablette ────────────────────────────────────────────────── */
@media (min-width: 768px) {
    .hero-section {
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        padding: 3rem 2.5rem;
        gap: 2rem;
    }

    .hero-section > div:first-child {
        flex: 1;
        max-width: 50%;
        position: relative;
        top: 4rem ;
    }

    .pic-wrapper {
        flex: 1;
        padding: 90px 110px;
    }

    .pic-container {
        max-width: 300px;
    }

    .pic-container img {
        min-width: clamp(300px, 40vw, 380px);

    }

    .floating-card {
        width: 175px !important;
    }
}

/* ── Desktop ─────────────────────────────────────────────────── */
@media (min-width: 1200px) {
    .hero-section {
        flex-direction: row;
        padding: 4rem 5rem;
        gap: 3rem;
    }

    .hero-section > div:first-child {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    position: relative;
    top: -3rem;
    }

    .pic-wrapper {
        padding: 100px 130px;
    }

    .pic-container {
        max-width: 340px;
    }

    .pic-container img {
        width: 340px;
    }

    .floating-card {
        width: 200px !important;
    }
}
</style>