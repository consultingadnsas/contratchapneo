<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      
      <!-- En-tête de la modale -->
      <div class="modal-header">
        <h3 class="dark-text">Détails de la demande</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <!-- Corps de la modale -->
      <div class="modal-body">
        
        <!-- Informations Client (Grid pastel) -->
        <div class="client-details">
          <div class="info-block">
            <p class="label-text">Client</p>
            <p class="dark-text font-bold">{{ message.clientName }}</p>
          </div>
          <div class="info-block">
            <p class="label-text">Contact</p>
            <p class="dark-text">{{ message.clientEmail }} <br> <span class="gray-text">{{ message.clientPhone }}</span></p>
          </div>
          <div class="info-block">
            <p class="label-text">Date & Heure</p>
            <p class="dark-text">{{ message.date }} <br> <span class="gray-text">{{ message.time }}</span></p>
          </div>
        </div>

        <!-- Zone du message -->
        <div class="message-box">
          <p class="label-text mb-2">Message / Contexte</p>
          <div class="message-content">
            <p class="dark-text">{{ message.description }}</p>
          </div>
        </div>

        <!-- Fichiers joints -->
        <div class="attachments" v-if="message.files > 0">
          <p class="label-text mb-2">Fichiers joints ({{ message.files }})</p>
          <div class="file-item">
            <div class="flex-align">
              <span class="doc-icon">📄</span>
              <span class="dark-text font-bold">Document_Client.pdf</span>
            </div>
            <button class="action-btn download-btn">
              <component :is="ArrowDownTrayIcon" class="icon-sm" /> Télécharger
            </button>
          </div>
        </div>

      </div>

      <!-- Pied de la modale -->
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
/* L'OVERLAY (Plus clair pour correspondre au thème) */
.modal-overlay { 
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
  background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px); 
  display: flex; justify-content: center; align-items: center; z-index: 1000; padding: 1rem; 
}

/* LE CONTENEUR DE LA MODALE */
.modal-content { 
  width: 100%; max-width: 650px; max-height: 90vh; overflow-y: auto; 
  background: #ffffff; border-radius: 24px; padding: 2rem; 
  font-family: 'Inter', sans-serif; box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}

/* Scrollbar discrète */
.modal-content::-webkit-scrollbar { width: 6px; }
.modal-content::-webkit-scrollbar-track { background: transparent; }
.modal-content::-webkit-scrollbar-thumb { background-color: #e2e8f0; border-radius: 10px; }

/* HEADER */
.modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem; margin-bottom: 1.5rem; }
.dark-text { color: #1e293b; margin: 0; font-weight: 700; font-size: 1.2rem; }
.close-btn { background: #f1f5f9; border: none; color: #64748b; font-size: 1.5rem; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }
.close-btn:hover { background: #e2e8f0; color: #1e293b; }

/* BODY */
.modal-body { display: flex; flex-direction: column; gap: 1.5rem; }
.font-bold { font-weight: 600; }
.gray-text { color: #94a3b8; font-size: 0.85rem; }
.label-text { color: #cbd5e1; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 0.2rem 0; }
.mb-2 { margin-bottom: 0.5rem; }

/* BLOCS D'INFORMATIONS */
.client-details { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; }
.info-block { background: #f8fafc; padding: 1rem; border-radius: 16px; border: 1px solid #f1f5f9; }

/* ZONE MESSAGE */
.message-content { background: #f8fafc; padding: 1.2rem; border-radius: 16px; border: 1px solid #f1f5f9; }
.message-content .dark-text { font-size: 0.95rem; line-height: 1.6; font-weight: 400; }

/* FICHIERS JOINTS */
.file-item { display: flex; justify-content: space-between; align-items: center; background: #ffffff; padding: 0.8rem 1rem; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
.flex-align { display: flex; align-items: center; gap: 0.8rem; }
.doc-icon { background: #eff6ff; padding: 0.5rem; border-radius: 10px; font-size: 1.2rem; }
.action-btn { display: flex; align-items: center; gap: 0.4rem; background: transparent; border: none; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
.download-btn { color: #2563eb; background: #eff6ff; padding: 0.4rem 1rem; border-radius: 50px; }
.download-btn:hover { background: #dbeafe; }
.icon-sm { width: 18px; height: 18px; }

/* FOOTER */
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid #f1f5f9; padding-top: 1.5rem; margin-top: 1rem; }
.btn-outline { background: white; border: 1px solid #e2e8f0; color: #475569; padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-outline:hover { background: #f8fafc; }
.btn-primary { display: flex; align-items: center; gap: 0.5rem; background: #2563eb; color: #ffffff; border: none; padding: 0.6rem 1.2rem; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); }
.btn-primary:hover { background: #1d4ed8; transform: translateY(-2px); }

/* RESPONSIVE */
@media (max-width: 480px) {
  .modal-content { padding: 1.2rem; }
  .modal-footer { flex-direction: column; }
  .btn-outline, .btn-primary { width: 100%; justify-content: center; }
}
</style>