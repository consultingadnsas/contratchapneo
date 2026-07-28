<template>
    <div class="cards-container">

        <proCards
            v-for="(pro, index) in proStore.professionals" 
            :key="pro.id"
            :data-index="index"
            :title="`${pro.first_name} ${pro.last_name}`"
            :subtitle="pro.title_display"
            :image="pro.profile_picture || undefined"
            @view="checkProfile(pro)"
            @pro-checkout="Download(pro.id)"
            class="clickable-card"
        />

        <!-- ⚡️ AJOUT : Le composant de notification -->
        <BaseNotification 
            v-model:show="notifShow"
            :type="notifType"
            :title="notifTitle"
            :message="notifMessage"
        />

    </div>
</template>

<script lang="ts">
import proCards from '../../cards/proCards.vue'
// ⚡️ AJOUT : Import du composant (Vérifie le chemin exact dans ton projet)
import BaseNotification from '../../tools/baseNotification.vue' 
import { useProStore } from '../../../stores/proStore';
import { useProfileStore } from '../../../stores/profileStore'; 
import { onMounted, ref } from 'vue'; // ⚡️ AJOUT : Import de 'ref'
import { useRouter } from 'vue-router';

export default {
    components: {
        proCards,
        BaseNotification // ⚡️ AJOUT : Déclaration du composant
    },

    setup() {
        const proStore = useProStore();
        const profileStore = useProfileStore(); 
        const router = useRouter();

        // ⚡️ VARIABLES DE NOTIFICATION
        const notifShow = ref(false);
        const notifType = ref('success');
        const notifTitle = ref('');
        const notifMessage = ref('');

        async function Download(pro_id: string) {
            const activePack = profileStore.userPacks.find((pack: any) => pack.is_active === true);
            const proCredits = activePack?.cartes_pro_restantes || 0;

            // ⚡️ LE VERROU AVEC NOTIFICATION
            if (proCredits <= 0) {
                notifType.value = 'error';
                notifTitle.value = 'Action impossible';
                notifMessage.value = "Vous n'avez plus de crédits expert. Veuillez mettre à jour votre pack.";
                notifShow.value = true;
                return; 
            }

            try {
                const success = await proStore.downloadProCard(pro_id);
                
                if (success) {
                    await profileStore.getPacks(); 
                    
                    // ⚡️ OPTIONNEL : Petite notification de succès
                    notifType.value = 'success';
                    notifTitle.value = 'Succès';
                    notifMessage.value = 'La carte expert a été téléchargée avec succès.';
                    notifShow.value = true;
                }
                
            } catch(err: any) {
                console.warn("Erreur lors du téléchargement :", err);
                
                // ⚡️ NOTIFICATION EN CAS D'ERREUR (ex: 500 Backend)
                notifType.value = 'error';
                notifTitle.value = 'Erreur serveur';
                notifMessage.value = "Le téléchargement a échoué. Veuillez réessayer plus tard.";
                notifShow.value = true;
            }
        }

        async function checkProfile(pro: any){
            try {
                console.log("Consultation du profil de :", pro.first_name);
                // Ta logique pour ouvrir la modale ou la page profil
            } catch(err:any) {
                console.error("Erreur", err);
            } 
        }

        onMounted(() => {
            proStore.getProfessionals();
        });

        return {
            router,
            proStore,
            profileStore,
            Download,
            checkProfile,
            // ⚡️ EXPOSITION DES VARIABLES POUR LE TEMPLATE
            notifShow,
            notifType,
            notifTitle,
            notifMessage
        }
    }
}
</script>

<style scoped>
.cards-container {
    width: 100%;
    max-width: 1400px;
    display: grid;
    grid-template-columns: 1fr;
    place-items: center;
    gap: 1.5rem;
}

@media (min-width: 768px) and (max-width:  1023px){
    .cards-container {
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }
}

@media (min-width: 1280px){
    .cards-container {
        grid-template-columns: repeat(3, 1fr);
    }
}
</style>