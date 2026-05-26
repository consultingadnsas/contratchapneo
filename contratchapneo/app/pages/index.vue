<template>

    <div class="main-wrapper">
        
        <Navbar />

        <heroSecondSection />

        <bankContratSection />

        <companySolutions/>

        <numberGreen />

        <ProSection title-head="Les professionnels du droits"/>

        <calcul-tool-section/>

        <companieSection />

        <footer-section/>

    </div>
    
</template>

<script lang="ts">
import Navbar from '../components/navigation/navbar.vue';
import heroSecondSection from '../components/sections/heroSecondSection.vue';
import bankContratSection from '../components/sections/bankContratSection.vue';
import companySolutions from '../components/sections/companySolutions.vue';
import ProSection from '../components/sections/proSection.vue';
import calculToolSection from '../components/sections/calculToolSection.vue';
import companieSection from '../components/sections/companieSection.vue';
import numberGreen from '../components/sections/numberGreen.vue';
import FooterSection from '../components/sections/footerSection.vue';

import {ref} from 'vue'

export default {
    name: 'HomePage',
    components:{
        Navbar,
        companieSection,
        bankContratSection,
        ProSection,
        calculToolSection,
        heroSecondSection,
        FooterSection,
        companySolutions,
        numberGreen
    },
    setup() {

        // state

        
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