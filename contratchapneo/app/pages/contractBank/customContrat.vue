<template>

    <div class="main-wrapper">
        
        <navbar theme="light"/>

        <customContratSection/>
        
        <footerSection/>

    </div>

</template>

<script>
import navbar from '../../components/navigation/navbar.vue'
import cardSection from '../../components/sections/bankContratSections/cardSection.vue'
import customContratSection from '../../components/sections/bankContratSections/customContratSection.vue'
import footerSection from '../../components/sections/footerSection.vue'

export default {

    components:{
        navbar,
        cardSection,
        customContratSection,
        footerSection
    }

}
</script>

<style>

</style>