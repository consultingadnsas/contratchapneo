<template>
    <div class="main-wrapper">
         <div class="checkout-header">
                <button 
                    type="button" 
                    class="btn-back-home" 
                    :disabled="isClearing || cartStore.isLoading"
                    @click="handleReturnHome"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="back-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    <span>{{ isClearing ? 'Vidage du panier...' : '' }}</span>
                </button>
            </div>
        <div class="checkout-wrapper">
            
            <!-- ⚡️ En-tête avec le bouton de retour -->

            <!-- Ton composant de caisse -->
            <checkoutSectionVue/>
            
        </div>
        <footerSection/>
    </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCartStore } from '../../stores/cartStore';

import Navbar from '../../components/navigation/navbar.vue';
import checkoutSectionVue from '../../components/sections/orderSections/checkoutSection.vue';
import footerSection from '../../components/sections/footerSection.vue';

export default {
    name: 'CheckoutPage',
    components: {
        Navbar,
        checkoutSectionVue,
        footerSection
    },
    setup() {
        const router = useRouter();
        const cartStore = useCartStore();
        const isClearing = ref(false);

        const handleReturnHome = async () => {
            isClearing.value = true;
            try {
                // 1. On appelle l'action clearCart() du store pour vider l'API et le state local
                await cartStore.clearCart();
                console.log('🗑️ Panier vidé avec succès avant retour à l\'accueil.');
            } catch (err) {
                // 2. Sécurité : si l'API échoue, on vide quand même le panier en local
                // pour éviter de bloquer l'utilisateur
                console.warn('⚠️ Erreur API lors du vidage, réinitialisation locale...', err);
                cartStore.cart = { items: [] };
            } finally {
                isClearing.value = false;
                // 3. Redirection vers la page d'accueil
                router.push('/');
            }
        };

        return {
            cartStore,
            isClearing,
            handleReturnHome
        };
    }
};
</script>

<style scoped>
.main-wrapper {
    background: radial-gradient(circle, #202b4a 30%, #0f0f0f 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.checkout-wrapper {
    width: 95%;
    min-height: 80vh;
    max-width: 800px;
    margin: 2rem auto;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    display: flex;
    overflow: hidden;
}

/* ── En-tête de retour ── */
.checkout-header {
    width: 100%;
    padding: 1.25rem 1.5rem 0.5rem 1.5rem;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    box-sizing: border-box;
}

.btn-back-home {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    width: fit-content;
    display: flex;
    color: #202b4a;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
}

.btn-back-home:hover:not(:disabled) {
    background: #e2e8f0;
    color: #0f172a;
    transform: translateX(-3px);
}

.btn-back-home:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.back-icon {
    width: 16px;
    height: 16px;
}
</style>