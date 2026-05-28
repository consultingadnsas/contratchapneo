<template>

    <div class="main-wrapper">
        
        <navbar/>

        <companySolutions/>

        <footerSection/>

    </div>

</template>

<script>
import navbar from '../../components/navigation/navbar.vue'
import companySolutions from '../../components/sections/companySolutions.vue'
import footerSection from '../../components/sections/footerSection.vue'

export default {

    components:{
        navbar,
        footerSection,
        companySolutions
    }

}
</script>

<style>

</style>