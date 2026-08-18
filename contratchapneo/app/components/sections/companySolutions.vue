<template>
    <section class="main-section pack-section">
        <div class="puddle-bg"></div>
        <h3>
            Découvrez nos packs adaptés à
            <span>vos besoins</span>
        </h3>
        
        <div v-if="packStore.isLoading" style="text-align: center; padding: 2rem;">
            Chargement de nos offres...
        </div>

        <div v-else class="cards-container">
            <packCards 
                v-for="pack in packStore.packs" 
                :key="pack.id"
                :title="pack.title"
                :description="pack.description"
                :price="pack.prix"
                :promoPrice="pack.prix_promo" 
                :nombreCredits="pack.nombre_credits"
                :nombreCustomedContract="pack.nombre_customed_contract"
                :nombreCartesPro="pack.nombre_cartes_pro"
                :dureeValiditeJours="pack.duree_validite_jours"
                :planType="pack.prix < 30000 ? 'basique' : (pack.prix < 60000 ? 'business' : 'business-pro')"
            />
        </div>
    </section>
</template>

<script lang="ts">
import { onMounted } from 'vue';
import packCards from '../cards/packCards.vue';
import mainButton from '../buttons/mainButton.vue';
import { usePackStore } from '../../stores/packStore';

export default {
    name: 'CompanySection',
    components: {
        packCards,
        mainButton
    },
    setup() {
        const packStore = usePackStore();

        onMounted(() => {
            if (packStore.packs.length === 0) {
                packStore.fetchPacks();
            }
        });

        return {
            packStore
        };
    }
};
</script>

<style lang="css" scoped>
/* Conserve exactement ton CSS précédent ici */
.main-section { width: 100%; position: relative; top: -90px; bottom: 10px; overflow: hidden; background: #98f7abdd; padding-bottom: 3rem; }
.puddle-bg { position: absolute; bottom: -20px; left: -5%; width: 110%; height: 250px; background: #32f459; border-radius: 50% 50% 0 0 / 60% 60% 0 0; filter: blur(30px); opacity: 0.15; z-index: 0; pointer-events: none; }
.main-section h3 { text-align: center; font-size: clamp(1.5rem, 4vw, 2.5rem); padding: 2rem 1rem 1rem 1rem; font-weight: 700; color: #111827; }
.cards-container { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 1.5rem; padding: 1.5rem 1rem 3rem 1rem; width: 100%; box-sizing: border-box; scrollbar-width: none; -webkit-overflow-scrolling: touch; }
.cards-container::-webkit-scrollbar { display: none; }
.cards-container > * { flex: 0 0 280px; scroll-snap-align: center; }
@media (min-width: 768px) { .cards-container { padding: 2rem 2rem 3rem 2rem; gap: 2rem; } .cards-container > * { flex: 0 0 340px; } }
@media (min-width: 1024px) { .main-section h3 { font-size: 2.2rem; padding: 3rem 1rem 2rem 1rem; } .cards-container { max-width: 1300px; margin: 0 auto; } .cards-container > * { flex: 0 0 380px; } }
@media (min-width: 1280px) { .cards-container { justify-content: center; } }
</style>