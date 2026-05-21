<template>

    <button class="main-button" @click="handleClick">
        
        <template v-if="!isLoading">
            {{ label }}
        </template>

        <template v-else>
            <span class="loading loading-spinner loading-md"></span>
        </template>

    </button>

</template>

<script lang="ts">
export default {
    name:'mainButton',
    emits:['click','handleClicked'],
    props:{
        label:{
            type:String,
            default:'Payer mon contrat'
        },
        isLoading:{
            type: Boolean,
            default: false
        }
    },
    methods: {
        handleClick(event: Event) {
            this.$emit('click', event);
            this.$emit('handleClicked', event);
        }
    }
}
</script>

<style scoped>

.main-button{
    background-color: var(--primary-color);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    cursor: pointer;
    padding: 0.9rem;
}

</style>