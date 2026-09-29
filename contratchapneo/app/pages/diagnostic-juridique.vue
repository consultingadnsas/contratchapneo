<template>
    <div class="page-wrapper">
        <main class="diagnostic-page">
            <Navbar theme="light"/>
            
            <!-- HERO SECTION -->
            <section class="hero-section">
                <div class="hero-container">
                    <!-- Left: Content -->
                    <div class="hero-content">                   
                        <h1 class="main-title slide-up-delay">Un doute juridique?<br><span class="hl">Obtenez votre diagnostic.</span></h1>
                        <p class="hero-description slide-up-delay-2">
                            En quelques minutes au téléphone, nos juristes analysent votre situation, 
                            identifient les risques et vous indiquent les bonnes démarches à suivre.
                        </p>
                        
                        <div class="action-container slide-up-delay-3">
                            <button @click="scrollToContact" class="btn-primary motion-btn">
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
                        <div class="q-mark q-3">?</div>
                        
                        <div class="thought-bubble tb-1">Dois-je signer ce contrat ?</div>
                        <div class="thought-bubble tb-2">Quels sont mes droits ici ?</div>
                        <div class="thought-bubble tb-3">Comment me protéger ?</div>
                        <div class="thought-bubble tb-4">Que faire face à ce litige ?</div>  
                        <img src="/Diagnostic.png" alt="Diagnostic Juridique" class="hero-image" />
                    </div>
                </div>
            </section>
            
            <!-- BENEFITS SECTION -->
            <section class="benefits-section">
                <div class="section-header">
                    <h2 class="section-title">Pourquoi demander un diagnostic ?</h2>
                    <p class="section-subtitle">Parce que chaque situation juridique mérite d’être analysée avant d’agir.</p>
                </div>
                
                <div class="benefits-grid">
                    <div class="benefit-card">
                        <div class="b-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        </div>
                        <h3>Diagnostic rapide</h3>
                        <p>Votre situation analysée en un seul appel, pour vous faire gagner un temps précieux.</p>
                    </div>
                    <div class="benefit-card">
                        <div class="b-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                        </div>
                        <h3>Analyse personnalisée</h3>
                        <p>Une réponse claire, spécifiquement adaptée à votre situation et à vos enjeux.</p>
                    </div>
                    <div class="benefit-card">
                        <div class="b-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                        </div>
                        <h3>Risques identifiés</h3>
                        <p>Repérez rapidement les points de vigilance avant de vous engager juridiquement.</p>
                    </div>
                    <div class="benefit-card">
                        <div class="b-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                        </div>
                        <h3>Bonnes démarches</h3>
                        <p>Sachez exactement quoi faire, dans quel ordre, et avec quels documents.</p>
                    </div>
                </div>
            </section>

            <!-- STEPS SECTION -->
            <section class="steps-section">
                <div class="section-header">
                    <h2 class="section-title">Trois étapes simples</h2>
                    <p class="section-subtitle">Obtenir votre diagnostic n'a jamais été aussi simple.</p>
                </div>
                
                <div class="steps-container">
                    <div class="step-line"></div>
                    
                    <div class="step-card">
                        <div class="step-num-bubble">1</div>
                        <div class="step-content">
                            <h3>Vous exposez votre situation</h3>
                            <p>Un expert vous écoute et vous pose les bonnes questions pour cerner précisément votre cas et vos objectifs.</p>
                        </div>
                    </div>
                    
                    <div class="step-card">
                        <div class="step-num-bubble">2</div>
                        <div class="step-content">
                            <h3>Nous analysons les risques</h3>
                            <p>Les enjeux, les points de vigilance et les conséquences potentielles de votre situation sont évalués en direct.</p>
                        </div>
                    </div>
                    
                    <div class="step-card">
                        <div class="step-num-bubble">3</div>
                        <div class="step-content">
                            <h3>Vous recevez votre diagnostic</h3>
                            <p>Vous obtenez une orientation claire et savez avec précision quelle démarche entreprendre ensuite pour vous sécuriser.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- NEW CTA / REPLACES NUMBER GREEN -->
            <section id="contact" class="trust-cta-section">
                <div class="trust-cta-card">
                    <div class="cta-text-content">
                        <h2>Prêt à éclaircir votre situation ?</h2>
                        <p>Ne restez pas seul face à vos doutes. Nos juristes sont à votre disposition pour établir votre diagnostic.</p>
                        
                        <div class="cta-actions">
                            <a href="tel:+2250508884088" class="contact-btn phone-btn">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.864-1.051l-3.21-.536a2.25 2.25 0 00-2.15.586l-1.22 1.22a15.042 15.042 0 01-6.918-6.918l1.22-1.22a2.25 2.25 0 00.586-2.15l-.536-3.21C8.088 2.601 7.638 2.25 7.116 2.25H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
                                </svg>
                                +225 05 08 88 40 88
                            </a>
                            <a href="https://wa.me/2250508884088" target="_blank" class="contact-btn wa-btn">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                  <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c-.003 1.398.366 2.76 1.062 3.964L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
                                </svg>
                                Discuter sur WhatsApp
                            </a>
                        </div>
                    </div>
                </div>
            </section>
            
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

export default defineComponent({
    name: 'DiagnosticJuridiquePage',
    components: {
        Navbar,
        Footer,
        faqSection
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

        const scrollToContact = () => {
            const el = document.getElementById('contact');
            if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        };

        return { 
            diagnosticFaqs, 
            scrollToContact
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

.section-header {
    text-align: center;
    max-width: 700px;
    margin: 0 auto 3rem;
}

.section-title {
    font-size: clamp(2rem, 4vw, 2.5rem);
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.75rem;
    line-height: 1.2;
}

.section-subtitle {
    font-size: 1.15rem;
    color: #64748b;
    line-height: 1.6;
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

@keyframes floatBubble {
    0%, 100% { transform: translateY(0) rotate(var(--rot)); }
    50% { transform: translateY(-8px) rotate(var(--rot)); }
}

/* --- QUESTION MARKS --- */
.q-mark {
    position: absolute;
    font-weight: 900;
    color: #10507e;
    z-index: 5;
    user-select: none;
}

@keyframes floatQM {
    0%, 100% { transform: translateY(0) scale(1) rotate(var(--rot)); }
    50% { transform: translateY(-15px) scale(1.05) rotate(calc(var(--rot) + 5deg)); }
}

.q-1 {
    top: 15%;
    left: 20%;
    font-size: 5rem;
    opacity: 0.15;
    --rot: -15deg;
    animation: floatQM 6s ease-in-out infinite;
}
.q-2 {
    top: 10%;
    right: 25%;
    font-size: 3rem;
    opacity: 0.2;
    --rot: 20deg;
    animation: floatQM 5s ease-in-out infinite 1s;
}
.q-3 {
    bottom: 30%;
    right: 15%;
    font-size: 6rem;
    opacity: 0.1;
    --rot: -10deg;
    animation: floatQM 7s ease-in-out infinite 2s;
}

/* 1: Top Left (tail points down-right) */
.tb-1 {
    top: -5%;
    left: 2%;
    --rot: -4deg;
    animation: floatBubble 4s ease-in-out infinite;
}
.tb-1::before { bottom: -12px; right: 25px; width: 16px; height: 16px; }
.tb-1::after { bottom: -25px; right: 15px; width: 8px; height: 8px; }

/* 2: Top Right (tail points down-left) */
.tb-2 {
    top: 5%;
    right: -5%;
    --rot: 5deg;
    animation: floatBubble 4.5s ease-in-out infinite 1s;
}
.tb-2::before { bottom: -12px; left: 25px; width: 16px; height: 16px; }
.tb-2::after { bottom: -25px; left: 15px; width: 8px; height: 8px; }

/* 3: Middle Left (tail points up-right) */
.tb-3 {
    top: 55%;
    left: -15%;
    --rot: -3deg;
    animation: floatBubble 5s ease-in-out infinite 0.5s;
}
.tb-3::before { top: -12px; right: 25px; width: 16px; height: 16px; }
.tb-3::after { top: -25px; right: 15px; width: 8px; height: 8px; }

/* 4: Middle Right (tail points up-left) */
.tb-4 {
    top: 65%;
    right: -5%;
    --rot: 4deg;
    animation: floatBubble 5.5s ease-in-out infinite 1.5s;
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
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
    gap: 1.25rem;
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
    font-size: clamp(2.5rem, 5vw, 3.8rem);
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
.slide-up-delay-2 {
    animation: slideUpFade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-delay: 0.4s;
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
    margin-top: 1.5rem;
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
   BENEFITS SECTION
========================================== */
.benefits-section {
    padding: 6rem 2rem;
    background: #fafcfd;
    border-top: 1px solid #f1f5f9;
    border-bottom: 1px solid #f1f5f9;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}

.benefit-card {
    background: #fff;
    padding: 2.5rem 2rem;
    border-radius: 24px;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #f8fafc;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.benefit-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
    border-color: #e2e8f0;
}

.b-icon {
    width: 56px; height: 56px;
    background: #f1f5f9;
    color: #10507e;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 1.5rem;
}

.benefit-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.75rem;
}

.benefit-card p {
    color: #64748b;
    line-height: 1.6;
    font-size: 0.95rem;
    margin: 0;
}

/* ==========================================
   STEPS SECTION (Fluid Design)
========================================== */
.steps-section {
    padding: 6rem 2rem;
    background: #ffffff;
}

.steps-container {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
}

.step-line {
    position: absolute;
    left: 28px;
    top: 30px;
    bottom: 30px;
    width: 2px;
    background: #e2e8f0;
    z-index: 0;
}

.step-card {
    position: relative;
    display: flex;
    align-items: flex-start;
    gap: 2rem;
    margin-bottom: 3.5rem;
    z-index: 1;
}
.step-card:last-child { margin-bottom: 0; }

.step-num-bubble {
    flex-shrink: 0;
    width: 58px; height: 58px;
    background: #10507e;
    color: #ffffff;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 800;
    box-shadow: 0 0 0 8px #ffffff, 0 4px 15px rgba(16, 80, 126, 0.2);
}

.step-content {
    background: #f8fafc;
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid #f1f5f9;
    flex-grow: 1;
    transition: transform 0.3s ease;
}

.step-card:hover .step-content {
    transform: translateX(10px);
    background: #ffffff;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
    border-color: #e2e8f0;
}

.step-content h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.3rem;
    color: #0f172a;
    font-weight: 700;
}

.step-content p {
    margin: 0;
    color: #475569;
    line-height: 1.6;
    font-size: 1rem;
}

/* ==========================================
   TRUST CTA SECTION (Replaces numberGreen)
========================================== */
.trust-cta-section {
    padding: 2rem 2rem 6rem;
    background: #ffffff;
    display: flex;
    justify-content: center;
}

.trust-cta-card {
    background: linear-gradient(145deg, #10507e 0%, #0c3e62 100%);
    width: 100%;
    max-width: 1000px;
    border-radius: 32px;
    padding: 4rem 3rem;
    box-shadow: 0 20px 40px rgba(16, 80, 126, 0.15);
    position: relative;
    overflow: hidden;
    text-align: center;
}

.trust-cta-card::before {
    content: ''; position: absolute;
    top: -50%; left: -20%;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 60%);
    border-radius: 50%;
}

.cta-text-content {
    position: relative; z-index: 1;
    display: flex; flex-direction: column; align-items: center;
}

.cta-text-content h2 {
    color: #ffffff;
    font-size: clamp(2rem, 4vw, 2.8rem);
    font-weight: 800;
    margin: 0 0 1rem 0;
}

.cta-text-content p {
    color: #cbd5e1;
    font-size: 1.15rem;
    max-width: 600px;
    line-height: 1.6;
    margin: 0 0 2.5rem 0;
}

.cta-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
}

.contact-btn {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 1rem 2rem; border-radius: 50px;
    font-weight: 700; font-size: 1.05rem;
    text-decoration: none;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.contact-btn:hover {
    transform: translateY(-3px);
}

.phone-btn {
    background: #ffffff;
    color: #10507e;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.wa-btn {
    background: #25D366;
    color: #ffffff;
    box-shadow: 0 10px 20px rgba(37, 211, 102, 0.2);
}
.wa-btn:hover { background: #20b958; }

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

    .hero-image {
        max-width: 90%;
    }

    .benefits-section { padding: 4rem 1.5rem; }
    
    .steps-container { padding-left: 0; }
    .step-line { display: none; }
    .step-card { flex-direction: column; align-items: center; gap: 1rem; text-align: center; }
    .step-content { width: 100%; }
    .step-card:hover .step-content { transform: translateY(-5px); }
    
    .trust-cta-section { padding: 2rem 1rem 4rem; }
    .trust-cta-card { padding: 3rem 1.5rem; border-radius: 24px; }
    .cta-actions { flex-direction: column; width: 100%; }
    .contact-btn { justify-content: center; width: 100%; }
}
</style>
