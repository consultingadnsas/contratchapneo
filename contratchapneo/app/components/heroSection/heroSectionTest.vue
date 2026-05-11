<template>
    <section class="hero-section">
        <div class="left-side flex flex-col gap-4 items-start justify-center">
            <h3 class="typewriter">
                {{ displayText }}<span class="cursor">|</span>
            </h3>
            <h1>
                Téléchargez nos contrats <span>
                    dès maintenant.
                </span>
            </h1>
            
            <!-- <p>
                Téléchargez librement des contrats conformes 
                au droit OHADA et prêts à l'emploi, pour sécuriser
                vos affaires.
            </p> --> 

            <BaseResearchInput label="Chercher un contrat">
                <template #prepend>
                    <svg 
                    class="custom-search-icon" 
                    xmlns="http://www.w3.org/2000/svg" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                    >
                    <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2.5" 
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
                    />
                </svg>
                </template>
            </BaseResearchInput>
        </div>

        <div class="right-side w-full flex flex-col gap-4 items-center justify-center">

            <h3>
                Nos catégories de contrats
            </h3>
            
            <div class=" grid grid-cols-2 gap-4">
                <StatCards v-for="cards in 4"/>
            </div>

        </div>
    </section>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import BaseResearchInput from '../input/BaseResearchInput.vue';
import StatCards from '../cards/statCards.vue';

export default {
  name: 'HeroSection',
  components: { BaseResearchInput, StatCards },
  setup() {
    const phrases = [
      "Profitez de nos contrats gratuits.",
      "Sécurisez vos affaires juridiques.",
      "Accédez à des modèles conformes."
    ];
    
    const displayText = ref("");
    const phraseIndex = ref(0);
    const charIndex = ref(0);
    const isDeleting = ref(false);
    const typeSpeed = ref(100);

    const handleType = () => {
      const currentPhrase = phrases[phraseIndex.value];
      
      if (isDeleting.value) {
        // On efface
        displayText.value = currentPhrase.substring(0, charIndex.value - 1);
        charIndex.value--;
        typeSpeed.value = 50; // Plus rapide quand on efface
      } else {
        // On écrit
        displayText.value = currentPhrase.substring(0, charIndex.value + 1);
        charIndex.value++;
        typeSpeed.value = 100;
      }

      // Gestion des pauses et changement de mode
      if (!isDeleting.value && charIndex.value === currentPhrase.length) {
        isDeleting.value = true;
        typeSpeed.value = 3000; // Pause à la fin de la phrase
      } else if (isDeleting.value && charIndex.value === 0) {
        isDeleting.value = false;
        phraseIndex.value = (phraseIndex.value + 1) % phrases.length;
        typeSpeed.value = 500; // Pause avant de recommencer
      }

      setTimeout(handleType, typeSpeed.value);
    };

    onMounted(() => {
      handleType();
    });

    return { displayText };
  }
}
</script>

<style scoped>
/* Mobile first (Style par défaut) */
.hero-section {
    padding: 6rem 1rem 2rem 1rem; /* Plus d'espace en haut pour le header mobile */
    min-height: 100vh;
    width: 100%;
    background-image: 
        linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('../../assets/pictures/ContratChap/black-person-signing-job-contract.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed; /* Fixe l'image pour un effet de parallaxe fluide */
    
    display: flex;
    flex-direction: column;
    gap: 3rem;
    align-items: center;
    color: white;
}

.left-side {
    width: 100%;
    max-width: 600px;
    /* Sur mobile, on centre souvent le texte pour un meilleur look */
    text-align: center; 
}

/* On force l'alignement à gauche pour les titres si tu préfères garder ton style */
.left-side h3, .left-side h1, .typewriter {
    text-align: center; 
}

.left-side h1 {
    font-size: 2.2rem; /* Plus petit sur mobile */
    font-weight: 700;
    line-height: 1.1;
    margin-top: 1rem;
}

.typewriter {
    font-size: 1.2rem;
    min-height: 3rem;
}

.right-side {
    width: 100%;
    max-width: 500px;
}

.right-side h3 {
    margin-bottom: 1.5rem;
    font-size: 1.4rem;
    font-weight: 500;
    opacity: 0.9;
}

/* Ajustement de la grille des cartes sur mobile */
.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* 2 colonnes même sur mobile */
    gap: 1rem;
    width: 100%;
}

/* ----- TABLETTE & DESKTOP ----- */
@media (min-width: 768px) {
    .hero-section {
        display: grid;
        grid-template-columns: 1.2fr 0.8fr; /* Le texte prend plus de place que les cartes */
        gap: 2rem;
        padding: 0 5%;
        text-align: left;
    }

    .left-side, .left-side h1, .left-side h3, .typewriter {
        text-align: left; /* On repasse en alignement gauche sur grand écran */
    }

    .left-side h1 {
        font-size: 3.5rem; /* On l'agrandit sur desktop */
    }

    .typewriter {
        font-size: 1.8rem;
    }

    .right-side {
        align-items: flex-end; /* Aligne les cartes vers la droite */
    }

    .right-side h3 {
        text-align: right;
        width: 100%;
    }
}

@media (min-width: 1200px) {
    .hero-section {
        padding: 0 10%; /* Plus d'air sur les très grands écrans */
    }
    
    .left-side h1 {
        font-size: 4.5rem;
    }
}

/* Curseur et animation */
.cursor {
    color: var(--secondary-light-color);
    animation: blink 0.7s infinite;
    margin-left: 4px;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.left-side h1 span {
    color: var(--secondary-light-color);
    display: inline; /* On le remet en ligne pour desktop, géré par le h1 */
}

.custom-search-icon {
    width: 22px;
    height: 22px;
    color: var(--secondary-light-color); 
}
</style>