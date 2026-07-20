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
            label="Confirmer"
            type="submit"
            :isLoading="cartStore.isLoading"
        />

        <!-- Le composant de notification injecté dans le body pour éviter les problèmes d'affichage -->
        <Teleport to="body">
            
            <BaseNotification 
                v-model:show="notify.show"
                :type="notify.type"
                :title="notify.title"
                :message="notify.message"
            />
            
        </Teleport>
    </form>
</template>

<script>
import { ref, reactive } from 'vue'

import BaseInput from '../input/BaseInput.vue'
import CheckoutButton from '../buttons/checkoutButton.vue'
import BaseSelect from '../input/BaseSelect.vue'
import BaseNotification from '../tools/baseNotification.vue' // 👈 Import du nouveau composant

import { useCartStore } from '../../stores/cartStore'
import { useOrderStore } from '../../stores/orderStore'

export default {
    name: 'CheckoutForm',

    components: {
        BaseInput,
        CheckoutButton,
        BaseSelect,
        BaseNotification // 👈 Déclaration du composant
    },

    props: {
        formTitle: {
            type: String,
            default: 'Confirmer votre achat',
        },
    },

    emits: ['success'],

    setup(props, { emit }) {
        const cartStore = useCartStore()
        const orderStore = useOrderStore()

        // ── État de la notification ───────────────────────────────────────
        const notify = ref({
            show: false,
            type: 'success',
            title: '',
            message: ''
        });

        const showNotification = (type, title, message = '') => {
            notify.value = { show: true, type, title, message };
        };

        // ── État du formulaire ────────────────────────────────────────────
        const checkoutform = reactive({
            full_name: '',
            email: '',
            phone_number: '',
            payment_method: '',
        })

        // ── Validation avec Notifications ─────────────────────────────────
        const validate = () => {
            if (!checkoutform.full_name.trim()) {
                showNotification('error', 'Champs manquant', 'Le nom complet est requis.');
                return false;
            }
            if (!checkoutform.email.trim()) {
                showNotification('error', 'Champs manquant', "L'adresse email est requise.");
                return false;
            }
            if (!/\S+@\S+\.\S+/.test(checkoutform.email)) {
                showNotification('error', 'Format invalide', "L'adresse email n'est pas valide.");
                return false;
            }
            if (!checkoutform.payment_method) {
                showNotification('error', 'Paiement', 'Veuillez choisir un moyen de paiement.');
                return false;
            }
            return true;
        }

        // ── Soumission ────────────────────────────────────────────────────
        // ── Soumission ────────────────────────────────────────────────────
        const submitForm = async () => {
            
            // 🛑 On bloque la soumission si la validation échoue
            if (!validate()) {
                return;
            }

            // 🔥 LA CORRECTION EST ICI : Enregistrement de l'email en Cookie
            // On utilise useCookie fourni par Nuxt (qui le gère automatiquement côté front et back)
            // On lui donne une durée de vie (maxAge) d'une heure (3600 secondes)
            const backupEmailCookie = useCookie('backup_checkout_email', { maxAge: 3600 });
            backupEmailCookie.value = checkoutform.email;
            console.log("💉 Email sécurisé dans le cookie avant paiement :", backupEmailCookie.value);

            try {
                const payload = {
                    guest: {
                        full_name: checkoutform.full_name,
                        email: checkoutform.email,
                        phone_number: checkoutform.phone_number || null,
                    },
                }

                const order = await orderStore.checkout(payload)
                
                if (!order?.id) {
                    showNotification('error', 'Erreur système', "Impossible de générer l'identifiant de la commande.");
                    return;
                }

                const paiementResponse = await cartStore.initiatePayment(
                    {
                        order_id: order.id,
                        payment_method: checkoutform.payment_method.toUpperCase()
                    },
                    checkoutform.email
                )

                // Envoi de l'événement de succès
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
                // ❌ Affichage de l'erreur API
                showNotification('error', 'Échec de la commande', cartStore.error || "Une erreur est survenue lors de l'initialisation du paiement.");
                console.error('Échec de la soumission :', err)
            }
        }

        return {
            cartStore,
            orderStore,
            notify, // Exposer l'état
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
    padding: 1.5rem; /* Ajout d'un peu de padding pour l'esthétique */
}

.checkout-form h3 {
    color: #202b4a;
    margin-bottom: 1rem;
}

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