<template>
    <!-- On désactive le bouton s'il est en train de charger -->
    <button class="main-button" :disabled="isLoading">
        
        <!-- ⚡️ CORRECTION : S'il NE charge PAS (!isLoading), on met le texte normal -->
        <template v-if="!isLoading">
            {{ label }}
            <span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                </svg>
            </span>
        </template>

        <!-- ⚡️ CORRECTION : S'il charge, on met le spinner -->
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
            // ⚡️ CORRECTION : Par défaut, un bouton ne charge pas
            default: false
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
    align-items: center; /* Ajout pour bien centrer le spinner et le texte */
    justify-content: center; /* Ajout pour bien centrer le spinner et le texte */
}

.main-button:hover:not(:disabled){
    background: #135b8f;
    transition: all 0.3s;
}

/* Style quand le bouton est désactivé (pendant le chargement) */
.main-button:disabled {
    cursor: not-allowed;
    opacity: 0.8;
}

@media (max-width: 768px) {
    .main-button {
        width: 100%;
    }
}
@media (max-width: 1280px) {
    .main-button {
        width: 280px;
    }
}
</style>