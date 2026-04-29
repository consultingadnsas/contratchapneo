<template>

    <nav class="main-nav">
        <h3><span>Contrat</span>ChapNeo</h3>
        <Hamburger />
    </nav>

</template>

<script lang="ts">
import Hamburger from '../buttons/hamburger.vue';


export default {
    name: 'Navbar',
    components:{
        Hamburger
    }
}


</script>

<style scoped>

/* Mobile */
.main-nav{
    position: fixed;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 1rem;
    border-bottom: 1px solid var(--primary-color);
    z-index: 1000;
    background: white;
}

.main-nav h3{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 1.5rem;
    color: var(--primary-color);
    font-weight: 600;
}

.main-nav h3 span{
    color: #f3f3f3;
    background: var(--primary-color);
}
</style>