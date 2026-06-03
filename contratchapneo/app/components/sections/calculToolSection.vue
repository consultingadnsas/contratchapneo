<template>
    <section class="main-section">
        
        <!-- En-tête de la section -->
        <div class="header-container flex flex-col items-center justify-center gap-3">
            <h2 class="main-title">
                <span>
                    Et si on calculait vos droits en quelques clics ?
                </span>
                
            </h2>
            <p class="subtitle">
                Anticipez vos démarches grâce à notre outil de simulation conforme à la législation en vigueur.
            </p>
        </div>

        <!-- Zone principale de l'outil -->
        <div class="calculator-section w-full flex justify-center items-center flex-col">
            <div class="section-overlay"></div>
            
            <div class="content-wrapper">
                <h3 class="section-title">Que souhaitez-vous évaluer aujourd'hui ?</h3>

                <!-- La grille dynamique qui affiche ce qu'on peut calculer -->
                <div class="cards-grid">
                    <featuresCards 
                        v-for="(item, index) in calculOptions" 
                        :key="index"
                        :title="item.title"
                        class="calc-card"
                    />
                </div>

                <!-- Bouton d'action centré -->
                <div class="action-container">
                    <mainButton label="Calculez vos droits" />
                </div>
            </div>
        </div>
        
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import featuresCards from '../cards/featuresCards.vue';

export default {
    name: 'CalculToolSection',
    components: {
        mainButton,
        featuresCards
    },
    setup() {
        // J'ai renommé legalPro en calculOptions et adapté les titres 
        // pour qu'ils correspondent à des éléments de calcul réels.
        const calculOptions = ref([
            { title: 'Indemnités de licenciement' },
            { title: 'Frais d\'actes notariés' },
            { title: 'Honoraires d\'avocat' },
            { title: 'Frais de commissaire de justice' }
        ]);

        return {
            calculOptions
        };
    }
}
</script>

<style scoped>
/* --- Structure globale --- */
.main-section {
    padding: 4rem 1rem; /* Plus d'espace pour respirer */
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3rem;
    color:aquamarine;
}

/* --- En-tête (Textes du haut) --- */
.header-container {
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}

.main-title {
    font-size: clamp(1.5rem, 4vw, 2.2rem);
    font-weight: 800;
    color:#10507e;
    line-height: 1.2;
    margin: 0;
}

.subtitle {
    font-size: 1rem;
    color: #666;
    margin: 0;
}

/* --- Zone Bleue (Le Simulateur) --- */
.calculator-section {
    position: relative;
    background: var(--primary-color-dark); /* Un bleu très sombre fait sérieux/juridique */
    padding: 4rem 1rem;
    border-radius: 1.5rem; /* Coins plus arrondis pour moderniser */
    overflow: hidden;
    width: 100%;
    max-width: 1200px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.section-overlay {
    position: absolute;
    inset: 0;
    /* Petit effet visuel de fond pour habiller le bloc */
    background: radial-gradient(circle at top right, rgba(255,255,255,0.05) 0%, transparent 40%);
    pointer-events: none;
}

.content-wrapper {
    position: relative;
    z-index: 2;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2.5rem;
}

.section-title {
    color: #ffffff;
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    font-weight: 600;
    text-align: center;
    margin: 0;
}

/* --- Grille des options de calcul --- */
.cards-grid {
    display: grid;
    grid-template-columns: 1fr; /* Mobile : 1 colonne */
    gap: 1.2rem;
    width: 100%;
    max-width: 900px;
}

@media(min-width: 768px){
    .cards-grid {
        grid-template-columns: repeat(2, 1fr); /* Tablette/Desktop : 2 colonnes */
    }
}

/* Optionnel : si vous voulez que vos cards s'intègrent parfaitement sur le fond sombre */
.calc-card {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    /* On réutilise votre effet glassmorphism préféré */
    backdrop-filter: blur(10px); 
}

/* --- Bouton --- */
.action-container {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
}
</style>