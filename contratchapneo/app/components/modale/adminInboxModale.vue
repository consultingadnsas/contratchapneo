<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      
      <!-- En-tête de la modale -->
      <div class="modal-header">
        <h3 class="modal-title">Détails de la demande</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <!-- Corps de la modale -->
      <div class="modal-body">
        
        <!-- Date et Heure mises en retrait -->
        <div class="timestamp-box">
          <span class="gray-text">Reçu le {{ message.date }} à {{ message.time }}</span>
        </div>

        <!-- Informations Client (Mises en avant) -->
        <div class="client-details">
          <div class="info-block">
            <p class="label-text">Nom du Client</p>
            <p class="client-name break-word">{{ message.clientName }}</p>
          </div>
          <div class="info-block">
            <p class="label-text">Email de contact</p>
            <p class="client-email break-word">{{ message.clientEmail }}</p>
            <span v-if="message.clientPhone" class="client-phone break-word">{{ message.clientPhone }}</span>
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
          
          <!-- Carte du fichier avec bouton en dessous -->
          <div class="file-item">
            <div class="file-info">
              <span class="doc-icon">📄</span>
              <span class="file-name break-word">Document_Client.pdf</span>
            </div>
            <button class="action-btn download-btn">
              <component :is="ArrowDownTrayIcon" class="icon-sm" /> Télécharger le document
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
/* L'OVERLAY */
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
.modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem; margin-bottom: 0.5rem; }
.modal-title { color: #0f172a; margin: 0; font-weight: 800; font-size: 1.3rem; }
.close-btn { background: #f1f5f9; border: none; color: #64748b; font-size: 1.5rem; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; flex-shrink: 0; }
.close-btn:hover { background: #e2e8f0; color: #1e293b; }

/* BODY */
.modal-body { display: flex; flex-direction: column; gap: 1.5rem; }

/* DATE ET HEURE (Mise en retrait) */
.timestamp-box { text-align: right; margin-top: -0.5rem; }
.gray-text { color: #64748b; font-size: 0.85rem; }

/* TITRES DE SECTIONS (Mise en avant) */
.label-text { 
  color: #334155; 
  font-size: 0.85rem; 
  font-weight: 800; 
  text-transform: uppercase; 
  letter-spacing: 0.5px; 
  margin: 0 0 0.5rem 0; 
}
.mb-2 { margin-bottom: 0.8rem; }

/* UTILITAIRE CRITIQUE : Empêche le texte de déborder */
.break-word {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-all;
  hyphens: auto;
  max-width: 100%;
}

/* BLOCS D'INFORMATIONS CLIENT */
.client-details { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.info-block { background: #f8fafc; padding: 1.2rem; border-radius: 16px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; }

/* Nom et Email ultra-lisibles */
.client-name { font-size: 1.2rem; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.3; }
.client-email { font-size: 1.1rem; font-weight: 700; color: #2563eb; margin: 0; line-height: 1.3; }
.client-phone { font-size: 0.9rem; color: #64748b; font-weight: 500; margin-top: 0.3rem; }

/* ZONE MESSAGE */
.message-content { background: #f8fafc; padding: 1.2rem; border-radius: 16px; border: 1px solid #e2e8f0; }
.message-content .dark-text { font-size: 1rem; line-height: 1.6; font-weight: 400; color: #1e293b; margin: 0; }

/* FICHIERS JOINTS (Bouton en dessous) */
.file-item { 
  display: flex; 
  flex-direction: column; /* Aligne les éléments verticalement */
  align-items: flex-start; /* Aligne le contenu à gauche */
  gap: 1rem; 
  background: #ffffff; 
  padding: 1rem 1.2rem; 
  border-radius: 16px; 
  border: 1px solid #cbd5e1; 
}
.file-info { display: flex; align-items: center; gap: 0.8rem; width: 100%; }
.doc-icon { background: #eff6ff; padding: 0.6rem; border-radius: 12px; font-size: 1.2rem; flex-shrink: 0; }
.file-name { font-size: 1.05rem; font-weight: 700; color: #0f172a; }

.action-btn { display: flex; align-items: center; gap: 0.5rem; border: none; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
.download-btn { color: #2563eb; background: #eff6ff; padding: 0.6rem 1.2rem; border-radius: 8px; width: 100%; justify-content: center; }
.download-btn:hover { background: #dbeafe; }
.icon-sm { width: 18px; height: 18px; }

/* FOOTER */
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid #f1f5f9; padding-top: 1.5rem; margin-top: 1rem; }
.btn-outline { background: white; border: 1px solid #cbd5e1; color: #475569; padding: 0.7rem 1.5rem; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-outline:hover { background: #f8fafc; border-color: #94a3b8; }
.btn-primary { display: flex; align-items: center; justify-content: center; gap: 0.5rem; background: #111827; color: #ffffff; border: none; padding: 0.7rem 1.5rem; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #1f2937; transform: translateY(-2px); }

/* RESPONSIVE */
@media (max-width: 600px) {
  .client-details { grid-template-columns: 1fr; } /* Passe sur 1 colonne */
  .modal-footer { flex-direction: column-reverse; }
  .btn-outline, .btn-primary { width: 100%; justify-content: center; }
}
</style>