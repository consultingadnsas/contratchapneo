<template>
  <main class="preview-section">
    <div class="a4-document">

      <!-- 
        <h1 class="doc-title reveal-text" style="animation-delay: 0.1s">
          {{ store.contrat?.title || "Votre contrat" }}
        </h1>
      -->

      <template v-if="formattedBlocks.length > 0">
        <p
          v-for="(block, index) in formattedBlocks"
          :key="'block-' + index"
          class="doc-paragraph reveal-text"
          :style="{ animationDelay: `${0.2 + (index * 0.1)}s` }"
        >
          <!-- 🔹 Affichage des nœuds (texte ou tag) -->
          <template v-for="(node, nodeIndex) in block.nodes" :key="'node-' + index + '-' + nodeIndex">
            <span v-if="node.type === 'text'">{{ node.content }}</span>
            <input
              v-else-if="node.type === 'tag'"
              v-model="contractData[node.tagName]"
              class="dynamic-input"
              :type="getInputType(node.tagName)"
              :placeholder="node.tagName.replace(/_/g, ' ')"
              :style="{ width: Math.max(15, (contractData[node.tagName]?.toString().length || node.tagName.length)) + 'ch' }"
            />
          </template>
        </p>
      </template>

      <div v-else-if="store.tags && store.tags.length === 0" class="no-tags-state" style="text-align: center; margin-top: 5rem;">
         <p style="color: #6c757d;">Ce document ne nécessite aucune information supplémentaire. Il est prêt !</p>
      </div>

      <div v-else class="text-center" style="margin-top: 5rem; color: #6c757d;">
         <p>En attente de l'analyse du document...</p>
      </div>

      <!-- 
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
      -->
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useContratStore } from '../../stores/contratStore';
import { usePaiementStore } from '../../stores/paiementStore'
// On appelle le store pour avoir accès aux blocs de contextes (store.tags)
const store = usePaiementStore();

const emit = defineEmits(['validity-change', 'tags-loaded']);

// Données tapées par l'utilisateur reçues via syncData
const contractData = ref<Record<string, any>>({});

// Compute unique tags pour l'initialisation et la validation
const uniqueTags = computed(() => {
  if (!store.tags || store.tags.length === 0) return [];
  const allTags = new Set<string>();
  store.tags.forEach((block: any) => {
    if (block.tags && Array.isArray(block.tags)) {
      block.tags.forEach((tag: string) => allTags.add(tag));
    }
  });
  return Array.from(allTags);
});

import { watch } from 'vue';

watch(uniqueTags, (tags) => {
  emit('tags-loaded', tags.length === 0 && store.tags && store.tags.length > 0);
  
  tags.forEach(tag => {
    if (!(tag in contractData.value)) {
      contractData.value[tag] = '';
    }
  });
}, { immediate: true });

const isFormValid = computed(() => {
  if (uniqueTags.value.length === 0) return true;
  return uniqueTags.value.every(tag => {
    const value = contractData.value[tag];
    return value !== undefined && value !== null && String(value).trim() !== '';
  });
});

watch(isFormValid, (isValid) => {
  emit('validity-change', isValid);
}, { immediate: true });

const getInputType = (tagName: string) => {
  if (tagName.startsWith('date_')) return 'date';
  if (tagName.startsWith('num_')) return 'number';
  if (tagName.startsWith('email_')) return 'email';
  return 'text';
};

// 🪄 L'ASTUCE CONTRATCHAP : Remplacement dynamique MULTIPLE
// contextStr est le paragraphe, tagsInBlock est le tableau des variables (ex: ['nom_societe', 'capital'])
// On ajoute un data-tag-anchor sur chaque span généré : c'est ce qui permet
// de retrouver précisément le bon passage du document depuis le formulaire.
// (Un data-attribute plutôt qu'un id classique : si jamais le même tag est
// utilisé dans deux paragraphes différents, on évite des id HTML dupliqués.)
// 🔹 NOUVELLE LOGIQUE : Découpage du texte en nœuds réactifs
const formattedBlocks = computed(() => {
  if (!store.tags || store.tags.length === 0) return [];

  return store.tags.map((block) => {
    const nodes: Array<{ type: 'text'; content: string } | { type: 'tag'; content: string; tagName: string }> = [];
    let remainingText = block.context;

    // 1. Trouver toutes les positions des tags dans ce bloc
    const tagMatches: Array<{ tag: string; start: number; end: number }> = [];
    block.tags.forEach((tagName: string) => {
      const regex = new RegExp(`\\{\\{\\s*${tagName}\\s*\\}\\}`, 'g');
      let match;
      while ((match = regex.exec(block.context)) !== null) {
        tagMatches.push({
          tag: tagName,
          start: match.index,
          end: match.index + match[0].length,
        });
      }
    });

    // 2. Trier les matches par position dans le texte
    tagMatches.sort((a, b) => a.start - b.start);

    // 3. Découper le texte en morceaux (texte normal + tags)
    let lastIndex = 0;
    tagMatches.forEach((match) => {
      // Ajouter le texte avant le tag
      if (match.start > lastIndex) {
        nodes.push({
          type: 'text',
          content: block.context.slice(lastIndex, match.start),
        });
      }

      // Ajouter le tag
      nodes.push({
        type: 'tag',
        content: '',
        tagName: match.tag,
      });

      lastIndex = match.end;
    });

    // Ajouter le texte restant après le dernier tag
    if (lastIndex < block.context.length) {
      nodes.push({
        type: 'text',
        content: block.context.slice(lastIndex),
      });
    }

    return { ...block, nodes };
  });
});

// Appelée depuis index.vue quand un champ du formulaire reçoit le focus (desktop uniquement).
// Elle scrolle jusqu'au passage correspondant dans le document et le fait
// "flasher" brièvement pour bien montrer l'endroit désigné.
const scrollToField = (tagName: string) => {
  const elements = document.querySelectorAll<HTMLElement>(`[data-tag-anchor="${tagName}"]`);
  if (elements.length === 0) return;

  // Scroll vers le premier élément
  elements[0]?.scrollIntoView({ behavior: 'smooth', block: 'center' });

  // Faire pulser TOUTES les occurrences
  elements.forEach(el => {
    el.classList.add('tag-highlight-pulse');
  });
  setTimeout(() => {
    elements.forEach(el => {
      el.classList.remove('tag-highlight-pulse');
    });
  }, 1600);
};

// Fonction optionnelle si tu veux déclencher l'envoi depuis ici
const submitToBackend = (finalData: Record<string, any>) => {
  console.log('🚀 Envoi au backend depuis preview :', finalData);
};

const getContractData = () => {
  return contractData.value;
};

// Très important : Exposer les fonctions pour que le Parent puisse les appeler via sa ref="previewRef"
defineExpose({
  getContractData,
  submitToBackend,
  scrollToField
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
   MISE EN ÉVIDENCE AU CLIC SUR UN CHAMP
   ========================================= */
@keyframes tagPulse {
  0%   { box-shadow: 0 0 0 0 rgba(26, 86, 219, 0.45); background-color: rgba(26, 86, 219, 0.35); }
  70%  { box-shadow: 0 0 0 8px rgba(26, 86, 219, 0); }
  100% { box-shadow: 0 0 0 0 rgba(26, 86, 219, 0); background-color: rgba(26, 86, 219, 0.05); }
}

:deep(.tag-highlight-pulse) {
  animation: tagPulse 1.4s ease-out;
  border-radius: 3px;
}

/* =========================================
   FAUX DOCUMENT A4 (Droite/Bas)
   ========================================= */
.preview-section {
  flex: 2;
  display: flex;
  justify-content: center;
  align-items: flex-start;
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

.dynamic-input {
  color: #1a56db;
  background-color: transparent;
  border: none;
  border-bottom: 2px dashed #1a56db;
  font-family: inherit;
  font-size: inherit;
  padding: 0 4px;
  text-align: center;
  transition: all 0.2s;
  outline: none;
}

.dynamic-input:focus {
  background-color: rgba(26, 86, 219, 0.1);
  border-bottom-style: solid;
}

.dynamic-input::placeholder {
  color: #9ca3af;
  font-style: italic;
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