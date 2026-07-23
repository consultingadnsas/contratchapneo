<template>
    <section class="custom-contrat">

        <add-button/>

    </section>
</template>

<script>
import addButton from '../../buttons/addButton.vue'
export default {

    components:{
        addButton
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