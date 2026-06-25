<template>
    <div class="left-panel">
        <h1>Faites analyser <span>votre contrat</span></h1>
        <p>Confiez vos documents à nos experts juridiques en vue d'une révision complète, confidentielle et sécurisée pour la protection de vos intérêts.</p>

        <div class="info-cards-container">
            <div class="info-card">
                <div class="icon-box">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                </div>
                <div class="info-texts">
                    <h4>Expertise OHADA</h4>
                    <span>Avocats et juristes qualifiés</span>
                </div>
            </div>

            <div class="info-card">
                <div class="icon-box">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                </div>
                <div class="info-texts">
                    <h4>Confidentialité absolue</h4>
                    <span>Vos données sont 100% protégées</span>
                </div>
            </div>

            <div class="info-card">
                <div class="icon-box">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                </div>
                <div class="info-texts">
                    <h4>Réponse rapide</h4>
                    <span>Sous 48h à 72h ouvrées</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: 'EtudeContratLeft',
    setup() {
        return {};
    }
};
</script>

<style scoped>
/* ── COLONNE GAUCHE ── */
.left-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding-top: 2rem;
}

.left-panel h1 {
    font-size: clamp(3rem, 4.5vw, 4rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1rem;
    color: #ffffff;
}

.left-panel span {
    color: var(--primary-color)
}

.left-panel p {
    font-size: 1.15rem;
    color: #a0aec0;
    line-height: 1.6;
    margin-bottom: 3rem;
    max-width: 90%;
}

.info-cards-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.info-card {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 1rem 1.2rem;
    border-radius: 16px;
    transition: all 0.3s ease;
    cursor: default;
}

.icon-box {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    margin-right: 1.2rem;
    color: #a0aec0;
    flex-shrink: 0;
}

.info-card:hover .icon-box {
    color: #32f459;
}

.info-texts {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.info-texts h4 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: #ffffff;
}

.info-texts span {
    font-size: 0.85rem;
    color: #718096;
    margin-top: 0.2rem;
}

/* ── Reponsive Mobile & Tablette ── */
@media (max-width: 992px) {
    .left-panel {
        padding-top: 0;
        align-items: center;
        text-align: center;
    }
    .left-panel p {
        margin-bottom: 2rem;
    }
    .info-cards-container {
        width: 100%;
        max-width: 500px;
    }
}
</style>