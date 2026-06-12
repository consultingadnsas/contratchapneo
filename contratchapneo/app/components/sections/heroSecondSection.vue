<template>
    <section class="hero-section">
        <div class="bg-shape shape-bottom-right"></div>
        <div class="bg-shape shape-top-left"></div>

        <div class="flex flex-col gap-4 content-wrapper">
            <span>
                {{ displayText }}<span class="cursor">|</span>
            </span>
            <h1>
                Téléchargez facilement tous vos contrats
            </h1>
            <base-research-input/>
        </div>
        <div class="pic-wrapper">
            <div class="pic-container">
                <img src="/Accueil_madame SANS FOND.png" alt="Contrats OHADA">

                <stat-cards class="floating-card card-top-left"    title="Banque de contrats" @click="router.push('/contractBank')" />
                <stat-cards class="floating-card card-top-right"   title="Outil de Calcul" @click="router.push('/lawCalcul')" />
                
                <stat-cards class="floating-card card-bottom-left"  title="Services juridiques" @click="router.push('/services')" />
                <stat-cards class="floating-card card-bottom-right" title="Nos professionnels" @click="router.push('/pro')" />
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { onMounted, ref, defineComponent } from 'vue'
import mainButton from '../buttons/mainButton.vue'
import BaseResearchInput from '../input/BaseResearchInput.vue'
import statCards from '../cards/statCards.vue'
import { useRouter } from 'vue-router'

export default defineComponent({
    name: 'HeroSecondSection',
    components: { 
        mainButton, 
        BaseResearchInput, 
        statCards,
    },

    setup() {
        const router = useRouter();

        const phrases = [
            'Profitez de nos contrats gratuits.',
            'Sécurisez juridiquement vos business.',
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
    position: relative;
    width: 100%;
    min-height: 100vh;
    overflow-x: hidden;
    border-bottom-left-radius: 1rem;
    border-bottom-right-radius: 1rem;
    display: flex;
    justify-content: center;
    flex-direction: column; 
    align-items: center;
    gap: 1rem;
    padding: 4rem 1rem 1rem 1rem;
    background: radial-gradient(circle, #202b4a 30%, #0f0f0f 100%);
}

/* Bloc texte */
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
    padding: 70px 40px;
    box-sizing: border-box;
    width: 100%;
}

.pic-container {
    position: relative;
    width: 180px; 
    display: inline-flex; 
    justify-content: center;
    align-items: center;
    z-index: 1;
}
.pic-container::before {
    content: '';
    position: absolute;
    
    /* 1. Le déplacement en haut à gauche */
    /* Des valeurs négatives le font sortir de sa boîte vers le haut et la gauche */
    top: 12%; 
    left: -30%; 
    
    /* 2. Une forme concrète et stricte */
    width: 155%; /* Le cercle fait la même taille que le conteneur du téléphone */
    aspect-ratio: 1 / 1;
    border-radius: 50%; /* Ça force la forme en cercle parfait */
    
    /* 3. Ton dégradé exact */
    background: radial-gradient(circle, #32f459 30%, #4db562 100%);
    
    /* Assure que le cercle reste bien derrière le téléphone */
    z-index: 0; 
}

.pic-container img {
    min-width: 320px;
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
    z-index: 5;
    width: 105px !important;
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

.card-top-left, .card-top-right       { --ty-base: -140px; }
.card-bottom-left, .card-bottom-right { --ty-base: 40px; }
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
    .pic-container::before {
    content: '';
    position: absolute;
    
    /* 1. Le déplacement en haut à gauche */
    /* Des valeurs négatives le font sortir de sa boîte vers le haut et la gauche */
    top: 20%; 
    left: 10%; 
    
    /* 2. Une forme concrète et stricte */
    width: 80%; /* Le cercle fait la même taille que le conteneur du téléphone */
    aspect-ratio: 1 / 1;
    border-radius: 50%; /* Ça force la forme en cercle parfait */
    
    /* 3. Ton dégradé exact */
    background: radial-gradient(circle, #32f459 30%, #4db562 100%);
    
    /* Assure que le cercle reste bien derrière le téléphone */
    z-index: 0; 
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
    }

    .hero-section > .content-wrapper {
        top: 2rem;
    }

    .pic-wrapper {
        padding: 160px 80px;
    }
    /* L'image passe à sa taille moyenne */
    .pic-container, .pic-container img {
        width: 300px;
        min-width: 300px;
    }
    .pic-container::before {
    content: '';
    position: absolute;
    
    /* 1. Le déplacement en haut à gauche */
    /* Des valeurs négatives le font sortir de sa boîte vers le haut et la gauche */
    top: 20%; 
    left: 10%; 
    
    /* 2. Une forme concrète et stricte */
    width: 80%; /* Le cercle fait la même taille que le conteneur du téléphone */
    aspect-ratio: 1 / 1;
    border-radius: 50%; /* Ça force la forme en cercle parfait */
    
    /* 3. Ton dégradé exact */
    background: radial-gradient(circle, #32f459 30%, #4db562 100%);
    
    /* Assure que le cercle reste bien derrière le téléphone */
    z-index: 0; 
}

    .floating-card {
        width: 160px !important;
    }

    .card-top-left, .card-top-right       { --ty-base: -220px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 80px; }
    .card-top-left, .card-mid-left, .card-bottom-left   { --tx: -65%; }
    .card-top-right, .card-mid-right, .card-bottom-right { --tx: 65%; }
}

/* ── 💻 Desktop (A partir de 1200px) ─────────────────────────── */
@media (min-width: 1200px) {
    
    .hero-section {
        flex-direction: row; 
        justify-content: space-between;
        align-items: center;
        padding: 1rem 3rem !important;
        gap: 5rem;
        height: 100vh !important;
        min-height: 600px !important;
        top: 0; /* Plus besoin de pousser vers le bas */
    }

    .hero-section > .content-wrapper {
        width: 50%;
        top: 0; 
    }

    .pic-wrapper {
        width: 50%;
        padding: 60px 40px;
    }
    
    .pic-container, .pic-container img {
        width: 300px;
        min-width: 355px;
    }

    .pic-container::before {
    content: '';
    position: absolute;
    
    /* 1. Le déplacement en haut à gauche */
    /* Des valeurs négatives le font sortir de sa boîte vers le haut et la gauche */
    top: 10%; 
    left: 5%; 
    
    /* 2. Une forme concrète et stricte */
    width: 90%; /* Le cercle fait la même taille que le conteneur du téléphone */
    aspect-ratio: 1 / 1;
    border-radius: 50%; /* Ça force la forme en cercle parfait */
    
    /* 3. Ton dégradé exact */
    background: radial-gradient(circle, #32f459 30%, #4db562 100%);
    
    /* Assure que le cercle reste bien derrière le téléphone */
    z-index: 0; 
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