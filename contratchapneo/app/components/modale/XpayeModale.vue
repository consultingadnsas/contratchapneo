<template>
    <div class="glass-modal-overlay">

        <div class="kkiapay-modal-content">
            <h3>Formulaire de Paiement</h3>

            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>

            <button
                class="pay-button"
                :disabled="loading"
                @click="lancerPaiement"
            >
                <span v-if="loading">Initialisation...</span>
                <span v-else>Payer {{ paiementStore.paiement.amount }} FCFA</span>
            </button>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useHead } from '#imports'
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
        success: boolean
        url: string
        error: string
        getUrlPayment(): Promise<void>
    }
}

const MARCHAND_ID = 'VOTRE_ID_MARCHAND' // 👈 Remplacer par votre ID

const paiementStore = usePaiementStore()
const loading = ref(false)
const errorMessage = ref('')
const scriptPret = ref(false)

// Charge le script PaiementPro dans le <head>
useHead({
    script: [
        {
            src: 'https://www.paiementpro.net/webservice/onlinepayment/js/paiementpro.v1.0.2.js',
            onload: () => { scriptPret.value = true },
        }
    ]
})

// Fallback : vérifie si PaiementPro est déjà disponible au montage
// (cas où le script était déjà en cache)
onMounted(() => {
    if (typeof PaiementPro !== 'undefined') {
        scriptPret.value = true
    }
})

// Attend que PaiementPro soit disponible dans le window
function attendreScript(timeout = 10000): Promise<void> {
    return new Promise((resolve, reject) => {
        if (typeof PaiementPro !== 'undefined') return resolve()

        const debut = Date.now()
        const intervalle = setInterval(() => {
            if (typeof PaiementPro !== 'undefined') {
                clearInterval(intervalle)
                resolve()
            } else if (Date.now() - debut > timeout) {
                clearInterval(intervalle)
                reject(new Error('Le script PaiementPro n\'a pas pu se charger.'))
            }
        }, 100)
    })
}

async function lancerPaiement() {
    loading.value = true
    errorMessage.value = ''

    try {
        // S'assure que le script externe est chargé
        await attendreScript()

        const { paiement } = paiementStore

        const paiementPro = new PaiementPro(MARCHAND_ID)
        paiementPro.amount              = paiement.amount
        paiementPro.channel             = paiement.channel
        paiementPro.referenceNumber     = paiement.referenceNumber
        paiementPro.customerEmail       = paiement.customerEmail
        paiementPro.customerFirstName   = paiement.customerFirstName
        paiementPro.customerLastname    = paiement.customerLastname
        paiementPro.customerPhoneNumber = paiement.customerPhoneNumber
        paiementPro.description         = paiement.description

        await paiementPro.getUrlPayment()

        if (paiementPro.success) {
            // Redirection vers la passerelle de paiement
            window.location.href = paiementPro.url
        } else {
            errorMessage.value = 'Erreur : ' + paiementPro.error
        }

    } catch (err: unknown) {
        errorMessage.value = err instanceof Error
            ? err.message
            : 'Une erreur inattendue est survenue.'
    } finally {
        loading.value = false
    }
}
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
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    animation: modalFadeIn 0.3s ease-out forwards;
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

.error-message {
    background: #fef2f2;
    border: 1px solid #fca5a5;
    color: #b91c1c;
    border-radius: 0.5rem;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
}

@keyframes modalFadeIn {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>