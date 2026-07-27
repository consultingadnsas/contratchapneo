<template>

    <div class="cards-container">

        <contractCardProfile
            v-for="(contrat, index) in contratStore.contracts" 
            :key="contrat.id || index"
            :title="contrat.title"
            :description="contrat.description"
            :image="contrat.picture || undefined"
            @view="openViewModal(contrat.id)" 
            @buy="()=>{fillContract(contrat.id)}"
        />

    </div>

</template>

<script lang="ts">
import contratCards from '../../cards/contratCards.vue';
import contractCardProfile from '../../cards/contractCardProfile.vue';
import { useContratStore } from '../../../stores/contratStore';
// ⚡️ AJOUT : on importe watch et useRoute
import { onMounted, watch } from 'vue'; 
import { useRouter, useRoute } from 'vue-router'; 

export default {
    components: {
        contratCards,
        contractCardProfile
    },

    setup() {
        const contratStore = useContratStore();
        const router = useRouter();
        const route = useRoute(); // ⚡️ AJOUT : pour lire l'URL

        // Actions
        async function fillContract(contract_id: string) {
            try {
                router.push(`/contractwritter/${contract_id}`);
                console.log("Navigation vers le générateur avec l'id :", contract_id);
            } catch(err: any) {
                console.warn("Un avertissement est survenu lors de la redirection", err);
            }
        }

        // ⚡️ NOUVEAU : On surveille l'URL. Si la barre de recherche change l'URL, on filtre.
        watch(() => route.query.q, (newQuery) => {
            if (newQuery) {
                // J'utilise fetchContracts en supposant que c'est ta méthode de recherche dans le store
                contratStore.fetchContracts(1, '', newQuery as string);
            } else {
                contratStore.getContracts(1);
            }
        });

        // ⚡️ MODIFICATION : Au chargement, on vérifie s'il y a déjà une recherche dans l'URL
        onMounted(() => {
            if (route.query.q) {
                contratStore.fetchContracts(1, '', route.query.q as string);
            } else {
                contratStore.getContracts(1);
            }
        });

        return {
            router,
            contratStore,
            fillContract
        }
    }
}
</script>

<style scoped>
.cards-container {
    width: 100%;
    max-width: 1400px;
    display: grid;
    grid-template-columns: 1fr;
    place-items: center;
    gap: 1.5rem;
}

@media (min-width: 768px) and (max-width:  1023px){
    .cards-container {
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }
}

@media (min-width: 1280px){
    .cards-container {
        grid-template-columns: repeat(3, 1fr);
    }
}
</style>