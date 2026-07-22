<template>

    <div class="cards-container">

        <proCards
            v-for="(pro, index) in proStore.professionals" 
            :key="pro.id"
            :data-index="index"
            :title="`${pro.first_name} ${pro.last_name}`"
            :subtitle="pro.title_display"
            :image="pro.profile_picture || undefined"
            @view="checkProfile(pro)"
            @pro-checkout="Download(pro.id)"
            class="clickable-card"
        />

    </div>

</template>

<script lang="ts">
import contratCards from '../../cards/contratCards.vue';
import contractCardProfile from '../../cards/contractCardProfile.vue';
import proCards from '../../cards/proCards.vue'
import { useProStore} from '../../../stores/proStore';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
    components: {
        contratCards,
        contractCardProfile,
        proCards
    },

    setup() {
        const proStore = useProStore();
        const router = useRouter();

        // Actions
        async function Download(pro_id: string) {
            try {
                // 🚀 MODIFICATION ICI : On passe l'ID dans l'URL
                // Cela va rediriger vers une URL du type /contractwritter/1234-5678-...
                proStore.downloadProCard(pro_id)
                
                console.log("Navigation vers le générateur avec l'id :", contract_id);
            } catch(err: any) {
                console.warn("Un avertissement est survenu lors de la redirection", err);
            }
        }

        async function checkProfile(){

            try {

            } catch(err:any) {

            } finally {
                
            }

        }

        onMounted(() => {
            proStore.getProfessionals();
        });

        return {
            router,
            proStore,
            Download,
            checkProfile
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