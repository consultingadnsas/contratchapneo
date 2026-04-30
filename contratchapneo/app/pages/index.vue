<template>

    <div class="main-wrapper">
        
        <Navbar />
        
        <HeroSection />

        <companieSection />

        <ordinarySection />

        <bankContratSection />

        <ProSection title-head="Les professionnels du droits"/>

        

    </div>
    
</template>

<script lang="ts">
import Navbar from '~/components/navigation/navbar.vue';
import HeroSection from '~/components/sections/heroSection.vue';
import companieSection from '~/components/sections/companieSection.vue';
import ordinarySection from '~/components/sections/ordinarySection.vue';
import bankContratSection from '~/components/sections/bankContratSection.vue';
import ProSection from '~/components/sections/proSection.vue';


export default {
    name: 'HomePage',
    components:{
        Navbar,
        HeroSection,
        companieSection,
        ordinarySection,
        bankContratSection,
        ProSection
    }
}

</script>

<style scoped>
/* Mobile first */

.hero-section{
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 1rem;
}

.hero-section h1{
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    width: 100%;
    text-align: start;
    padding: 1rem;
}

.hero-section h1 span{
    color: var(--primary-color);
    font-weight: 700;
}

</style>