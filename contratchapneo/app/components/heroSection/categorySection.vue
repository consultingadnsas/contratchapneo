<template>
    <div class="category-section">

        <h3>
            Nos catégories de contrats
        </h3>

        <div class="cards-wrapper">
            <contratCategoryCards v-for="i in 4" :key="i"/>
        </div>

    </div>
</template>

<script>
import contratCategoryCards from '../cards/contratCategoryCards.vue'
import bankContratSection from '../sections/bankContratSection.vue'
export default {
    component:{
        contratCategoryCards
    },
    setup(){

    }
}
</script>

<style scoped>
.category-section{
    background: var(--my-white);
    width: 100%;
    min-height: 100vh;
}

.category-section h3 {
    color: var(--primary-color);
    font-size: 1.3rem;
}

.cards-wrapper{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}
</style>