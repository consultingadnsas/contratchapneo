<template>
    <form
        class="checkout-form w-full flex flex-col gap-2"
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

        <CheckoutButton
            label="Payer"
            type="submit"
            :isLoading="cartStore.isLoading"
        />

        <p v-if="cartStore.error" class="text-red-600 text-sm mt-2">{{ cartStore.error }}</p>
    </form>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'

import BaseInput    from '../input/BaseInput.vue'
import CheckoutButton from '../buttons/checkoutButton.vue'   // renommer en PascalCase côté fichier aussi
import BaseSelect   from '../input/BaseSelect.vue'

import { useCartStore }  from '../../stores/cartStore'
import { useOrderStore } from '../../stores/orderStore'

export default {
    name: 'CheckoutForm',

    components: {
        BaseInput,
        CheckoutButton,
        BaseSelect,
    },

    props: {
        formTitle: {
            type: String,
            default: 'Confirmer votre achat',
        },
    },

    emits: ['success'],   // ✅ corrigé : 'succes' → 'success'

    setup(props, { emit }) {
        console.log('📋 [CheckoutForm] Montage du composant CheckoutForm')
        const cartStore  = useCartStore()
        const orderStore = useOrderStore()
        console.log('🛒 [CheckoutForm] CartStore:', { totalPrice: cartStore.totalPrice, totalItems: cartStore.totalItems })
        console.log('🛍️ [CheckoutForm] OrderStore:', { hasOrder: !!orderStore.currentOrder })

        // ── État du formulaire ────────────────────────────────────────────
        const checkoutform = reactive({
            full_name:      '',
            email:          '',
            phone_number:   '',
            payment_method: '',
        })

        // ── Validation basique ────────────────────────────────────────────
        const validate = () => {
            console.log('🔍 [CheckoutForm] Validation du formulaire')
            if (!checkoutform.full_name.trim()) {
                console.warn('⚠️ Le nom complet est requis.')
                return 'Le nom complet est requis.'
            }
            if (!checkoutform.email.trim()) {
                console.warn('⚠️ L\'adresse email est requise.')
                return "L'adresse email est requise."
            }
            if (!/\S+@\S+\.\S+/.test(checkoutform.email)) {
                console.warn('⚠️ L\'adresse email est invalide:', checkoutform.email)
                return "L'adresse email est invalide."
            }
            if (!checkoutform.payment_method) {
                console.warn('⚠️ Veuillez choisir un moyen de paiement.')
                return 'Veuillez choisir un moyen de paiement.'
            }
            console.log('✅ Validation réussie')
            return null
        }

        // ── Soumission ────────────────────────────────────────────────────
        const submitForm = async () => {

            // 🕵️‍♂️ LOGS DE DÉBOGAGE À AJOUTER ICI
            console.log("🔍 Contenu complet de currentOrder:", orderStore.currentOrder)
            console.log("🔍 L'ID extrait est-il valide ? :", orderStore.currentOrder?.id)

            try {
                // Envoyer au backend : uniquement les données invité requises pour le checkout
                const payload = {
                    guest: {
                        full_name:    checkoutform.full_name,
                        email:        checkoutform.email,
                        phone_number: checkoutform.phone_number || null,
                    },
                }

                const order = await orderStore.checkout(payload)
                
                if (!order?.id) {
                    console.error("❌ order.id manquant après checkout :", order)
                    return
                }

                console.log("✅ Order créé avec ID :", order.id)

                // Étape 3 : Initier le paiement avec le vrai order.id
                const paiementResponse = await cartStore.initiatePayment(
                    {
                        order_id:       order.id,           // ✅ depuis le retour direct, pas orderStore.currentOrder
                        payment_method: checkoutform.payment_method.toUpperCase() // souvent attendu en majuscules
                    },
                    checkoutform.email
                )

                emit('success', {
                    paymentMethod: checkoutform.payment_method,
                    email: checkoutform.email,
                    fullName: checkoutform.full_name,
                    phone: checkoutform.phone_number,
                    paymentUrl: paiementResponse?.payment_url || null,
                })

                // Reset
                Object.assign(checkoutform, {
                    full_name: '', email: '', phone_number: '', payment_method: '',
                })

            } catch (err) {
                console.error('Échec de la soumission :', err)
            } finally {
                console.log("Soumission terminée")
            }
        }

        return {
            cartStore,
            orderStore,
            paymentOptions: [
                { value: 'WAVE',         name: 'Wave' },
                { value: 'WAVESN',       name: 'Wave Sénégal' },
                { value: 'OMCIV2',       name: 'Orange Money' },
                { value: 'FLOOZ',        name: 'Moov Money' },
                { value: 'MOOTG',        name: 'Moov Money Togo'},
                { value: 'MOMOCM',       name: 'Mtn Money Cameroun' },
                { value: 'MOMOCI',       name: 'Mtn Money Ci'},
                { value: 'OMBF',         name: 'Orange money BF'},
                { value: 'OMML',         name: 'Orange money Mali'},
                { value: 'OMSN',         name: 'Orange money Sénégal'},
                { value: 'OMGN',         name: 'Orange money Guinée Bissau'},
                { value: 'OMCM',         name: 'Orange money Cameroun' },
                { value: 'MOMOBJ',       name: 'Mtn Money Benin'},
                { value: 'CARD',         name: 'Visa/MasterCard'},
                { value: 'FLOOZBJ',      name: 'Moov Benin'},
                { value: 'AIRTELNG',     name: 'Airtel Niger'},
            ],
            checkoutform,
            submitForm,
        }
    },
}
</script>

<style scoped>
.checkout-form {
    background:    #eef2ff;
    border-radius: 8px;
    box-shadow:    0 8px 32px 0 rgba(31, 38, 135, 0.15);
}

.checkout-form h3 {
    color: #202b4a;
}

/* Donne au CardElement Stripe un aspect cohérent avec tes BaseInput */
.stripe-card-element {
    border:        1px solid #d1d5db;
    border-radius: 6px;
    padding:       10px 12px;
    background:    #fff;
    transition:    border-color 0.2s;
}

.stripe-card-element:focus-within {
    border-color: #6366f1;
    outline:      none;
}
</style>