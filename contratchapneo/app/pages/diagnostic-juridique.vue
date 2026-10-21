<template>
    <div class="page-wrapper">
        <main class="diagnostic-page">
            <Navbar />
            
            <Transition name="page-fade" mode="out-in">
                
                <section v-if="!showTunnel" key="hero" class="hero-section">
                    <div class="hero-container">
                        
                        <div class="hero-content">
                            <h1 class="main-title slide-up-delay">Besoin de<br><span class="hl">conseil</span>?</h1>
                            <p>Obtenez des conseils et des solutions juridique directement de nos experts du droit.</p>


                            <div class="action-container slide-up-delay-3">
                                <div class="revision-cta main-action premium-shadow" role="button" tabindex="0" @click="startTunnel" @keydown.enter="startTunnel">
                                    <div class="btn-shine"></div>
                                    <div class="cta-texts">
                                        <p>Prendre rendez-vous</p>
                                    </div>
                                    <div class="cta-arrow floating-arrow">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                                        </svg>
                                    </div>
                                </div>
                            </div>

                            <!-- Informations & stats de réassurance -->
                            <div class="hero-trust-indicators slide-up-delay-3">
                                <div class="trust-indicator-card">
                                    <div class="trust-indicator-icon">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                                        </svg>
                                    </div>
                                    <div class="trust-indicator-content">
                                        <span class="trust-stat-num">01</span>
                                        <p class="trust-stat-title">Exposez votre situation</p>
                                    </div>
                                </div>

                                <div class="trust-indicator-card">
                                    <div class="trust-indicator-icon">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                        </svg>
                                    </div>
                                    <div class="trust-indicator-content">
                                        <span class="trust-stat-num">100%</span>
                                        <p class="trust-stat-title">Consultation audio ou présentiel sécurisé</p>
                                    </div>
                                </div>

                                <div class="trust-indicator-card">
                                    <div class="trust-indicator-icon">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                                        </svg>
                                    </div>
                                    <div class="trust-indicator-content">
                                        <span class="trust-stat-num">OHADA</span>
                                        <p class="trust-stat-title">Nos experts sont des spécialistes du droit OHADA</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Right: Image with 4 Thought Bubbles -->
                        <div class="hero-image-wrapper slide-up">
                            <!-- Cercles concentriques qui s'étendent sur toute la section -->
                            <div class="photo-circles-ripple" aria-hidden="true">
                                <div class="circle circle-core"></div>
                                <div class="circle circle-1"></div>
                                <div class="circle circle-2"></div>
                                <div class="circle circle-3"></div>
                                <div class="circle circle-4"></div>
                                <div class="circle circle-5"></div>
                                <div class="circle circle-6"></div>
                            </div>

                            <img src="/PRINCIPALE2.png" alt="Diagnostic Juridique" class="hero-image" />
                        </div>
                    </div>

                    <!-- Queue de bulle de dialogue pour relier à la FAQ -->
                    <div class="hero-bubble-tail" aria-hidden="true">
                        <svg width="54" height="32" viewBox="0 0 54 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0 0 C12 0 24 8 40 30 L42 32 C38 20 40 8 46 0 Z" fill="#0f0f0f"/>
                        </svg>
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
    overflow-x: hidden;
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
    overflow: visible;
    z-index: 2;
    background: radial-gradient(circle at 72% 48%, #202b4a 20%, #141c30 45%, #0f0f0f 80%);
}

/* Queue de bulle de dialogue reliant à la FAQ */
.hero-bubble-tail {
    position: absolute;
    bottom: -31px;
    left: 90%;
    transform: translateX(-50%);
    z-index: 20;
    line-height: 0;
    pointer-events: none;
    filter: drop-shadow(0 6px 8px rgba(15, 23, 42, 0.08));
}

.hero-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 4rem;
}

.hero-container p {
    color:aliceblue
}

.hero-image-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    width: 100%;
}

.hero-image {
    display: flex;
    min-width: 690px;
    object-fit: contain;
    margin-bottom: 110px;
    position: relative;
    z-index: 2;
}

/* --- THOUGHT BUBBLES (4 around image) --- */
.thought-bubble {
    position: absolute;
    background: #ffffff;
    border: 2px solid rgba(226, 232, 240, 0.95);
    padding: 0.85rem 1.2rem;
    border-radius: 30px;
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35), 0 0 20px rgba(255, 255, 255, 0.1);
    color: #0f2744;
    max-width: 195px;
    z-index: 10;
    text-align: center;
    transform: rotate(var(--rot, 0deg));
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease, border-color 0.3s ease;
    animation: floatBubble 6s ease-in-out infinite;
    cursor: default;
    user-select: none;
}

.thought-bubble:hover {
    transform: rotate(0deg) scale(1.05);
    box-shadow: 0 20px 42px rgba(0, 0, 0, 0.45), 0 0 25px rgba(56, 189, 248, 0.3);
    border-color: #38bdf8;
    z-index: 15;
}

.thought-bubble .bubble-text {
    color: #0f2744 !important;
    display: block;
    margin: 0;
    font-size: 0.88rem;
    font-weight: 700;
    line-height: 1.35;
}

/* Base tail circles (petits ronds de pensée) */
.thought-bubble::before,
.thought-bubble::after {
    content: '';
    position: absolute;
    background: #ffffff;
    border: 2px solid rgba(226, 232, 240, 0.95);
    border-radius: 50%;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25);
    transition: border-color 0.3s ease;
}

.thought-bubble:hover::before,
.thought-bubble:hover::after {
    border-color: #38bdf8;
}

@keyframes floatBubble {
    0%, 100% {
        transform: translateY(0) rotate(var(--rot, 0deg));
    }
    50% {
        transform: translateY(-8px) rotate(var(--rot, 0deg));
    }
}

/* --- QUESTION MARKS --- */
.q-mark {
    position: absolute;
    font-weight: 900;
    color: #b6b7b8;
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

/* 1: Top Left (queue vers le bas à droite) */
.tb-1 {
    top: 30%;
    left: 10%;
    animation-delay: 0s;
}


/* 2: Top Right (queue vers le bas à gauche) */
.tb-2 {
    top: 30%;
    right: -2%;
    animation-delay: 1.5s;
}


/* 3: Middle/Bottom Left (queue vers le haut à droite) */
.tb-3 {
    top: 70%;
    left: 10%;
    animation-delay: 3s;
}

/* 4: Middle/Bottom Right (queue vers le haut à gauche) */
.tb-4 {
    top: 75%;
    right: 5%;
    animation-delay: 4.5s;
}

/* --- CERCLES CONCENTRIQUES QUI S'ÉTENDENT SUR TOUTE LA SECTION --- */
.photo-circles-ripple {
    position: absolute;
    top: calc(50% - 45px);
    left: 50%;
    width: 0;
    height: 0;
    pointer-events: none;
    z-index: 1;
}

.circle {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    pointer-events: none;
    transition: all 0.4s ease;
}

/* 1. Cœur : premier cercle lumineux et clair sous la photo */
.circle-core {
    width: 440px;
    height: 440px;
    border: 1.5px solid rgba(49, 151, 245, 0.45);
    background: radial-gradient(circle at 40% 40%, rgba(56, 189, 248, 0.28) 0%, rgba(49, 151, 245, 0.16) 45%, rgba(15, 23, 42, 0) 75%);
    box-shadow: 0 0 50px 15px rgba(49, 151, 245, 0.25), inset 0 0 35px rgba(56, 189, 248, 0.15);
    animation: ripplePulse 7s ease-in-out infinite;
}

/* 2. Cercles concentriques s'étendant à travers la section */
.circle-1 {
    width: 640px;
    height: 640px;
    border: 1px solid rgba(49, 151, 245, 0.35);
    background: radial-gradient(circle, rgba(26, 98, 204, 0.12) 0%, rgba(15, 23, 42, 0) 70%);
    box-shadow: 0 0 40px rgba(49, 151, 245, 0.08);
    animation: ripplePulse 7s ease-in-out infinite;
}

.circle-2 {
    width: 880px;
    height: 880px;
    border: 1px solid rgba(49, 151, 245, 0.25);
    background: radial-gradient(circle, rgba(26, 98, 204, 0.08) 0%, rgba(15, 23, 42, 0) 70%);
    animation: ripplePulse 7s ease-in-out infinite 0.8s;
}

.circle-3 {
    width: 1160px;
    height: 1160px;
    border: 1px solid rgba(49, 151, 245, 0.2);
    background: radial-gradient(circle, rgba(26, 98, 204, 0.05) 0%, rgba(15, 23, 42, 0) 75%);
    animation: ripplePulse 7s ease-in-out infinite 1.6s;
}

.circle-4 {
    width: 1480px;
    height: 1480px;
    border: 1px dashed rgba(49, 151, 245, 0.16);
    background: radial-gradient(circle, rgba(26, 98, 204, 0.03) 0%, transparent 75%);
    animation: ripplePulse 7s ease-in-out infinite 2.4s;
}

.circle-5 {
    width: 1840px;
    height: 1840px;
    border: 1px solid rgba(49, 151, 245, 0.1);
    animation: ripplePulse 7s ease-in-out infinite 3.2s;
}

.circle-6 {
    width: 2240px;
    height: 2240px;
    border: 1px solid rgba(49, 151, 245, 0.06);
    animation: ripplePulse 7s ease-in-out infinite 4s;
}

@keyframes ripplePulse {
    0%, 100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 1;
    }
    50% {
        transform: translate(-50%, -50%) scale(1.02);
        opacity: 0.85;
    }
}

.hero-content {
    flex: 1.2;
    position: relative;
    z-index: 3;
    display: flex;
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
    font-size: clamp(4rem, 6vw, 4.7rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
    margin-top: 70px;
    color: #ffffff;
    letter-spacing: -1px;
}
.hl {
    color: #007fda;
    font-size: 4.7rem;
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

/* --- BUTTON CTA (Identique à heroSecondSection) --- */
.action-container {
    margin-top: 1rem;
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

.revision-cta:hover { transform: translateY(-4px) scale(1.02); }
.main-action:hover { box-shadow: 0 20px 40px -5px rgba(50, 244, 89, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3); }

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
    color: #ffffff !important;
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
.main-action:hover .cta-arrow { background: #32f459; color: #080a0f; transform: rotate(45deg); }

.floating-arrow svg { width: 18px; height: 18px; }

/* --- INFORMATIONS & STATS DE RÉASSURANCE --- */
.hero-trust-indicators {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    gap: 0.85rem;
    margin-top: 1.8rem;
    width: 100%;
    max-width: 620px;
}

.trust-indicator-card {
    flex: 1;
    min-width: 50%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.65rem;
    padding: 0.95rem 1rem;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: none;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}

.trust-indicator-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(56, 189, 248, 0.35);
    transform: translateY(-3px);
    box-shadow: 0 15px 30px -5px rgba(0, 127, 218, 0.25);
}

.trust-indicator-card:hover::before {
    opacity: 1;
}

.trust-indicator-icon {
    width: 35px;
    height: 35px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(0, 127, 218, 0.2), rgba(56, 189, 248, 0.1));
    border: 1px solid rgba(56, 189, 248, 0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #38bdf8;
    flex-shrink: 0;
}

.trust-indicator-icon svg {
    width: 17px;
    height: 17px;
}

.trust-indicator-content {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.trust-stat-num {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    color: #38bdf8;
    display: inline-block;
}

.trust-stat-title {
    font-size: 0.75rem;
    color: #f1f5f9 !important;
    line-height: 1.35;
    margin: 0;
}

/* ==========================================
   RESPONSIVE
========================================== */

@media (max-width: 1050px) {
    .page-wrapper { padding: 0; background: #ffffff; }
    .diagnostic-page { border-radius: 0; box-shadow: none; margin-bottom: 0; }
    
    .hero-section {
        padding: 5rem 1.5rem 3rem;
        background: radial-gradient(circle at 50% 30%, #202b4a 20%, #141c30 45%, #0f0f0f 80%);
    }
    
    .hero-container {
        flex-direction: column-reverse;
        text-align: center;
        gap: 2.5rem;
    }
    
    /* Bulles adaptées sur tablette/mobile */
    .thought-bubble {
        max-width: 160px;
        font-size: 0.8rem;
        padding: 0.65rem 0.95rem;
    }
    
    .thought-bubble .bubble-text {
        font-size: 0.8rem;
    }
    
    .tb-1 {
        left: 0%;
        top: -4%;
    }
    .tb-2 {
        right: 0%;
        top: 2%;
    }
    .tb-3 {
        left: 0%;
        top: 56%;
    }
    .tb-4 {
        right: 0%;
        top: 66%;
    }
    
    .hero-content {
        align-items: center;
        text-align: center;
    }

    .hero-trust-indicators {
        justify-content: center;
        max-width: 480px;
        margin-top: 1.5rem;
    }

    .action-container {
        bottom: 1.5rem;
        padding: 0 1.5rem;
        width: 100%;
        display: flex;
        justify-content: center;
    }

    .action-container .revision-cta {
        width: 100%;
        max-width: 320px;
    }

    .hero-image {
        margin-bottom: 0;
        margin-right: 20px;
        min-width: 400px;
    }

    .photo-circles-ripple {
        top: 50%;
        left: calc(50% - 10px);
    }

    .circle-core { width: 320px; height: 320px; }
    .circle-1 { width: 460px; height: 460px; }
    .circle-2 { width: 640px; height: 640px; }
    .circle-3 { width: 860px; height: 860px; }
    .circle-4 { width: 1120px; height: 1120px; }
    .circle-5 { width: 1420px; height: 1420px; }
    .circle-6 { width: 1760px; height: 1760px; }
}

@media (max-width: 768px) {
    .hero-trust-indicators {
        flex-direction: column;
        width: 100%;
        max-width: 360px;
        gap: 0.65rem;
    }

    .trust-indicator-card {
        flex-direction: row;
        align-items: center;
        gap: 0.85rem;
        padding: 0.75rem 0.95rem;
        text-align: left;
    }

    .hero-image {
        top: 20px;
        margin-right: 20px;
        min-width: 400px;
    }
}

@media (max-width: 500px) {
    .circle-core { width: 250px; height: 250px; }
    .circle-1 { width: 350px; height: 350px; }
    .circle-2 { width: 480px; height: 480px; }
    .circle-3 { width: 640px; height: 640px; }
    .circle-4 { width: 820px; height: 820px; }
    .circle-5 { width: 1040px; height: 1040px; }
    .circle-6 { width: 1300px; height: 1300px; }
}
</style>