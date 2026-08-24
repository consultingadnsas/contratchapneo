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

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '../../stores/orderStore';
import { useProStore } from '../../stores/proStore';
import { useProfileStore } from '../../stores/profileStore';

import footerSection from '../../components/sections/footerSection.vue';
import succesForm from '../../components/forms/succesForm.vue';

// 1. MACRO NUXT (Parfaitement à sa place ici)
definePageMeta({
  middleware: 'payment-guard'
});

// 2. INITIALISATION DES STORES ET VARIABLES
const router = useRouter();
const orderStore = useOrderStore();
const proStore = useProStore();
const profileStore = useProfileStore();

const countdown = ref(5);
let timer: ReturnType<typeof setInterval> | null = null;

const getItems = () => {
    return orderStore.currentOrder?.order_items || orderStore.currentOrder?.items || [];
};

const getItemTitle = (item: any): string => {
    return String(
        item.title || 
        item.name || 
        item.designation || 
        item.label || 
        item.customed_contract?.title || 
        item.customed_contract?.name || 
        item.contrat?.title || 
        item.contrat?.name || 
        ''
    ).toLowerCase();
};

// ==========================================================
// 1. 📝 DÉTECTION STRICTE DU CONTRAT SUR MESURE
// ==========================================================
const customContractItem = computed(() => {
    return getItems().find((item: any) => {
        const title = getItemTitle(item);
        const normalizedTitle = title.replace(/\s+/g, '');

        const hasCustomContractKey = (
            (item.customed_contract !== undefined && item.customed_contract !== null) ||
            (item.customed_contract_id !== undefined && item.customed_contract_id !== null)
        );

        const isCustomType = (
            item.type === 'customed_contract' ||
            item.type === 'custom' ||
            item.product_type === 'custom'
        );

        const hasCustomTitle = (
            title.includes('sur mesure') ||
            title.includes('sur-mesure') ||
            normalizedTitle.includes('surmesure') ||
            normalizedTitle.includes('suremesure')
        );

        const isNotOtherProduct = (
            !item.contrat && 
            !item.contrat_id && 
            !item.pro && 
            !item.pro_id && 
            !item.pack && 
            !item.pack_id && 
            !item.contract_revision && 
            !item.contract_revision_id
        );

        return hasCustomContractKey || isCustomType || hasCustomTitle || isNotOtherProduct;
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
            (item.contract_revision !== undefined && item.contract_revision !== null) ||
            (item.contract_revision_id !== undefined && item.contract_revision_id !== null) ||
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
            (item.credits !== undefined && item.credits !== null)
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
// 5. 📄 DÉTECTION STRICTE DU CONTRAT STANDARD
// ==========================================================
const isStandardContractOrder = computed(() => {
    if (isProOrder.value || isPackOrder.value || isCustomContractOrder.value || isRevisionOrder.value) {
        return false;
    }
    return getItems().some((item: any) => !!(item.contrat || item.contrat_id));
});

// ==========================================================
// 6. 👔 ACTION MANUELLE : TÉLÉCHARGEMENT CARTE PRO
// ==========================================================
const handleDownloadProCard = async () => {
    if (!proItem.value) {
        alert("Impossible de retrouver les détails de votre commande Pro.");
        return;
    }

    const proId = (typeof proItem.value.pro === 'string' ? proItem.value.pro : proItem.value.pro?.id) ||
                  proItem.value.pro_id ||
                  (typeof proItem.value.professional === 'string' ? proItem.value.professional : proItem.value.professional?.id) ||
                  proItem.value.professional_id ||
                  (proItem.value.type === 'pro' ? proItem.value.id : null);

    if (!proId) {
        console.error("🚨 Identifiant du Pro introuvable dans :", proItem.value);
        alert("Erreur technique : l'identifiant du professionnel est introuvable.");
        return;
    }

    console.log("👔 Lancement du téléchargement pour le Pro ID :", proId);
    const success = await proStore.downloadProCard(String(proId));

    if (!success) {
        alert(proStore.error || "Une erreur est survenue pendant le téléchargement de la carte de visite.");
    }
};

// ==========================================================
// 7. ⏱️ GESTION DU COMPTE À REBOURS & AUTOMATISATIONS
// ==========================================================
onMounted(() => {
    console.log("🔍 [OrderSucces] Articles reçus :", getItems());
    console.log("👉 Types — Pro:", isProOrder.value, "| Pack:", isPackOrder.value, "| Custom:", isCustomContractOrder.value, "| Revision:", isRevisionOrder.value);

    if (!isProOrder.value) {
        timer = setInterval(async () => {
            countdown.value--;
            
            if (countdown.value <= 0) {
                if (timer) clearInterval(timer);
                
                if (isCustomContractOrder.value || isRevisionOrder.value) {
                    console.log("📝/🔍 Contrat sur mesure ou Révision détecté -> Redirection Accueil ('/')...");
                    router.push('/');
                }
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
                else if (isStandardContractOrder.value) {
                    console.log("📄 Contrat standard -> Redirection vers l'éditeur...");
                    router.push('/contractWritter');
                }
                else {
                    console.log("🛡️ Article non standard -> Redirection Accueil ('/')...");
                    router.push('/');
                }
            }
        }, 1000);
    } else {
        console.log("👔 Commande Pro détectée : Compte à rebours désactivé.");
        
        console.log("📥 Lancement automatique du téléchargement de la carte...");
        setTimeout(() => {
            handleDownloadProCard();
        }, 800);
    }
});

onBeforeUnmount(() => {
    if (timer) clearInterval(timer);
});

// 🎉 Pas besoin de return() ! Tout est exposé automatiquement à la <template>
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