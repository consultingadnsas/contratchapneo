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
                
                <!-- Un petit texte de chargement le temps que l'API réponde -->
                <p v-if="proStore.isLoading && selectedPros.length === 0" class="text-sm opacity-50 my-4">
                    Chargement des professionnels...
                </p>

                <div v-else class="cards-container">
                    <prodCards 
                        v-for="(pro, index) in selectedPros" 
                        :key="pro.id"
                        :ref="el => setCardRef(el)"
                        :data-index="index"
                        :title="`${pro.first_name} ${pro.last_name}`"
                        :subtitle="pro.title_display"
                        :image="pro.profile_picture || undefined"
                        @view="goToProDirectory(pro)"
                        @pro-checkout="goToProDirectory(pro)"
                        class="clickable-card"
                        :class="[
                            'card-item',
                            { 'card-animate': animatedCards[index] },
                            animatedCards[index] ? `card-animate-${(index % 6) + 1}` : ''
                        ]"
                    />
                </div>
            </div>

            <mainButton label="Voir tous les experts" @click="router.push('/pro')" />
        </div>
    </section>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUpdate, onBeforeUnmount, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import mainButton from '../buttons/mainButton.vue';
import prodCards from '../cards/proCards.vue'; // Ton vrai composant de carte Pro
import { useProStore } from '../../stores/proStore'; 

export default {
    name: 'OrdinarySection',
    components: { mainButton, prodCards },
    setup() {
        const router = useRouter();
        const proStore = useProStore();

        // 🪄 L'algorithme de "Pêche" aux professionnels
        const selectedPros = computed(() => {
            const allPros = proStore.professionals;
            if (!allPros || allPros.length === 0) return [];

            const targets = ['avocat', 'notaire', 'juriste', 'conseill'];
            const result: typeof allPros = [];
            const usedIds = new Set(); // Pour ne pas afficher deux fois la même personne

            // 1. On cherche 1 profil pour chaque mot-clé
            for (const target of targets) {
                const found = allPros.find(pro => 
                    !usedIds.has(pro.id) && 
                    pro.domains.some(d => d.slug.toLowerCase().includes(target) || d.name.toLowerCase().includes(target))
                );
                
                if (found) {
                    result.push(found);
                    usedIds.add(found.id);
                }
            }

            // 2. Si jamais on n'en a pas trouvé 4 (ex: pas de notaire en base), 
            // on comble les trous avec les autres pros disponibles pour garder un beau design.
            for (const pro of allPros) {
                if (result.length >= 4) break;
                if (!usedIds.has(pro.id)) {
                    result.push(pro);
                    usedIds.add(pro.id);
                }
            }

            return result;
        });

        // 🚀 Si on clique sur la carte depuis l'accueil, on l'envoie vers l'annuaire filtré
        const goToProDirectory = (pro: any) => {
            const primaryDomain = pro.domains?.[0]?.slug || '';
            router.push({ path: '/pro', query: { domaine: primaryDomain } });
        };

        // --- Gestion des Animations (inchangé) ---
        const cardRefs = ref<HTMLElement[]>([]);
        const animatedCards = ref<boolean[]>([false, false, false, false]);
        let observer: IntersectionObserver | null = null;

        onBeforeUpdate(() => {
            cardRefs.value = [];
        });

        const setCardRef = (el: any) => {
            if (el && el.$el) {
                cardRefs.value.push(el.$el);
            }
        };

        const initObserver = () => {
            if (observer) observer.disconnect();
            
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

            cardRefs.value.forEach((cardEl) => {
                if (cardEl) observer?.observe(cardEl);
            });
        };

        onMounted(async () => {
            // Demander au store de charger les professionnels s'ils ne sont pas encore là
            if (proStore.professionals.length === 0) {
                await proStore.getProfessionals();
            }

            // Attendre que le DOM affiche les cartes, puis lancer les animations
            nextTick(() => {
                setTimeout(() => {
                    initObserver();
                }, 150); // Léger délai supplémentaire pour la fluidité
            });
        });

        onBeforeUnmount(() => {
            if (observer) observer.disconnect();
        });

        return { 
            proStore,
            selectedPros,
            animatedCards,
            setCardRef,
            router,
            goToProDirectory
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

/* Rendre toute la carte cliquable */
.clickable-card {
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.clickable-card:hover {
    transform: translateY(-5px);
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
  opacity: 0; 
  transition: opacity 0.2s;
}

.card-animate {
  animation: fadeUp 0.6s ease forwards;
}

.card-animate-1 { animation-delay: 0.1s; }
.card-animate-2 { animation-delay: 0.2s; }
.card-animate-3 { animation-delay: 0.3s; }
.card-animate-4 { animation-delay: 0.4s; }
</style>