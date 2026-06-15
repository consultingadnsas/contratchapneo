<template>
    <section class="main-section">
        <div class="wrapper-content">
            <div class="flex flex-col items-center justify-center gap-2">
                <h3>
                    Besoin d'accompagnement personnel? Faites-vous suivre
                    <span>par nos professionnels</span>
                </h3>
            </div>

            <div class="green-dark-section w-full flex justify-center items-center flex-col">
                <div class="cards-container">
                    <prodCards 
                        v-for="(card, index) in legalPro" 
                        :key="index"
                        :ref="el => setCardRef(el)"
                        :data-index="index"
                        :title="card.title"
                        :image="card.visuel"
                        :class="[
                            'card-item',
                            { 'card-animate': animatedCards[index] },
                            animatedCards[index] ? `card-animate-${(index % 6) + 1}` : ''
                        ]"
                    />
                </div>
            </div>

            <mainButton label="consulter un pro" @click="router.push('/pro')" />
        </div>
    </section>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import prodCards from '../cards/proCards.vue';
import proCardSecond from '../cards/proCardSecond.vue';
import { useRouter } from 'vue-router';

export default {
    name: 'OrdinarySection',
    components: { mainButton, prodCards, proCardSecond },
    setup() {
        const router = useRouter();
        const legalPro = ref([
            { title: 'Avocat', visuel: '/avocat.jpg' },
            { title: 'Commissaire de justice', visuel: '/commissaire.jpg' },
            { title: 'Notaire', visuel: '/notaire.jpg' },
            { title: 'Juriste droit des affaires', visuel: '/affaire.jpg' },
        ]);

        // Références DOM des cartes
        const cardRefs = ref<HTMLElement[]>([]);
        const setCardRef = (el: any) => {
            if (el && el.$el) {
                cardRefs.value.push(el.$el);
            }
        };

        const animatedCards = ref<boolean[]>([]);
        let observer: IntersectionObserver | null = null;

        onMounted(() => {
            // Initialiser le tableau des animations à false
            animatedCards.value = new Array(legalPro.value.length).fill(false);

            // Créer l'observateur d'intersection
            observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const target = entry.target as HTMLElement;
                        const index = Number(target.getAttribute('data-index'));

                        if (!isNaN(index) && !animatedCards.value[index]) {
                            animatedCards.value[index] = true;
                            observer?.unobserve(target);
                        }
                    }
                });
            }, { threshold: 0.2, rootMargin: '0px 0px -20px 0px' });

            // Observer chaque carte après un court délai pour laisser le DOM se stabiliser
            setTimeout(() => {
                cardRefs.value.forEach((cardEl) => {
                    if (cardEl) observer?.observe(cardEl);
                });
            }, 100);
        });

        onBeforeUnmount(() => {
            if (observer) observer.disconnect();
        });

        return { 
            legalPro,
            animatedCards,
            setCardRef,
            router
        };
    }
}
</script>

<style scoped>
.main-section {
    padding: 2rem 0;
    background: #f4faff;
}

.wrapper-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    width: 100%;
}

/* --- Carrousel mobile (par défaut) --- */
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1rem;
    padding: 0.5rem 1rem;
    width: 100%;
    scrollbar-width: thin;
}

.cards-container > * {
    flex: 0 0 85%;
    scroll-snap-align: start;
}

/* --- Grille à partir de 768px (tablette et desktop) --- */
@media (min-width: 768px) {
    .cards-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        overflow-x: visible;
        scroll-snap-type: none;
        padding: 0;
    }

    .cards-container > * {
        flex: auto;
        scroll-snap-align: none;
    }
}

/* --- Animation fade-up --- */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-item {
  opacity: 0; /* caché par défaut */
  transition: opacity 0.2s;
}

.card-animate {
  animation: fadeUp 0.6s ease forwards;
}

.card-animate-1 { animation-delay: 0.1s; }
.card-animate-2 { animation-delay: 0.2s; }
.card-animate-3 { animation-delay: 0.3s; }
.card-animate-4 { animation-delay: 0.4s; }
.card-animate-5 { animation-delay: 0.5s; }
.card-animate-6 { animation-delay: 0.6s; }
</style>