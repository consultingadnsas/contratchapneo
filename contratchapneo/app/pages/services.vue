<template>
    <div class="page-wrapper">
        <main class="legal-services-page">
            <Navbar theme="light"/>
            <section class="hero-section">
                <div class="hero-content">
                    <h1 class="main-title">
                        L'expertise derrière<span class="text-accent"> ContratChap.</span>
                    </h1>
                    <p class="hero-description muted-text">
                        Créateur de la plateforme technologique ContratChap, le cabinet <strong>ADN Consulting SAS</strong> vous accompagne au quotidien avec une gamme complète de services juridiques, fiscaux et stratégiques pour propulser votre croissance.
                    </p>
                </div>
                <div class="stats-bar">
                    <div v-for="(stat, index) in stats" :key="index" class="stat-item">
                        <span class="stat-number">{{ stat.number }}</span>
                        <span class="stat-label">{{ stat.label }}</span>
                    </div>
                </div>
            </section>

            <section class="services-section">
                <div class="section-header">
                    <h2>Nos Domaines d'Intervention</h2>
                    <p class="muted-text">Cliquez sur un service pour être mis en relation avec nos experts.</p>
                </div>
                <servicesCards :services="services" />
            </section>

            <section id="contact-section" class="contact-section">
                <div class="section-header">
                    <h2>Nos Coordonnées</h2>
                    <p class="muted-text">Une question ? Un projet ? Nos experts sont à votre disposition.</p>
                </div>

                <div class="contact-grid">
                    <div class="contact-item">
                        <div class="contact-icon-wrapper">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                        </div>
                        <h4>Adresse</h4>
                        <p>Angré 8e Tranche près de Chicken Nation </p>
                    </div>
                    
                    <div class="contact-item">
                        <div class="contact-icon-wrapper">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                        </div>
                        <h4>Email</h4>
                        <p>Consultingadnsas@gmail.com</p>
                    </div>

                    <div class="contact-item">
                        <div class="contact-icon-wrapper">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                        </div>
                        <h4>Téléphone</h4>
                        <p><a href="tel:+2250779101170">+225 07 79 10 11 70</a></p>
                    </div>
                </div>
            </section>          
        </main>
    </div>
    <Footer /> 
</template>

<script lang="ts">
import { ref } from 'vue';
import Navbar from '../components/navigation/navbar.vue';
import Footer from '../components/sections/footerSection.vue';
import servicesCards from '../components/cards/servicesCards.vue';

export default {
    name: 'ServicesJuridiquesPage',
    components: {
        Navbar,
        Footer,
        servicesCards
    },
    setup() {
        const stats = ref([
            { number: '9', label: 'Années d\'Expertise' },
            { number: '1000+', label: 'Entreprises Accompagnées' },
            { number: '1', label: 'Solution Legaltech Innovante' }
        ]);

        const services = ref([
            {
                id: 'assistance',
                title: 'Assistance Juridique et Fiscale',
                shortTitle: 'Assistance', // Titre court pour l'onglet réduit
                description: 'Accompagnement rigoureux pour sécuriser vos opérations commerciales, optimiser votre fiscalité et garantir votre conformité légale.',
                longDescription:'L’accompagnement juridique permanent consiste à devenir le département juridique externalisé de l’entreprise cliente. un service proposé par le cabinet ADN, visant à fournir aux entreprises une assistance juridique continue pour prévenir les litiges, garantir la conformité légale et sécuriser les décisions de gestion. Elle comporte tous les éléments prévus au programme trimestriel ainsi que tous autres besoins d’ordre juridique que peut avoir l’entreprise.',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
                image:'/services/4.jpg',
                features: ['Assistance juridique quotidienne', 'Rédaction et Validation de documents juridiques','Veille Réglementaire et Alerte Juridique','Gestion de risque Juridique','Assistance en cas de Précontentieux et Contentieux'],
                price: '150 000 FCFA',
            },
            {
                id: 'programmes',
                title: 'Programmes Juridiques',
                shortTitle: 'Programmes',
                description: 'Mise en place de programmes de mise en conformité, d\'audits structurés et de formations sur mesure pour vos équipes.',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
                image:'/services/2.jpg',
                features: ['Accompagnement par des avocats','Mise en conformité'],
                price:'250 000 FCFA'
            },
            {
                id: 'brevets',
                title: 'Brevet d\'Invention',
                shortTitle: 'Brevets',
                description: 'Démarches complètes pour protéger vos innovations technologiques, industrielles et scientifiques à l\'échelle nationale et internationale.',
                longDescription:'Nous vous accompagnons dans le processus, en fonction de votre égibilité et des conditions de brevetabilité. le dépôt d\'un brevet invention reste un titre de propriété industrielle qui confère à son titulaire le droit exclusif d’exploiter une invention pendant une durée déterminée (en général 20 ans), sous certaines conditions Nous constituons tout le dossier comportant: un formulaire de demande, une description de l’invention, tous les dessins techniques, un résumé des travaux d’invention, un justificatif du paiement des taxes, etc..',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1.5.5 2.5 1.5 3.5.76.76 1.23 1.52 1.41 2.5"></path></svg>',
                image:'/services/3.jpg',
                features:['droit exclusive d’exploitation', 'Possibiliter de licencier ou vendre le brevet','Valorisation de la technologie aupres d’investisseurs'],
                price:'1 000 000 FCFA'
            },
            {
                id: 'marques',
                title: 'Dépôt de Marque',
                shortTitle: 'Marques',
                description: 'Sécurisation de votre identité visuelle, logos et signes distinctifs auprès des instances compétentes (OAPI).',
                longDescription:'Nous vous accompagnons dans le processus, en fonction de votre dossier. le dépôt demarque reste une démarche juridique qui consiste à enregistrer officiellement une marque(nom, logo, slogan, etc.) auprès d’un office de propriété intellectuelle O.A.P.I. pour en obtenir l’exclusivité d’utilisation.',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>',
                image:'/services/5.jpg',
                features:['Protéger votre nom, logo ou slogan contre l’utilisation non autorisée par d’autres.','Obtenir un droit exclusif d’exploitation sur un territoire donné.','Valoriser vos produits ou services, renforcer votre image de marque.','Faciliter des actions juridiques en cas de contrefaçon'],
                price:'300 000 FCFA'
            },
            {
                id:'tech',
                title: 'Legaltech',
                shortTitle: 'Legaltech',
                description: 'Développement de solutions technologiques innovantes (à l\'image de ContratChapNeo) pour dématérialiser et automatiser le droit.',
                longDescription:'Nous rédigeons la mise en conformité, qui constitue dansl’ensemble es actions nécessaires pour s’assurer qu’un site respecte les lois et réglementations en vigueur. Il s’agit d’une formule appliquée à un site web ou une application mobile qui consiste en:',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>',
                image:'/services/2.jpg',
                features: ['la rédaction des conditions générales d’utilisation et/ou de vente', 'Accessibilité numérique (RGAA – Référentiel Général d\'Amélioration de l\'Accessibilité)', 'Sécurité du site et Conformité E-commerce', 'Propriété Intellectuelle'],
                price: '250 000 FCFA'
            },
            {
                id: 'noms',
                title: 'Enregistrement Noms',
                shortTitle: 'Noms Commerciaux',
                description: 'Prise en charge de vos démarches administratives pour réserver et protéger juridiquement le nom de votre structure.',
                icon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m3.75 9v7.5m2.25-6.466a9.016 9.016 0 0 0-3.461-.203c-.536.072-.974.478-1.021 1.017a4.559 4.559 0 0 0-.018.402c0 .464.336.844.775.994l2.95 1.012c.44.15.775.53.775.994 0 .136-.006.27-.018.402-.047.539-.485.945-1.021 1.017a9.077 9.077 0 0 1-3.461-.203M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" /></svg>',
                image:'/services/2.jpg',
                features: ['formalisation commerciale'],
                price: '250 000 FCFA'
            },
            {
                id:'créa',
                title:'Création d\'entreprise',
                shortTitle: 'Création',
                description:'prise en charge pour la création de votre entreprise, on met en place tous les documents nécessaire à celà- et on vous accompagne tout au long du processus juridique',
                longDescription:'Nous prenons en charge, sur la base des pièces fournies, de rediger entièrement tous les documents nécessaires aux formalités administratives et dont certains aussi font partie des livrables en termes de documents légaux de votre entreprise (statuts; déclaration de souscription et versement; liste de dirigeants etc.)',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
                image:'/services/1.jpg',
                features: ['Diagnostic juridique', 'Création clé en main de société','Création basique de société'],
                price: '1 250 000 FCFA'
            }
        ]);

        // Fonction de défilement fluide vers la section contact
        const scrollToContact = () => {
            const contactSection = document.getElementById('contact-section');
            if (contactSection) {
                contactSection.scrollIntoView({ behavior: 'smooth' });
            }
        };

        return { stats, services, scrollToContact }
    }
}
</script>

<style scoped>
/* --- FOND GRIS ET CARTE BLANCHE --- */
.page-wrapper {
    background-color: #ffffff; 
    padding: 3rem 1rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
}

.legal-services-page {
    background-color: #ffffff; 
    width: 100%;
    max-width: 1200px;
    border-radius: 40px; 
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05); 
    color: #0f172a; 
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

/* --- TYPOGRAPHIE --- */
.muted-text {
    color: #64748b;
}

.pill-badge {
    display: inline-block;
    border: 1px solid #e2e8f0;
    color: #34d399; 
    background-color: rgba(52, 211, 153, 0.1);
    padding: 6px 18px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}

.text-accent {
    color:#10507e; 
}

/* --- 1. HERO SECTION --- */
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
    font-size: clamp(2.5rem, 5vw, 4rem);
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
}

.hero-description strong {
    color: #0f172a;
}

/* Barre de stats épurée */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 4rem;
    width: 100%;
    max-width: 900px;
    padding: 3rem 0 1rem 0;
    border-bottom: 1px solid #f1f5f9;
    margin-top: 2rem;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.2rem;
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #0f172a;
}

.stat-label {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* --- 2. SERVICES OFFERTS --- */
.services-section {
    padding: 5rem 2rem;
    max-width: 1100px;
    margin: 0 auto;
    width: 100%;
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-header h2 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    color: #0f172a;
}

.section-header p {
    font-size: 1.1rem;
    margin: 0;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.service-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    transition: all 0.3s ease;
    cursor: pointer; /* Indique clairement que c'est cliquable */
}

/* Effet interactif renforcé au survol */
.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(52, 211, 153, 0.1); /* Ombre très légèrement teintée de vert */
    border-color: #34d399; 
}

.card-icon {
    width: 50px;
    height: 50px;
    color: #34d399;
    background: rgba(52, 211, 153, 0.1);
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease;
}

/* Petite animation de l'icône au survol de la carte */
.service-card:hover .card-icon {
    transform: scale(1.1);
}

.service-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0 0 0.8rem 0;
}

.service-card p {
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
}

/* --- 3. SECTION COORDONNÉES --- */
.contact-section {
    padding: 2rem 2rem 6rem 2rem;
    max-width: 1100px;
    margin: 0 auto;
    width: 100%;
    /* Petit effet d'ancrage visuel */
    scroll-margin-top: 4rem; 
}

.contact-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-top: 3rem;
}

.contact-item {
    background: #f8fafc; 
    border-radius: 20px;
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    border: 1px solid transparent;
    transition: all 0.3s ease;
}

.contact-item:hover {
    background: #ffffff;
    border-color: #e2e8f0;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
}

.contact-icon-wrapper {
    width: 56px;
    height: 56px;
    background-color: #0f172a; 
    color: #ffffff;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
}

.contact-icon-wrapper svg {
    width: 24px;
    height: 24px;
}

.contact-item h4 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.5rem 0;
}

.contact-item p {
    color: #64748b;
    font-size: 1rem;
    margin: 0;
}

/* --- RESPONSIVE MOBILE --- */
@media (max-width: 900px) {
    .page-wrapper {
        padding: 0; 
    }

    .legal-services-page {
        border-radius: 0; 
    }

    .stats-bar {
        flex-direction: column;
        gap: 2rem;
        padding-top: 2rem;
    }

    .contact-grid {
        grid-template-columns: 1fr;
    }
}
</style>