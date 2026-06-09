<template>
    <main class="legal-advice-page">
        <Navbar />
        
        <!-- 1. HERO SECTION -->
        <section class="hero-section">
            <div class="hero-content">
                <h1 class="main-title">
                    Besoin d'un Conseil Juridique ?<br>
                    <span class="text-gradient">Consultez nos experts aujourd'hui.</span>
                </h1>
                <p class="hero-description">
                    Obtenez l'accompagnement que vous méritez avec nos professionnels du droit. 
                </p>
                <div class="hero-actions">
                    <button class="btn-primary">Prendre rendez-vous</button>
                    <button class="btn-outline">En savoir plus</button>
                </div>
            </div>

            <div class="stats-bar glass-panel">
                <div v-for="(stat, index) in stats" :key="index" class="stat-item">
                    <span class="stat-number">{{ stat.number }}</span>
                    <span class="stat-label">{{ stat.label }}</span>
                </div>
            </div>
        </section>

        <!-- 2. SERVICES OFFERTS -->
        <section class="services-section">
            <div class="section-header">
                <h2>Services Proposés</h2>
                <p>Une expertise complète pour sécuriser chaque étape de votre business</p>
            </div>

            <div class="services-grid">
                <article v-for="(service, index) in services" :key="index" class="service-card glass-card">
                    <div class="card-icon" v-html="service.icon"></div>
                    <h3>{{ service.title }}</h3>
                    <p>{{ service.description }}</p>
                    <a href="#" class="read-more">En savoir plus <span class="arrow">→</span></a>
                </article>
            </div>
        </section>

        <!-- 3. SECTION CONTACTEZ-NOUS -->
        <section class="contact-section">
            <div class="contact-header">
                <h2>Contactez-nous</h2>
                <div class="header-line"></div>
            </div>

            <div class="contact-container">
                <!-- Colonne de gauche : Informations de contact -->
                <div class="contact-info glass-card">
                    <h3>Discutons de votre projet</h3>
                    
                    <div class="info-list">
                        <div class="info-item">
                            <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                            <span>Abidjan, Côte d'Ivoire</span>
                        </div>
                        <div class="info-item">
                            <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                            <span>contact@contratchapneo.com</span>
                        </div>
                        <div class="info-item">
                            <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                            <span>(+225) 00 00 00 00 00</span>
                        </div>
                        <div class="info-item">
                            <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                            <span>(+225) 00 00 00 00 00</span>
                        </div>
                    </div>
                </div>

                <!-- Colonne de droite : Formulaire -->
                <form class="contact-form" @submit.prevent="submitForm">
                    <input type="text" class="glass-input" placeholder="Votre Nom" required />
                    <input type="email" class="glass-input" placeholder="Votre Email" required />
                    <textarea class="glass-input" placeholder="Votre Message" rows="5" required></textarea>
                    
                    <button type="submit" class="btn-primary form-submit">Envoyer le message</button>
                </form>
            </div>
        </section>

        <Footer /> 
    </main>
</template>

<script lang="ts">
import { ref } from 'vue';
import Navbar from '../components/navigation/navbar.vue';
import Footer from '../components/sections/footerSection.vue';

export default {
    name: 'LegalAdvicePage',
    components: {
        Navbar,
        Footer
    },
    setup() {
        const stats = ref([
            { number: '500+', label: 'Dossiers Traités' },
            { number: '98%', label: 'Clients Satisfaits' },
            { number: '50+', label: 'Experts Juridiques' },
            { number: '100%', label: 'Confidentialité' }
        ]);

        const services = ref([
            {
                title: 'Offre de création',
                description: 'Assistance pour la création, la modification et la restructuration de votre entreprise en zone OHADA.',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M5 21V5a2 2 0 012-2h10a2 2 0 012 2v16M9 21v-4a2 2 0 012-2h2a2 2 0 012 2v4"/></svg>'
            },
            {
                title: 'Offre de conformité',
                description: 'Rédaction, révision et négociation de contrats juridiquement solides pour sécuriser vos affaires.',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>'
            },
            {
                title: 'Offre de suivi et accompagnement',
                description: 'Gestion des contrats de travail, licenciements et conformité avec la législation sociale locale.',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5c-1.2 0-2 .8-2 2v2M9 7a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>'
            },
        ]);
        
        const submitForm = () => {
            // Logique d'envoi du formulaire
            console.log("Formulaire envoyé");
        };

        return { stats, services, submitForm }
    }
}
</script>

<style scoped>
/* --- FOND ET LAYOUT GLOBAL --- */
.legal-advice-page {
    background-color: #0f172a; 
    color: #ffffff;
    min-height: 100vh;
    overflow-x: hidden;
}

/* --- 1. HERO SECTION --- */
.hero-section {
    position: relative;
    padding: 8rem 2rem 10rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background: radial-gradient(circle at center, rgba(39, 33, 71, 0.8) 0%, rgba(15, 23, 42, 1) 100%);
}

.hero-content {
    max-width: 800px;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}

.main-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
}

.text-gradient {
    background: linear-gradient(to right, #ffffff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    font-size: 1.1rem;
    color: #cbd5e1;
    line-height: 1.6;
    max-width: 650px;
}

.hero-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

/* Boutons standards */
.btn-primary {
    background-color: #34d399;
    color: #0f172a;
    font-weight: 700;
    padding: 0.8rem 1.8rem;
    border-radius: 50px;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(52, 211, 153, 0.2);
}

.btn-outline {
    background-color: transparent;
    color: #ffffff;
    font-weight: 600;
    padding: 0.8rem 1.8rem;
    border-radius: 50px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.btn-outline:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

.glass-panel {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

/* Barre de stats sous le Hero */
.stats-bar {
    position: absolute;
    bottom: -40px; 
    display: flex;
    justify-content: space-around;
    width: 90%;
    max-width: 1000px;
    padding: 2rem;
    border-radius: 20px;
    z-index: 10;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.stat-number {
    font-size: 2rem;
    font-weight: 800;
    color: #34d399;
}

.stat-label {
    font-size: 0.9rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* --- 2. SERVICES OFFERTS --- */
.services-section {
    padding: 8rem 2rem 4rem 2rem; 
    max-width: 1200px;
    margin: 0 auto;
}

.section-header {
    margin-bottom: 3rem;
    text-align: left;
}

.section-header h2 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
}

.section-header p {
    color: #94a3b8;
    font-size: 1.1rem;
    margin: 0;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}

.glass-card {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    transition: transform 0.3s ease, background 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(52, 211, 153, 0.3);
}

.card-icon {
    width: 48px;
    height: 48px;
    color: #34d399;
    background: rgba(52, 211, 153, 0.1);
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}

.service-card h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
}

.service-card p {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0 0 2rem 0;
    flex-grow: 1;
}

.read-more {
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: color 0.2s ease;
}

.read-more:hover {
    color: #34d399;
}

.arrow {
    transition: transform 0.2s ease;
}

.read-more:hover .arrow {
    transform: translateX(4px);
}

/* --- 3. SECTION CONTACT --- */
.contact-section {
    padding: 4rem 2rem 8rem 2rem;
    max-width: 1100px;
    margin: 0 auto;
}

.contact-header {
    text-align: center;
    margin-bottom: 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.contact-header h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
}

.header-line {
    width: 60px;
    height: 4px;
    background-color: #34d399;
    border-radius: 2px;
}

.contact-container {
    display: grid;
    grid-template-columns: 1fr 1.2fr; /* Formulaire légèrement plus large que la carte info */
    gap: 2rem;
}

/* Carte Info Gauche */
.contact-info {
    padding: 3rem 2.5rem;
    display: flex;
    flex-direction: column;
}

.contact-info h3 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 2rem 0;
    color: #ffffff;
}

.info-list {
    display: flex;
    flex-direction: column;
    gap: 1.8rem;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    color: #cbd5e1;
    font-size: 1rem;
}

.contact-icon {
    width: 24px;
    height: 24px;
    color: #34d399;
    flex-shrink: 0;
}

/* Formulaire Droite */
.contact-form {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    justify-content: space-between;
}

.glass-input {
    width: 100%;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.2rem;
    color: #ffffff;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.3s ease, background 0.3s ease;
    box-sizing: border-box;
}

.glass-input::placeholder {
    color: #64748b;
}

.glass-input:focus {
    outline: none;
    border-color: #34d399;
    background: rgba(255, 255, 255, 0.05);
}

textarea.glass-input {
    resize: vertical;
    min-height: 150px;
}

.form-submit {
    align-self: flex-start;
    padding: 1rem 2.5rem;
    border-radius: 12px; /* Coins un peu moins arrondis que les boutons classiques pour coller au formulaire */
    margin-top: 0.5rem;
}

/* --- RESPONSIVE MOBILE --- */
@media (max-width: 900px) {
    .stats-bar {
        position: relative;
        bottom: 0;
        margin-top: 3rem;
        flex-direction: column;
        gap: 2rem;
        width: 100%;
    }

    .services-section {
        padding-top: 4rem;
    }

    /* Le grid passe sur une seule colonne */
    .contact-container {
        grid-template-columns: 1fr;
        gap: 3rem;
    }
    
    .contact-info {
        padding: 2rem;
    }
}
</style>