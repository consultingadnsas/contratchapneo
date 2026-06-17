<template>
  <div class="success__screen">
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
    <mainButton 
        label="aller page d'accueil" 
        @click="()=>router.push('/')"
    />
  </div>
</template>

<script lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue';

import mainButton from '../buttons/mainButton.vue';

export default {
    components:{
        mainButton
    },
    props: {
        message: {
            type: String,
            default: 'Paiement effectuée avec succès !'
        }
    },
    emits:['succes'],
    setup(props, {emit}) {
        
        const router = useRouter()
        const route = useRoute()
        const countdown = ref(3);
        let countdownTimer: any = null;

        onMounted(() => {
            if (Object.keys(route.query).length > 0) {
                router.replace({ path: route.path, query: {} })
            }
            // CRUCIAL : Lancer le décompte dès que le composant apparaît
            countdownTimer = setInterval(() => {
                countdown.value--;
                if (countdown.value <= 0) {
                    clearInterval(countdownTimer);
                    emit('succes')
                }
            }, 1000);
        });

        onUnmounted(() => {
            // Nettoyage pour éviter les fuites de mémoire
            if (countdownTimer) clearInterval(countdownTimer);
        });

        return {
            route,
            router,
            countdown
        }
    }
}
</script>

<style scoped>
/* ── Écran de succès ── */
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
    color: #202b4a;
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
</style>