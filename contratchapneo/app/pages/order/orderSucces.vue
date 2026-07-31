<template>
    <div class="main-wrapper">
        <succesForm :countdown="countdown" />
        <footerSection/>
    </div>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '../../stores/orderStore'; // 👈 Import du store pour le gardien

import footerSection from '../../components/sections/footerSection.vue';
import succesForm from '../../components/forms/succesForm.vue';

definePageMeta({
  middleware: 'payment-guard'
})


export default {
    name: 'OrderSuccessPage',
    components: {
        footerSection,
        succesForm
    },
    setup() {

        const router = useRouter();
        const orderStore = useOrderStore();
        
        const countdown = ref(5); // 5 secondes avant redirection
        let timer: ReturnType<typeof setInterval> | null = null;

        onMounted(() => {
            // ── 1. LE GARDIEN (Vérification de sécurité) ──
            const order = orderStore.currentOrder;
            
            // Si aucune commande n'existe ou si le statut indique une erreur
            if (!order || order.status === 'FAILED') {
                console.warn("Accès refusé : aucune commande valide trouvée.");
                // Redirection vers l'échec ou l'accueil
                router.push('/orderFails'); 
                return;
            }

            // ── 2. LE COMPTE À REBOURS AUTOMATIQUE ──
            timer = setInterval(() => {
                countdown.value--;
                
                if (countdown.value <= 0) {
                    if (timer) clearInterval(timer);
                    // Redirection vers la page de remplissage du contrat
                    router.push('/contractWritter'); 
                }
            }, 1000);
        });

        // Nettoyage de l'intervalle si l'utilisateur quitte la page manuellement avant la fin
        onBeforeUnmount(() => {
            if (timer) clearInterval(timer);
        });

        return {
            countdown
        }
    }
}
</script>

<style scoped>
.main-wrapper {
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #f7fafc;
}

.checkout-wrapper {
    width: 95%;
    min-height: 100vh;
    max-width: 800px;
    margin: 1rem auto;
    background: #fff;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
</style>