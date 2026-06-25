<template>
  <div v-if="isVerifying" class="verify__screen">
    <div class="spinner"></div>
    <h3 class="verify__title">Vérification de votre paiement...</h3>
    <p class="verify__subtitle">
        Veuillez patienter pendant que nous confirmons la transaction avec la banque.<br>
        <strong>Ne fermez pas cette page.</strong>
    </p>
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
        label="Aller à la page d'accueil" 
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

        // C'EST ICI LA CLÉ : La page commence TOUJOURS en mode "Vérification" (Spinner)
        const isVerifying = ref(true) 
        
        const countdown = ref(3)
        let countdownTimer: any = null

        const activeOrderId = computed(() => orderStore.currentOrder?.id || route.query.order_id || route.query.id);
        const canDownload = computed(() => !!activeOrderId.value)
        const downloading = computed(() => paiementStore.isLoading)

        const downloadContract = async () => {
            if (!activeOrderId.value) return;
            await paiementStore.downloadContracts(activeOrderId.value as string);
        }

        onMounted(async () => {
            const status = (route.query.status || '').toString().toLowerCase();

            // 1. Coupe-circuit (Fast-Fail) : On bloque immédiatement les annulations de Xpay
            if (['failed', 'canceled', 'cancelled', 'error'].includes(status)) {
                router.replace('/order/orderFails');
                return;
            }

            if (!activeOrderId.value) {
                router.replace('/order/orderFails');
                return;
            }

            // 2. Le Gardien tente de télécharger.
            // Le spinner tourne pendant que le store patiente pour le Webhook Ngrok
            const isSuccess = await paiementStore.downloadContracts(activeOrderId.value as string);

            if (isSuccess) {
                // Le PDF a été téléchargé, preuve que c'est payé !
                router.replace({ path: route.path, query: {} })
                
                // On fait disparaître le spinner et on affiche le succès
                isVerifying.value = false;

                // On lance le compte à rebours vers l'accueil
                countdownTimer = setInterval(() => {
                    countdown.value--;
                    if (countdown.value <= 0) {
                        clearInterval(countdownTimer);
                        emit('succes');
                    }
                }, 1000);
            } else {
                // Si après 15s le webhook n'est pas arrivé (ou paiement vraiment échoué)
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
/* ── 1. Écran de vérification (Le fameux Spinner) ── */
.verify__screen {
    height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    animation: fadeIn 0.3s ease;
}

.spinner {
    width: 60px;
    height: 60px;
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
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.verify__subtitle {
    color: #4a5568;
    font-size: 1rem;
    line-height: 1.6;
}

.verify__subtitle strong {
    color: #ef4444;
}

/* ── 2. Écran de succès (Ton design) ── */
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
    color: #32f459;
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