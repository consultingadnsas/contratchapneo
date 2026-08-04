<template>
    <div class="main-wrapper">
        <succesForm 
            :countdown="countdown" 
            :isPro="isProOrder"
            :isPack="isPackOrder"
            :isCustomContract="isCustomContractOrder"
            :isRevision="isRevisionOrder"
            :isDownloading="proStore.isLoading"
            @download-pro="handleDownloadProCard"
        />
        <footerSection/>
    </div>
</template>

<script lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '../../stores/orderStore';
import { useProStore } from '../../stores/proStore';
import { useProfileStore } from '../../stores/profileStore';

import footerSection from '../../components/sections/footerSection.vue';
import succesForm from '../../components/forms/succesForm.vue';

definePageMeta({
  middleware: 'payment-guard'
});

export default {
    name: 'OrderSuccessPage',
    components: {
        footerSection,
        succesForm
    },
    setup() {
        const router = useRouter();
        const orderStore = useOrderStore();
        const proStore = useProStore();
        const profileStore = useProfileStore();
        
        const countdown = ref(5);
        let timer: ReturnType<typeof setInterval> | null = null;

        const getItems = () => {
            return orderStore.currentOrder?.order_items || orderStore.currentOrder?.items || [];
        };

        // ⚡️ UTILITAIRE : FOUILLE PARTOUT POUR TROUVER LE TITRE DE L'ARTICLE
        const getItemTitle = (item: any): string => {
            return String(
                item.title || 
                item.name || 
                item.designation || 
                item.label || 
                item.customed_contract?.title || 
                item.customed_contract?.name || 
                item.customized_contract?.title || 
                item.customized_contract?.name || 
                item.custom_contract?.title || 
                item.contrat?.title || 
                item.contrat?.name || 
                ''
            ).toLowerCase();
        };

        // ==========================================================
        // 1. 📝 DÉTECTION DU CONTRAT SUR MESURE
        // ==========================================================
        const customContractItem = computed(() => {
            return getItems().find((item: any) => {
                const jsonStr = JSON.stringify(item || {}).toLowerCase();
                
                return (
                    // ⚡️ AJOUT CRITIQUE : On cible exactement "customed_contracts" (singulier et pluriel)
                    jsonStr.includes('customed_contracts') ||
                    jsonStr.includes('customed_contract') ||
                    item.customed_contracts ||
                    item.customed_contract ||
                    item.customed_contracts_id ||
                    item.customed_contract_id ||
                    item.customized_contract ||
                    item.custom_contract ||
                    item.type === 'customed_contracts' ||
                    item.type === 'customed_contract' ||
                    jsonStr.includes('custom') ||
                    jsonStr.includes('mesure') ||
                    jsonStr.includes('personnalis')
                );
            });
        });

        const isCustomContractOrder = computed(() => !!customContractItem.value);

        // ==========================================================
        // 2. 🔍 DÉTECTION DE LA RÉVISION DE CONTRAT
        // ==========================================================
        const revisionItem = computed(() => {
            return getItems().find((item: any) => {
                const title = getItemTitle(item);
                return (
                    item.contract_revision ||
                    item.contract_revision_id ||
                    item.revision ||
                    item.revision_id ||
                    item.type === 'revision' ||
                    title.includes('révision') ||
                    title.includes('revision')
                );
            });
        });

        const isRevisionOrder = computed(() => !!revisionItem.value);

        // ==========================================================
        // 3. 📦 DÉTECTION DU PACK DE CRÉDITS
        // ==========================================================
        const packItem = computed(() => {
            if (isCustomContractOrder.value || isRevisionOrder.value) return null;

            return getItems().find((item: any) => {
                const title = getItemTitle(item);
                return (
                    item.pack_id || 
                    item.pack || 
                    item.type === 'pack' || 
                    item.product_type === 'pack' ||
                    item.is_pack === true ||
                    title.includes('pack') || 
                    title.includes('crédit') || 
                    title.includes('credit') ||
                    item.credits !== undefined ||
                    item.customs !== undefined ||
                    item.credits_restants !== undefined
                );
            });
        });

        const isPackOrder = computed(() => !!packItem.value);

        // ==========================================================
        // 4. 👔 DÉTECTION DU PRODUIT PRO (Carte de visite)
        // ==========================================================
        const proItem = computed(() => {
            if (isPackOrder.value || isCustomContractOrder.value || isRevisionOrder.value) return null;

            return getItems().find((item: any) => {
                const title = getItemTitle(item);
                return (
                    item.pro ||
                    item.pro_id || 
                    item.professional_id || 
                    item.professional || 
                    item.type === 'pro' || 
                    item.product_type === 'pro' ||
                    item.is_pro === true ||
                    title.includes('carte') || 
                    title.includes('visite') || 
                    title.includes('professionnel')
                );
            });
        });

        const isProOrder = computed(() => !!proItem.value);

        // ==========================================================
        // 5. 👔 ACTION MANUELLE : TÉLÉCHARGEMENT CARTE PRO
        // ==========================================================
        const handleDownloadProCard = async () => {
            if (!proItem.value) {
                alert("Impossible de retrouver les détails de votre commande Pro.");
                return;
            }

            const proId = proItem.value.pro_id || 
                          proItem.value.professional_id || 
                          proItem.value.professional?.id || 
                          proItem.value.pro?.id ||
                          proItem.value.id;

            if (!proId) {
                console.error("🚨 Élément Pro trouvé, mais son identifiant est manquant :", proItem.value);
                alert("Erreur technique : l'identifiant de la carte est introuvable.");
                return;
            }

            console.log("👔 Lancement du téléchargement pour l'identifiant :", proId);
            const success = await proStore.downloadProCard(String(proId));

            if (!success) {
                alert(proStore.error || "Une erreur est survenue pendant le téléchargement.");
            }
        };

        // ==========================================================
        // 6. ⏱️ GESTION DU COMPTE À REBOURS & REDIRECTIONS
        // ==========================================================
        onMounted(() => {
            console.log("🔍 [OrderSucces] Articles reçus :", getItems());
            console.log("👉 Types — Pro:", isProOrder.value, "| Pack:", isPackOrder.value, "| Custom:", isCustomContractOrder.value, "| Revision:", isRevisionOrder.value);

            if (!isProOrder.value) {
                timer = setInterval(async () => {
                    countdown.value--;
                    
                    if (countdown.value <= 0) {
                        if (timer) clearInterval(timer);
                        
                        // ── CAS A : CONTRAT SUR MESURE OU RÉVISION -> REDIRECTION ACCUEIL ('/') ──
                        if (isCustomContractOrder.value || isRevisionOrder.value) {
                            console.log("📝/🔍 Contrat sur mesure ou Révision détecté -> Redirection Accueil ('/')...");
                            router.push('/');
                        }
                        // ── CAS B : PACK DE CRÉDITS -> REDIRECTION DASHBOARD ──
                        else if (isPackOrder.value) {
                            console.log("📦 Pack détecté -> Redirection Dashboard...");
                            try {
                                await profileStore.getPacks();
                                console.log("✅ Crédits synchronisés avec succès.");
                            } catch (err) {
                                console.warn("⚠️ Impossible de rafraîchir les crédits :", err);
                            }
                            router.push('/profile/Dashboard');
                        } 
                        // ── CAS C : CONTRAT STANDARD -> ÉDITEUR DE CONTRAT ──
                        else {
                            console.log("📄 Contrat standard -> Redirection vers l'éditeur...");
                            router.push('/contractWritter');
                        }
                    }
                }, 1000);
            } else {
                console.log("👔 Commande Pro détectée : Compte à rebours automatique désactivé.");
            }
        });

        onBeforeUnmount(() => {
            if (timer) clearInterval(timer);
        });

        return {
            countdown,
            isProOrder,
            isPackOrder,
            isCustomContractOrder,
            isRevisionOrder,
            proStore,
            handleDownloadProCard
        };
    }
};
</script>

<style scoped>
.main-wrapper {
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #f7fafc;
}
</style>