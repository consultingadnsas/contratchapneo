<template>
    <section class="h-full flex flex-col justify-center items-center gap-2">

        <contractCardSkeleton v-if="profileStore.isLoading" />

        <emptyState 
            v-else-if="!profileStore.isLoading && profileStore.userPacks.length === 0"
            title="Aucun pack acheté"
            description="Vous n'avez aucun pack disponible"
            textAction="Acheter pack"
        />

        <div v-else class="pack-container">
            
            <!--
                <pack-buying-card 
                    v-for="(pack, index) in profileStore.userPacks" 
                    :key="pack.id || index"
                    :title="pack.title" 
                    :price="pack.prix"
                    :description="pack.description"
                    @buy="addToCart(pack.id)"
                />
            -->
             
                <dash-board-input label="Je recherche mon contrat"/>
            
            
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
import DashBoardInput from '../../input/dashBoardInput.vue';

export default {
    components: {
        contractCardSkeleton,
        emptyState,
        packBuyingCard,
        dashboardInput,
        DashBoardInput
    },

    setup() {
        const cartStore = useCartStore();
        const profileStore = useProfileStore();

        const router = useRouter();

        const addToCart = async(packId:string)=> {

            await cartStore.addPackToCart(packId);

            router.push('/order/checkout/')

        }

        onMounted(async () => {
            await profileStore.fetchPacks();

            await profileStore.getPacks();
        });

        return {
            cartStore,
            profileStore,
            router,
            addToCart
        }
    }
}
</script>

<style scoped>
.pack-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: normal;
    align-items: center;
    padding: 1rem;
    gap: 0.5rem;
}

@media(min-width: 768px) {
    .pack-container {
        
    }
}
</style>