<template>
  <div class="inbox-wrapper">
    
    <!-- EN-TÊTE : RECHERCHE ET ONGLETS -->
    <div class="header-section">
      <div class="title-and-search">
        <h2 class="page-title">Boîte de réception</h2>
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-sm text-gray" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher un client, un email..." />
        </div>
      </div>

      <div class="tabs-group">
        <button class="tab-btn" :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'">
          <component :is="InboxIcon" class="icon-sm" /> Toutes
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'review' }" @click="activeTab = 'review'">
          <component :is="DocumentMagnifyingGlassIcon" class="icon-sm" /> Révisions
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'custom' }" @click="activeTab = 'custom'">
          <component :is="PencilSquareIcon" class="icon-sm" /> Sur-Mesure
        </button>
      </div>
    </div>

    <!-- TABLEAU DES MESSAGES -->
    <div class="panel">
      <table class="clean-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Client (Contact)</th>
            <th>Type de demande</th>
            <th>Statut</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="msg in filteredMessages" :key="msg.id" :class="{ 'unread': !msg.isRead }">
            
            <td class="text-gray time-cell">
              <span class="date text-white font-bold" v-if="!msg.isRead">{{ msg.date }}</span>
              <span class="date" v-else>{{ msg.date }}</span>
              <span class="time">{{ msg.time }}</span>
            </td>
            
            <td>
              <div class="client-info">
                <span class="font-bold" :class="!msg.isRead ? 'text-white' : 'text-gray'">{{ msg.clientName }}</span>
                <span class="client-contact">{{ msg.clientEmail }} • {{ msg.clientPhone }}</span>
              </div>
            </td>
            
            <td>
              <span class="badge" :class="msg.type === 'review' ? 'badge-blue' : 'badge-purple'">
                {{ msg.type === 'review' ? 'Révision de contrat' : 'Contrat Sur-Mesure' }}
              </span>
            </td>
            
            <td class="font-bold" :class="getStatusColor(msg.status)">
              {{ msg.status }}
            </td>
            
            <td class="text-right flex-align-right">
              <button class="action-btn view-btn" @click="openMessage(msg)" title="Lire la demande">
                <component :is="EyeIcon" class="icon-sm text-white" /> Lire
              </button>
            </td>
            
          </tr>
        </tbody>
      </table>

      <!-- ÉTAT VIDE -->
      <div v-if="filteredMessages.length === 0" class="empty-state">
        <p class="text-gray">Aucun message trouvé dans cette catégorie.</p>
      </div>
    </div>

    <!-- APPEL PROPRE DE LA NOUVELLE MODALE -->
    <adminInboxModal 
      v-if="selectedMessage" 
      :message="selectedMessage" 
      @close="closeMessage" 
      @mark-processed="markAsProcessed"
    />

  </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import adminInboxModal from '../../modale/adminInboxModale.vue'; // <-- N'oublie pas d'importer ton nouveau composant
import { 
  MagnifyingGlassIcon, 
  InboxIcon, 
  DocumentMagnifyingGlassIcon, 
  PencilSquareIcon,
  EyeIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminInbox',
  components: {
    adminInboxModal
  },
  setup() {
    const activeTab = ref('all');
    const searchQuery = ref('');
    const selectedMessage = ref<any>(null);

    const messages = ref([
      { 
        id: 1, date: "Aujourd'hui", time: '10:45', 
        clientName: 'Yvan Pascal', clientEmail: 'yvan@exemple.com', clientPhone: '+225 07070707', 
        type: 'review', status: 'Nouveau', isRead: false, files: 1,
        description: "Bonjour, j'aimerais faire vérifier les clauses de confidentialité de ce contrat de prestation de service avant de le signer avec mon partenaire. Merci." 
      },
      { 
        id: 2, date: 'Hier', time: '14:30', 
        clientName: 'Entreprise XYZ', clientEmail: 'contact@xyz.ci', clientPhone: '+225 05050505', 
        type: 'custom', status: 'En cours', isRead: true, files: 0,
        description: "Nous avons besoin d'un contrat de partenariat exclusif sur-mesure pour la distribution de nos produits agricoles dans la sous-région OHADA." 
      },
      { 
        id: 3, date: '10 Juin 2024', time: '09:15', 
        clientName: 'Awa Sylla', clientEmail: 'awa.sylla@yahoo.fr', clientPhone: '+221 77777777', 
        type: 'review', status: 'Traité', isRead: true, files: 2,
        description: "Veuillez analyser ce contrat de bail commercial. Le propriétaire a ajouté des clauses qui me semblent abusives concernant les charges." 
      },
    ]);

    const filteredMessages = computed(() => {
      let list = messages.value;
      if (activeTab.value !== 'all') {
        list = list.filter(msg => msg.type === activeTab.value);
      }
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        list = list.filter(msg => 
          msg.clientName.toLowerCase().includes(query) ||
          msg.clientEmail.toLowerCase().includes(query)
        );
      }
      return list;
    });

    const getStatusColor = (status: string) => {
      if (status === 'Nouveau') return 'text-green';
      if (status === 'En cours') return 'text-blue';
      return 'text-gray';
    };

    const openMessage = (msg: any) => {
      msg.isRead = true;
      selectedMessage.value = msg;
    };

    const closeMessage = () => {
      selectedMessage.value = null;
    };

    const markAsProcessed = (id: number) => {
      const msg = messages.value.find(m => m.id === id);
      if (msg) {
        msg.status = 'Traité';
      }
      closeMessage();
    };

    return {
      activeTab, searchQuery, filteredMessages, selectedMessage,
      getStatusColor, openMessage, closeMessage, markAsProcessed,
      MagnifyingGlassIcon, InboxIcon, DocumentMagnifyingGlassIcon, PencilSquareIcon, EyeIcon
    };
  }
}
</script>

<style scoped>
.inbox-wrapper {
  --bg-panel: #161618;
  --bg-panel-light: #1e1e20;
  --border-color: #2a2a2c;
  --text-main: #ffffff;
  --text-muted: #8a8a8e;
  --accent-blue: #0A84FF;
  --accent-green: #30D158;
  --accent-purple: #BF5AF2;
  display: flex; flex-direction: column; gap: 1.5rem; font-family: 'Inter', sans-serif;
}

/* EN-TÊTE */
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-and-search { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.page-title { color: var(--text-main); font-size: 1.2rem; font-weight: 600; margin: 0; }
.search-box { display: flex; align-items: center; gap: 0.5rem; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 50px; padding: 0.6rem 1.2rem; flex: 1; max-width: 400px; }
.search-box input { background: transparent; border: none; color: var(--text-main); font-size: 0.9rem; outline: none; width: 100%; }
.search-box input::placeholder { color: var(--text-muted); }

/* ONGLETS */
.tabs-group { display: flex; background: var(--bg-panel); border-radius: 50px; padding: 0.3rem; border: 1px solid var(--border-color); width: fit-content; }
.tab-btn { display: flex; align-items: center; gap: 0.5rem; background: transparent; border: none; color: var(--text-muted); font-size: 0.85rem; font-weight: 500; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: 0.2s; }
.tab-btn.active { background: var(--bg-panel-light); color: var(--text-main); border: 1px solid var(--border-color); }
.icon-sm { width: 18px; height: 18px; }

/* TABLEAU */
.panel { background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 20px; padding: 1.5rem; overflow-x: auto; }
.clean-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 800px; }
.clean-table th { color: var(--text-muted); font-size: 0.8rem; font-weight: 500; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }
.clean-table td { padding: 1rem 0; font-size: 0.9rem; border-bottom: 1px solid rgba(255,255,255,0.02); vertical-align: middle; }
.clean-table tr:hover td { background-color: rgba(255,255,255,0.01); }
.unread td { background-color: rgba(48, 209, 88, 0.03); }

/* ÉLÉMENTS DE LA TABLE */
.text-white { color: var(--text-main); }
.text-gray { color: var(--text-muted); }
.text-green { color: var(--accent-green); }
.text-blue { color: var(--accent-blue); }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.flex-align-right { display: flex; justify-content: flex-end; align-items: center; gap: 0.5rem; }
.badge { padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.75rem; font-weight: 600; }
.badge-blue { background: rgba(10, 132, 255, 0.1); color: var(--accent-blue); border: 1px solid rgba(10, 132, 255, 0.2); }
.badge-purple { background: rgba(191, 90, 242, 0.1); color: var(--accent-purple); border: 1px solid rgba(191, 90, 242, 0.2); }
.time-cell { display: flex; flex-direction: column; gap: 0.2rem; }
.time { font-size: 0.75rem; }
.client-info { display: flex; flex-direction: column; gap: 0.2rem; }
.client-contact { font-size: 0.75rem; color: var(--text-muted); }
.action-btn { display: flex; align-items: center; gap: 0.4rem; background: var(--bg-panel-light); border: 1px solid var(--border-color); color: var(--text-main); padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.8rem; cursor: pointer; transition: 0.2s; }
.view-btn:hover { background: rgba(255,255,255,0.05); }
.empty-state { text-align: center; padding: 3rem 0; }
</style>