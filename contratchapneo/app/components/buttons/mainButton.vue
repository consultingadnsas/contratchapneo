<template>

    <button class="main-button">
        
        <template v-if="isLoading">
            {{ label }}
            <span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
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
    props:{
        label:{
            type:String,
            default:'Télécharger vos contrats'
        },
        isLoading:{
            type:Boolean,
            default: true
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
    width: 100%;
    transition: all ease 0.2s;
}

.main-button:hover{
    background: #135b8f;
    transition: all 0.3s;
}

@media (max-width: 768px) {
    .main-button {
        width: 100%;
        justify-content: center;
    }
}
@media (max-width: 1280px) {
    .main-button {
        width: 280px;
        justify-content: center;
    }
}

</style>