<template>
  <div class="inbox-wrapper">
    
    <!-- EN-TÊTE : RECHERCHE ET ONGLETS -->
    <div class="header-section">
      <div class="title-and-search">
        <h3 class="section-title">Boîte de réception</h3>
        
        <div class="search-box">
          <component :is="MagnifyingGlassIcon" class="icon-gray" />
          <input type="text" v-model="searchQuery" placeholder="Rechercher un client, un email..." />
        </div>
      </div>

      <div class="tabs-group">
        <button class="tab-btn" :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'">
          Toutes
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'review' }" @click="activeTab = 'review'">
          Révisions
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'custom' }" @click="activeTab = 'custom'">
          Sur-Mesure
        </button>
      </div>
    </div>

    <!-- TABLEAU DES MESSAGES -->
    <div class="panel clean-list-container">
      <table class="minimal-table">
        <thead>
          <tr>
            <th>Date & Heure</th>
            <th>Client (Contact)</th>
            <th>Type de demande</th>
            <th>Statut</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- Ligne non-lue : On rajoute la classe 'unread-row' -->
          <tr v-for="msg in filteredMessages" :key="msg.id" :class="{ 'unread-row': !msg.isRead }">
            
            <!-- Date -->
            <td>
              <div class="info-stack">
                <span :class="!msg.isRead ? 'dark-text font-bold' : 'gray-text'">{{ msg.date }}</span>
                <span class="gray-text text-sm">{{ msg.time }}</span>
              </div>
            </td>
            
            <!-- Client -->
            <td>
              <div class="info-stack">
                <span class="dark-text font-bold">{{ msg.clientName }}</span>
                <span class="gray-text text-sm">{{ msg.clientEmail }}</span>
              </div>
            </td>
            
            <!-- Type (Badges Pastel) -->
            <td>
              <span class="pastel-badge" :class="msg.type === 'review' ? 'badge-blue' : 'badge-purple'">
                {{ msg.type === 'review' ? 'Révision' : 'Sur-Mesure' }}
              </span>
            </td>
            
            <!-- Statut -->
            <td>
              <span class="status-dot" :class="getStatusDot(msg.status)"></span>
              <span class="dark-text font-bold">{{ msg.status }}</span>
            </td>
            
            <!-- Action -->
            <td class="text-right">
              <button class="pill-btn" @click="openMessage(msg)">
                <component :is="EyeIcon" class="icon-sm mr-1" />
                Ouvrir
              </button>
            </td>
            
          </tr>
        </tbody>
      </table>

      <!-- ÉTAT VIDE -->
      <div v-if="filteredMessages.length === 0" class="empty-state">
        <p class="gray-text">Aucun message trouvé dans cette catégorie.</p>
      </div>
    </div>

    <!-- MODALE IMPORTÉE -->
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
import adminInboxModal from '../../modale/adminInboxModale.vue'; // Vérifie bien le chemin
import { 
  MagnifyingGlassIcon, 
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
        id: 1, date: "05 Oct 2026", time: '10:45', 
        clientName: 'Yvan Pascal', clientEmail: 'yvan@exemple.com', clientPhone: '+225 07070707', 
        type: 'review', status: 'Nouveau', isRead: false, files: 1,
        description: "Bonjour, j'aimerais faire vérifier les clauses de confidentialité de ce contrat de prestation de service avant de le signer avec mon partenaire. Merci." 
      },
      { 
        id: 2, date: '12 Sep 2026', time: '14:30', 
        clientName: 'Entreprise XYZ', clientEmail: 'contact@xyz.ci', clientPhone: '+225 05050505', 
        type: 'custom', status: 'En cours', isRead: true, files: 0,
        description: "Nous avons besoin d'un contrat de partenariat exclusif sur-mesure pour la distribution de nos produits agricoles dans la sous-région OHADA." 
      },
      { 
        id: 3, date: '10 Jun 2026', time: '09:15', 
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

    const getStatusDot = (status: string) => {
      if (status === 'Nouveau') return 'dot-green';
      if (status === 'En cours') return 'dot-yellow';
      return 'dot-gray';
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
      getStatusDot, openMessage, closeMessage, markAsProcessed,
      MagnifyingGlassIcon, EyeIcon
    };
  }
}
</script>

<style scoped>
/* ==============================================================
   CHARTE GRAPHIQUE (MoonInc / ContratChap)
   ============================================================== */
.inbox-wrapper {
  --bg-main: #f8fafc;        
  --bg-panel: #ffffff;       
  --bg-panel-light: #f1f5f9; 
  --text-dark: #1e293b;      
  --text-gray: #94a3b8;      
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2rem; 
  font-family: 'Inter', sans-serif;
}

/* --- EN-TÊTE --- */
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-and-search { display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.2rem; color: var(--text-dark); font-weight: 700; margin: 0; }

.search-box {
  display: flex; align-items: center; gap: 0.8rem; background: var(--bg-panel);
  border: 1px solid #e2e8f0; border-radius: 50px; padding: 0.6rem 1.2rem; 
  flex: 1; max-width: 400px; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}
.search-box input { background: transparent; border: none; color: var(--text-dark); font-size: 0.9rem; outline: none; width: 100%; font-weight: 500; }
.search-box input::placeholder { color: #cbd5e1; font-weight: 400; }
.icon-gray { width: 18px; height: 18px; color: var(--text-gray); }

/* --- ONGLETS --- */
.tabs-group { display: flex; background: var(--primary-color); border-radius: 50px; padding: 0.3rem; width: fit-content; }
.tab-btn { 
  background: transparent; border: none; color: #ffffff; 
  font-size: 0.85rem; font-weight: 600; padding: 0.6rem 1.2rem; 
  border-radius: 50px; cursor: pointer; transition: all 0.2s ease; 
}
.tab-btn.active { background: var(--secondary-light-color); color: #ffffff; box-shadow: 0px 2px 10px rgba(0,0,0,0.05); }

/* --- PANNEAU & TABLEAU --- */
.clean-list-container {
  background: var(--bg-panel); border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03); border: 1px solid #f1f5f9;
  overflow-x: auto;
}
.minimal-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 800px; }
.minimal-table th { color: #cbd5e1; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding-bottom: 1.5rem; }
.minimal-table td { padding: 1.2rem 0; border-bottom: 1px solid #f8fafc; vertical-align: middle; transition: 0.2s; }
.minimal-table tr:last-child td { border-bottom: none; }

/* Ligne "Non lue" (Légère surbrillance pastel) */
.unread-row td { background-color: #f8fafc; }

/* --- ÉLÉMENTS DE LA TABLE --- */
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); font-size: 0.9rem; }
.font-bold { font-weight: 600; }
.text-right { text-align: right; }
.text-sm { font-size: 0.75rem; display: block; margin-top: 0.2rem; }
.mr-1 { margin-right: 0.2rem; }

/* Cellules Spéciales */
.info-stack { display: flex; flex-direction: column; }

/* Badges Pastel */
.pastel-badge { padding: 0.4rem 1rem; border-radius: 50px; font-size: 0.75rem; font-weight: 700; display: inline-block; }
.badge-blue { background: #eff6ff; color: #3b82f6; }
.badge-purple { background: #faf5ff; color: #a855f7; }

/* Statut Point */
.status-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 0.5rem; vertical-align: middle; }
.dot-green { background-color: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }
.dot-yellow { background-color: #f59e0b; }
.dot-gray { background-color: #cbd5e1; }

/* Boutons Actions */
.pill-btn {
  display: inline-flex; align-items: center; justify-content: center;
  background: white; border: 1px solid #e2e8f0; color: var(--text-dark);
  padding: 0.5rem 1.2rem; border-radius: 50px; font-size: 0.8rem; font-weight: 600; 
  cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.02); transition: 0.2s;
}
.pill-btn:hover { background: #f8fafc; border-color: #cbd5e1; }
.icon-sm { width: 16px; height: 16px; }

.empty-state { text-align: center; padding: 3rem 0; }
</style>