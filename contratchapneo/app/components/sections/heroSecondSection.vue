<template>
    <section class="hero-section">
        <div class="flex flex-col gap-4">
            <span>
                {{ displayText }}<span class="cursor">|</span>
            </span>
            <h1>
                Télécharger librement vos contrats
            </h1>
            <base-research-input/>
        </div>
        <div class="pic-wrapper">
            <!-- Les cartes sont positionnées par rapport à l'image -->
            <div class="pic-container">
                <img src="../../assets/pictures/ContratChap/pexels-picha-stock-2210122-3894377.jpg" alt="Contrats OHADA">

                <!-- Haut-gauche : chevauche le coin supérieur gauche de l'image -->
                <stat-cards class="floating-card card-top-left"     title="Modèles OHADA" />
                <!-- Haut-droit : chevauche le coin supérieur droit -->
                <stat-cards class="floating-card card-top-right"    title="Conformes OHADA" />
                <!-- Bas-gauche : chevauche le coin inférieur gauche -->
                <stat-cards class="floating-card card-bottom-left"  title="100% Gratuit" />
                <!-- Bas-droit : chevauche le coin inférieur droit -->
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
    /* empêche le débordement horizontal causé par les cartes absolues */
    overflow-x: hidden;

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
    display: inline-flex;   /* se réduit à la taille de l'image */
    justify-content: center;
    align-items: center;
}

.pic-container img {
    width: 220px;
    height: auto;
    border-radius: 130px;
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
}

/* Haut-gauche : ancré au coin supérieur-gauche, décalé vers l'extérieur */
.card-top-left {
    top: 15%;
    left: 0;
    transform: translateX(-60%);
    animation-delay: 0s;
}

/* Haut-droit : ancré au coin supérieur-droit */
.card-top-right {
    top: 15%;
    right: 0;
    transform: translateX(60%);
    animation-delay: 1s;
}

/* Bas-gauche */
.card-bottom-left {
    bottom: 15%;
    left: 0;
    transform: translateX(-60%);
    animation-delay: 2s;
}

/* Bas-droit */
.card-bottom-right {
    bottom: 15%;
    right: 0;
    transform: translateX(60%);
    animation-delay: 3s;
}

@keyframes float {
    0%, 100% { transform: translateX(var(--tx, 0)) translateY(0); }
    50%       { transform: translateX(var(--tx, 0)) translateY(-12px); }
}

/* On surcharge l'animation pour préserver le translateX propre à chaque côté */
.card-top-left,
.card-bottom-left {
    --tx: -60%;
}
.card-top-right,
.card-bottom-right {
    --tx: 60%;
}

@keyframes float {
    0%, 100% { transform: translateX(var(--tx)) translateY(0); }
    50%       { transform: translateX(var(--tx)) translateY(-12px); }
}

/* ── Tablette ────────────────────────────────────────────────── */
@media (min-width: 768px) {
    .hero-section {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        padding: 3rem 2.5rem;
        gap: 2rem;
    }

    .hero-section > div:first-child {
        flex: 1;
        max-width: 50%;
    }

    .pic-wrapper {
        flex: 1;
        padding: 90px 110px;
    }

    .pic-container img {
        width: 280px;
    }

    .floating-card {
        width: 175px !important;
    }
}

/* ── Desktop ─────────────────────────────────────────────────── */
@media (min-width: 1200px) {
    .hero-section {
        padding: 4rem 5rem;
        gap: 3rem;
    }

    .pic-wrapper {
        padding: 100px 130px;
    }

    .pic-container img {
        width: 340px;
    }

    .floating-card {
        width: 200px !important;
    }
}
</style>