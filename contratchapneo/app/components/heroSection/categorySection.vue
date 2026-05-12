<template>
    <section class="hero-section">
        <div class="left-side">
            <h3 class="typewriter">
                {{ displayText }}<span class="cursor">|</span>
            </h3>
            <h1>
                Téléchargez nos contrats 
                <span>dès maintenant.</span>
            </h1>

            <BaseResearchInput>
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

        <div class="right-side">
            <h3>Nos catégories de contrats</h3>

            <!-- Classe sémantique "cards-grid" au lieu de "grid" (évite le conflit avec Tailwind) -->
            <div class="cards-grid">
                <StatCards 
                    v-for="(cards, index) in contratCards" 
                    :key="index" 
                    :title="cards.title"
                />
            </div>

            <mainButton label="Toutes les catégories"/>
        </div>
    </section>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import BaseResearchInput from '../input/BaseResearchInput.vue';
import StatCards from '../cards/statCards.vue';
import mainButton from '../buttons/mainButton.vue';

export default {
    name: 'HeroSection',
    components: { BaseResearchInput, StatCards, mainButton },
    setup() {
        const phrases = [
            'Profitez de nos contrats gratuits.',
            'Sécurisez vos affaires juridiques.',
            'Accédez à des modèles conformes à l\'OHADA.',
        ];

        const displayText = ref('');
        const phraseIndex = ref(0);
        const charIndex = ref(0);
        const isDeleting = ref(false);
        const typeSpeed = ref(100);

        const handleType = () => {
            const currentPhrase = phrases[phraseIndex.value];

            if (isDeleting.value) {
                displayText.value = currentPhrase.substring(0, charIndex.value - 1);
                charIndex.value--;
                typeSpeed.value = 50;
            } else {
                displayText.value = currentPhrase.substring(0, charIndex.value + 1);
                charIndex.value++;
                typeSpeed.value = 100;
            }

            if (!isDeleting.value && charIndex.value === currentPhrase.length) {
                isDeleting.value = true;
                typeSpeed.value = 3000;
            } else if (isDeleting.value && charIndex.value === 0) {
                isDeleting.value = false;
                phraseIndex.value = (phraseIndex.value + 1) % phrases.length;
                typeSpeed.value = 500;
            }

            setTimeout(handleType, typeSpeed.value);
        };

        const contratCards = [
            {title:"Création et cession"},
            {title: "Prestation de services"},
            {title:"Contrat de freelance"},
            {title: "Contrat de bénévolat"}
        ]

        onMounted(() => {
            handleType();
        });

        return { displayText, contratCards };
    },
};
</script>

<style scoped>
/* =============================================
   BASE — Mobile first (< 480px)
   Colonne unique, contenu centré
   ============================================= */
.hero-section {
    padding: 6rem 1rem 1rem 1rem;
    min-height: 100vh;
    width: 100%;

    background-image:
        linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
        url('../../assets/pictures/ContratChap/black-person-signing-job-contract.jpg');
    background-size: cover; 
    background-position: center;

    display: flex;
    flex-direction: column; /* ← colonne unique sur mobile */
    gap: 2rem;
    align-items: center;
    justify-content: center;
    color: white;
}

/* --- Left side --- */
.left-side {
    width: 100%;
    text-align: center; /* centré sur mobile */
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
}

.left-side h3,
.left-side h1,
.typewriter {
    text-align: center;
}

.left-side h1 {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.15;
}

.typewriter {
    font-size: 1.1rem;
    height: 50px;
    font-weight: 500;
    text-align: center;
    width: 100%;
}
/* --- Right side --- */
.right-side {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
}

.right-side h3 {
    font-size: 1.2rem;
    font-weight: 500;
    opacity: 0.9;
    text-align: center;
}

/* --- Cards grid ---
   Classe sémantique propre, pas de conflit avec Tailwind ".grid"
   1 colonne sur très petit mobile, 2 à partir de 480px
*/
.cards-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; /* ← 1 colonne sous 480px */
    gap: 0.5rem;
    width: 100%;
}

/* =============================================
   BREAKPOINT SM — à partir de 480px
   2 colonnes pour les cartes
   ============================================= */
@media (min-width: 480px) {
    .cards-grid {
        grid-template-columns: repeat(2, 1fr); /* ← 2 colonnes dès 480px */
        width: 100%;
    }
}

/* =============================================
   BREAKPOINT MD — Tablette & Desktop (≥ 768px)
   Layout 2 colonnes côte à côte
   ============================================= */
@media (min-width: 768px) {
    .hero-section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* Réalignement gauche sur grand écran */
    .left-side,
    .left-side h1,
    .left-side h3,
    .typewriter {
        text-align: center;
    }

    .left-side h1 {
        font-size: 3rem;
    }

    .typewriter {
        font-size: 1.6rem;
    }

}

/* =============================================
   BREAKPOINT XL — Grand desktop (≥ 1200px)
   Marges plus généreuses + titres plus grands
   ============================================= */
@media (min-width: 1200px) {
    .hero-section {
        display: flex;
        flex-direction: row;
        width: 100%;
        gap: 1rem;
    }

    .left-side, .right-side{
        width: 50%;
    }

    .left-side h1 {
        font-size: 3.5rem;
    }

    .typewriter {
        font-size: 1.8rem;
    }
}

/* =============================================
   ÉLÉMENTS COMMUNS
   ============================================= */
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
}

.custom-search-icon {
    width: 22px;
    height: 22px;
    color: var(--secondary-light-color);
}
</style>