<template>
    <section class="hero-section">
        <!-- Les vagues fluides en arrière-plan -->
        <div class="wave-section"></div>

        <!-- ── ZONE TEXTE ANIMÉE ── -->
        <div class="content-wrapper">
            
            <!-- ETAPE 1 & 2 : L'animation "Unroll" du CC -->
            <div v-if="step <= 2" 
                 class="brand-unroll-container" 
                 :class="{ 'is-landing': step === 0, 'is-hidden': step === 2 }">
                
                <span class="welcome-text" :class="{ 'show': step >= 1 }">
                    Bienvenue sur
                </span>
                
                <div class="logo-morph premium-gradient" :class="{ 'is-unrolling': step >= 1 }">
                    <span class="letter">C</span><span class="hidden-letters" :class="{ 'show': step >= 1 }">ontrat</span><span class="letter">C</span><span class="hidden-letters" :class="{ 'show': step >= 1 }">hap</span>
                </div>
            </div>

            <!-- ETAPE 3 : Apparition cinématique mot par mot -->
            <div v-if="step >= 3" class="final-phrase">
                <span class="word show-1">Téléchargez&nbsp;</span>
                <span class="word show-2">facilement&nbsp;</span>
                <span class="word show-4"><span class="premium-gradient">tous vos contrats</span></span>
            </div>
            
            <!-- ETAPE 4 : Apparition des boutons (Principal + Secondaire) -->
            <div class="buttons-group" :class="{ 'show': showButton }">
                
                <div class="revision-cta main-action premium-shadow" @click="router.push('/contractBank')">
                    <div class="btn-shine"></div>
                    <div class="cta-texts">
                        <p>Télécharger vos contrats</p>
                    </div>
                    <div class="cta-arrow floating-arrow">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
                    </div>
                </div>

            </div>
        </div>
        
        <!-- ── ZONE IMAGE & CARTES FLOTTANTES ── -->
        <div class="pic-wrapper" :class="{ 'fade-in-image': step >= 0 }">
            <div class="pic-container">
                <img src="/Accueil_2.png" alt="Contrats OHADA">

                <stat-cards class="floating-card card-top-left"    title="Contrats" @click="router.push('/contractBank')" />
                <stat-cards class="floating-card card-top-right"   title="Calcul de droits" @click="router.push('/lawCalcul')" />
                
                <stat-cards class="floating-card card-bottom-left"  title="Centre d'appel" @click="router.push('/services')" />
                <stat-cards class="floating-card card-bottom-right" title="Experts" @click="router.push('/pro')" />
            </div>
        </div>

        <caroussel-countries/>
    </section>
</template>

<script lang="ts">
import { onMounted, ref, defineComponent } from 'vue'
import mainButton from '../buttons/mainButton.vue'
import statCards from '../cards/statCards.vue'
import { useRouter } from 'vue-router'
import carousselCountries from '../carousselCountries.vue'

export default defineComponent({
    name: 'HeroSecondSection',
    components: { 
        mainButton, 
        statCards,
        carousselCountries
    },

    setup() {
        const router = useRouter();

        const step = ref<number>(-1); 
        const showButton = ref<boolean>(false);

        onMounted(() => {
            setTimeout(() => { step.value = 0; }, 100);    
            setTimeout(() => { step.value = 1; }, 1600);   
            setTimeout(() => { step.value = 2; }, 4200);   
            setTimeout(() => { step.value = 3; }, 4800);   
            setTimeout(() => { showButton.value = true; }, 5800); 
        })

        return {
            step,
            showButton,
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
    padding: 1rem;
    padding-bottom: 4rem;
    background: radial-gradient(circle, #202b4a 30%, #0f0f0f 100%);
}

.content-wrapper {
    position: relative;
    z-index: 10; 
    display: flex;
    flex-direction: column;
    align-items: center; /* Centré sur mobile */
    justify-content: center;
    width: 100%;
    margin-top: 4rem;
}

/* ── NOUVELLES VAGUES FLUIDES ──────────────────── */
.wave-section {
    position: absolute;
    inset: 0;
    overflow: hidden;
    z-index: 0;
    pointer-events: none; 
}

.wave-section::before,
.wave-section::after {
    content: "";
    position: absolute;
    width: 250vw; 
    height: 250vw;
    top: 50%; 
    left: 50%;
    transform: translateX(-50%);
    border-radius: 42%; 
    opacity: 0.6;
}

.wave-section::before {
    background: linear-gradient(to top, rgba(21, 107, 169, 0.016), rgba(21, 107, 169, 0.203));
    animation: rotate-waves 30s linear infinite;
}

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

/* ========================================================
   ANIMATIONS TEXTUELLES (CC & PHRASE)
======================================================== */
.brand-unroll-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Centré sur mobile */
    justify-content: center;
    transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    min-height: 120px;
}

.welcome-text {
    display: block;
    font-size: clamp(1rem, 4vw, 1.5rem);
    font-weight: 500;
    color: #e2e8f0; 
    opacity: 0;
    transform: translateY(20px);
    transition: transform 1s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.8s ease;
    margin-bottom: -5px; 
}

.welcome-text.show { transform: translateY(0); opacity: 1; }

.logo-morph {
    font-size: clamp(4rem, 15vw, 6rem);
    font-weight: 800;
    display: flex;
    align-items: baseline;
    line-height: 1.1;
    letter-spacing: -0.04em;
    white-space: nowrap;
    transition: font-size 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.brand-unroll-container.is-landing {
    animation: landIn 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes landIn {
    0% { transform: scale(1.1) translateY(-20px); filter: blur(10px); opacity: 0; }
    100% { transform: scale(1) translateY(0); filter: blur(0px); opacity: 1; }
}

.logo-morph.is-unrolling {
    font-size: clamp(2rem, 8vw, 3.5rem);
    letter-spacing: -0.02em;
}

.letter { display: inline-block; font-size: 5rem }

.hidden-letters {
    display: inline-block;
    overflow: hidden;
    max-width: 0; 
    opacity: 0;
    vertical-align: bottom;
    white-space: nowrap;
    transition: max-width 1.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.8s ease 0.2s;
}

.hidden-letters.show { max-width: 300px; opacity: 1; }

.brand-unroll-container.is-hidden {
    animation: cinematicVanish 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes cinematicVanish {
    0% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    100% { opacity: 0; transform: translateY(-30px) scale(1.05); filter: blur(15px); display: none; }
}

.final-phrase {
    font-size: clamp(2rem, 7.5vw, 3.5rem);
    font-weight: 700;
    color: var(--my-white, #ffffff);
    line-height: 1.2;
    margin: 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: center; /* Centré sur mobile */
    gap: 0.25em;
    letter-spacing: -0.02em;
}

.word { display: inline-block; opacity: 0; }

.show-1 { animation: cinematicReveal 1s cubic-bezier(0.16, 1, 0.3, 1) forwards 0s; }
.show-2 { animation: cinematicReveal 1s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.15s; }
.show-3 { animation: cinematicReveal 1s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.3s; }
.show-4 { animation: cinematicReveal 1s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.45s; }

@keyframes cinematicReveal {
    0% { transform: translateY(30px) rotate(2deg); opacity: 0; filter: blur(8px); }
    100% { transform: translateY(0) rotate(0deg); opacity: 1; filter: blur(0px); }
}

.premium-gradient {
    background: linear-gradient(110deg, #32f459 0%, #156ca9 40%, #5ceb7a 60%, #156ca9 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    animation: shineText 5s linear infinite;
    display: inline-block; 
}

@keyframes shineText { to { background-position: 200% center; } }

/* ── BOUTONS ── */
.buttons-group {
    margin-top: 2.5rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    opacity: 0;
    transform: translateY(20px);
    transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.buttons-group.show {
    opacity: 1;
    transform: translateY(0);
}

.revision-cta {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    padding: 12px 16px 12px 24px;
    border-radius: 50px;
    cursor: pointer;
    width: 100%;
    max-width: 320px;
    overflow: hidden; 
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.main-action {
    background: linear-gradient(135deg, #156ca9 0%, #0d4670 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.premium-shadow {
    box-shadow: 0 15px 35px -5px rgba(21, 108, 169, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.glass-btn {
    background: rgba(255, 255, 255, 0.05); 
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.revision-cta:hover { transform: translateY(-4px) scale(1.02); }
.main-action:hover { box-shadow: 0 20px 40px -5px rgba(50, 244, 89, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3); }
.glass-btn:hover { background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.3); }

.btn-shine {
    position: absolute;
    top: 0; left: -100%; width: 50%; height: 100%;
    background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0) 100%);
    transform: skewX(-25deg);
    animation: sweep 4s infinite 2s; 
    pointer-events: none;
}

@keyframes sweep { 0% { left: -100%; } 20% { left: 200%; } 100% { left: 200%; } }

.cta-texts p {
    color: #ffffff;
    font-weight: 500;
    font-size: clamp(0.95rem, 2vw, 1.05rem);
    margin: 0;
    position: relative;
    z-index: 2;
}

.cta-arrow {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    flex-shrink: 0;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.main-action .cta-arrow { background: #ffffff; color: #156ca9; }
.glass-btn .cta-arrow { background: #156ca9; color: #ffffff; }

.main-action:hover .cta-arrow { background: #32f459; color: #080a0f; transform: rotate(45deg); }
.glass-btn:hover .cta-arrow { background: #ffffff; color: #156ca9; transform: rotate(45deg); }

.floating-arrow svg { width: 18px; height: 18px; }

/* ── ZONE IMAGE & CARTES ── */
.pic-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 10px;
    box-sizing: border-box;
    width: 100%;
    opacity: 0;
    transition: opacity 2s ease 0.5s;
}

.pic-wrapper.fade-in-image { opacity: 1; }

.pic-container {
    position: relative;
    width: 200px; 
    display: inline-flex; 
    justify-content: center;
    align-items: center;
    z-index: 1;
}

.pic-container::before {
    content: '';
    position: absolute;
    top: 22%; left: -2%; width: 100%; aspect-ratio: 1 / 1;
    border-radius: 50%; 
    background: radial-gradient(circle at 40% 65%, #3197f5 0%, #1a62cc 55%, #082d73 100%);
    box-shadow: 0 0 60px 20px rgba(11, 16, 12, 0.4); 
    z-index: 0; 
}

.pic-container img {
    min-width: 250px;
    aspect-ratio: 1 / 1; 
    object-fit: cover; 
    border-radius: 50%; 
    position: relative;
    z-index: 1;
}

.floating-card {
    position: absolute;
    z-index: 5;
    width: 110px !important;
    top: 50%;
    transform: translateX(var(--tx)) translateY(var(--ty-base));
    animation: float 4s ease-in-out infinite;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.card-top-left, .card-top-right       { --ty-base: -120px; }
.card-bottom-left, .card-bottom-right { --ty-base: 60px; }
.card-top-left, .card-bottom-left   { left: 0; --tx: -50%; }
.card-top-right, .card-bottom-right { right: 0; --tx: 50%; }

.card-top-left { animation-delay: 0s; }
.card-top-right { animation-delay: 0.8s; }
.card-bottom-left { animation-delay: 1.6s; }
.card-bottom-right { animation-delay: 2.4s; }

@media (min-width: 480px) {
    .pic-container { width: 250px; }
    .pic-container img { min-width: 300px; }
    .floating-card { width: 130px !important; }
    .card-top-left, .card-top-right       { --ty-base: -150px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 80px; }
    .card-top-left, .card-bottom-left   { --tx: -55%; }
    .card-top-right, .card-bottom-right { --tx: 55%; }
}

/* ── 平板 Tablettes (A partir de 768px) ───────────────────────── */
@media (min-width: 768px) {
    .buttons-group { flex-direction: row; justify-content: center; }
    .revision-cta { width: fit-content; }
    
    .pic-wrapper { padding: 80px 40px; }
    .pic-container { width: 300px; }
    .pic-container img { min-width: 350px; }
    .floating-card { width: 160px !important; }
    .card-top-left, .card-top-right       { --ty-base: -180px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 100px; }
    .card-top-left, .card-bottom-left   { --tx: -60%; }
    .card-top-right, .card-bottom-right { --tx: 60%; }
}

/* ── 💻 Desktop (A partir de 1200px) ─────────────────────────── */
@media (min-width: 1200px) {
    .hero-section {
        flex-direction: row; justify-content: space-between; align-items: center;
        padding: 1rem 3rem !important; gap: 2rem; min-height: 100vh;
    }
    
    /* On aligne le texte et l'animation sur la gauche */
    .content-wrapper { 
        width: 50%; 
        align-items: flex-start; 
        margin-top: 0;
        text-align: left;
    }
    .brand-unroll-container { align-items: flex-start; min-height: 180px; }
    .final-phrase { justify-content: flex-start; }
    .buttons-group { justify-content: flex-start; }

    .logo-morph.is-unrolling { font-size: clamp(3rem, 5vw, 5.5rem); }
    .final-phrase { font-size: clamp(3rem, 5vw, 5.5rem); }

    .pic-wrapper { width: 50%; padding: 60px 40px; justify-content: flex-end; }
    .pic-container { width: 350px; }
    .pic-container img { min-width: 450px; }
    
    .floating-card { width: 140px !important; min-height: 110px; }
    .floating-card:hover {
        animation-play-state: paused; cursor: pointer;
        transform: translateX(var(--tx)) translateY(var(--ty-base)) scale(1.05);
        transition: transform 0.2s ease-in-out; z-index: 20; 
    }
    .card-top-left, .card-top-right       { --ty-base: -180px; }
    .card-bottom-left, .card-bottom-right { --ty-base: 120px; }
    .card-top-left, .card-bottom-left   { --tx: -20%; }
    .card-top-right, .card-bottom-right { --tx: 20%; }
}

@keyframes float {
    0%, 100% { transform: translateX(var(--tx)) translateY(var(--ty-base)); }
    50%      { transform: translateX(var(--tx)) translateY(calc(var(--ty-base) - 8px)); }
}
</style>