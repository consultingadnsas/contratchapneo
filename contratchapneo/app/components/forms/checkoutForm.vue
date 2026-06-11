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

        <!-- Section Stripe : on utilise CardElement, jamais des inputs manuels -->
        <div
            v-if="checkoutform.payment_method === 'stripe'"
            class="stripe-section w-full flex flex-col gap-2"
        >
            <label class="text-sm font-medium text-gray-700">
                Informations de carte bancaire
            </label>

            <!--
                Stripe monte son CardElement ici.
                NE PAS remplacer par des <BaseInput> — les données
                ne doivent jamais transiter par ton code.
            -->
            <div
                id="card-element"
                class="stripe-card-element"
            />

            <p v-if="stripeError" class="text-red-500 text-sm">
                {{ stripeError }}
            </p>
        </div>

        <CheckoutButton
            label="Payer"
            type="submit"
            :isLoading="loading"
        />

        <p v-if="error" class="text-red-600 text-sm mt-2">{{ error }}</p>
    </form>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { loadStripe } from '@stripe/stripe-js'

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
        const cartStore  = useCartStore()
        const orderStore = useOrderStore()

        // ── État du formulaire ────────────────────────────────────────────
        const checkoutform = reactive({
            full_name:      '',
            email:          '',
            phone_number:   '',
            payment_method: '',
        })

        const loading     = ref(false)
        const error       = ref(null)
        const stripeError = ref(null)   // erreurs spécifiques au CardElement

        // ── Instances Stripe ──────────────────────────────────────────────
        let stripe      = null
        let cardElement = null

        // Monte le CardElement quand l'utilisateur sélectionne Stripe
        const mountCardElement = async () => {
            // loadStripe est mis en cache automatiquement — un seul chargement
            stripe = await loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

            const elements = stripe.elements()
            cardElement = elements.create('card', {
                style: {
                    base: {
                        fontSize:    '16px',
                        color:       '#202b4a',
                        fontFamily:  'inherit',
                        '::placeholder': { color: '#9ca3af' },
                    },
                    invalid: { color: '#dc2626' },
                },
                hidePostalCode: true,
            })

            cardElement.mount('#card-element')

            // Affiche les erreurs de saisie en temps réel
            cardElement.on('change', (event) => {
                stripeError.value = event.error ? event.error.message : null
            })
        }

        // Monte/démonte le CardElement selon le moyen de paiement choisi
        watch(
            () => checkoutform.payment_method,
            async (method) => {
                if (method === 'stripe') {
                    // nextTick pour laisser Vue afficher le div #card-element
                    await new Promise((r) => setTimeout(r, 50))
                    await mountCardElement()
                } else if (cardElement) {
                    cardElement.destroy()
                    cardElement = null
                }
            },
        )

        // ── Validation basique ────────────────────────────────────────────
        const validate = () => {
            if (!checkoutform.full_name.trim())      return 'Le nom complet est requis.'
            if (!checkoutform.email.trim())           return "L'adresse email est requise."
            if (!/\S+@\S+\.\S+/.test(checkoutform.email)) return "L'adresse email est invalide."
            if (!checkoutform.payment_method)         return 'Veuillez choisir un moyen de paiement.'
            return null
        }

        // ── Soumission ────────────────────────────────────────────────────
        const submitForm = async () => {
            error.value       = null
            stripeError.value = null

            const validationError = validate()
            if (validationError) {
                error.value = validationError
                return
            }

            loading.value = true

            try {
                let paymentMethodId = null

                // Flux Stripe : créer un PaymentMethod depuis le CardElement
                if (checkoutform.payment_method === 'stripe') {
                    const { paymentMethod, error: stripeErr } =
                        await stripe.createPaymentMethod({
                            type: 'card',
                            card: cardElement,
                            billing_details: {
                                name:  checkoutform.full_name,
                                email: checkoutform.email,
                                phone: checkoutform.phone_number || undefined,
                            },
                        })

                    if (stripeErr) {
                        // Erreur retournée par Stripe (carte refusée, numéro invalide…)
                        stripeError.value = stripeErr.message
                        return
                    }

                    paymentMethodId = paymentMethod.id
                }

                // Envoyer au backend : payload complet incluant le moyen de paiement
                const payload = {
                    guest: {
                        full_name:    checkoutform.full_name,
                        email:        checkoutform.email,
                        phone_number: checkoutform.phone_number || null,
                    },
                    payment_method:    checkoutform.payment_method,
                    // Pour Stripe : le backend utilise cet ID pour créer/confirmer le PaymentIntent
                    stripe_payment_method_id: paymentMethodId,
                }

                await orderStore.checkout(payload)
                await cartStore.fetchCart()

                emit('success')   // ✅ corrigé

                // Reset
                Object.assign(checkoutform, {
                    full_name: '', email: '', phone_number: '', payment_method: '',
                })

            } catch (err) {
                error.value = err?.message ?? String(err)
                console.error('Échec de la soumission :', err)
            } finally {
                loading.value = false
            }
        }

        return {
            cartStore,
            orderStore,
            paymentOptions: [
                { value: 'wave',         name: 'Wave' },
                { value: 'orange_money', name: 'Orange Money' },
                { value: 'moov_money',   name: 'Moov Money' },
                { value: 'stripe',       name: 'Carte Bancaire (Stripe)' },
            ],
            checkoutform,
            loading,
            error,
            stripeError,
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