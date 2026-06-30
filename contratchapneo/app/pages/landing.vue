<template>
    <div class="main-wrapper">
        <navbar/>
        <heroSecondSection/>
        <bankContratSection />
        <companieSection/>
    </div>
</template>

<script>
import categorySection from '../components/heroSection/categorySection.vue'
import navbar from '../components/navigation/navbar.vue'
import companieSection from '../components/sections/companieSection.vue'
import heroSecondSection from '../components/sections/heroSecondSection.vue'
import bankContratSection from '../components/sections/bankContratSection.vue'

export default {
    components:{
        navbar,
        heroSecondSection,
        bankContratSection,
        companieSection,
        categorySection
    }
}
</script>

<style scoped>
.main-wrapper {
    width: 100%;
    overflow-x: hidden; /* évite le scroll horizontal global */
    box-sizing: border-box;
}
</style>