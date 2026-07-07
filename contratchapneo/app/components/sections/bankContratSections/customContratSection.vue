<template>
    <div class="contrat-card-section">

        <div class="form-container">
            <customContratForm/>
        </div>
        
        <div class="image-container">
            <img src="/custom.jpg" alt="Illustration contrat">
        </div>

    </div>
</template>

<script lang="ts">
import contratCards from '../../cards/contratCards.vue'
import customContratForm from '../../forms/customContratForm.vue'
import { ref } from 'vue'

export default {
    components: {
        contratCards,
        customContratForm
    },
    setup() {
        const legalContrat = ref([
            { title: 'Contrat de travail' , subtitle: '100% Gratuit', description: 'Un contrat de travail est un accord entre un employeur et son employé.'},
            { title: 'Contrat de freelance', subtitle: '15 000 FCFA', description: 'Un contrat de freelance est un accord entre un travailleur indépendant et un client.'},
            { title: 'contrat de vente', subtitle: '40 000 FCFA', description: 'Un contrat de vente est un accord entre un vendeur et un acheteur.'},
            { title: 'contrat de bail', subtitle: '5 000 FCFA', description: 'Un contrat de bail est un accord entre un propriétaire et un locataire.'},
            { title: 'Contrat de travail' , subtitle: '100% Gratuit', description: 'Un contrat de travail est un accord entre un employeur et son employé.'},
            { title: 'Contrat de freelance', subtitle: '15 000 FCFA', description: 'Un contrat de freelance est un accord entre un travailleur indépendant et un client.'},
            { title: 'contrat de vente', subtitle: '40 000 FCFA', description: 'Un contrat de vente est un accord entre un vendeur et un acheteur.'},
            { title: 'contrat de bail', subtitle: '5 000 FCFA', description: 'Un contrat de bail est un accord entre un propriétaire et un locataire.'},
        ]);

        return {
            legalContrat
        }
    }
}
</script>

<style scoped>
/* ==========================================
    CONTENEUR PRINCIPAL
========================================== */
.contrat-card-section {
    width: 100%;
    max-width: 1400px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    padding: 6rem 1rem 1rem 1rem;
    background: #FDFCFC;
}

.contrat-card-section h2 {
    font-size: 2rem;
    font-weight: 500;
    line-height: 1.5;
    color: var(--primary-color);
}

header {
    margin-top: 2rem;
    margin-bottom: 1rem;
}

header p {
    font-size: 1.2rem;
}

/* ==========================================
    GESTION FORMULAIRE & IMAGE
========================================== */
.form-container {
    width: 100%;
}

.image-container {
    display: none; /* Masqué par défaut sur mobile et tablette */
    width: 100%;
    justify-content: center;
    align-items: center;
    padding: 0.5rem;
}

.image-container img {
    width: 100%;
    height: auto;
    /*max-height: 600px;*/
    object-fit: cover;
    border-radius: 8px; /* Optionnel: adoucit les angles de l'image */
}

/* ==========================================
    TOOLBAR : filtre + recherche
========================================== */
.toolbar {
    width: 100%;
    max-width: 1200px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    gap: 0.75rem;
    padding: 0.5rem;
}

.toolbar__filter {
    min-width: 0;
    margin: 0;
}

.toolbar__search {
    flex: 0 0 auto;
}

:deep(.search-container.is-mobile.is-expanded) {
    width: auto;
    flex: 1 1 auto;
    min-width: 0;
}

/* ==========================================
    TABLETTE (>= 768px)
========================================== */
@media (min-width: 768px) {
    .toolbar__search {
        max-width: 360px;
        margin-left: auto;
    }
}

/* ==========================================
    LAPTOP / DESKTOP (>= 1024px)
========================================== */
@media (min-width: 1024px) {
    .contrat-card-section {
        display: grid;
        grid-template-columns: 1fr 1fr; /* Formulaire à gauche, image à droite */
        align-items: start; /* Aligne le haut des deux blocs */
        gap: 2rem;
    }

    .image-container {
        display: flex; /* L'image s'affiche enfin sur laptop */
    }

    .cards-container {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* ==========================================
    GRAND ÉCRAN (>= 1300px)
========================================== */
@media (min-width: 1300px) {
    .cards-container {
        grid-template-columns: repeat(4, 1fr);
    }
}
</style>