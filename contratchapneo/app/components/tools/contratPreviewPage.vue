<template>
  <main class="preview-section">
    <div class="a4-document">
      
      <h1 class="doc-title reveal-text" style="animation-delay: 0.1s">
        APERÇU DU DOCUMENT
      </h1>

      <template v-if="store.tags && store.tags.length > 0">
        <p 
          v-for="(block, index) in store.tags" 
          :key="'block-' + index"
          class="doc-paragraph reveal-text"
          :style="{ animationDelay: `${0.2 + (index * 0.1)}s` }"
          v-html="formatContext(block.context, block.tags)"
        >
        </p>
      </template>
      
      <div v-else class="text-center" style="margin-top: 5rem; color: #6c757d;">
         <p>En attente de l'analyse du document...</p>
      </div>

      <div class="signatures reveal-text" style="animation-delay: 1s">
        <div class="sign-box">
          <p>Pour le Prestataire</p>
          <div class="sign-space"></div>
        </div>
        <div class="sign-box">
          <p>Pour le Client</p>
          <div class="sign-space"></div>
        </div>
      </div>
      
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useContratStore } from '../../stores/contratStore';

// On appelle le store pour avoir accès aux blocs de contextes (store.tags)
const store = useContratStore();

// Données tapées par l'utilisateur reçues via syncData
const contractData = ref<Record<string, any>>({});

// Fonction appelée par le parent pour mettre à jour les frappes
const syncData = (newData: Record<string, any>) => {
  contractData.value = { ...newData };
};

// 🪄 L'ASTUCE CONTRATCHAP : Remplacement dynamique MULTIPLE
// contextStr est le paragraphe, tagsInBlock est le tableau des variables (ex: ['nom_societe', 'capital'])
const formatContext = (contextStr: string, tagsInBlock: string[]) => {
  if (!contextStr) return '';
  
  let finalHtml = contextStr;

  // On boucle sur chaque variable présente dans ce paragraphe
  tagsInBlock.forEach(tagName => {
    // 1. On récupère la valeur tapée, ou on met un nom générique s'il n'a rien tapé
    const typedValue = contractData.value[tagName];
    const displayValue = typedValue ? typedValue : `[ ${tagName.replace(/_/g, ' ')} ]`;

    // 2. On crée le bloc HTML stylisé en bleu
    const highlightedHtml = `<span class="dynamic-data" style="color: #1a56db; background-color: rgba(26, 86, 219, 0.05); padding: 0 4px; border-radius: 2px;">${displayValue}</span>`;

    // 3. On remplace {{ variable }} dans la phrase par le bloc HTML
    const regex = new RegExp(`\\{\\{\\s*${tagName}\\s*\\}\\}`, 'g');
    finalHtml = finalHtml.replace(regex, highlightedHtml);
  });

  return finalHtml;
};

// Fonction optionnelle si tu veux déclencher l'envoi depuis ici
const submitToBackend = (finalData: Record<string, any>) => {
  console.log('🚀 Envoi au backend depuis preview :', finalData);
};

// Très important : Exposer les fonctions pour que le Parent puisse les appeler via sa ref="previewRef"
defineExpose({
  syncData,
  submitToBackend
});
</script>

<style scoped>
/* =========================================
   ANIMATION DE RÉVÉLATION PROGRESSIVE
   ========================================= */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.reveal-text {
  opacity: 0; /* caché avant l'animation */
  animation: fadeInUp 0.6s ease forwards;
}

/* =========================================
   FAUX DOCUMENT A4 (Droite/Bas)
   ========================================= */
.preview-section {
  flex: 2;
  display: flex;
  justify-content: center;
  overflow-x: auto;
}

.a4-document {
  background: #ffffff;
  width: 100%;
  max-width: 210mm;
  min-height: 297mm;
  padding: 12% 10%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  font-family: 'Times New Roman', Times, serif;
  color: #000000;
  line-height: 1.6;
}

.dynamic-data {
  color: #1a56db;
  background-color: rgba(26, 86, 219, 0.05);
  padding: 0 4px;
  border-radius: 2px;
}

.doc-title {
  text-align: center;
  font-size: 1.4rem;
  text-decoration: underline;
  margin-bottom: 3rem;
  text-transform: uppercase;
}

.doc-subtitle {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  text-decoration: underline;
}

.doc-paragraph {
  margin-bottom: 1.2rem;
  text-align: justify;
}

.doc-paragraph-end {
  margin-bottom: 1.2rem;
  text-align: end;
}

.signatures {
  display: flex;
  justify-content: space-between;
  margin-top: 5rem;
}

.sign-box {
  width: 40%;
}

.sign-box p {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.sign-space {
  border-top: 1px dotted #000;
  height: 100px;
  margin-top: 3rem;
}
</style>