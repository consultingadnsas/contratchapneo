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
                quote: "Voulez-vous savoir si je trouve utile ou correcte le pack juridique ? Je dirai oui, Dans toutes les activités avec des humains il faut un contrat et les vôtres sont bien rédigés. Après il y a des détails du contrat que vous ne pouvez pas deviner donc il revient aux concernés de les ajouter. Pour ma part, tout y est. Vos modeles passent en tout cas.",
                company: "O'Mouton Roz",
                name: "M. Amara BAMBA",
                role: "CEO"
            },
            {
                quote: "Je suis tres satisfait du pack de documents juridiques. J'ai utilisé deux modèles de contrat : le contrat à durée indéterminée et le contrat dapporteur d'affaires. Ils étaient clairs et faciles à comprendre, ce qui m'a permis de les utiliser immédiatement. Merci pour cette excellente ressource qui me fait gagner du temps. Je recommande vivement et vous remercie pour votre excellent travail.",
                company: "INTERPRET-CITY",
                name: "M. Ibrahim DOUMBIA",
                role: "Gérant"
            },
            {
                quote: "Je tiens à vous remercier pour le pack de documents juridiques, Ça m'apporte de l'aide dans mes différents partenariats avec les usines chinoises et malaisiennes Le pack nous a fait gagner du temps et a rendu notre activité plus professionnelle Je suis satisfait à 100% . Encore merci à vous.",
                company: "Word Transit et services",
                name: "David BOUDA",
                role: "Gérant"
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