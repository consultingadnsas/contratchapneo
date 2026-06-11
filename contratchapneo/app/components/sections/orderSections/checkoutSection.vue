<template>
    <section class="checkout-section">
        <div class="sides" v-if="!isSucces">
            <itemsListVue/>
            <checkoutFormVue @succes="()=>isSucces=true"/>
        </div>
        <succesFormVue
            message="Contrat acheté. Le Téléchargement commence maintenant"
            v-else
        />
        <paiementModale :isOpen="false"/>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue'
import checkoutFormVue from '../../forms/checkoutForm.vue'
import succesFormVue from '../../forms/succesForm.vue'
import itemsListVue from '../../lists/itemsList.vue'
import paiementModale from '../../modale/paiementModale.vue'

export default {
    name:'CheckoutSection',
    components:{
        checkoutFormVue,
        itemsListVue,
        succesFormVue,
        paiementModale
    },
    setup(){

        // state
        const isSucces = ref<boolean>(false)

        return{
            isSucces
        }


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
    padding: 0.5rem;
}

.checkout-section h2{
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--primary-color);
}

.sides{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

@media(min-width:1024px){

    .sides{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        justify-content: space-around;
        align-items: center;
    }

}
</style>