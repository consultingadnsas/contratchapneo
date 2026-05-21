<template>
    <div class="view-modale">
        <div class="modal-content">
        <button class="close-btn" @click="$emit('close')">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
        <h2 class="modal-title">Contrat de travail CDD</h2>
        <p class="modal-subtitle">Détails du contrat</p>
        <div class="modal-body">
            <p><strong>Parties :</strong> Employeur : ABC Entreprise, Employé : Jean Dupont</p>
            <p><strong>Durée :</strong> 6 mois (du 1er juillet 2024 au 31 décembre 2024)</p>
            <p><strong>Rémunération :</strong> 500 000 FCFA par mois</p>
            <p><strong>Description :</strong> Ce contrat de travail à durée déterminée (CDD) est conclu entre ABC Entreprise et Jean Dupont pour une période de six mois. Le contrat précise les obligations de l'employeur et de l'employé, ainsi que les conditions de travail, la rémunération et les modalités de résiliation.</p>
        </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ViewModale',
    components: { },
    props: {
        isViewOpen: {
            type: Boolean,
            default: false
        }
    },
    emits: ['close'],
    setup(props, { emit }) {
        // Aucune logique spécifique pour l'instant, mais tu peux ajouter des méthodes ou des données ici si nécessaire
        return {};
    }

}
</script>

<style>
.view-modale {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
.modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    position: relative;
}
.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    cursor: pointer;
}

</style>