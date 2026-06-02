<template>
    <main class="about-page">
        
        <!-- En-tête de la page -->
        <div class="about-header">
            <span class="badge">Notre ADN</span>
            <h1>L'innovation juridique à votre portée</h1>
        </div>

        <div class="about-content">
            
            <!-- SECTION 1 : Qu'est-ce que Contrat Chap (Image Gauche / Texte Droite) -->
            <section class="about-row">
                <div class="about-image glass-border">
                    <!-- Remplace par ton image -->
                    <img src="../../assets/pictures/ContratChap/pexels-thirdman-5060819.jpg" alt="Qu'est-ce que Contrat Chap">
                </div>
                <div class="about-text">
                    <span class="section-number">01</span>
                    <h2>Qu'est-ce que Contrat ChapNeo ?</h2>
                    <p>
                        Contrat ChapNeo est la première plateforme digitale intelligente dédiée à l'espace OHADA. 
                        Nous transformons la création, la gestion et la sécurisation de vos documents juridiques 
                        et contrats professionnels en une expérience fluide et accessible à tous.
                    </p>
                </div>
            </section>

            <!-- SECTION 2 : Nos Solutions (Texte Gauche / Image Droite) -->
            <!-- Note la classe "reverse" qui inverse l'ordre sur grand écran -->
            <section class="about-row reverse">
                <div class="about-image glass-border">
                    <!-- Remplace par ton image -->
                    <img src="../../assets/pictures/ContratChap/image_d_accueil.png" alt="Nos solutions">
                </div>
                <div class="about-text">
                    <span class="section-number">02</span>
                    <h2>Les solutions que nous apportons</h2>
                    <p>
                        Fini les modèles obsolètes et les démarches longues. Nous vous offrons :
                    </p>
                    <ul class="benefits-list">
                        <li><strong>Génération rapide :</strong> Vos contrats sur-mesure prêts en quelques clics.</li>
                        <li><strong>Conformité absolue :</strong> Des documents validés par des experts du droit.</li>
                        <li><strong>Protection totale :</strong> Sécurisation de vos cessions de droits et affaires.</li>
                    </ul>
                </div>
            </section>

            <!-- SECTION 3 : À propos de nous (Image Gauche / Texte Droite) -->
            <section class="about-row">
                <div class="about-image glass-border">
                    <!-- Remplace par ton image -->
                    <img src="../../assets/pictures/ContratChap/konkapo-home-office-10207248_1920.jpg" alt="À propos de notre équipe">
                </div>
                <div class="about-text">
                    <span class="section-number">03</span>
                    <h2>Qui sommes-nous ?</h2>
                    <p>
                        Nous sommes une alliance de passionnés : experts technologiques et professionnels du droit. 
                        Notre mission quotidienne est de casser les barrières du monde juridique pour le rendre transparent, 
                        moderne et au service des entrepreneurs africains.
                    </p>
                </div>
            </section>

        </div>
    </main>
</template>

<script setup lang="ts">
// Plus besoin de logique complexe ici pour le moment !
</script>

<style scoped>
/* ── Couleurs et Fonds ── */
.about-page {
    background: #0f172a; /* Bleu nuit pour garder ton thème */
    min-height: 100vh;
    padding: 6rem 2rem;
    color: #ffffff;
    overflow-x: hidden;
}

/* ── Header de la page ── */
.about-header {
    text-align: center;
    margin-bottom: 5rem;
}

.badge {
    background: rgba(52, 211, 153, 0.15);
    color: #34d399;
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.about-header h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    margin: 1rem 0 0;
    font-weight: 700;
}

/* ── Conteneur Principal ── */
.about-content {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 6rem; /* Grand espace entre chaque section pour respirer */
}

/* ── Structure des Lignes (Flexbox) ── */
.about-row {
    display: flex;
    align-items: center; /* Centre le texte verticalement par rapport à l'image */
    gap: 4rem; /* Espace entre l'image et le texte */
}

/* La classe magique qui inverse l'ordre (Image passe à droite) */
.about-row.reverse {
    flex-direction: row-reverse;
}

/* ── Les Blocs Images (Les "Cards") ── */
.about-image {
    flex: 1; /* Prend 50% de la largeur disponible */
    aspect-ratio: 4 / 3; /* Format d'image harmonieux */
    border-radius: 1.5rem;
    overflow: hidden;
    position: relative;
    /* Petit effet d'ombre pour décoller l'image du fond */
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.about-image img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* L'image remplit la boîte sans se déformer */
    display: block;
    transition: transform 0.5s ease;
}

.about-image:hover img {
    transform: scale(1.03); /* Léger zoom au survol pour le dynamisme */
}

/* Une petite bordure style Glassmorphism pour garder la D.A. */
.glass-border {
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* ── Les Blocs Textes ── */
.about-text {
    flex: 1; /* Prend l'autre 50% de la largeur */
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.section-number {
    font-size: 1.2rem;
    font-weight: 800;
    color: #34d399; /* Ton vert d'accentuation */
    margin-bottom: 0.5rem;
    opacity: 0.8;
}

.about-text h2 {
    font-size: clamp(1.8rem, 3vw, 2.2rem);
    font-weight: 700;
    margin: 0 0 1.5rem 0;
    line-height: 1.2;
}

.about-text p {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #94a3b8; /* Gris clair agréable à lire */
    margin: 0 0 1.5rem 0;
}

/* ── Liste des solutions ── */
.benefits-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.benefits-list li {
    font-size: 1rem;
    color: #94a3b8;
    position: relative;
    padding-left: 1.5rem;
}

/* Ajout d'une puce personnalisée verte */
.benefits-list li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: #34d399;
    font-weight: bold;
}

.benefits-list strong {
    color: #ffffff;
}

/* ── RESPONSIVE : Mobile et Tablettes ── */
@media (max-width: 900px) {
    .about-row, 
    .about-row.reverse {
        /* Sur petit écran, on empile tout verticalement (Image en haut, Texte en bas) */
        flex-direction: column; 
        gap: 2.5rem;
        text-align: center; /* On centre le texte sur mobile */
    }

    .about-content {
        gap: 4rem; /* Réduit l'espace entre les sections sur mobile */
    }

    .about-text {
        align-items: center; /* Centre le contenu flex sur mobile */
    }

    .benefits-list li {
        text-align: left; /* Garde la liste alignée à gauche pour la lisibilité */
    }
}
</style>