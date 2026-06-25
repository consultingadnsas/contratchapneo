<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content panel">
      <div class="modal-header">
        <h3 class="text-white">Détails de la demande</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="client-details">
          <div>
            <p class="text-gray text-xs uppercase">Client</p>
            <p class="text-white font-bold">{{ message.clientName }}</p>
          </div>
          <div>
            <p class="text-gray text-xs uppercase">Contact</p>
            <p class="text-white">{{ message.clientEmail }} <br> {{ message.clientPhone }}</p>
          </div>
          <div>
            <p class="text-gray text-xs uppercase">Date</p>
            <p class="text-white">{{ message.date }} à {{ message.time }}</p>
          </div>
        </div>

        <div class="message-box">
          <p class="text-gray text-xs uppercase mb-2">Message / Contexte</p>
          <p class="text-white description-text">{{ message.description }}</p>
        </div>

        <div class="attachments" v-if="message.files > 0">
          <p class="text-gray text-xs uppercase mb-2">Fichiers joints ({{ message.files }})</p>
          <div class="file-item">
            <span class="text-white flex-align"><span class="doc-icon">📄</span> Document_Client.pdf</span>
            <button class="action-btn download-btn">
              <component :is="ArrowDownTrayIcon" class="icon-sm text-blue" /> Télécharger
            </button>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn-outline" @click="$emit('close')">Fermer</button>
        <button class="btn-primary" @click="$emit('mark-processed', message.id)">
          <component :is="CheckCircleIcon" class="icon-sm" /> Marquer comme traité
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { PropType } from 'vue';
import { CheckCircleIcon, ArrowDownTrayIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'AdminInboxModal',
  props: {
    message: {
      type: Object as PropType<any>,
      required: true
    }
  },
  emits: ['close', 'mark-processed'],
  setup() {
    return {
      CheckCircleIcon,
      ArrowDownTrayIcon
    };
  }
}
</script>

<style scoped>
/* COULEURS ET VARIABLES */
.modal-overlay {
  --bg-panel: #161618;
  --bg-panel-light: #1e1e20;
  --border-color: #2a2a2c;
  --text-main: #ffffff;
  --text-muted: #8a8a8e;
  --accent-blue: #0A84FF;
  
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
  background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); 
  display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem; 
}
.modal-content { 
  width: 100%; max-width: 600px; display: flex; flex-direction: column; gap: 1.5rem; 
  box-shadow: 0 20px 40px rgba(0,0,0,0.5); background: var(--bg-panel); 
  border: 1px solid var(--border-color); border-radius: 20px; padding: 1.5rem;
  font-family: 'Inter', sans-serif;
}

/* HEADER */
.modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; }
.text-white { color: var(--text-main); margin: 0; }
.close-btn { background: transparent; border: none; color: var(--text-muted); font-size: 1.5rem; cursor: pointer; }
.close-btn:hover { color: var(--text-main); }

/* BODY */
.modal-body { display: flex; flex-direction: column; gap: 1.5rem; }
.client-details { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; background: var(--bg-panel-light); padding: 1rem; border-radius: 12px; }
.text-gray { color: var(--text-muted); margin: 0; }
.text-xs { font-size: 0.75rem; }
.uppercase { text-transform: uppercase; letter-spacing: 0.5px; }
.font-bold { font-weight: 600; }
.mb-2 { margin-bottom: 0.5rem; }
.description-text { line-height: 1.6; font-size: 0.95rem; background: rgba(255,255,255,0.02); padding: 1rem; border-radius: 12px; border: 1px solid var(--border-color); margin: 0; }

/* ATTACHMENTS */
.doc-icon { background: var(--bg-panel); padding: 0.4rem; border-radius: 8px; font-size: 1.1rem; }
.file-item { display: flex; justify-content: space-between; align-items: center; background: var(--bg-panel-light); padding: 0.8rem 1rem; border-radius: 12px; border: 1px solid var(--border-color); }
.flex-align { display: flex; align-items: center; gap: 0.5rem; }
.action-btn { display: flex; align-items: center; gap: 0.4rem; background: var(--bg-panel-light); border: 1px solid var(--border-color); color: var(--text-main); padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.8rem; cursor: pointer; transition: 0.2s; }
.download-btn { border-color: rgba(10, 132, 255, 0.3); color: var(--accent-blue); }
.download-btn:hover { background: rgba(10, 132, 255, 0.1); }
.icon-sm { width: 18px; height: 18px; }
.text-blue { color: var(--accent-blue); }

/* FOOTER */
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid var(--border-color); padding-top: 1rem; }
.btn-outline { background: transparent; border: 1px solid var(--border-color); color: var(--text-main); padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; }
.btn-primary { display: flex; align-items: center; gap: 0.5rem; background: var(--text-main); color: #000; border: none; padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 600; cursor: pointer; }
.btn-primary:hover { opacity: 0.9; }
</style>