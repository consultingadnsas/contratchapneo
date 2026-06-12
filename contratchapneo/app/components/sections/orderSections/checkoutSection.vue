<template>
    
    <section class="checkout-section">
        <div class="sides" v-if="!isPaiementModale && !isXpayeModale">
            <itemsListVue/>
            <checkoutFormVue @success="handlePaiementSuccess"/>
        </div>
        <paiementModale
            :isOpen="isPaiementModale"
        />

        <XpayeModale
            :isOpen="isXpayeModale"
            :paymentMethod="selectedPaymentMethod"
            @close="isXpayeModale = false"
        />
        <succesFormVue
            v-if="isSuccess"
            message="Contrat acheté. Le Téléchargement commence maintenant"
        />
    </section>
    
</template>

<script lang="ts">
import { ref, defineAsyncComponent } from 'vue'
import checkoutFormVue from '../../forms/checkoutForm.vue'
import succesFormVue from '../../forms/succesForm.vue'
import itemsListVue from '../../lists/itemsList.vue'
import paiementModale from '../../modale/paiementModale.vue'
import { usePaiementStore } from '../../../stores/paiementStore'
import { useCartStore } from '../../../stores/cartStore'
import { useOrderStore } from '../../../stores/orderStore'
const XpayeModale = defineAsyncComponent(() => import('../../modale/XpayeModale.vue') as Promise<any>)

export default {
    name:'CheckoutSection',
    components:{
        checkoutFormVue,
        itemsListVue,
        succesFormVue,
        paiementModale,
        XpayeModale
    },
    setup(){

        // state
        const isPaiementModale = ref<boolean>(false);
        const isXpayeModale = ref<boolean>(false);
        const selectedPaymentMethod = ref<string>('');
        const isSuccess = ref<boolean>(false);

        const handlePaiementSuccess = (data: any) => {
            console.log('💳 [CheckoutSection] handlePaiementSuccess appelé avec:', data);
            const paiementStore = usePaiementStore();
            const cartStore = useCartStore();
            const orderStore = useOrderStore();

            console.log('📊 [CheckoutSection] CartStore state:', {
                totalPrice: cartStore.totalPrice,
                items: cartStore.cart?.items?.length || 0
            });
            console.log('🔑 [CheckoutSection] OrderStore state:', {
                currentOrderId: orderStore.currentOrder?.id
            });

            selectedPaymentMethod.value = data.paymentMethod;
            console.log('✓ Méthode de paiement définie:', data.paymentMethod);

            // Remplir le store paiement avec les données de la commande
            if (data.paymentMethod !== 'stripe') {
                console.log('📝 [CheckoutSection] Remplissage du paiementStore...');
                paiementStore.paiement.amount = cartStore.totalPrice;
                paiementStore.paiement.channel = data.paymentMethod;
                paiementStore.paiement.customerEmail = data.email;
                paiementStore.paiement.customerFirstName = data.fullName.split(' ')[0];
                paiementStore.paiement.customerLastname = data.fullName.split(' ').slice(1).join(' ');
                paiementStore.paiement.customerPhoneNumber = data.phone || '';
                paiementStore.paiement.referenceNumber = orderStore.currentOrder?.id || '';
                paiementStore.paiement.description = 'Achat de contrats';
                
                console.log('✅ [CheckoutSection] PaiementStore rempli:', paiementStore.paiement);
            }

            if (data.paymentMethod === 'stripe') {
                console.log('🔵 [CheckoutSection] Ouverture modale Stripe');
                isPaiementModale.value = true;
            } else {
                console.log('🟢 [CheckoutSection] Ouverture modale Xpaye');
                isXpayeModale.value = true;
            }
        };

        return{
            isPaiementModale,
            isXpayeModale,
            selectedPaymentMethod,
            isSuccess,
            handlePaiementSuccess,
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