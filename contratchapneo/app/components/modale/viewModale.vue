<template>
  <div class="view-modale" @click.self="$emit('close')">
    <div class="modal-content">
      
      <button class="close-btn" @click="$emit('close')" aria-label="Fermer">
        X
      </button>

      <div class="word-preview-container">
        <div class="page-a4">
          
          <p class="document-text">
            {{ previewText }}
          </p>
          
          <div class="fade-bottom"></div>
        </div>
      </div>

    </div>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    // On renomme la prop en 'previewText' car ce n'est plus un 'file' (fichier physique), mais du texte
    previewText: {
      type: String,
      default: 'Aperçu du document non disponible...' 
    }
  },
  emits: ['close'],
  
  setup() {
    // 🎉 Regarde comme c'est vide ! 
    // Plus besoin de Computed complexes ni de décodage Base64.
    // Vue.js s'occupe juste d'afficher la variable de la prop directement.
    return {};
  }
}
</script>

<style scoped>
/* --- Styles de la modale inchangés --- */
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
  background: #f3f4f6; /* Un gris clair autour de la page pour bien la faire ressortir */
  border-radius: 12px;
  overflow: hidden;
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

.word-preview-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: flex-start; /* ← empêche le stretch qui causait la coupure */
}

.page-a4 {
  background: white;
  width: 100%;
  max-width: 700px;
  padding: 3rem 4rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  position: relative;
  /* min-height: 100% n'est plus nécessaire ici, mais tu peux le garder si tu veux que la page A4 fasse au moins la hauteur de la fenêtre quand le texte est court */
  min-height: 100%;
}

.document-text {
  white-space: pre-wrap; /* ⚠️ TRÈS IMPORTANT : Garde les sauts de lignes de ton backend */
  font-family: 'Times New Roman', Times, serif; /* Police classique et pro des contrats */
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
  text-align: justify; /* Aligne le texte à gauche et à droite */
}

/* L'effet de dégradé blanc à la fin de l'aperçu */
.fade-bottom {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 150px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
  pointer-events: none; /* Empêche le dégradé de bloquer les clics de la souris */
}
</style>