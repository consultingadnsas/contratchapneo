<template>
    <section class="main-section">
        
        <div class="wrapper-content">
            <div class="flex flex-col items-center justify-center gap-2">
                <h3>
                    Trouvez des contrats qui vous correspondent
                    <span>conformes aux lois en vigueur</span>
                </h3>
            </div>

            <div class="green-dark-section w-full flex justify-center items-center flex-col gap-4 mt-12">
                <div class="subtitle-wrapper">
                    <h4 class="subtitle">Nos contrats les plus téléchargés</h4>
                </div>
                <div class="divider"></div>
                
                <div class="cards-container">
                    <ContratCards 
                        v-for="(card, index) in legalContrat" 
                        :key="index"
                        :ref="el => setCardRef(el)"
                        :data-index="index"
                        :title="card.title"
                        :description="card.description"
                        :subtitle="card.subtitle"
                        :image="card.visuel"
                        @buy="openModal" 
                        @view="openViewModal"
                        :class="[
                            'card-item',
                            { 'card-animate': animatedCards[index] },
                            animatedCards[index] ? `card-animate-${(index % 6) + 1}` : ''
                        ]"
                    />
                </div>

                <MainButton label="voir tous nos contrats" />
            </div>
            
        </div>

        <Teleport to="body">
            <CartModale 
                :isOpen="isOpen" 
                @close="isOpen = false"
            />
            <ViewModale 
                v-if="isViewOpen" 
                @close="isViewOpen = false"
            />
        </Teleport>

    </section>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';

// Convention : Majuscule pour les composants Vue
import MainButton from '../buttons/mainButton.vue';
import ContratCards from '../cards/contratCards.vue';
import ContratCategoryCards from '../cards/contratCategoryCards.vue';
import CartModale from '../modale/cartModale.vue';
import ViewModale from '../modale/viewModale.vue';

import { useContratStore } from '../../stores/contratStore';
import {useCartStore} from '../../stores/cartStore'

export default {
    name: 'OrdinarySection',
    components: { 
        MainButton, 
        ContratCards,
        ContratCategoryCards,
        CartModale,
        ViewModale
    },
    setup() {
        
        const contratStore = useContratStore();
        const cartStore = useCartStore();

        const legalContrat = ref([
            { title: 'Contrat de travail' , subtitle: '100% Gratuit', description: 'Un contrat de travail est un accord entre un employeur et son employé.', visuel:'/pexels-mikhail-nilov-8729948.jpg'},
            { title: 'Contrat de Graphiste', subtitle: '15 000 FCFA', description: 'Un contrat de graphiste est un accord entre un graphiste indépendant et un client.', visuel:'/graphiste.jpg'},
            { title: 'contrat de vidéaste', subtitle: '40 000 FCFA', description: 'Un contrat de vidéaste est un accord entre un vidéaste et un acheteur.', visuel:'/videaste.jpg'},
            { title: 'contrat de restauration', subtitle: '5 000 FCFA', description: 'Un contrat de de restauration certifie une fourniture d\'aliment entre une entreprise et un restaurant.', visuel:'/resto.jpg'},
        ]);

        // Gestion propre des références du DOM via Vue
        const cardRefs = ref<HTMLElement[]>([]);
        const setCardRef = (el: any) => {
            if (el && el.$el) {
                cardRefs.value.push(el.$el); // Récupère le nœud HTML du composant
            }
        };

        const animatedCards = ref<boolean[]>([]);
        let observer: IntersectionObserver | null = null;

        const isOpen = ref<boolean>(false);
        const openModal = () => {
            isOpen.value = true;
            console.log('Événement achat émis !!!');
        }

        const isViewOpen = ref<boolean>(false);
        const openViewModal = () => {
            isViewOpen.value = true;
            console.log('Événement visualisation émis !!!');
        }

        onMounted(() => {
            animatedCards.value = new Array(legalContrat.value.length).fill(false);
            
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

            // On utilise les refs Vue au lieu de document.querySelectorAll
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
            contratStore,
            cartStore,
            legalContrat,
            animatedCards,
            setCardRef, // Exposé au template
            isOpen,
            openModal,
            isViewOpen,
            openViewModal
        };
    }
}
</script>

<style scoped>
.main-section {
    padding: 2rem 0;
    background: none;
    position: relative;
    top: -40px;
    width: 100%;
    overflow-x: hidden; /* Prévient tout dépassement horizontal imprévu */
}

.wrapper-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0rem;
    width: 100%; /* CORRIGÉ : 110% cause un scroll horizontal sur mobile */
    padding: 0 1rem; /* CORRIGÉ : On utilise le padding plutôt qu'un margin-left arbitraire */
}

/* --- STYLES ORIGINAUX DES CONTRATS (carrousel mobile / grille desktop) --- */
.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1rem;
    padding: 0.5rem;
    width: 100%;
    scrollbar-width: thin;
}

.cards-container > * {
    flex: 0 0 85%;
    scroll-snap-align: start;
}

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

/* --- STYLES DU CARROUSEL POUR CATÉGORIES --- */
.category-section {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

.subtitle-wrapper.carousel-header {
    display: flex;
    align-items: center;
    width: 100%;
    gap: 1rem;
    flex-wrap: wrap;
}

.carousel-controls {
    display: flex;
    gap: 0.5rem;
    margin-left: auto;
}

.carousel-btn {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    color: var(--primary-color, #4ade80);
}

.carousel-btn svg {
    width: 20px;
    height: 20px;
}

.carousel-btn:hover {
    background: var(--primary-color, #4ade80);
    color: white;
    border-color: var(--primary-color, #4ade80);
    transform: scale(1.05);
}

.category-carousel-container {
    width: 100%;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    scrollbar-width: thin;
    padding-bottom: 10px;
}

.category-carousel-container::-webkit-scrollbar {
    height: 6px;
}

.category-carousel-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.category-carousel-container::-webkit-scrollbar-thumb {
    background: var(--primary-color, #4ade80);
    border-radius: 10px;
}

.category-carousel-track {
    display: flex;
    gap: 1.5rem;
    width: max-content;
    padding: 0.5rem 0;
}

.category-carousel-track > * {
    flex-shrink: 0;
    scroll-snap-align: start;
    width: 240px;
}

/* Animation fade-up */
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

.card-animate {
  opacity: 0;
  animation: fadeUp 0.6s ease forwards;
}

.card-animate-1 { animation-delay: 0.1s; }
.card-animate-2 { animation-delay: 0.2s; }
.card-animate-3 { animation-delay: 0.3s; }
.card-animate-4 { animation-delay: 0.4s; }
.card-animate-5 { animation-delay: 0.5s; }
.card-animate-6 { animation-delay: 0.6s; }

.card-item {
  opacity: 0;
  transition: opacity 0.2s;
}

@media (max-width: 767px) {
    .category-carousel-track > * {
        width: 85vw;
        max-width: 280px;
    }
    .carousel-controls {
        margin-left: 0;
        width: 100%;
        justify-content: flex-end;
    }
}

@media (min-width: 768px) {
    .category-carousel-track > * {
        width: 220px;
    }
}

/* --- Autres styles partagés --- */
.subtitle-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    gap: 1rem;
    padding: 0 1rem;
}

.subtitle {
    font-size: 1.1rem;
    font-weight: 600;
    color: currentColor;
    white-space: nowrap;
}

.divider {
    flex: 1;
    height: 0.5px;
    background: linear-gradient(to right, var(--primary-color, #4ade80), transparent);
    opacity: 0.6;
    margin-left: 0; /* CORRIGÉ : le 40px n'était pas très esthétique sur mobile */
}

@media (min-width: 768px) {
    .subtitle-wrapper {
        padding: 0;
    }
    .subtitle {
        font-size: 1.3rem;
        width: 100%;
        text-align: left;
        margin-left: 50px;
    }
    .wrapper-content {
        padding: 0; /* On retire le padding sur desktop si nécessaire */
    }
    .wrapper-content h3{
        font-size: 2.2rem;
        font-weight: 700;
        max-width: 900px;
    }
    .divider {
        margin-left: 50px;
        max-width: 50%;
    }
}
</style>