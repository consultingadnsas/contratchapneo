<template>
    <section class="custom-contrat">

        <add-button 
            v-if="!isVisible"
            @click="setIsVisible"
        />

        <pack-custom-contract 
            v-else
        />

    </section>
</template>

<script>
import {ref} from 'vue'
import addButton from '../../buttons/addButton.vue'
import packCustomContract from '../../forms/packCustomContract.vue'

export default {

    components:{
        addButton,
        packCustomContract
    },

    setup(){

        const isVisible = ref(false);

        const setIsVisible = ()=>{
            if( isVisible.value === false ){
                isVisible.value = true;
            } else{
                isVisible.value = false;
            }
        }


        return {
            isVisible,
            setIsVisible
        }

    }

}
</script>

<style scoped>
.custom-contrat{

    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>