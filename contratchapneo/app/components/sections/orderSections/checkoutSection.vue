<template>
    <section class="checkout-section">
        <h2>Finalisez votre commande</h2>
        <div class="sides" v-if="!isSucces">
            <itemsListVue/>
            <checkoutFormVue @succes="()=>isSucces=true"/>
        </div>
        <succesFormVue
            message="Contrat acheté. Le Téléchargement commence maintenant"
            v-else
        />
    </section>
</template>

<script lang="ts">
import { ref } from 'vue'
import checkoutFormVue from '../../forms/checkoutForm.vue'
import succesFormVue from '../../forms/succesForm.vue'
import itemsListVue from '../../lists/itemsList.vue'

export default {
    name:'CheckoutSection',
    components:{
        checkoutFormVue,
        itemsListVue,
        succesFormVue
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
    padding: 3rem 1rem 1rem 1rem;
}

.sides{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

@media(min-width:1024px){

    .sides{
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
    }

}
</style>