<template>
    <div class="page-wrapper">
        <main class="diagnostic-page">
            <Navbar theme="light"/>

            <!-- HERO <-> TUNNEL (fondu sur la même page) -->
            <Transition name="page-fade" mode="out-in">
                <!-- HERO SECTION -->
                <section v-if="!showTunnel" key="hero" class="hero-section">
                    <div class="hero-container">
                        <!-- Left: Content -->
                        <div class="hero-content">
                            <h1 class="main-title slide-up-delay">Un doute juridique?<br><span class="hl">Obtenez votre Consultation.</span></h1>

                            <div class="action-container slide-up-delay-3">
                                <button @click="startTunnel" class="btn-primary motion-btn">
                                    Démarrer mon diagnostic
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <line x1="5" y1="12" x2="19" y2="12"></line>
                                        <polyline points="12 5 19 12 12 19"></polyline>
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Right: Image with 4 Thought Bubbles -->
                        <div class="hero-image-wrapper slide-up">
                            <!-- Points d'interrogation flottants -->
                            <div class="q-mark q-1">?</div>
                            <div class="q-mark q-2">?</div>

                            <div class="thought-bubble tb-1">Dois-je signer ce contrat ?</div>
                            <div class="thought-bubble tb-2">Quels sont mes droits ici ?</div>
                            <div class="thought-bubble tb-3">Comment me protéger ?</div>
                            <div class="thought-bubble tb-4">Que faire face à ce litige ?</div>
                            <img src="/Diagnostic2.png" alt="Diagnostic Juridique" class="hero-image" />
                        </div>
                    </div>
                </section>

                <!-- TUNNEL DE COMMUNICATION -->
                <DiagnosticTunnel v-else key="tunnel" @back="backToHero" />
            </Transition>

            <faqSection :faqsData="diagnosticFaqs" />
        </main>
    </div>
    <Footer />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Navbar from '../components/navigation/navbar.vue';
import Footer from '../components/sections/footerSection.vue';
import faqSection from '../components/sections/faqSection.vue'; 
import DiagnosticTunnel from '../components/sections/diagnosticTunnel.vue';

export default defineComponent({
    name: 'DiagnosticJuridiquePage',
    components: {
        Navbar,
        Footer,
        faqSection,
        DiagnosticTunnel
    },
    setup() {
        const diagnosticFaqs = ref([
            {
                question: "Sur quels sujets puis-je obtenir un diagnostic ?",
                answer: "Contrats, création d’entreprise, litiges, droit du travail, immobilier, fiscalité… Si vous hésitez, décrivez simplement votre situation.",
                isOpen: false
            },
            {
                question: "Le diagnostic est-il confidentiel ?",
                answer: "Oui, tous vos échanges avec nos juristes sont strictement confidentiels. Les informations que vous partagez ne sont utilisées que pour vous fournir une analyse appropriée.",
                isOpen: false
            },
            {
                question: "Quels sont les horaires de la ligne diagnostic ?",
                answer: "Notre ligne diagnostic est ouverte du lundi au vendredi, de 9h à 18h. Vous pouvez nous appeler directement pendant ces heures.",
                isOpen: false
            },
            {
                question: "Le diagnostic téléphonique remplace-t-il une consultation complète ?",
                answer: "Non. Il s’agit d’un premier état des lieux de votre situation. Le juriste vous indiquera si une consultation ou un accompagnement approfondi est utile.",
                isOpen: false
            },
            {
                question: "Que dois-je préparer avant mon appel ?",
                answer: "Il est conseillé de rassembler les documents clés liés à votre situation (contrat, correspondances, dates importantes, noms des parties). Cela permet un diagnostic plus précis en moins de temps.",
                isOpen: false
            }
        ]);

        const showTunnel = ref(false);

        const startTunnel = () => {
            showTunnel.value = true;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        const backToHero = () => {
            showTunnel.value = false;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        return { 
            diagnosticFaqs, 
            showTunnel,
            startTunnel,
            backToHero
        };
    }
});
</script>

<style scoped>
/* ==========================================
   STYLE GLOBAL & MISE EN PAGE 
========================================== */
.page-wrapper {
    background-color: #f8fafc; 
    padding: 2rem 1rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Inter', sans-serif;
}

.diagnostic-page {
    background-color: #ffffff; 
    width: 100%;
    max-width: 1200px;
    border-radius: 40px; 
    box-shadow: 0 25px 60px rgba(15, 23, 42, 0.04); 
    color: #0f172a; 
    overflow: hidden;
    display: flex;
    flex-direction: column;
    margin-bottom: 2rem; 
}

/* ==========================================
   FONDU HERO <-> TUNNEL
========================================== */
.page-fade-enter-active,
.page-fade-leave-active {
    transition: opacity 0.45s ease, transform 0.45s ease;
}
.page-fade-enter-from,
.page-fade-leave-to {
    opacity: 0;
    transform: translateY(12px);
}

/* ==========================================
   HERO SECTION (Motion Design)
========================================== */
.hero-section {
    width: 100%;
    padding: 7rem 2rem 5rem 2rem;
    position: relative;
    overflow: hidden;
    background: #ffffff;
}

.hero-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 4rem;
}

.hero-image-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.hero-image {
    width: 100%;
    max-width: 550px;
    object-fit: contain;
    /* Removed box-shadow and border-radius for transparent PNG */
}

/* --- THOUGHT BUBBLES (4 around image) --- */
.thought-bubble {
    position: absolute;
    background: #ffffff;
    border: 2px solid #e2e8f0;
    padding: 0.75rem 1.1rem;
    border-radius: 40px;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
    font-weight: 700;
    color: #10507e;
    max-width: 170px;
    font-size: 0.9rem;
    z-index: 10;
    text-align: center;
    line-height: 1.3;
}

/* Base tail circles */
.thought-bubble::before,
.thought-bubble::after {
    content: '';
    position: absolute;
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 50%;
}

/* --- QUESTION MARKS --- */
.q-mark {
    position: absolute;
    font-weight: 900;
    color: #10507e;
    z-index: 5;
    user-select: none;
}

.q-1 {
    top: 5%;
    left: 20%;
    font-size: 5rem;
    opacity: 0.15;
    --rot: -15deg;
}
.q-2 {
    top: -5%;
    right: 30%;
    font-size: 3rem;
    opacity: 0.2;
    --rot: 20deg;
}

/* 1: Top Left (tail points down-right) */
.tb-1 {
    top: -5%;
    left: 2%;
    --rot: -4deg;
}
.tb-1::before { bottom: -12px; right: 25px; width: 16px; height: 16px; }
.tb-1::after { bottom: -25px; right: 15px; width: 8px; height: 8px; }

/* 2: Top Right (tail points down-left) */
.tb-2 {
    top: 5%;
    right: -5%;
    --rot: 5deg;
}
.tb-2::before { bottom: -12px; left: 25px; width: 16px; height: 16px; }
.tb-2::after { bottom: -25px; left: 15px; width: 8px; height: 8px; }

/* 3: Middle Left (tail points up-right) */
.tb-3 {
    top: 55%;
    left: -15%;
    --rot: -3deg;
}
.tb-3::before { top: -12px; right: 25px; width: 16px; height: 16px; }
.tb-3::after { top: -25px; right: 15px; width: 8px; height: 8px; }

/* 4: Middle Right (tail points up-left) */
.tb-4 {
    top: 65%;
    right: -5%;
    --rot: 4deg;
}
.tb-4::before { top: -12px; left: 25px; width: 16px; height: 16px; }
.tb-4::after { top: -25px; left: 15px; width: 8px; height: 8px; }

.hero-bg-glow {
    position: absolute;
    top: -50%; left: 50%;
    transform: translateX(-50%);
    width: 80vw; height: 80vw;
    max-width: 800px; max-height: 800px;
    background: radial-gradient(circle, rgba(16, 80, 126, 0.04) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
    z-index: 0;
}

.hero-content {
    flex: 1.2;
    position: relative;
    z-index: 1;
    display: flex;
    padding-bottom: 5rem;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
    gap: 1rem;
}

.lab {
    background-color: #f1f5f9;
    color: #10507e;
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 2px 10px rgba(16, 80, 126, 0.05);
}

.main-title {
    font-size: clamp(2.5rem, 5vw, 3.7rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
    color: #0f172a;
    letter-spacing: -1px;
}
.hl {
    color: #10507e;
}

.hero-description {
    font-size: 1.2rem;
    line-height: 1.7;
    max-width: 650px;
    color: #475569;
}

/* --- ANIMATIONS HERO --- */
.slide-up {
    animation: slideUpFade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(30px);
}
.slide-up-delay {
    animation: slideUpFade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-delay: 0.2s;
    opacity: 0;
    transform: translateY(30px);
}

.slide-up-delay-3 {
    animation: slideUpFade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-delay: 0.6s;
    opacity: 0;
    transform: translateY(30px);
}
@keyframes slideUpFade {
    to { opacity: 1; transform: translateY(0); }
}

.hero-svg {
    width: 32px; height: 32px;
}

@keyframes pulse {
    0% { transform: scale(0.8); opacity: 1; }
    100% { transform: scale(2.2); opacity: 0; }
}

/* --- BUTTON CTA --- */
.action-container {
    margin-top: 1rem;
}

.btn-primary {
    background-color: #10507e;
    color: #ffffff;
    border: none;
    padding: 1rem 2.2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 10px 20px rgba(16, 80, 126, 0.15);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
}

.btn-primary:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 15px 25px rgba(16, 80, 126, 0.25);
    background-color: #0c426b;
}

/* ==========================================
   RESPONSIVE
========================================== */
@media (max-width: 899px) {
    .page-wrapper { padding: 0; background: #ffffff; }
    .diagnostic-page { border-radius: 0; box-shadow: none; margin-bottom: 0; }
    
    .hero-section { padding: 5rem 1.5rem 3rem; }
    
    .hero-container {
        flex-direction: column-reverse;
        text-align: center;
        gap: 2.5rem;
    }
    
    /* Hide some bubbles on mobile so it doesn't get too crowded */
    .tb-3, .tb-4 {
        display: none;
    }
    
    .tb-1 {
        left: -5%;
        top: -5%;
    }
    .tb-2 {
        right: -5%;
        top: 0%;
    }
    
    .hero-content {
        align-items: center;
        text-align: center;
    }

    .action-container {
        bottom: 1.5rem;
        padding: 0 1.5rem;
    }

    .action-container > button {
        width: 100%;
        justify-content: center;
    }

    .hero-image {
        max-width: 90%;
    }
}
</style>