<template>
    <section class="checkout-section">
        <h2>Finalisez votre commande</h2>
        <div class="">
            <itemsListVue/>
            <checkoutFormVue/>
        </div>
    </section>
</template>

<script>
import checkoutFormVue from '../../forms/checkoutForm.vue'
import itemsListVue from '../../lists/itemsList.vue'
export default {
    name:'CheckoutSection',
    components:{
        checkoutFormVue,
        itemsListVue
    }
}
</script>

<style scoped>
.checkout-section{
    min-height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 4rem 1rem 1rem 1rem;
}
</style>