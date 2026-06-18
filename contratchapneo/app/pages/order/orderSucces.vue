<template>
    <div class="main-wrapper">
        <succesForm/>
        <footerSection/>
    </div>
</template>

<script>
import footerSection from '../../components/sections/footerSection.vue';
import succesForm from '../../components/forms/succesForm.vue'

export default {
    components:{
        footerSection,
        succesForm
    }
}
</script>

<style scoped>

.checkout-wrapper {
    width: 95%;
    min-height: 100vh;
    max-width: 800px;
    margin: 1rem auto;
    background: #fff;
    border-radius: 8px;
    /*  */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
</style>