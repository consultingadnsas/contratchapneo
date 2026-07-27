<template>

    <section class="w-full flex flex-col items-center gap-4 py-4">

        <contractCardSkeleton v-if="profileStore.isLoading" />

        <div v-else-if="profileStore.userPacks.length === 0" class="pack-section">
            
            <emptyState 
                title="Aucun pack acheté"
                description="Vous n'avez aucun pack disponible. Découvrez nos offres ci-dessous."
                textAction=""
                class="mb-6"
            />
            
            <div class="packs-grid">
                
                <pack-buying-card 
                    v-for="(pack, index) in profileStore.availablePacks" 
                    :key="pack.id || index"
                    :title="pack.title" 
                    :price="pack.prix"
                    :description="pack.description"
                    :planType="getPlanType(pack.title)"
                    @buy="addToCart(pack.id)"
                />

            </div>
        </div>
    
        <div v-else class="pack-section">
            
            <dashboard-input label="Je recherche mon contrat" class="search-bar" />
            
            <div class="packs-grid">
                
                <pack-buying-card 
                    v-for="(item, index) in profileStore.userPacks" 
                    :key="item.id || index"
                    :title="getFullPackInfo(item.pack).title" 
                    :price="getFullPackInfo(item.pack).prix"
                    :description="getFullPackInfo(item.pack).description"
                    :planType="getPlanType(getFullPackInfo(item.pack).title)" 
                    :isActive="true"
                    @buy="addToCart(item.pack)"
                />

            </div>
        </div>

    </section>
</template>

<script lang="ts">
import { useProfileStore } from '../../../stores/profileStore'
import { useCartStore } from '../../../stores/cartStore';
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

import contractCardSkeleton from '../../cards/contractCardSkeleton.vue';
import emptyState from '../../tools/emptyState.vue'
import packBuyingCard from '../../cards/packBuyingCard.vue'
import dashboardInput from '../../input/dashboardInput.vue'

export default {
    components: {
        contractCardSkeleton,
        emptyState,
        packBuyingCard,
        dashboardInput,
    },

    setup() {
        const cartStore = useCartStore();
        const profileStore = useProfileStore();

        const router = useRouter();

        const addToCart = async(packId:string)=> {

            await cartStore.addPackToCart(packId);

            router.push('/order/checkout/')

        }

        const getPlanType = (title?: string) => {
            // Si title n'existe pas (undefined ou null), on renvoie le type par défaut sans crasher
            if (!title) return 'basique'; 

            const lowerTitle = title.toLowerCase();
            if (lowerTitle.includes('pro')) {
                return 'business-pro';
            } else if (lowerTitle.includes('business')) {
                return 'business';
            }
            return 'basique'; 
        };

        const getFullPackInfo = (packId: string) => {
            const foundPack = profileStore.availablePacks.find(p => p.id === packId);
            
            // Si on trouve le pack, on le renvoie. Sinon on renvoie des valeurs par défaut pour éviter les crashs.
            return foundPack || { 
                title: 'Pack inconnu', 
                prix: '0', 
                description: 'Description indisponible' 
            };
        };

        onMounted(async () => {
            await profileStore.fetchPacks();

            await profileStore.getPacks();
        });

        return {
            cartStore,
            profileStore,
            router,
            addToCart,
            getPlanType,
            getFullPackInfo
        }
    }
}
</script>

<style scoped>
/* =========================================
   CONTENEUR PRINCIPAL
========================================= */
.pack-section {
    width: 100%;
    max-width: 1200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5rem;
    min-width: 0; 
}

.search-bar {
    width: 100%;
    max-width: 500px;
    margin-bottom: 1rem;
}

/* =========================================
   📱 MOBILE : CARROUSEL HORIZONTAL FLUIDE
========================================= */
.packs-grid {
    width: 100%;
    display: flex;
    flex-wrap: nowrap; 
    overflow-x: auto;  
    gap: 1rem;
    
    /* Espacement pour l'ombre et le scroll */
    padding-bottom: 1.5rem; 
    padding-left: 1rem;
    padding-right: 1rem;
    
    /* Défilement ultra-fluide sur iOS */
    -webkit-overflow-scrolling: touch; 
    
    /* Magnétisme du scroll */
    scroll-snap-type: x mandatory; 
    
    /* Masquer la scrollbar */
    scrollbar-width: none; 
}

.packs-grid::-webkit-scrollbar {
    display: none;
}

.packs-grid > * {
    /* La carte prend 85% de l'écran, avec une largeur max pour les grands téléphones */
    flex: 0 0 85%; 
    max-width: 320px; 
    
    /* Centre la carte à l'arrêt du scroll */
    scroll-snap-align: center; 
}

/* =========================================
   💊 TABLETTES : GRILLE 2 COLONNES
========================================= */
@media(min-width: 768px) {
    .packs-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        overflow-x: visible; 
        padding: 0; /* Retire les marges de scroll mobile */
        gap: 2rem;
    }
    
    .packs-grid > * {
        flex: auto; 
        max-width: none;
    }
}

/* =========================================
   💻 ORDINATEURS : GRILLE 3 COLONNES
========================================= */
@media(min-width: 1024px) {
    .packs-grid {
        display: grid;
        /* ⚡️ LA SOLUTION ANTI-DÉBORDEMENT */
        /* Crée des colonnes d'au moins 280px qui s'étirent (1fr) pour remplir l'espace.
           S'il n'y a pas la place pour 3, ça passe à 2, etc. */
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        overflow-x: visible; 
        padding: 0; 
        gap: 1rem;
        width: 100%;
    }
    .packs-grid > * {
        flex: auto; 
        /* Force la carte à ne jamais dépasser la taille de sa colonne */
        max-width: 320px; 
        width: 100%;
    }
}
</style>