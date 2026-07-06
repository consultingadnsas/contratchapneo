<template>
  <div class="fail__screen">
    <!-- Icône d'erreur (Croix) -->
    <div class="fail__icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="11" stroke="currentColor" stroke-width="1.5"/>
            <path d="M9 9L15 15M15 9L9 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    
    <h3 class="fail__title">{{ message }}</h3>
    
    <p class="fail__subtitle">
        Votre transaction a été annulée ou n'a pas abouti. Aucun montant n'a été débité. <br>
        Vous serez redirigé dans <span>{{ countdown }}s</span>.
    </p>
    
    <div class="fail__actions">
        <button
            class="fail__retry"
            @click="goToCart"
        >
            Réessayer le paiement
        </button>
        
        <mainButton 
            label="Aller à la page d'accueil" 
            @click="()=>router.push('/')"
        />
    </div>
  </div>
</template>

<script lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue';
import mainButton from '../buttons/mainButton.vue';

export default {
    name: 'FailForm',
    components: {
        mainButton
    },
    props: {
        message: {
            type: String,
            default: 'Paiement annulé !'
        }
    },
    emits: ['timeout'],
    setup(props, { emit }) {
        const router = useRouter();
        const route = useRoute();
        
        // On donne un peu plus de temps (5s) pour lire le message d'erreur
        const countdown = ref(5);
        let countdownTimer: ReturnType<typeof setInterval> | null = null;

        // Nettoyage de l'URL comme sur la page succès
        onMounted(() => {
            if (Object.keys(route.query).length > 0) {
                router.replace({ path: route.path, query: {} });
            }
            
            countdownTimer = setInterval(() => {
                countdown.value--;
                if (countdown.value <= 0) {
                    if (countdownTimer) clearInterval(countdownTimer);
                    emit('timeout'); // Avertit la page parente
                }
            }, 1000);
        });

        onUnmounted(() => {
            if (countdownTimer) clearInterval(countdownTimer);
        });

        const goToCart = () => {
            if (countdownTimer) clearInterval(countdownTimer);
            router.push('/panier'); // Remplace par la route de ton panier ou checkout
        };

        return {
            router,
            countdown,
            goToCart
        }
    }
}
</script>

<style scoped>
/* ── Écran d'échec ── */
.fail__screen {
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

.fail__icon {
    width: 72px;
    height: 72px;
    /* Couleur rouge pour l'erreur */
    color: #ef4444; 
    animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes popIn {
    from { opacity: 0; transform: scale(0.4); }
    to   { opacity: 1; transform: scale(1); }
}

.fail__title {
    color: #202b4a;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
}

.fail__subtitle {
    color: #4a5568;
    font-size: 0.95rem;
    line-height: 1.7;
    margin: 0;
}

.fail__subtitle span {
    font-weight: 700;
    color: #ef4444;
}

.fail__actions {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
}

.fail__retry {
    background: #ef4444;
    color: #fff;
    border: none;
    border-radius: 999px;
    padding: 0.9rem 1.5rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.2s ease, background 0.2s ease;
}

.fail__retry:hover {
    transform: translateY(-2px);
    background: #dc2626;
}
</style>