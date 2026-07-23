<template>

    <button class="main-button" @click="handleClick">
        
        <template v-if="!isLoading">
            {{ label }}
        
            <span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
            </span>
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
            default:'Contrat sur mesure'
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
    background-color: #34477a;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    cursor: pointer;
    padding: 0.9rem;
    border-radius: 0.5rem;
    width: 100%;
    max-width: 250px;
    transition: all 0.4s;
}

.main-button:hover{
    background-color: #253257;
    transition: all 0.3s;
    transform: translateY(-4px);
}

</style>