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
                        v-for="(contrat, index) in topDownloadedContracts" 
                        :key="contrat.id || index"
                        :ref="setCardRef"
                        :title="contrat.title"
                        :description="contrat.description"
                        :price="contrat.prix"
                        :image="contrat.picture || undefined"
                        :data-index="index"
                        @view="openViewModal(contrat.id)" 
                        @buy="()=>{addTocart(contrat.id)}"
                    />
                </div>

                <MainButton label="voir tous nos contrats" @click="router.push('/contractBank')" />
            </div>
            
        </div>

        <Teleport to="body">
            <CartModale 
                :isOpen="isOpen" 
                @close="isOpen = false"
            />
            <viewModale
                v-if="isViewOpen" 
                :contract="contratStore.contrat"
                @close="isViewOpen = false"
                @buy="(id) => { addTocart(id); isViewOpen = false; }"
            />
        </Teleport>

    </section>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount, computed, onBeforeUpdate, nextTick, watch } from 'vue';
import { useRouter } from 'vue-router';

import MainButton from '../buttons/mainButton.vue';
import ContratCards from '../cards/contratCards.vue';
import ContratCategoryCards from '../cards/contratCategoryCards.vue';
import CartModale from '../modale/cartModale.vue';
import ViewModale from '../modale/viewModale.vue';
import { useContratStore } from '../../stores/contratStore';
import { useCartStore } from '../../stores/cartStore';

export default {
    name: 'OrdinarySection',
    components: { 
        MainButton, 
        ContratCards,
        ContratCategoryCards,
        CartModale,
        ViewModale,
    },
    setup() {
        const router = useRouter();
        const contratStore = useContratStore();
        const cartStore = useCartStore();

        const topDownloadedContracts = computed(() => {
            return [...contratStore.contracts]
                .sort((a, b) => (b.downloads || 0) - (a.downloads || 0))
                .slice(0, 4);
        });

        const cardRefs = ref<HTMLElement[]>([]);
        
        onBeforeUpdate(() => {
            cardRefs.value = [];
        });

        const setCardRef = (el: any) => {
            const domElement = el?.$el || el;
            if (domElement instanceof Element) {
                cardRefs.value.push(domElement as HTMLElement);
            }
        };

        const animatedCards = ref<boolean[]>([]);
        let observer: IntersectionObserver | null = null;

        const isOpen = ref<boolean>(false);
        const openModal = () => {
            isOpen.value = true;
        }

        const addTocart = async (contratId: string) => {
            try {
                await cartStore.addToCart(contratId);
            } catch (error: any) {
                console.error("Erreur lors de l'ajout au panier", error)
            }
        }

        const editContract = async (contratId: string) => {
            try {
                await contratStore.toCurrentId(contratId);
                console.log("Contrat sélectionné", contratId);
                router.push("/contractWritter");
            } catch (error: any) {
                console.error("Erreur lors de l'ajout au panier", error)
            }
        }

        const isViewOpen = ref<boolean>(false);
        const selectedPreviewText = ref<string>(''); 

        const openViewModal = async(contratId:string) => {
            await contratStore.getSpecificContract(contratId);
            selectedPreviewText.value = contratStore.contrat?.document_preview || '';
            isViewOpen.value = true; 
        }

        onMounted(() => {            
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
            
            contratStore.getContracts();
        });

        watch(() => contratStore.contracts, async () => {
            await nextTick();
            cardRefs.value.forEach((cardEl) => {
                if (cardEl instanceof Element) {
                    observer?.observe(cardEl);
                }
            });
        }, { deep: true, immediate: true });

        onBeforeUnmount(() => {
            if (observer) observer.disconnect();
        });

        return { 
            contratStore,
            cartStore,
            topDownloadedContracts,
            animatedCards,
            setCardRef, 
            isOpen,
            openModal,
            isViewOpen,
            selectedPreviewText,
            addTocart,
            openViewModal,
            router,
            editContract
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
    overflow-x: hidden;
}

.wrapper-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0rem;
    width: 100%;
    padding: 0 1rem;
}

/* --- CONTENEUR DES CARTES (Mobile First) --- */
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

/* ── 📐 TABLETTES & IPAD PRO (De 600px à 1279px) ── */
@media (min-width: 600px) {
    .cards-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr); /* 👈 Reste sur 2 colonnes même pour l'iPad Pro */
        gap: 1.5rem;
        overflow-x: visible;
        scroll-snap-type: none;
        padding: 0 1rem;
    }

    .cards-container > * {
        flex: auto;
        scroll-snap-align: none;
        width: 100%;
    }
}

/* ── 💻 DESKTOP (À partir de 1280px) ── */
@media (min-width: 1280px) {
    .cards-container {
        grid-template-columns: repeat(4, 1fr); /* 👈 4 colonnes repoussées aux grands écrans */
        padding: 0;
        gap: 1rem;
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
    margin-left: 0;
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
        padding: 0;
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