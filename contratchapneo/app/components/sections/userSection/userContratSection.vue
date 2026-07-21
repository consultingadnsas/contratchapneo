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
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
    components: {
        contratCards,
        contractCardProfile
    },

    setup() {
        const contratStore = useContratStore();
        const router = useRouter();

        // Actions
        async function fillContract(contract_id: string) {
            try {
                // 🚀 MODIFICATION ICI : On passe l'ID dans l'URL
                // Cela va rediriger vers une URL du type /contractwritter/1234-5678-...
                router.push(`/contractwritter/${contract_id}`);
                
                console.log("Navigation vers le générateur avec l'id :", contract_id);
            } catch(err: any) {
                console.warn("Un avertissement est survenu lors de la redirection", err);
            }
        }

        onMounted(() => {
            contratStore.getContracts(1);
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