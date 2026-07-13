<template>
    <section class="main-section">

    </section>
</template>

<script lang="ts">
import { useProfileStore } from '../../../stores/profileStore'
import {ref, onMounted} from 'vue'

export default{

    setup(){

        const profileStore = useProfileStore();

        /*onMounted(async()=>{

            profileStore.getProfile();

        })*/

        return {

            profileStore,
        }

    }

}
</script>