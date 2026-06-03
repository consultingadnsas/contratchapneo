<template>

    <div class="main-wrapper">
        
        <navbar theme="light"/>

        <proSection/>
        
        <!-- <mostContratViewed/> -->
        
        <footerSection/>

    </div>

</template>

<script>
import navbar from '../../components/navigation/navbar.vue'
import mostContratViewed from '../../components/sections/bankContratSections/mostContratViewed.vue'
import cardSection from '../../components/sections/bankContratSections/cardSection.vue'
import proSection from '../../components/sections/proSections/proSection.vue'
import footerSection from '../../components/sections/footerSection.vue'

export default {

    components:{
        navbar,
        mostContratViewed,
        cardSection,
        proSection,
        footerSection
    }

}
</script>

<style>

</style>