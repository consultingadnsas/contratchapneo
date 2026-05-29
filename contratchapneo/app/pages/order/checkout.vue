<template>
    <div class="main-wrapper">
        <Navbar theme="light"/>
        <checkoutSectionVue/>
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

<style>

</style>