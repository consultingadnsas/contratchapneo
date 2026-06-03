<template>
    <section class="hero-section">
        <div class="bg-shape shape-bottom-right"></div>
        <div class="bg-shape shape-top-left"></div>

        <div class="flex flex-col gap-4 content-wrapper">
            
            <!--  

             <span>
                {{ displayText }}<span class="cursor">|</span>
            </span>
            
            -->
            
            <h1>
                Téléchargez librement vos contrats
            </h1>
            <base-research-input/>
        </div>
        <div class="pic-wrapper">
            <div class="pic-container">
                <img src="../../assets/pictures/ContratChap/Accueil 2.png" alt="Contrats OHADA">

                <stat-cards class="floating-card card-top-left"    title="Banque de contrats" @click="router.push('/contractBank')" />
                <stat-cards class="floating-card card-top-right"   title="Outil de Calcul" />
                
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
import { useRouter } from 'vue-router'

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
    gap: 2rem;
    padding: 4rem 1rem 1rem 1rem;
    background: var(--nathan-blue);
    position: relative; 
    z-index: 1;
}

/* ── Le fond d'écran avec motif Outils d'Affaires ──────── */
.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    
    /* Motif SVG avec plusieurs outils d'affaires (Mallette, Document, Graphique, Calculatrice, Dossier) */
    background-image: url("data:image/svg+xml,%3Csvg width='300' height='300' viewBox='0 0 300 300' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23ffffff' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round' stroke-opacity='0.08'%3E%3C!-- Mallette --%3E%3Cg transform='translate(40, 40) scale(1.5)'%3E%3Crect x='2' y='7' width='20' height='14' rx='2' ry='2'/%3E%3Cpath d='M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16'/%3E%3C/g%3E%3C!-- Document --%3E%3Cg transform='translate(200, 50) scale(1.5)'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='16' y1='13' x2='8' y2='13'/%3E%3Cline x1='16' y1='17' x2='8' y2='17'/%3E%3Cpolyline points='10 9 9 9 8 9'/%3E%3C/g%3E%3C!-- Graphique --%3E%3Cg transform='translate(120, 140) scale(1.5)'%3E%3Cpolyline points='23 6 13.5 15.5 8.5 10.5 1 18'/%3E%3Cpolyline points='17 6 23 6 23 12'/%3E%3C/g%3E%3C!-- Calculatrice --%3E%3Cg transform='translate(40, 220) scale(1.5)'%3E%3Crect x='4' y='2' width='16' height='20' rx='2' ry='2'/%3E%3Cline x1='8' y1='6' x2='16' y2='6'/%3E%3Cline x1='16' y1='10' x2='16' y2='10'/%3E%3Cline x1='12' y1='10' x2='12' y2='10'/%3E%3Cline x1='8' y1='10' x2='8' y2='10'/%3E%3Cline x1='8' y1='14' x2='8' y2='14'/%3E%3Cline x1='12' y1='14' x2='12' y2='14'/%3E%3Cline x1='16' y1='14' x2='16' y2='14'/%3E%3Cline x1='8' y1='18' x2='8' y2='18'/%3E%3Cline x1='12' y1='18' x2='12' y2='18'/%3E%3Cline x1='16' y1='18' x2='16' y2='18'/%3E%3C/g%3E%3C!-- Dossier --%3E%3Cg transform='translate(220, 210) scale(1.5)'%3E%3Cpath d='M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    
    background-size: 300px 300px; /* Contrôle l'espacement du groupe d'icônes */
    background-repeat: repeat;
    
    z-index: -1; 
    pointer-events: none; 
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
    padding: 140px 40px;
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
    top: 25%; 
    left: -12%; 
    
    /* 2. Une forme concrète et stricte */
    width: 120%; /* Le cercle fait la même taille que le conteneur du téléphone */
    aspect-ratio: 1 / 1;
    border-radius: 50%; /* Ça force la forme en cercle parfait */
    
    /* 3. Ton dégradé exact */
    background: radial-gradient(circle, #32f459 30%, #4db562 100%);
    
    /* Assure que le cercle reste bien derrière le téléphone */
    z-index: 0; 
}

.pic-container img {
    min-width: 300px;
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
        padding: 1rem 2rem !important;
        gap: 6rem;
        height: 100vh !important;
        min-height: 600px !important;
        top: 0; /* Plus besoin de pousser vers le bas */
    }

    .hero-section > .content-wrapper {
        width: 50%;
        top: 0; 
    }

    .content-wrapper span{
        font-weight: 500;
        color: #32f459;
    }

    .pic-wrapper {
        width: 50%;
        padding: 60px 40px;
    }

    .pic-container, .pic-container img {
        width: 300px;
        min-width: 350px;
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