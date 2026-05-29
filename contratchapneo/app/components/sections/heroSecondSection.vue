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
                <stat-cards class="floating-card card-top-left"    title="Banque de contrats" @click="router.push('/contractBank')" />
                <stat-cards class="floating-card card-top-right"   title="Outil de Calcul" />
                
                <!-- BAS -->
                <stat-cards class="floating-card card-bottom-left"  title="Conseil juridique" />
                <stat-cards class="floating-card card-bottom-right" title="Nos professionnels" />
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { onMounted, ref, defineComponent } from 'vue'
import mainButton from '../buttons/mainButton.vue'
import BaseResearchInput from '../input/BaseResearchInput.vue'
import statCards from '../cards/statCards.vue'
import {useRouter} from 'vue-router'

export default defineComponent({
    name: 'HeroSecondSection',
    components: { 
        mainButton, 
        BaseResearchInput, 
        statCards 
    },

    setup() {
        const router = useRouter();

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
            displayText,
            router
        }
    }
})
</script>

<style scoped>
/* ── 📱 Mobile First (Valeurs par défaut pour Téléphones) ─────── */
.hero-section {
    background: var(--background-color);
    width: 110%;
    margin-left: 0;
    min-height: 100vh;
    overflow-x: hidden; /* empêche le débordement horizontal causé par les cartes absolues */
    border-bottom-left-radius: 1rem;
    border-bottom-right-radius: 1rem;
    display: flex;
    flex-direction: column;   /* empilé sur mobile */
    align-items: center;
    gap: 2rem;
    padding: 2rem 2.25rem;
    box-sizing: border-box;
    position: relative;
}

/* Bloc texte */
.hero-section > div:first-child {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    position: relative;
    top: 1rem;
}

.hero-section h1 {
    font-size: clamp(1.8rem, 6vw, 3rem); 
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

/* ── Conteneur image + cartes (Mobile) ────────────────────────── */

.pic-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 140px 40px; /* Moins de padding sur les côtés pour maximiser l'espace écran */
    box-sizing: border-box;
    width: 100%;
}

.pic-container {
    position: relative;
    width: 180px; /* Image plus petite sur téléphone pour laisser la place aux cartes */
    display: inline-flex; 
    justify-content: center;
    align-items: center;
}

.pic-container img {
    width: 200px;
    min-width: 200px;
    aspect-ratio: 1 / 1; 
    height: auto; 
    object-fit: cover; 
    border-radius: 50%; 
    display: block;
    position: relative;
    z-index: 1;
}

/* ── Cartes flottantes (Mobile) ──────────────────────────────── */
.floating-card {
    position: absolute;
    z-index: 10;
    width: 105px !important; /* Cartes compactes sur mobile */
    height: auto !important;
    top: 50%;
    transform: translateX(var(--tx)) translateY(var(--ty-base));
    animation: float 4s ease-in-out infinite;

    box-sizing: border-box;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}



/* Décalages Verticaux Adaptés au format 180px de l'image */
.card-top-left, .card-top-right       { --ty-base: -140px; }
.card-bottom-left, .card-bottom-right { --ty-base: 40px; }

/* Décalages Horizontaux Resserres pour écrans étroits */
.card-top-left, .card-bottom-left   { left: 0; --tx: -55%; }
.card-top-right, .card-bottom-right { right: 0; --tx: 55%; }

.card-top-left { animation-delay: 0s; }
.card-top-right { animation-delay: 0.8s; }
.card-bottom-left { animation-delay: 1.6s; }
.card-bottom-right { animation-delay: 2.4s; }

/* ── 📐 Phablettes (Écrans larges ou téléphones en paysage) ──── */
@media (min-width: 480px) {
    .pic-container, .pic-container img {
        width: 230px;
        min-width: 230px;
    }
    .floating-card {
        width: 130px !important;
    }
    .card-top-left, .card-top-right       { --ty-base: -170px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 80px; }
    .card-top-left, .card-mid-left, .card-bottom-left   { --tx: -60%; }
    .card-top-right, .card-mid-right, .card-bottom-right { --tx: 60%; }
}

/* ── 平板 Tablettes (A partir de 768px) ───────────────────────── */
@media (min-width: 768px) {
    .hero-section {
        padding: 3rem 2.5rem;
        gap: 3rem;
        margin-left: 2%;
    }

    .hero-section > div:first-child {
        top: 2rem;
    }

    .pic-wrapper {
        padding: 160px 80px;
    }

    /* L'image passe à sa taille moyenne */
    .pic-container, .pic-container img {
        width: 280px;
        min-width: 280px;
    }

    /* Les cartes s'agrandissent */
    .floating-card {
        width: 160px !important;
    }

    /* On recalcule les espacements verticaux et horizontaux */
    .card-top-left, .card-top-right       { --ty-base: -220px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 80px; }
    .card-top-left, .card-mid-left, .card-bottom-left   { --tx: -65%; }
    .card-top-right, .card-mid-right, .card-bottom-right { --tx: 65%; }
}

/* ── 💻 Desktop (A partir de 1200px) ─────────────────────────── */
@media (min-width: 1200px) {
    .hero-section {
        flex-direction: row; /* Le texte à gauche, l'image à droite */
        justify-content: space-between;
        align-items: center; /* Centre les éléments verticalement */
        padding: 1rem 5rem !important; /* Un peu plus de padding latéral sur grand écran */
        gap: 5rem;
        width: 100%;
        margin-left: 0; /* On s'assure qu'il n'y a plus de marge gauche */
        height: 100vh !important;
        min-height: 600px !important;
    }

    .hero-section > div:first-child {
        width: 50%;
        top: 0; /* Plus besoin de pousser vers le bas */
    }

    .pic-wrapper {
        width: 50%;
        padding: 60px 40px;
    }

    /* Taille maximale pour le grand écran */
    .pic-container, .pic-container img {
        width: 300px;
        min-width: 340px;
    }

    .floating-card {
        width: 160px !important;
        min-height: 140px;
        box-sizing: border-box;
        padding: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .floating-card:hover {
        animation-play-state: paused;
        cursor: pointer;
        transform: translateX(var(--tx)) translateY(var(--ty-base)) scale(1.05);
        transition: transform 0.2s ease-in-out;
        z-index: 20; 
    }

    /* Espacements amples pour le grand écran */
    .card-top-left, .card-top-right       { --ty-base: -190px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 50px; }
    .card-top-left, .card-bottom-left   { --tx: -60%; }
    .card-top-right, .card-bottom-right { --tx: 60%; }
}

/* ── Animation de flottaison globale ─────────────────────────── */
@keyframes float {
    0%, 100% { transform: translateX(var(--tx)) translateY(var(--ty-base)); }
    50%      { transform: translateX(var(--tx)) translateY(calc(var(--ty-base) - 8px)); }
}
</style>