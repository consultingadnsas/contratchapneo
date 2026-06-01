<template>
    <section class="support-banner">
        <div class="banner-container">
            
            <div class="banner-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                </svg>
            </div>

            <div class="banner-text">
                <h2>Besoin d'aide ?</h2>
                <p>Contactez-nous par appel ou sur WhatsApp pour être guidé par nos experts.</p>
            </div>

            <div class="banner-action">
                <div class="action-buttons">
                    
                    <a href="tel:+2250779101170" class="contact-btn btn-call">
                        <span class="pulse-dot"></span>
                        <span class="btn-text">Appeler le +225 07 79 10 11 70</span>
                    </a>

                    <a href="https://wa.me/2250779101170" target="_blank" rel="noopener noreferrer" class="contact-btn btn-whatsapp">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c-.003 1.398.366 2.76 1.062 3.964L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
                        </svg>
                        <span class="btn-text">WhatsApp</span>
                    </a>

                </div>
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
    --color-success: #4db562; /* Ce vert s'accorde bien avec WhatsApp */
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
    padding: 0 1rem;
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
    color: var(--color-success);
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
    color: #cbd5e1;
    margin: 0;
    max-width: 600px;
}

/* ── Bloc d'action ───────────────────────────────────────────── */
.banner-action {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-top: 0.5rem;
}

/* Groupe de boutons (Colonne sur mobile) */
.action-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 380px; /* Limite la largeur sur mobile pour ne pas que ça soit immense */
}

/* Base commune pour les deux boutons */
.contact-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease, opacity 0.3s ease;
    width: 100%;
    box-sizing: border-box;
}

.contact-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
}

/* Spécifique : Bouton Appel (Blanc) */
.btn-call {
    background-color: #ffffff;
    color: var(--color-primary);
}

/* Spécifique : Bouton WhatsApp (Vert) */
.btn-whatsapp {
    background-color: var(--color-success);
    color: #ffffff;
}

.btn-whatsapp:hover {
    opacity: 0.9;
}

/* ── Animation Point Vert ────────────────────────────────────── */
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
    .support-banner {
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
        flex-shrink: 0;
    }

    .banner-text {
        flex: 1;
    }

    .banner-action {
        align-items: flex-end;
        width: auto;
        flex-shrink: 0;
        margin-top: 0;
    }

    /* Sur Desktop, on met les boutons côte à côte */
    .action-buttons {
        flex-direction: row;
        max-width: none;
    }

    .contact-btn {
        width: auto; /* Les boutons reprennent la taille de leur texte */
    }
}

@media (min-width: 1200px) {
    .support-banner {
        width: 95%;
    }
}
</style>