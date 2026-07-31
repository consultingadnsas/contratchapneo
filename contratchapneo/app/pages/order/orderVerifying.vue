<template>
  <div class="verifying-wrapper">
    <div class="verifying-card shadow-2xl">
      
      <!-- Icône de bouclier de sécurité animée -->
      <div class="icon-container">
        <div class="shield-pulse">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="shield-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
          </svg>
        </div>
      </div>

      <h1 class="title">Vérification de votre paiement</h1>
      <p class="subtitle">
        Nous confirmons la transaction. Veuillez ne pas fermer cette page.
      </p>

      <!-- Barre de progression visuelle -->
      <div class="progress-bar-container">
        <div class="progress-bar-fill"></div>
      </div>

      
      
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useOrderStore } from '../../stores/orderStore';

export default {
  name: 'OrderVerifyingPage',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const orderStore = useOrderStore();

    const statusMessage = ref('Connexion sécurisée en cours...');
    let checkInterval: ReturnType<typeof setInterval> | null = null;

    onMounted(async () => {
      // 1. DÉTECTION IMMÉDIATE D'UN ÉCHEC DANS L'URL XPAY
      const urlString = JSON.stringify(route.query).toUpperCase();
      const failedKeywords = ['FAILED', 'FAIL', 'CANCELLED', 'CANCELED', 'CANCEL', 'ERROR', 'REFUSED', 'REJECTED', 'DECLINED', 'ABORTED'];
      
      const isExplicitFailure = failedKeywords.some(kw => urlString.includes(kw));
      if (isExplicitFailure) {
        console.warn("🚨 Échec ou annulation détectée dans l'URL XPay.");
        router.replace('/order/orderFails');
        return;
      }

      // 2. RÉCUPÉRATION DE L'ID COMMANDE
      const orderId = String(
        route.query.ref || 
        route.query.reference || 
        route.query.order_id || 
        route.query.id || 
        orderStore.currentOrder?.id || 
        ''
      );

      if (!orderId) {
        console.warn("🚨 Aucun ID de commande trouvé. Redirection accueil.");
        router.replace('/');
        return;
      }

      // 3. BOUCLE DE VÉRIFICATION (POLLING INTÉLLIGENT)
      // On interroge Django toutes les 1.5 secondes (max 5 tentatives = ~7.5 secondes)
      let attempts = 0;
      const maxAttempts = 5;

      const checkStatus = async () => {
        attempts++;
        statusMessage.value = `Confirmation de la transaction (tentative ${attempts}/${maxAttempts})...`;
        console.log(`[Order Verifying] 🔍 Tentative ${attempts} pour la commande${orderId}...`);

        try {
          const freshOrder = await orderStore.fetchOrder(orderId);
          const statut = String(freshOrder?.status || '').toUpperCase();

          // ✅ STATUT SUCCÈS CONFIRMÉ PAR LE BACKEND
          if (['PAID', 'SUCCESS', 'COMPLETED', 'APPROVED', 'OK'].includes(statut)) {
            if (checkInterval) clearInterval(checkInterval);
            console.log("✅ Paiement confirmé ! Redirection vers /orderSucces");
            router.replace('/order/orderSucces');
            return;
          }

          // ❌ STATUT ÉCHEC CONFIRMÉ PAR LE BACKEND
          if (['FAILED', 'CANCELLED', 'CANCELED', 'REJECTED', 'REFUSED'].includes(statut)) {
            if (checkInterval) clearInterval(checkInterval);
            console.warn("🚨 Statut backend en échec. Redirection vers /orderFails");
            router.replace('/order/orderFails');
            return;
          }

          // ⏳ SI TOUJOURS PENDING À LA DERNIÈRE TENTATIVE
          if (attempts >= maxAttempts) {
            if (checkInterval) clearInterval(checkInterval);
            console.warn("⏳ Délai dépassé. Statut toujours PENDING après 5 tentatives.");
            
            // Si l'URL de XPay contient un mot de succès explicite (ex: ?status=SUCCESS),
            // on autorise l'accès par tolérance. Sinon -> Echec.
            const successKeywords = ['SUCCESS', 'PAID', 'COMPLETED', 'APPROVED', 'OK'];
            const hasSuccessInUrl = successKeywords.some(kw => urlString.includes(kw));

            if (hasSuccessInUrl) {
              router.replace('/order/orderSucces');
            } else {
              router.replace('/order/orderFails');
            }
          }
        } catch (err) {
          console.error("[Order Verifying] Erreur API lors du check :", err);
          if (attempts >= maxAttempts) {
            if (checkInterval) clearInterval(checkInterval);
            router.replace('/orderFails');
          }
        }
      };

      // Lancer le premier check immédiatement, puis toutes les 1500 ms
      await checkStatus();
      if (attempts < maxAttempts) {
        checkInterval = setInterval(checkStatus, 1500);
      }
    });

    onBeforeUnmount(() => {
      if (checkInterval) clearInterval(checkInterval);
    });

    return {
      statusMessage
    };
  }
};
</script>

<style scoped>
.verifying-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8fafc;
  padding: 1.5rem;
  font-family: 'Inter', sans-serif;
}

.verifying-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 3rem 2rem;
  max-width: 440px;
  width: 100%;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.icon-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.shield-pulse {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: rgba(32, 43, 74, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s infinite;
}

.shield-icon {
  width: 42px;
  height: 42px;
  color: #202b4a; /* Bleu Contratchap */
}

@keyframes pulse {
  0% { transform: scale(0.98); box-shadow: 0 0 0 0 rgba(32, 43, 74, 0.2); }
  70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(32, 43, 74, 0); }
  100% { transform: scale(0.98); box-shadow: 0 0 0 0 rgba(32, 43, 74, 0); }
}

.title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 2rem;
}

.progress-bar-container {
  width: 100%;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 99px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-bar-fill {
  width: 40%;
  height: 100%;
  background-color: #202b4a;
  border-radius: 99px;
  animation: progressMove 1.5s infinite ease-in-out;
}

@keyframes progressMove {
  0% { transform: translateX(-100%); width: 30%; }
  50% { width: 60%; }
  100% { transform: translateX(300%); width: 30%; }
}

.status-text {
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
  margin: 0;
}
</style>