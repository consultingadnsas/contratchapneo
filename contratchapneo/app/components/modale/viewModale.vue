<template>
  <div class="view-modale" @click.self="$emit('close')">
    <div class="modal-content">
      
      <button class="close-btn" @click="$emit('close')" aria-label="Fermer">
        X
      </button>

      <client-only>
        <vue-pdf-embed
          :source="pdfSource"
          class="pdf-preview"
        />
      </client-only>

    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineAsyncComponent } from 'vue';

// Import asynchrone pour Nuxt (SSR)
const VuePdfEmbed = defineAsyncComponent(() => import('vue-pdf-embed'));

export default {
  components: {
    VuePdfEmbed
  },
  props: {
    file: {
      type: String,
      default: '' 
    }
  },
  emits: ['close'],
  
  setup(props) {
    
    const pdfSource = computed(() => {
      if (!props.file) return '';

      if (props.file.startsWith('data:application/pdf;base64,')) {
        
        if (typeof window === 'undefined') return '';

        try {
          // 1. On sépare l'entête "data:application..." du contenu pur
          let base64Data = props.file.split(',')[1];
          
          // 2. CORRECTION : On supprime tous les espaces et retours à la ligne invisibles
          base64Data = base64Data.replace(/\s/g, '');
          
          // 3. On convertit le texte Base64 propre en tableau binaire
          const binaryString = window.atob(base64Data);
          const bytes = new Uint8Array(binaryString.length);
          for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
          }
          
          // 4. On crée un fichier virtuel (Blob) et on génère un lien local
          const blob = new Blob([bytes], { type: 'application/pdf' });
          return URL.createObjectURL(blob);
          
        } catch (error) {
          console.error("Erreur de décodage du PDF:", error);
          return props.file; 
        }
      }

      return props.file;
    });

    return {
      pdfSource
    };
  }
}
</script>

<style scoped>
.view-modale {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  position: relative;
  width: 90%;
  max-width: 900px;
  height: 90vh;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  /* Optionnel: Ajout d'une petite ombre pour le relief */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 50%;
  background: black;
  color: white;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.close-btn:hover {
  background: #333;
}

.pdf-preview {
  width: 100%;
  height: 100%;
  overflow-y: auto; /* Permet le scroll vertical interne si le PDF est long */
}
</style>