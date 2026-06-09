<template>
    <form 
        class="w-full flex flex-col gap-2"
        @submit.prevent="submitForm"
    >

        <h3>{{ formTitle }}</h3>

        <BaseInput 
            label="Nom complet" 
            name="full_name" 
            type="text" 
            placeholder="Entrez votre nom"
            v-model="checkoutform.full_name"
        />
        <BaseInput 
            label="Email" 
            name="email" 
            type="email" 
            placeholder="Entrez votre adresse email"
            v-model="checkoutform.email"
        />
        <BaseInput 
            label="Numéro de téléphone" 
            name="phone_number" 
            type="tel" 
            placeholder="Entrez votre numéro de téléphone"
            v-model="checkoutform.phone_number"
        />

        <BaseSelect 
            label="Sélectionner votre moyen de paiement"
            v-model="checkoutform.payment_method"
            :options="paymentOptions"
            placeholder="Choisissez un moyen de paiement"
        />

        <checkoutButton 
            label="Commander" 
            type="submit"
            :isLoading="loading"
        />

        <p v-if="error" class="text-red-600 text-sm mt-2">{{ error }}</p>
    </form>
</template>

<script>
import BaseInput from '../input/BaseInput.vue'
import checkoutButton from '../buttons/checkoutButton.vue'
import BaseSelect from '../input/BaseSelect.vue'

import { ref, reactive } from 'vue'
import { useCartStore } from '../../stores/cartStore';
import { useOrderStore } from '../../stores/orderStore';

export default {
    components:{
        BaseInput,
        checkoutButton,
        BaseSelect
    },
    props:{
        formTitle:{
            type:String,
            default: 'Confirmer votre achat'
        }
    },
    emits:['succes'],
    setup(props, {emit}){

        const cartStore = useCartStore();
        const orderStore = useOrderStore();

        const checkoutform = reactive(
            {
                full_name: "",
                email: "",
                phone_number: "",
                payment_method: ''
            }
        )

        const loading = ref(false)
        
        const error = ref(null)

        const paymentOptions = [
            { value: 'wave', name: 'Wave' },
            { value: 'orange_money', name: 'Orange Money' },
            { value: 'moov_money', name: 'Moov Money' }
        ];

        const submitForm = async () => {
            loading.value = true
            error.value = null

            try {
                const payload = {
                    guest: {
                        full_name: checkoutform.full_name,
                        email: checkoutform.email,
                        phone_number: checkoutform.phone_number || null,
                    }
                };

                await orderStore.checkout(payload);
                await cartStore.fetchCart();

                emit('succes')

                checkoutform.full_name = "";
                checkoutform.email = "";
                checkoutform.phone_number = "";
                checkoutform.payment_method = '';
            } catch (err) {
                error.value = err?.message ?? err
                console.error("Échec de la soumission :", err)
            } finally {
                loading.value = false
            }
        }

        return{
            cartStore,
            orderStore,
            checkoutform,
            loading,
            error,
            submitForm
        }

    }
}
</script>

<style>

</style>