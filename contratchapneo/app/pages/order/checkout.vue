<template>
    <div class="main-wrapper">
        <div class="checkout-wrapper">
            <checkoutSectionVue/>
        </div>
        <footerSection/>
    </div>
</template>

<script>
import Navbar from '../../components/navigation/navbar.vue';
import checkoutSectionVue from '../../components/sections/orderSections/checkoutSection.vue'
import footerSection from '../../components/sections/footerSection.vue';
export default {
    components:{
        Navbar,
        checkoutSectionVue,
        footerSection
    }
}
</script>

<style scoped>
.main-wrapper {
    background: radial-gradient(circle, #202b4a 30%, #0f0f0f 100%);
}

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