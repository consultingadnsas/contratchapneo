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
    <div class="paginator">
        <Paginator 
            :currentPage="proStore.currentPage" 
            :totalCount="proStore.totalCount" 
            :pageSize="proStore.pageSize" 
            @page-changed="handlePageChange"
        />
    </div>
</template>

<script lang="ts">
import proCards from '../../cards/proCards.vue'
// ⚡️ AJOUT : Import du composant (Vérifie le chemin exact dans ton projet)
import BaseNotification from '../../tools/baseNotification.vue'
import Paginator from '../../tools/Paginator.vue';
import { useProStore } from '../../../stores/proStore';
import { useProfileStore } from '../../../stores/profileStore'; 
import { onMounted, ref } from 'vue'; // ⚡️ AJOUT : Import de 'ref'
import { useRouter, useRoute } from 'vue-router';

export default {
    components: {
        proCards,
        BaseNotification,
        Paginator
    },

    setup() {
        const proStore = useProStore();
        const profileStore = useProfileStore(); 
        const route = useRoute();
        const router = useRouter();

        // ⚡️ VARIABLES DE NOTIFICATION
        const notifShow = ref(false);
        const notifType = ref('success');
        const notifTitle = ref('');
        const notifMessage = ref('');

        const activeDomainSlug = ref((route.query.domaine as string) || '');
        const activeCountryCode = ref('');
        const searchQuery = ref('');
        const currentPage = ref(1); // 👈 Ajout : On suit la page locale

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

        const fetchPros = (page = 1) => {
            currentPage.value = page; // On garde en mémoire la page actuelle
            // On suppose que ton store a une fonction qui prend (page, domaine, pays, recherche)
            // Adapte le nom de la fonction selon ton store (fetchProfessionals ou getProfessionals)
            proStore.getProfessionals(page, activeDomainSlug.value, activeCountryCode.value, searchQuery.value);
        }

         const handlePageChange = (page: number) => {
            fetchPros(page);
        };

        onMounted(() => {
            proStore.getProfessionals();
        });

        return {
            router,
            proStore,
            profileStore,
            Download,
            handlePageChange,
            checkProfile,
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