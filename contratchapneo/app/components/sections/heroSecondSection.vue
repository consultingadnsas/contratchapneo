<template>
    <section class="hero-section">
        <div class="wave-section"></div>

        <div class="flex flex-col gap-4 content-wrapper">
            <div class="research-desktop">
               <base-research-input/>
                <h1>
                    Téléchargez facilement tous <span class="gradient-text2">vos</span> 
                </h1>
                <span class="gradient-text">contrats</span>
            </div>
            
            <div class="desktop-buttons-group">
                <div class="revision-cta desktop-cta main-action" @click="router.push('/contractBank')">
                    <div class="cta-texts">
                        <p>Télécharger vos contrats</p>
                    </div>
                    <div class="cta-arrow floating-arrow">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
                    </div>
                </div>

                <div class="revision-cta desktop-cta secondary-action glass-btn" @click="router.push('/etudeContrat')">
                    <div class="cta-texts">
                        <p>Réviser un contrat</p>
                    </div>
                    <div class="cta-arrow floating-arrow">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
                     </div>
                </div>
            </div>

             <div class="research-mobile">
                <h1>
                    Téléchargez facilement tous <span class="gradient-text">vos contrats</span>
                </h1> 
                <base-research-input/>
            </div>
        </div>
        
        <div class="pic-wrapper">
            <div class="pic-container">
                <img src="/Accueil 2.png" alt="Contrats OHADA">

                <stat-cards class="floating-card card-top-left"    title="Banque de contrats" @click="router.push('/contractBank')" />
                <stat-cards class="floating-card card-top-right"   title="Calcul de droits" @click="router.push('/lawCalcul')" />
                
                <stat-cards class="floating-card card-bottom-left"  title="Services juridiques" @click="router.push('/services')" />
                <stat-cards class="floating-card card-bottom-right" title="Experts" @click="router.push('/pro')" />
            </div>
        </div>

        <div class="mobile-buttons-group">
            <div class="revision-cta mobile-cta main-action" @click="router.push('/contractBank')">
                <div class="cta-texts">
                    <p>Télécharger un contrat</p>
                </div>
                <div class="cta-arrow floating-arrow">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                    </svg>
                </div>
            </div>

            <div class="revision-cta mobile-cta secondary-action glass-btn" @click="router.push('/etude-contrats')">
                <div class="cta-texts">
                    <p>Besoin d'une révision de contrat ?</p>
                </div>
                <div class="cta-arrow floating-arrow">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                    </svg>
                </div>
            </div>
        </div>

        <caroussel-countries/>
    </section>
</template>

<script lang="ts">
import { onMounted, ref, defineComponent } from 'vue'
import mainButton from '../buttons/mainButton.vue'
import BaseResearchInput from '../input/BaseResearchInput.vue'
import statCards from '../cards/statCards.vue'
import { useRouter } from 'vue-router'
import carousselCountries from '../carousselCountries.vue'

export default defineComponent({
    name: 'HeroSecondSection',
    components: { 
        mainButton, 
        BaseResearchInput, 
        statCards,
        carousselCountries
    },

    setup() {
        const router = useRouter();

        const phrases = [
            'Profitez de nos contrats gratuits.',
            'Sécurisez juridiquement vos business en un clic.',
            'Accédez à des modèles conformes aux droits OHADA.'
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
            router,
        }
    }
})
</script>

<style scoped>
/* ── 📱 Mobile First ─────── */
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
    padding: 1rem 1rem 1rem 1rem;
    padding-bottom: 4rem;
    background: radial-gradient(circle, #202b4a 30%, #0f0f0f 100%);
}

.content-wrapper {
    position: relative;
    z-index: 10; /* Sécurise le contenu au-dessus des vagues */
}

/* Bloc texte */
.hero-section h1 {
    font-size: clamp(1.5rem, 6vw, 2.5rem); 
    font-weight: 600;
    color: var(--my-white);
    line-height: 1.2;
    margin: 0;
    padding-top: 5rem
}

/* DÉGRADÉS SUR TEXTE */
.gradient-text {
    font-size: clamp(1rem, 3.5vw, 1.3rem);
    font-weight: 600;
    line-height: 1.2;
    background: linear-gradient(90deg, #32f459 0%, #156ca9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block; 
}
.gradient-text2 {
    font-size: clamp(1rem, 3.5vw, 1.3rem);
    font-weight: 600;
    line-height: 1.2;
    background: linear-gradient(70deg, #32f459 0%, #156ca9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block; 
}

/* ── NOUVELLES VAGUES FLUIDES EN ARRIÈRE-PLAN ──────────────────── */
.wave-section {
    position: absolute;
    inset: 0;
    overflow: hidden;
    z-index: 0;
    pointer-events: none; /* CRUCIAL: Rend les vagues "fantômes" pour les clics */
}

/* La forme de base des vagues */
.wave-section::before,
.wave-section::after {
    content: "";
    position: absolute;
    width: 250vw; /* Très large pour avoir une courbure douce */
    height: 250vw;
    top: 50%; /* Position sur l'écran */
    left: 50%;
    transform: translateX(-50%);
    border-radius: 42%; /* Déformation du cercle pour l'effet vague */
    opacity: 0.6;
}

/* Vague 1 (Bleutée) */
.wave-section::before {
    background: linear-gradient(to top, rgba(21, 107, 169, 0.016), rgba(21, 107, 169, 0.203));
    animation: rotate-waves 30s linear infinite;
}

/* Vague 2 (Verte, légèrement décalée) */
.wave-section::after {
    top: 55%;
    border-radius: 38%;
    background: linear-gradient(to top, rgba(50, 244, 89, 0.071), rgba(50, 244, 89, 0.016));
    animation: rotate-waves 35s linear infinite reverse;
}

@keyframes rotate-waves {
    0% { transform: translateX(-50%) rotate(0deg); }
    100% { transform: translateX(-50%) rotate(360deg); }
}
/* ───────────────────────────────────────────────────────────── */

.cursor {
    color: var(--secondary-light-color);
    animation: blink 0.7s infinite;
    margin-left: 4px;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

/* Conteneur image + cartes */
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

/* CERCLE LUMINEUX DERRIÈRE L'IMAGE */
.pic-container::before {
    content: '';
    position: absolute;
    top: 12%; 
    left: -30%; 
    width: 155%; 
    aspect-ratio: 1 / 1;
    border-radius: 50%; 
    background: radial-gradient(circle at 40% 65%, #3197f5 0%, #1a62cc 55%, #082d73 100%);
    box-shadow: 0 0 60px 20px rgba(11, 16, 12, 0.4); 
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

/* Cartes flottantes */
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

/* ── BOUTONS ── */
.mobile-buttons-group {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    z-index: 10;
}

.desktop-buttons-group {
    display: none; 
    flex-direction: row;
    gap: 1.5rem;
    margin-top: 2rem;
    position: relative;
    z-index: 20;
}

.revision-cta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    padding: 12px 16px 12px 20px;
    border-radius: 50px;
    cursor: pointer;
    width: fit-content;
    transition: all 0.3s ease;
}

.main-action {
    background: var(--primary-color, #156ca9);
    border: 1px solid transparent;
}

.main-action:hover {
    background: #0f4c78; 
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(21, 108, 169, 0.4);
}

.glass-btn {
    background: rgba(255, 255, 255, 0.05); 
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.glass-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.revision-cta .cta-texts {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.revision-cta .cta-texts p {
    color: var(--my-white, #ffffff);
    font-weight: 600;
    font-size: clamp(0.8rem, 2vw, 0.8rem);
}

.cta-texts p{
    margin-left: 25px
}

.revision-cta .cta-texts span {
    color: #a3c2d1; 
    font-size: clamp(0.75rem, 1.5vw, 0.85rem);
    font-weight: 500;
    opacity: 0.9;
    margin-right: 15px
}

.cta-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height:30px;
    border-radius: 50%;
    background: white;
    color: var(--primary-color);
    flex-shrink: 0;
    transition: all 0.3s ease;
}

.glass-btn .cta-arrow {
    background: var(--primary-color);
    color: white;
}

.main-action:hover .cta-arrow {
    background: #32f459;
    color: #0f0f0f;
}

.glass-btn:hover .cta-arrow {
    background:white ;
    color: var(--primary-color)
}

.desktop-cta { display: none !important; }
.research-desktop{ display: none !important; }

.research-mobile{ display: grid !important; }
.research-mobile h1 .gradient-text{ font-size: 2rem; text-align: center; }
.mobile-cta { display: flex !important; width: 100%; }

@media (max-width: 480px) {
    .mobile-buttons-group { margin-top: -2rem; }
}

/* ── 📐 Phablettes ──── */
@media (min-width: 480px) {
    .pic-container, .pic-container img { width: 230px; min-width: 230px; }
    .pic-container::before {
        top: 20%; left: 10%; width: 80%; aspect-ratio: 1 / 1; border-radius: 50%; 
        background: radial-gradient(circle, #3279f4 30%, #212a5b 100%);
        box-shadow: 0 0 60px 20px rgba(11, 16, 12, 0.4); z-index: 0; 
    }
    .floating-card { width: 130px !important; }
    .card-top-left, .card-top-right       { --ty-base: -170px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 80px; }
    .card-top-left, .card-mid-left, .card-bottom-left   { --tx: -60%; }
    .card-top-right, .card-mid-right, .card-bottom-right { --tx: 60%; }
}

/* ── 平板 Tablettes (A partir de 768px) ───────────────────────── */
@media (min-width: 768px) {
    .hero-section { padding: 3rem 2.5rem; gap: 3rem; }
    .hero-section > .content-wrapper { top: 2rem; }
    .pic-wrapper { padding: 160px 80px; }
    .pic-container, .pic-container img { width: 300px; min-width: 300px; }
    .pic-container::before {
        top: 20%; left: 10%; width: 80%; aspect-ratio: 1 / 1; border-radius: 50%; 
        background: radial-gradient(circle at 40% 65%, #3197f5 0%, #1a62cc 55%, #082d73 100%);
        box-shadow: 0 0 60px 20px rgba(11, 16, 12, 0.4); z-index: 0; 
    }
    .floating-card { width: 160px !important; }
    .card-top-left, .card-top-right       { --ty-base: -220px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 80px; }
    .card-top-left, .card-mid-left, .card-bottom-left   { --tx: -65%; }
    .card-top-right, .card-mid-right, .card-bottom-right { --tx: 65%; }
    
    .desktop-cta { display: flex !important; }
    .desktop-buttons-group { display: flex; }
    .research-desktop{ display: grid !important; }
    .research-desktop h1{ font-size: 3.5rem; text-align: left; }
    .research-desktop .gradient-text { text-align: left; font-size: 3.5rem; }
    .gradient-text2 { text-align: left; font-size: 3.5rem; }
    .research-mobile{ display:none !important; }
    .mobile-buttons-group { display: none !important; }
}

/* ── 💻 Desktop (A partir de 1200px) ─────────────────────────── */
@media (min-width: 1200px) {
    .hero-section {
        flex-direction: row; justify-content: space-between; align-items: center;
        padding: 1rem 3rem !important; gap: 5rem; height: 100vh !important; min-height: 600px !important; top: 0; 
    }
    .hero-section > .content-wrapper { width: 50%; top: 0; gap: 0rem; align-items: flex-start; }
    .pic-wrapper { width: 50%; padding: 60px 40px; }
    .pic-container, .pic-container img { width: 300px; min-width: 450px; }

    .pic-container::before {
        top: 20%; left: 10%; width: 80%; aspect-ratio: 1 / 1; border-radius: 50%; 
        background: radial-gradient(circle at 40% 65%, #3197f5 0%, #1a62cc 55%, #082d73 100%);
        box-shadow: 0 0 60px 20px rgba(11, 16, 12, 0.4); z-index: 0; 
    }
    
    .floating-card {
        width: 130px !important; min-height: 110px; box-sizing: border-box; padding: 10px;
        display: flex; align-items: center; justify-content: center; text-align: center;
    }
    .floating-card:hover {
        animation-play-state: paused; cursor: pointer;
        transform: translateX(var(--tx)) translateY(var(--ty-base)) scale(1.05);
        transition: transform 0.2s ease-in-out; z-index: 20; 
    }
    .card-top-left, .card-top-right       { --ty-base: -180px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 80px; }
    .card-top-left, .card-bottom-left   { --tx: -10%; }
    .card-top-right, .card-bottom-right { --tx: 10%; }
}

@keyframes float {
    0%, 100% { transform: translateX(var(--tx)) translateY(var(--ty-base)); }
    50%      { transform: translateX(var(--tx)) translateY(calc(var(--ty-base) - 8px)); }
}
</style>