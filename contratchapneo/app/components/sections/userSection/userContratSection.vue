<template>
    <div class="content-wrapper">
        
        <!-- SECTION TOP 3 : Visible uniquement s'il n'y a pas de recherche en cours -->
        <div v-if="!route.query.q && topContracts.length > 0" class="section-block">
            <h2 class="section-title"> Les plus téléchargés</h2>
            
            <div class="cards-container">
                <contractCardProfile
                    v-for="(contrat, index) in topContracts" 
                    :key="'top-' + (contrat.id || index)"
                    :title="contrat.title"
                    :description="contrat.description"
                    :image="contrat.picture || undefined"
                    @view="fillContract(contrat.id)" 
                    @buy="()=>{fillContract(contrat.id)}"
                />
            </div>
        </div>

        <!-- SECTION TOUS LES CONTRATS / RÉSULTATS DE RECHERCHE -->
        <div class="section-block">
            <h2 class="section-title">
                {{ route.query.q ? `Résultats pour "${route.query.q}"` : 'Tous les contrats' }}
            </h2>

            <div class="cards-container">
                <contractCardProfile
                    v-for="(contrat, index) in contratStore.contracts" 
                    :key="contrat.id || index"
                    :title="contrat.title"
                    :description="contrat.description"
                    :image="contrat.picture || undefined"
                    @view="fillContract(contrat.id)" 
                    @buy="()=>{fillContract(contrat.id)}"
                />
            </div>
            <div class="pagination-wrapper">
                <Paginator 
                    :currentPage="contratStore.currentPage"
                    :totalCount="contratStore.totalCount"
                    :pageSize="contratStore.pageSize"
                    @page-changed="handlePageChange"
                />
            </div>
        </div>

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
import contratCards from '../../cards/contratCards.vue';
import contractCardProfile from '../../cards/contractCardProfile.vue';
import { useContratStore } from '../../../stores/contratStore';
import { useProfileStore } from '../../../stores/profileStore'; 
import { onMounted, watch, computed, ref } from 'vue'; // ⚡️ AJOUT : import de ref
import { useRouter, useRoute } from 'vue-router'; 
import Paginator from '../../tools/Paginator.vue';

// ⚡️ AJOUT : Import du composant de notification (Ajuste le chemin si nécessaire)
import BaseNotification from '../../tools/baseNotification.vue'; 

export default {
    components: {
        contratCards,
        contractCardProfile,
        Paginator,
        BaseNotification // ⚡️ AJOUT
    },

    setup() {
        const contratStore = useContratStore();
        const profileStore = useProfileStore();
        const router = useRouter();
        const route = useRoute(); 

        // ⚡️ AJOUT : Variables réactives pour contrôler la notification
        const notifShow = ref(false);
        const notifType = ref('success');
        const notifTitle = ref('');
        const notifMessage = ref('');

        const topContracts = computed(() => {
            const allContracts = [...contratStore.contracts];
            
            return allContracts
                .sort((a, b) => {
                    const popularityA = a.download || a.views || 0;
                    const popularityB = b.download || b.views || 0;
                    return popularityB - popularityA; 
                })
                .slice(0, 3); 
        });

        async function fillContract(contract_id: string) {
            const activePack = profileStore.userPacks.find(pack => pack.is_active === true);
            const creditsRestants = activePack?.credits_restants || 0;

            if (creditsRestants <= 0) {
                // ⚡️ MODIFICATION : Remplacement de alert() par la notification
                notifType.value = 'error';
                notifTitle.value = 'Action impossible';
                notifMessage.value = "Vous n'avez aucun crédit, veuillez acheter un pack.";
                notifShow.value = true;
                return; 
            }

            try {
                router.push(`/contractwritter/${contract_id}`);
                console.log("Navigation vers le générateur avec l'id :", contract_id);
            } catch(err: any) {
                console.warn("Un avertissement est survenu lors de la redirection", err);
            }
        }

        const handlePageChange = (newPage: number) => {
            const currentQuery = route.query.q as string;
            
            if (currentQuery) {
                contratStore.fetchContracts(newPage, '', currentQuery);
            } 
            else {
                contratStore.getContracts(newPage);
            }
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        watch(() => route.query.q, (newQuery) => {
            if (newQuery) {
                contratStore.fetchContracts(1, '', newQuery as string);
            } else {
                contratStore.getContracts(1);
            }
        });

        onMounted(() => {
            if (route.query.q) {
                contratStore.fetchContracts(1, '', route.query.q as string);
            } else {
                contratStore.getContracts(1);
            }
        });

        return {
            router,
            route,
            contratStore,
            profileStore,
            topContracts, 
            fillContract,
            handlePageChange,
            // ⚡️ AJOUT : Exposition des variables pour le template
            notifShow,
            notifType,
            notifTitle,
            notifMessage
        }
    }
}
</script>

<style scoped>
.content-wrapper {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 3rem; 
}

.section-block {
    width: 100%;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1.5rem;
    padding-left: 0.5rem;
    border-left: 4px solid #3b82f6; 
}

.cards-container {
    width: 100%;
    max-width: 1400px;
    display: grid;
    grid-template-columns: 1fr;
    place-items: center;
    gap: 1.5rem;
}

.pagination-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 3rem;
    padding-bottom: 2rem;
}

@media (min-width: 768px) and (max-width: 1023px){
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