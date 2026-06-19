<template>

    <div class="main-wrapper">
        
        <navbar/>

        <cardSection/>
        
        <!-- <mostContratViewed/> -->
        
        <footerSection/>

    </div>

</template>

<script>
import navbar from '../../components/navigation/navbar.vue'
import mostContratViewed from '../../components/sections/bankContratSections/mostContratViewed.vue'
import cardSection from '../../components/sections/bankContratSections/cardSection.vue'
import footerSection from '../../components/sections/footerSection.vue'

export default {

    components:{
        navbar,
        mostContratViewed,
        cardSection,
        footerSection
    }

}
</script>

<style>

</style>