<template>
    <div class="main-wrapper">
        <navbarVue/>
        <heroSecondSectionVue/>
    </div>
</template>

<script>
import navbarVue from '../components/navigation/navbar.vue'
import heroSecondSectionVue from '../components/sections/heroSecondSection.vue'

export default {
    components:{
        heroSecondSectionVue, navbarVue
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