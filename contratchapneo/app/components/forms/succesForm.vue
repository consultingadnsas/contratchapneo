<template>
  <div v-if="isVerifying" class="verify__screen">
    <div class="spinner"></div>
    <h3 class="verify__title">Vérification en cours...</h3>
    <p class="verify__subtitle">Veuillez patienter, nous confirmons la transaction avec la banque.</p>
  </div>

  <div v-else class="success__screen">
    <div class="success__icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="11" stroke="currentColor" stroke-width="1.5"/>
            <path d="M7 12.5L10.5 16L17 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <h3 class="success__title">{{ message }}</h3>
    <p class="success__subtitle">
        Vous serez redirigé dans <span>{{ countdown }}s</span>.
    </p>
    <button
        class="success__download"
        :disabled="downloading || !canDownload"
        @click="downloadContract"
    >
        {{ downloading ? 'Téléchargement en cours...' : 'Télécharger le contrat' }}
    </button>
    <mainButton 
        label="Aller page d'accueil" 
        @click="()=>router.push('/')"
    />
  </div>
</template>

<script lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useOrderStore } from '../../stores/orderStore'
import { usePaiementStore } from '../../stores/paiementStore'
import mainButton from '../buttons/mainButton.vue';

export default {
    components: {
        mainButton
    },
    props: {
        message: {
            type: String,
            default: 'Paiement effectué avec succès !'
        }
    },
    emits: ['succes'],
    setup(props, { emit }) {
        const router = useRouter()
        const route = useRoute()
        const orderStore = useOrderStore()
        const paiementStore = usePaiementStore()

        const isVerifying = ref(true) 
        const countdown = ref(3)
        let countdownTimer: any = null

        // 1. IDENTIFIANT DE TRANSACTION (Pour demander à Django si c'est payé)
        // On récupère "ref" que Xpay place dans l'URL à son retour
        const transactionRef = computed(() => route.query.ref || route.query.referenceNumber || paiementStore.paiement?.referenceNumber);

        // 2. IDENTIFIANT DE COMMANDE (Pour déclencher le téléchargement du PDF)
        const activeOrderId = computed(() => orderStore.currentOrder?.id || route.query.order_id);

        const canDownload = computed(() => !!activeOrderId.value)
        const downloading = computed(() => paiementStore.isLoading)

        const downloadContract = async () => {
            if (!activeOrderId.value) return;
            await paiementStore.downloadContracts(activeOrderId.value as string);
        }

        onMounted(async () => {
            const status = (route.query.status || '').toString().toLowerCase();

            // 1. Coupe-circuit (Fast-Fail) si annulé chez Xpay
            if (status === 'failed' || status === 'canceled' || status === 'cancelled' || status === 'error') {
                router.replace('/order/orderFails');
                return;
            }

            if (!transactionRef.value) {
                console.error("❌ Impossible de vérifier : Aucune référence de transaction trouvée.");
                router.replace('/order/orderFails');
                return;
            }

            // 2. Le Gardien interroge Django avec la RÉFÉRENCE DE LA TRANSACTION
            console.log("⏳ Vérification de la transaction :", transactionRef.value);
            const isSuccess = await paiementStore.verifyPayment(transactionRef.value as string);

            if (isSuccess) {
                // Le paiement est VALIDÉ !
                // On nettoie l'URL pour la rendre propre
                router.replace({ path: route.path, query: {} })
                isVerifying.value = false;
                
                // On télécharge le document avec l'ID de la commande
                downloadContract();

                countdownTimer = setInterval(() => {
                    countdown.value--;
                    if (countdown.value <= 0) {
                        clearInterval(countdownTimer);
                        emit('succes');
                    }
                }, 1000);
            } else {
                console.warn("❌ Django a refusé la transaction (Statut non-payé ou inconnu).");
                router.replace('/order/orderFails');
            }
        });

        onUnmounted(() => {
            if (countdownTimer) clearInterval(countdownTimer);
        });

        return {
            router,
            countdown,
            canDownload,
            downloading,
            downloadContract,
            isVerifying
        }
    }
}
</script>

<style scoped>
/* ── Écran de vérification (Gatekeeper) ── */
.verify__screen {
    height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(50, 244, 89, 0.2);
    border-top: 4px solid #32f459;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1.5rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.verify__title {
    color: #202b4a;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.verify__subtitle {
    color: #4a5568;
    font-size: 0.95rem;
}

/* ── Écran de succès (Ton design) ── */
.success__screen {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1.25rem;
    padding: 2.5rem 1.5rem;
    text-align: center;
    animation: fadeInUp 0.4s ease both;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.success__icon {
    width: 72px;
    height: 72px;
    color: #32f459; /* J'ai mis ton vert fluo ici pour la validation ! */
    animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes popIn {
    from { opacity: 0; transform: scale(0.4); }
    to   { opacity: 1; transform: scale(1); }
}

.success__title {
    color: #202b4a;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
}

.success__subtitle {
    color: #202b4a;
    font-size: 0.95rem;
    line-height: 1.7;
    margin: 0;
}

.success__download {
    background: #2f6dff;
    color: #fff;
    border: none;
    border-radius: 999px;
    padding: 0.9rem 1.5rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.2s ease, opacity 0.2s ease;
}

.success__download:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.success__download:hover:not(:disabled) {
    transform: translateY(-1px);
}
</style>