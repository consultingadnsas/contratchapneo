<template>

    <button class="main-button">
        {{ label }}

    </button>

</template>

<script lang="ts">
export default {
    name:'mainButton',
    props:{
        label:{
            type:String,
            default:'Télécharger vos contrats'
        }
    }
}
</script>

<style scoped>

.main-button{
    background-color: var(--primary-color);
    color: white;
    display: flex;
    gap: 1rem;
    cursor: pointer;
}

</style>