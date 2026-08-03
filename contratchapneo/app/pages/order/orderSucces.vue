<template>
    <div class="main-wrapper">
        <succesForm 
            :countdown="countdown" 
            :isPro="isProOrder"
            :isPack="isPackOrder"
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
import { useProfileStore } from '../../stores/profileStore'; // ⚡️ Ajout du store profil

import footerSection from '../../components/sections/footerSection.vue';
import succesForm from '../../components/forms/succesForm.vue';

// ⚡️ Activation du middleware de sécurité
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

        // --- UTILITAIRE : Récupération sécurisée des articles de la commande ---
        const getItems = () => {
            return orderStore.currentOrder?.order_items || orderStore.currentOrder?.items || [];
        };

        // ==========================================================
        // 1. 👔 DÉTECTION STRICTE DU PRODUIT PRO (Carte de visite)
        // ==========================================================
       const proItem = computed(() => {
            // SÉCURITÉ : Si c'est déjà identifié comme un Pack, ce n'est PAS un Pro !
            if (isPackOrder.value) return null;

            return getItems().find((item: any) => {
                const title = String(item.title || item.name || item.designation || item.label || '').toLowerCase();
                
                return (
                    item.pro_id || 
                    item.professional_id || 
                    item.professional || 
                    item.type === 'pro' || 
                    item.product_type === 'pro' ||
                    item.is_pro === true ||
                    title.includes('carte') || 
                    title.includes('visite') || 
                    title.includes('professionnel') ||
                    // ⚡️ LE RETOUR DU BOUCLIER : Si ce n'est NI un contrat NI un pack -> C'est un Pro !
                    (!item.contrat_id && !item.contrat && !isPackOrder.value)
                );
            });
        });

        const isProOrder = computed(() => !!proItem.value);

        // ==========================================================
        // 2. 📦 DÉTECTION STRICTE DU PACK DE CRÉDITS
        // ==========================================================
        const packItem = computed(() => {
            // SÉCURITÉ : Si c'est déjà identifié comme un Pro, ce n'est PAS un pack !
            if (isProOrder.value) return null;

            return getItems().find((item: any) => {
                const title = String(item.title || item.name || item.designation || '').toLowerCase();
                
                return (
                    item.pack_id || 
                    item.pack || 
                    item.type === 'pack' || 
                    item.product_type === 'pack' ||
                    item.is_pack === true ||
                    // Mots-clés exclusifs aux Packs dans le titre
                    (title.includes('pack') || title.includes('crédit') || title.includes('credit')) ||
                    // Présence de propriétés spécifiques aux packs
                    item.credits !== undefined ||
                    item.customs !== undefined ||
                    item.credits_restants !== undefined
                );
            });
        });

        const isPackOrder = computed(() => !!packItem.value);

        // ==========================================================
        // 3. 👔 ACTION MANUELLE : TÉLÉCHARGEMENT CARTE PRO
        // ==========================================================
        const handleDownloadProCard = async () => {
            if (!proItem.value) {
                alert("Impossible de retrouver les détails de votre commande Pro.");
                return;
            }

            const proId = proItem.value.pro_id || 
                          proItem.value.professional_id || 
                          proItem.value.professional?.id || 
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
        // 4. ⏱️ GESTION DU COMPTE À REBOURS & REDIRECTIONS
        // ==========================================================
        onMounted(() => {
            console.log("🔍 [OrderSucces] Articles reçus :", getItems());
            console.log("👉 Type détecté — Pro:", isProOrder.value, "| Pack:", isPackOrder.value);

            // On ne déclenche la minuterie QUE pour les Packs et les Contrats standards
            if (!isProOrder.value) {
                timer = setInterval(async () => {
                    countdown.value--;
                    
                    if (countdown.value <= 0) {
                        if (timer) clearInterval(timer);
                        
                        // ── CAS A : ACHAT DE PACK ──
                        if (isPackOrder.value) {
                            console.log("📦 Commande Pack terminée -> Mise à jour des crédits...");
                            
                            try {
                                // ⚡️ Indispensable : On rafraîchit les crédits dans Pinia avant d'afficher le Dashboard
                                await profileStore.getPacks();
                                console.log("✅ Crédits synchronisés avec succès.");
                            } catch (err) {
                                console.warn("⚠️ Impossible de rafraîchir les crédits avant redirection :", err);
                            }

                            router.push('/profile/Dashboard');
                        } 
                        // ── CAS B : ACHAT DE CONTRAT STANDARD ──
                        else {
                            console.log("📄 Commande Contrat terminée -> Redirection vers l'éditeur...");
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