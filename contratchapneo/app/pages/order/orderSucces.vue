<template>
    <div class="main-wrapper">
        <succesForm/>
        <footerSection/>
    </div>
</template>

<script>
import Navbar from '../../components/navigation/navbar.vue';
import checkoutSectionVue from '../../components/sections/orderSections/checkoutSection.vue'
import footerSection from '../../components/sections/footerSection.vue';
import succesForm from '../../components/forms/succesForm.vue'

export default {
    components:{
        Navbar,
        checkoutSectionVue,
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