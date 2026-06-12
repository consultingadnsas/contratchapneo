<template>
    <div class="glass-modal-overlay">
        
        <div class="kkiapay-modal-content">

            <h3>Formulaire de Paiement</h3>

        </div>

        <div class="kkiapay-container">

            <div class=""></div>

        </div>

    </div>  
</template>

<script>
import type { ListenerData} from "kkiapay";
import {onMounted} from "vue";
export default {

    setup(){
        
        const {$kkiapay} = useNuxtApp();

        const initPayment = ()=> {
            $kkiapay.openKkiapayWidget({
                amount: 1000,
                sandbox: true,
                key:"",
                phone: "22997000000"
            })
        }

        return {
            initPayment
        }
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
  height: 90%;
  max-height: 600px;
  overflow-y: auto;
  animation: modalFadeIn 0.3s ease-out forwards;
}
</style>