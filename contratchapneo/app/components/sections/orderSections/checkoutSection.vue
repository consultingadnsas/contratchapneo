<template>
    <section class="checkout-section">
        <h2>Finalisez votre commande</h2>
        <checkoutFormVue/>
    </section>
</template>

<script>
import checkoutFormVue from '../../forms/checkoutForm.vue'
export default {
    name:'CheckoutSection',
    components:{
        checkoutFormVue
    }
}
</script>

<style scoped>
.checkout-section{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 4rem 1rem 1rem 1rem;
}
</style>