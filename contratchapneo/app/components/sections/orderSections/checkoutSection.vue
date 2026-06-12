<template>
    
    <section class="checkout-section">
        <div class="sides" v-if="!isPaiementModale">
            <itemsListVue/>
            <checkoutFormVue @success="()=>isPaiementModale=true"/>
        </div>
        <paiementModale
            :isOpen="isPaiementModale"
        />
        <succesFormVue
            v-if="isSuccess"
            message="Contrat acheté. Le Téléchargement commence maintenant"
        />
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
        const isPaiementModale = ref<boolean>(false);
        const isSuccess = ref<boolean>(false);

        return{
            isPaiementModale,
            isSuccess
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