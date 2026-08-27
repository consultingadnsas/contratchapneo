<template>
    
    <section class="checkout-section">
        <div class="sides" v-if="!isXpayeModale">
            <itemsListVue :isCheckout="true"/>
            <checkoutFormVue 
                :formTitle="dynamicFormTitle" 
                @success="handlePaiementSuccess"
            />
        </div>
        <XpaySandBoxe 
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
import { ref, computed ,defineAsyncComponent } from 'vue'
import checkoutFormVue from '../../forms/checkoutForm.vue'
import succesFormVue from '../../forms/succesForm.vue'
import itemsListVue from '../../lists/itemsList.vue'
import { usePaiementStore } from '../../../stores/paiementStore'
import { useCartStore } from '../../../stores/cartStore'
import { useOrderStore } from '../../../stores/orderStore'
const XpaySandBoxe = defineAsyncComponent(()=>import('../../modale/XpaySandBoxe.vue'))

export default {
    name:'CheckoutSection',
    components:{
        checkoutFormVue,
        itemsListVue,
        succesFormVue,
        XpaySandBoxe
    },
    setup(){

        // state
        const isXpayeModale = ref<boolean>(false);
        const selectedPaymentMethod = ref<string>('');
        const isSuccess = ref<boolean>(false);
        const cartStore = useCartStore();

        // ⚡️ LOGIQUE DYNAMIQUE POUR LE TITRE
        const dynamicFormTitle = computed(() => {
            const items = cartStore.cart?.items || [];
            
            // Vérifie s'il y a au moins un élément dans le panier qui possède
            // soit la propriété `pro`, soit la propriété `packs` (c'est-à-dire un service).
            const hasService = items.some((item) => item.pro != null || item.packs != null);

            if (hasService) {
                return "Confirmer votre transaction";
            }
            return "Confirmer votre achat"; // Valeur par défaut pour les contrats
        });

        const handlePaiementSuccess = (data: any) => {
            console.log('💳 [CheckoutSection] handlePaiementSuccess appelé avec:', data);
            const paiementStore = usePaiementStore();
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
            console.log('📝 [CheckoutSection] Remplissage du paiementStore...');
            paiementStore.paiement = {
                amount: cartStore.totalPrice,
                channel: data.paymentMethod,
                customerEmail: data.email,
                customerFirstName: data.fullName.split(' ')[0],
                customerLastname: data.fullName.split(' ').slice(1).join(' '),
                customerPhoneNumber: data.phone || '',
                referenceNumber: orderStore.currentOrder?.id || '',
                description: 'Achat de contrats'
            };
            console.log('✅ [CheckoutSection] PaiementStore rempli:', paiementStore.paiement);

            if (data.paymentUrl) {
                console.log('🔗 [CheckoutSection] Redirection vers sandbox de paiement:', data.paymentUrl);
                window.location.href = data.paymentUrl;
                return;
            }

            console.log('🟢 [CheckoutSection] Ouverture modale Xpaye');
            isXpayeModale.value = true;
        };

        const handlePaymentConfirmed = () => {
            console.log('✅ [CheckoutSection] Paiement confirmé, affichage de l\'écran de succès');
            isSuccess.value = true;
            isXpayeModale.value = false;
        }

        return{
            isXpayeModale,
            selectedPaymentMethod,
            isSuccess,
            dynamicFormTitle,
            handlePaiementSuccess,
            handlePaymentConfirmed,
            
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