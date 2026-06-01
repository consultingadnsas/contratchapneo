<template>
    <section class="main-section">
        <div class="wrapper-content">
            <h3>
                Que disent nos partenaires sur nos produits ?
            </h3>
        </div>

        <div class="w-full flex justify-center items-center flex-col">
            <div class="cards-container">
                <testimonialCards 
                    v-for="(item, index) in testimonials" 
                    :key="index"
                    :quote="item.quote"
                    :companyName="item.company"
                    :authorName="item.name"
                    :authorRole="item.role"
                    :isFeatured="index === 0" 
                />
            </div>
        </div>
    </section>
</template>

<script>
import { ref } from 'vue'
import testimonialCards from '../cards/testimonialCards.vue'

export default {
    components: { testimonialCards },
    setup() {
        const testimonials = ref([
            {
                quote: "Contratchap a révolutionné notre gestion contractuelle. La rédaction sur-mesure et l'accès aux modèles nous ont fait gagner un temps précieux. Un outil indispensable pour toute PME ambitieuse.",
                company: "TechSolutions",
                name: "Aminata Diallo",
                role: "Directrice Juridique"
            },
            {
                quote: "En tant que startup, nous avions besoin de contrats solides sans exploser notre budget. Contratchap nous a offert exactement cela : professionnalisme et simplicité.",
                company: "Green Innov",
                name: "Koffi Mensah",
                role: "CEO & Co-fondateur"
            },
            {
                quote: "Le suivi juridique personnalisé est ce qui fait la différence. L'équipe de Contratchap est réactive et comprend parfaitement les enjeux de notre secteur.",
                company: "BTP Construction",
                name: "Sophie Morel",
                role: "Responsable Administratif"
            },
            {
                quote: "Nous utilisons Contratchap depuis 6 mois et nous avons déjà réduit nos coûts juridiques de 40 %. La plateforme est intuitive et les documents sont impeccables.",
                company: "Digital Services",
                name: "Jean-Pierre Kouassi",
                role: "Fondateur"
            }
        ])

        return {
            testimonials
        }
    }
}
</script>

<style scoped>
.main-section {
    padding: 4rem 1rem;
    background-color: #f9fafb;
}

.wrapper-content h3 {
    text-align: center;
    font-size: 1.8rem;
    color: #1f2937;
    margin-bottom: 2rem;
}

.cards-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 1rem;
    padding: 0.5rem 1rem;
    width: 100%;
    scrollbar-width: thin;
}

.cards-container > * {
    flex: 0 0 85%;
    scroll-snap-align: start;
}

@media (min-width: 768px) {
    .cards-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        overflow-x: visible;
        scroll-snap-type: none;
        padding: 0;
    }

    .cards-container > * {
        flex: auto;
        scroll-snap-align: none;
    }
}
</style>