<template>
    <div class="page-wrapper">
        <main class="contact-center-page">
            <Navbar theme="light"/>
            
            <!-- ── HERO SECTION ── -->
            <section class="hero-section">
                <div class="hero-content">
                    <h1 class="main-title">
                        Centre d'Appel & <span class="text-accent">Assistance.</span>
                    </h1>
                    <p class="hero-description muted-text">
                        Le cabinet <strong>ADN Consulting SAS</strong> est à votre écoute. Contactez nos experts pour toute assistance juridique, fiscale ou technique concernant la plateforme ContratChap.
                    </p>
                </div>
            </section>

            <!-- ── SECTION CONTACT PRINCIPALE (Importée) ── -->
            <!-- Assure-toi que le chemin d'importation correspond à ton architecture -->
            <numberGreen />

            <!-- ── SECTION FAQ (Importée) ── -->
            <faqSection />

        </main>
        <Footer />
    </div>
</template>

<script lang="ts">
import Navbar from '../components/navigation/navbar.vue';
import Footer from '../components/sections/footerSection.vue';
import numberGreen from '../components/sections/numberGreen.vue'; // <-- Ajout du composant
import faqSection from '../components/sections/faqSection.vue'; 

export default {
    name: 'CallCenterPage',
    components: {
        Navbar,
        Footer,
        numberGreen,
        faqSection
    },
    setup() {
        return {};
    }
}
</script>

<style scoped>
/* ==========================================
   STYLE GLOBAL DE LA PAGE 
========================================== */
.page-wrapper {
    background-color: #ffffff; 
    padding: 3rem 1rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.contact-center-page {
    background-color: #ffffff; 
    width: 100%;
    max-width: 1200px;
    border-radius: 40px; 
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05); 
    color: #0f172a; 
    overflow: hidden;
    display: flex;
    flex-direction: column;
    margin-bottom: 3rem; 
}

.text-accent {
    color: #10507e; 
}

.muted-text {
    color: #64748b;
}

/* ==========================================
   1. HERO SECTION 
========================================== */
.hero-section {
    padding: 6rem 2rem 4rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.hero-content {
    max-width: 800px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.main-title {
    font-size: clamp(2.5rem, 5vw, 3rem);
    font-weight: 800;
    line-height: 1.15;
    margin: 0;
    color: #0f172a;
}

.hero-description {
    font-size: 1.15rem;
    line-height: 1.6;
    max-width: 700px;
    margin-top: 1rem;
    text-align: center;
}

.hero-description strong {
    color: #0f172a;
}

/* ==========================================
   RESPONSIVE DESIGN (Allégé)
========================================== */
@media (max-width: 899px) {
    .page-wrapper {
        padding: 0; 
    }
    
    .contact-center-page {
        border-radius: 0; 
    }
}
</style>