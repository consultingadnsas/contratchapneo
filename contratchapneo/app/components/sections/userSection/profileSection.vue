<template>
    
    <section class="">

        <contractCardSkeleton v-if="false"/>

        <emptyState 
            title="Aucun pack acheté"
            description="Vous n'avez aucun pack disponible"
            textAction="Acheter pack"
        />

    </section>

</template>

<script lang="ts">
import { useProfileStore } from '../../../stores/profileStore'
import {ref, onMounted} from 'vue'

import contractCardSkeleton from '../../cards/contractCardSkeleton.vue';
import emptyState from '../../tools/emptyState.vue'

export default{

    components:{
        contractCardSkeleton,
        emptyState
    },

    setup(){

        const profileStore = useProfileStore();

        onMounted(async()=>{

            profileStore.getPacks();

        })

        return {

            profileStore,
        }

    }

}
</script>

<style scoped>

</style>