<template>
    <div v-if="isOpen" class="glass-modal-overlay" @click.self="closeModal">

        <div class="kkiapay-modal-content">
            <button class="close-btn" @click="closeModal" aria-label="Fermer">x</button>
            <h3>Formulaire de Paiement</h3>
            <p v-if="isSandbox" class="sandbox-badge">
                Mode sandbox activé — test uniquement
            </p>
            <p v-if="paymentMethod" class="payment-method-label">
                Mode de paiement : {{ paymentMethodLabel }}
            </p>

            <!-- Affichage des données de paiement -->
            <div class="payment-info">
                <div class="info-group">
                    <label>Montant :</label>
                    <p class="info-value">{{ paiementStore.paiement.amount.toLocaleString('fr-FR') }} FCFA</p>
                </div>
                <div class="info-group">
                    <label>Email :</label>
                    <p class="info-value">{{ paiementStore.paiement.customerEmail }}</p>
                </div>
                <div class="info-group">
                    <label>Nom :</label>
                    <p class="info-value">{{ paiementStore.paiement.customerFirstName }} {{ paiementStore.paiement.customerLastname }}</p>
                </div>
                <div class="info-group" v-if="paiementStore.paiement.customerPhoneNumber">
                    <label>Téléphone :</label>
                    <p class="info-value">{{ paiementStore.paiement.customerPhoneNumber }}</p>
                </div>
            </div>

            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>

            <button
                class="pay-button"
                :disabled="loading"
                @click="lancerPaiement"
            >
                <span v-if="loading">Initialisation...</span>
                <span v-else>Confirmer et Payer {{ paiementStore.paiement.amount.toLocaleString('fr-FR') }} FCFA</span>
            </button>
        </div>

    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { usePaiementStore } from '../../stores/paiementStore'

// Déclaration du type global pour éviter les erreurs TypeScript
declare global {
    class PaiementPro {
        amount: number
        channel: string
        referenceNumber: string
        customerEmail: string
        customerFirstName: string
        customerLastname: string
        customerPhoneNumber: string
        description: string
        notificationURL?: string
        returnURL?: string
        returnContext?: string
        success: boolean
        url: string
        error: string
        constructor(merchantId: string)
        getUrlPayment(): Promise<void>
    }
}

export default defineComponent({
    name: 'XpayeModale',
    props: {
        isOpen: { type: Boolean, default: false },
        paymentMethod: { type: String, default: '' },
    },
    emits: ['close'],
    setup(props, { emit }) {
        const paiementStore = usePaiementStore()
        const loading = ref(false)
        const errorMessage = ref('')
        const scriptPret = ref(false)

        const isSandbox = computed(() => paiementStore.sandboxMode)

        function mapPaymentChannel(method: string) {
            switch (method) {
                case 'wave':
                    return 'WAVECI'
                case 'orange_money':
                    return 'OMCIV2'
                case 'moov_money':
                    return 'FLOOZ'
                case 'card':
                case 'stripe':
                    return 'CARD'
                default:
                    return method.toUpperCase()
            }
        }

        onMounted(() => {
            console.log('🟢 [XpayeModale] Montage du composant');
            console.log('Props reçues:', { isOpen: props.isOpen, paymentMethod: props.paymentMethod });
            console.log('PaiementStore:', paiementStore.paiement);
            console.log('Sandbox actif:', isSandbox.value);
            
            if (typeof PaiementPro !== 'undefined') {
                console.log('✅ [XpayeModale] Script PaiementPro déjà disponible');
                scriptPret.value = true
                return
            }

            console.log('📥 [XpayeModale] Chargement du script PaiementPro...');
            const script = document.createElement('script')
            //https://sandbox.paiementpro.net/webservice/onlinepayment/init/curl-init.php
            script.src = 'https://www.paiementpro.net/webservice/onlinepayment/js/paiementpro.v1.0.2.js'
            script.async = true
            script.onload = () => {
                console.log('✅ [XpayeModale] Script PaiementPro chargé');
                scriptPret.value = true
            }
            script.onerror = () => {
                console.error('❌ [XpayeModale] Erreur lors du chargement du script PaiementPro');
                errorMessage.value = 'Impossible de charger le script PaiementPro.'
            }
            document.head.appendChild(script)
        })

        function attendreScript(timeout = 10000): Promise<void> {
            console.log('⏳ [XpayeModale] Attente du script PaiementPro (timeout:', timeout, 'ms)');
            return new Promise((resolve, reject) => {
                if (typeof PaiementPro !== 'undefined') {
                    console.log('✅ [XpayeModale] PaiementPro disponible immédiatement');
                    return resolve()
                }

                const debut = Date.now()
                const intervalle = setInterval(() => {
                    if (typeof PaiementPro !== 'undefined') {
                        clearInterval(intervalle)
                        console.log('✅ [XpayeModale] PaiementPro disponible après', Date.now() - debut, 'ms');
                        resolve()
                    } else if (Date.now() - debut > timeout) {
                        clearInterval(intervalle)
                        console.error('❌ [XpayeModale] Timeout: Le script PaiementPro n\'a pas pu se charger.');
                        reject(new Error('Le script PaiementPro n\'a pas pu se charger.'))
                    }
                }, 100)
            })
        }

        function closeModal() {
            emit('close')
        }

        const paymentMethodLabel = computed(() => {
            switch (props.paymentMethod) {
                case 'wave': return 'Wave'
                case 'orange_money': return 'Orange Money'
                case 'moov_money': return 'Moov Money'
                case 'stripe': return 'Carte bancaire'
                default: return 'Inconnu'
            }
        })

        async function lancerPaiement() {
            console.log('💰 [XpayeModale] Début du paiement');
            console.log('Données du paiement:', paiementStore.paiement);
            loading.value = true
            errorMessage.value = ''

            try {
                if (isSandbox.value) {
                    console.log('🧪 [XpayeModale] Mode sandbox activé');
                }

                console.log('⏳ [XpayeModale] Attente du script...');
                await attendreScript()
                console.log('✅ [XpayeModale] Script prêt');

                const paiement = paiementStore.paiement
                const marchandId = paiement.merchantId || 'PP-F324'
                const channel = mapPaymentChannel(paiement.channel || props.paymentMethod)

                console.log('🔨 [XpayeModale] Création de l\'instance PaiementPro avec ID:', marchandId);
                const paiementPro = new PaiementPro(marchandId)

                console.log('📝 [XpayeModale] Attribution des propriétés...');
                paiementPro.amount              = paiement.amount
                paiementPro.channel             = channel
                paiementPro.referenceNumber     = paiement.referenceNumber || `REF-${Date.now()}`
                paiementPro.customerEmail       = paiement.customerEmail || 'client@example.com'
                paiementPro.customerFirstName   = paiement.customerFirstName || 'Prénom'
                paiementPro.customerLastname    = paiement.customerLastname || 'Nom'
                paiementPro.customerPhoneNumber = paiement.customerPhoneNumber || '00000000'
                paiementPro.description         = paiement.description || 'Achat de contrats'

                if (paiement.notificationURL) paiementPro.notificationURL = paiement.notificationURL
                if (paiement.returnURL) paiementPro.returnURL = paiement.returnURL
                if (paiement.returnContext) paiementPro.returnContext = paiement.returnContext

                console.log('📤 [XpayeModale] Appel à getUrlPayment()...');
                await paiementPro.getUrlPayment()

                console.log('✓ [XpayeModale] Réponse reçue:', {
                    success: paiementPro.success,
                    error: paiementPro.error,
                    url: paiementPro.url ? 'URL disponible' : 'Pas d\'URL'
                });

                if (paiementPro.success) {
                    if (isSandbox.value && !paiementPro.url) {
                        const sandboxUrl = `${window.location.origin}/sandbox-result?status=success&ref=${encodeURIComponent(paiementPro.referenceNumber)}`
                        console.log('🧪 [XpayeModale] Sandbox simulée, redirection vers:', sandboxUrl);
                        window.location.href = sandboxUrl
                    } else {
                        console.log('✅ [XpayeModale] Paiement réussi! Redirection vers:', paiementPro.url);
                        window.location.href = paiementPro.url
                    }
                } else {
                    console.error('❌ [XpayeModale] Erreur PaiementPro:', paiementPro.error);
                    errorMessage.value = 'Erreur : ' + paiementPro.error
                }

            } catch (err: unknown) {
                console.error('❌ [XpayeModale] Exception lors du paiement:', err);
                if (isSandbox.value && err instanceof Error && err.message.includes('PaiementPro')) {
                    console.log('🧪 [XpayeModale] Simulation sandbox en cas d\'erreur du script PaiementPro');
                    const sandboxUrl = `${window.location.origin}/sandbox-result?status=error&ref=${encodeURIComponent(paiementStore.paiement.referenceNumber || 'sandbox')}`
                    window.location.href = sandboxUrl
                    return
                }
                errorMessage.value = err instanceof Error
                    ? err.message
                    : 'Une erreur inattendue est survenue.'
            } finally {
                loading.value = false
                console.log('📊 [XpayeModale] État final - loading:', loading.value);
            }
        }

        return {
            paiementStore,
            loading,
            errorMessage,
            isSandbox,
            paymentMethodLabel,
            closeModal,
            lancerPaiement,
        }
    }
})
</script>

<style scoped>
.glass-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.kkiapay-modal-content {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border-radius: 1.5rem;
    padding: 2.5rem 2rem;
    position: relative;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    animation: modalFadeIn 0.3s ease-out forwards;
}

.payment-info {
    background: #f5f7fa;
    border-radius: 0.75rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.sandbox-badge {
    color: #1d4ed8;
    font-weight: 700;
    margin: 0.25rem 0 0;
}

.info-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.info-group label {
    font-weight: 600;
    color: #334155;
    min-width: 100px;
}

.info-value {
    margin: 0;
    color: #1a1a1a;
    text-align: right;
    flex: 1;
}

.pay-button {
    width: 100%;
    padding: 0.85rem 1.5rem;
    background: #1a56db;
    color: white;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: background 0.2s, opacity 0.2s;
}

.pay-button:hover:not(:disabled) {
    background: #1e429f;
}

.pay-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.close-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: transparent;
    border: none;
    color: #334155;
    font-size: 1.4rem;
    cursor: pointer;
}

.payment-method-label {
    color: #334155;
    font-size: 0.95rem;
    margin: 0;
}

.error-message {
    background: #fef2f2;
    border: 1px solid #fca5a5;
    color: #b91c1c;
    border-radius: 0.5rem;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
}

h3 {
    margin: 0 0 0.5rem 0;
    color: #1a1a1a;
    font-size: 1.25rem;
    font-weight: 700;
    text-align: center;
}

@keyframes modalFadeIn {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>