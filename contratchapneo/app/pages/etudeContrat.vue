<template>
    <section class="study-section">
        <navbar/>
        <div class="bg-huge-text">CONTRAT</div>

        <div class="contact-container">
            <EtudeContratLeft />
            <EtudeContratRight />
        </div>
    </section>
</template>

<script lang="ts">
import navbar from '../components/navigation/navbar.vue';
import EtudeContratLeft from '../components/sections/etudeContrat/etudeContratLeft.vue';
import EtudeContratRight from '../components/sections/etudeContrat/etudeContratRight.vue';

export default {
    name: 'EtudeContratPage',
    components: {
        navbar,
        EtudeContratLeft,
        EtudeContratRight
    },
    setup() {
        return {};
    }
};
</script>

<style scoped>
/* ── Container Principal ── */
.study-section {
    position: relative;
    width: 100%;
    min-height: 100vh;
    padding: 8rem 2rem 4rem 2rem;
    background: radial-gradient(circle at center, #202b4a 0%, #0f0f0f 100%);
    color: var(--my-white, #ffffff);
    overflow-x: hidden;
    display: flex;
    justify-content: center;
}

/* ── Le grand texte en filigrane (façon "CONTACT" dans l'image) ── */
.bg-huge-text {
    position: absolute;
    top: 15%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 18vw;
    font-weight: 900;
    color: rgba(255, 255, 255, 0.053);
    z-index: 0;
    pointer-events: none;
    user-select: none;
    letter-spacing: 0.05em;
    font-family: Zalando Sans SemiExpanded, sans-serif;
}

/* ── Conteneur du Layout en 2 colonnes ── */
.contact-container {
    display: flex;
    gap: 4rem;
    max-width: 1200px;
    width: 100%;
    z-index: 2;
    position: relative;
    align-items: flex-start;
}

/* ── Reponsive Mobile & Tablette ── */
@media (max-width: 992px) {
    .contact-container {
        flex-direction: column;
        gap: 3rem;
    }
}

@media (max-width: 480px) {
    .study-section {
        padding: 6rem 1rem 3rem 1rem;
    }
    .bg-huge-text {
        font-size: 20vw;
        top: 10%;
    }
}
</style>