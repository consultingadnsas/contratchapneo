<template>
    <section class="main-section">
        
        <!-- En-tête de la section -->
        <div class="header-container">
            <h3 class="main-title">Calculons vos droits en <span>quelques clics</span></h3>
        </div>

        <div class="calculator-section">
            <div class="section-overlay"></div>
            
            <!-- NOUVEAU : Conteneur des symboles mathématiques 3D -->
            <div class="floating-symbols">
                <span class="math-symbol s-plus">+</span>
                <span class="math-symbol s-minus">-</span>
                <span class="math-symbol s-percent">%</span>
                <span class="math-symbol s-multiply">×</span>
                <span class="math-symbol s-divide">÷</span>
                <span class="math-symbol s-equal">=</span>
            </div>
            
            <div class="infographic-wrapper">
                
                <!-- GAUCHE : Le "Hub" central -->
                <div class="info-hub">
                    <div class="hub-circle glass">
                        <h4>Outil de<br>Calcul</h4>
                        <div class="hub-line"></div>
                        <p>Évaluez vos frais juridiques et indemnités en toute transparence.</p>
                    </div>
                </div>

                <!-- DROITE : Les nœuds/cartes -->
                <div class="info-nodes">
                    <!-- L'axe en pointillés -->
                    <div class="dashed-axis"></div>

                    <article 
                        v-for="(item, index) in calculOptions" 
                        :key="index"
                        class="node-item"
                    >
                        <!-- La carte (Pill Glassmorphism) -->
                        <div class="node-card glass-pill">
                            <div class="card-content">
                                <h5>{{ item.title }}</h5>
                                <p>{{ item.desc }}</p>
                            </div>
                            <!-- Icône SVG dynamique -->
                            <div class="card-icon" v-html="item.icon"></div>
                        </div>
                    </article>
                </div>

            </div>

            <!-- Bouton d'action centré en bas -->
            <div class="action-container">
                <secondButton label="Calculer vos droits" @click="router.push('/lawcalcul')" />
            </div>
            
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import secondButton from '../buttons/secondButton.vue';
import { useRouter } from 'vue-router';

export default {
    name: 'CalculToolSection',
    components: {
        mainButton,
        secondButton
    },
    setup() {
        const router = useRouter();
        const calculOptions = ref([
            { 
                title: 'Indemnités de licenciement', 
                desc: 'Estimez vos droits de départ selon le code du travail.',
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5c-1.2 0-2 .8-2 2v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>'
            },
        ]);

        return {
            calculOptions,
            router
        };
    }
}
</script>

<style scoped>
/* --- Structure globale --- */
.main-section {
    padding: 4rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3rem;
    width: 100%;
}

.header-container {
    text-align: center;
    max-width: 600px;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #111827;
    line-height: 1.2;
    margin: 0;
}

/* --- Bloc Principal Sombre (D.A. ContratChap) --- */
.calculator-section {
    position: relative;
    background: #0155b8;
    padding: 5rem 2rem;
    border-radius: 2rem;
    width: fit-content;
    max-width: 1100px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
}

.section-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at left, rgba(52, 211, 153, 0.05) 0%, transparent 40%);
    pointer-events: none;
}

/* --- SYMBOLES 3D FLOTTANTS --- */
.floating-symbols {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1; /* Reste derrière le contenu grâce au z-index */
    overflow: hidden;
}

.math-symbol {
    position: absolute;
    font-family: 'Arial', sans-serif;
    font-weight: 900;
    color: #32f459; /* Très transparent pour ne pas gêner la lecture */
    /* L'accumulation d'ombres crée l'effet d'épaisseur 3D avec une touche de vert à la base */
    text-shadow: 
        1px 1px 0 rgba(255, 255, 255, 0.05),
        2px 2px 0 rgba(255, 255, 255, 0.05),
        3px 3px 0 rgba(52, 211, 153, 0.3),
        4px 4px 0 rgba(52, 211, 153, 0.2),
        5px 5px 15px rgba(0, 0, 0, 0.5);
    transform-style: preserve-3d;
}

/* Position, taille et attribution des animations pour chaque symbole */
.s-plus { top: 5%; left: 8%; font-size: 5rem; animation: float3d-1 8s infinite ease-in-out; }
.s-minus { bottom: 10%; left: 35%; font-size: 6rem; animation: float3d-2 10s infinite ease-in-out reverse; }
.s-percent { top: 10%; right: 15%; font-size: 4rem; animation: float3d-3 9s infinite ease-in-out; }
.s-multiply { bottom: 15%; right: 8%; font-size: 5.5rem; animation: float3d-1 12s infinite ease-in-out reverse; }
.s-divide { top: 50%; left: 2%; font-size: 4.5rem; animation: float3d-2 9s infinite ease-in-out; }
.s-equal { top: 40%; right: 3%; font-size: 4rem; animation: float3d-3 8s infinite ease-in-out reverse; }

/* Animations Keyframes pour simuler la rotation 3D et le flottement */
@keyframes float3d-1 {
    0% { transform: translateY(0) rotateX(10deg) rotateY(15deg) rotateZ(0deg); }
    50% { transform: translateY(-25px) rotateX(-15deg) rotateY(25deg) rotateZ(15deg); }
    100% { transform: translateY(0) rotateX(10deg) rotateY(15deg) rotateZ(0deg); }
}
@keyframes float3d-2 {
    0% { transform: translateY(0) rotateX(-20deg) rotateY(-10deg) rotateZ(-10deg); }
    50% { transform: translateY(20px) rotateX(15deg) rotateY(-25deg) rotateZ(5deg); }
    100% { transform: translateY(0) rotateX(-20deg) rotateY(-10deg) rotateZ(-10deg); }
}
@keyframes float3d-3 {
    0% { transform: translateY(0) scale(1) rotate(0deg); }
    50% { transform: translateY(-15px) scale(1.1) rotate(-15deg); }
    100% { transform: translateY(0) scale(1) rotate(0deg); }
}

/* --- Layout Infographie (Flexbox) --- */
.infographic-wrapper {
    position: relative;
    z-index: 2; /* Reste devant les symboles flottants */
    display: flex;
    flex-direction: column;
    gap: 4rem;
    margin-bottom: 4rem;
}
.action-container{
    padding: 1rem;
    display: flex;
    justify-content: center;
    position: relative;
    z-index: 2;
}

@media (min-width: 1024px) {
    .infographic-wrapper {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
        padding: 2rem 1rem;
    }
}

/* --- GAUCHE : Hub Central --- */
.info-hub {
    flex: 0 0 35%;
    display: flex;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.hub-circle {
    width: 280px;
    height: 280px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 0.5rem 1rem 1rem 1rem;
    background: rgba(255, 255, 255, 0.155);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: inset 0 0 40px rgba(52, 211, 153, 0.1);
}

.hub-circle h4 {
    color: #ffffff;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.1;
}

.hub-line {
    width: 40px;
    height: 3px;
    background: #34d399;
    margin: 1rem 0;
    border-radius: 5px;
}

.hub-circle p {
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 0;
}

/* --- DROITE : Les Nœuds (Pills) --- */
.info-nodes {
    flex: 1;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding-left: 20px;
}

.dashed-axis {
    position: absolute;
    top: 20px;
    bottom: 20px;
    left: 40px;
    width: 2px;
    border-left: 2px dashed rgba(52, 211, 153, 0.4);
    z-index: 1;
}

.node-item {
    position: relative;
    display: flex;
    align-items: center;
    gap: 1rem;
    z-index: 2;
    transition: transform 0.2s ease;
}

.node-item:hover {
    transform: translateX(10px);
}

.glass-pill {
    flex: 1;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 50px;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.card-content {
    display: flex;
    flex-direction: column;
}

.card-content h5 {
    color: #ffffff;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.2rem 0;
}

.card-content p {
    color: #94a3b8;
    font-size: 0.85rem;
    margin: 0;
    line-height: 1.4;
}

.card-icon {
    width: 32px;
    height: 32px;
    color: #fff;
    flex-shrink: 0;
}

.calculator-section {
    width: 100%;
    max-width: 1100px;
    padding: 1rem 2rem;
}

/* --- Bouton d'action --- */
.action-container {
    padding: 0rem 1rem;
    display: flex;
    justify-content: center;
    position: relative;
    z-index: 2;
    margin-top: -2rem;
}

/* --- RESPONSIVE MOBILE --- */
@media (max-width: 768px) {
    .glass-pill {
        border-radius: 20px;
        padding: 1rem;
    }
    
    .hub-circle {
        width: 250px;
        height: 250px;
    }
    .calculator-section {
        width: fit-content;
        max-width: 1100px;
    }
    
    .hub-circle h4 {
        font-size: 1.4rem;
    }
    .action-container{
        padding: 1rem;
        display: flex;
        justify-content: center;
        position: relative;
        z-index: 2;
    }
}
</style>