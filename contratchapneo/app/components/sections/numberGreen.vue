<template>
    <section class="support-banner">
        <div class="banner-container">
            
            <!-- Icône Casque / Support -->
            <div class="banner-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                </svg>

            </div>

            <!-- Texte d'accroche -->
            <div class="banner-text">
                <h2>Besoin d'aide ?</h2>
                <p>Nos experts juridiques sont à votre écoute pour vous guider dans le choix et la rédaction de vos contrats.</p>
            </div>

            <!-- Bloc d'action / Numéro -->
            <div class="banner-action">
                <!-- Le lien "tel:" permet de lancer l'appel directement sur mobile -->
                <a href="tel:+2250779101170" class="toll-free-btn">
                    <span class="pulse-dot"></span>
                    <span class="btn-label">Appeler au :</span>
                    <span class="btn-number">+225 07 79 10 11 70</span>
                </a>
                <span class="free-text"></span>
            </div>

        </div>
    </section>
</template>

<script>
export default {
    name: 'SupportBanner'
}
</script>

<style scoped>
/* ── Couleurs du projet ──────────────────────────────────────── */
.support-banner {
    --color-primary: #156ca9;
    --color-success: #4db562;
    --color-dark: #294F62;
    
    background-color: var(--color-dark);
    color: #ffffff;
    padding: 3rem 1.5rem;
    width: 100%;
}

/* ── Conteneur principal ─────────────────────────────────────── */
.banner-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1.5rem;
}

/* ── Icône ───────────────────────────────────────────────────── */
.banner-icon {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.banner-icon svg {
    width: 40px;
    height: 40px;
    color: var(--color-success); /* Touche de vert pour rappeler le "numéro vert" */
}

/* ── Textes ──────────────────────────────────────────────────── */
.banner-text h2 {
    font-size: clamp(1.5rem, 4vw, 2rem);
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
}

.banner-text p {
    font-size: clamp(0.95rem, 2vw, 1.1rem);
    color: #cbd5e1; /* Gris clair très lisible sur fond bleu foncé */
    margin: 0;
    max-width: 600px;
}

/* ── Bloc d'action ───────────────────────────────────────────── */
.banner-action {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

/* Bouton / Pilule du numéro */
.toll-free-btn {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background-color: #ffffff;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.toll-free-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 20px -3px rgba(0, 0, 0, 0.3);
}

.btn-label {
    color: var(--color-dark);
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
}

.btn-number {
    color: var(--color-primary);
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 0.05em;
}

/* Petit texte sous le bouton */
.free-text {
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 500;
}

/* ── Animation Point Vert (Pulsation) ────────────────────────── */
.pulse-dot {
    width: 10px;
    height: 10px;
    background-color: var(--color-success);
    border-radius: 50%;
    position: relative;
}

.pulse-dot::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--color-success);
    border-radius: 50%;
    top: 0;
    left: 0;
    animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes ping {
    75%, 100% {
        transform: scale(2.5);
        opacity: 0;
    }
}

/* ── 💻 Desktop & Tablettes (A partir de 992px) ──────────────── */
@media (min-width: 992px) {
    .support-banner{
        border-radius: 10px;

    }

    .banner-container {
        flex-direction: row;
        text-align: left;
        justify-content: space-between;
        gap: 2rem;
        width: 90%;
        height: 80%;
    }

    .banner-icon {
        flex-shrink: 0; /* Empêche l'icône de s'écraser */
    }

    .banner-text {
        flex: 1; /* Le texte prend l'espace disponible au centre */
    }

    .banner-action {
        align-items: flex-end; /* Aligne le bouton à droite */
        flex-shrink: 0;
        margin-top: 0;
    }
}
</style>