<template>
  <div class="folder-card" @click="$emit('action')">

    <div class="folder-back" :class="`back-${color}`">
      <div class="folder-tab" :class="`back-${color}`"></div>
    </div>

    <div v-if="hasItems" class="folder-papers">
      <div class="paper paper-1"></div>
      
      <div class="paper paper-2">
        <div class="paper-line line-long"></div>
        <div class="paper-line line-medium"></div>
        <div class="paper-line line-short"></div>
      </div>
    </div>

    <div class="folder-front" :class="`front-${color}`">
      <h4 class="folder-title" :title="title">{{ title }}</h4>
      <span class="folder-subtitle">{{ subtitle }}</span>
    </div>

  </div>
</template>

<script lang="ts">
export default {
  name: 'AdminFolderCard',
  props: {
    title: { 
      type: String, 
      required: true 
    },
    subtitle: { 
      type: String, 
      default: '' 
    },
    color: { 
      type: String, 
      default: 'gray' 
    },
    hasItems: { 
      type: Boolean, 
      default: false 
    }
  },
  emits: ['action'],
  setup() {
    return {};
  }
}
</script>

<style scoped>
/* =========================================
   CONTENEUR GLOBAL (Fluide)
   ========================================= */
.folder-card {
  position: relative;
  width: 100%;
  height: 110px; 
  cursor: pointer;
  margin-top: 15px; 
  transition: all 0.3s ease;
}

/* MICRO-ANIMATION AU SURVOL */
@media (hover: hover) {
  .folder-card:hover .folder-front { transform: translateY(2px); }
  .folder-card:hover .paper-1 { transform: translateY(-4px) rotate(-4deg); }
  .folder-card:hover .paper-2 { transform: translateY(-6px) rotate(3deg); }
}

/* =========================================
   1. LE DOS DU DOSSIER
   ========================================= */
.folder-back {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 100px;
  border-radius: 12px;
  z-index: 1;
  transition: height 0.3s ease;
}
.folder-tab {
  position: absolute;
  top: -12px; left: 0;
  width: 40%; 
  min-width: 50px; /* Sécurité : l'onglet ne devient jamais trop petit */
  max-width: 80px; /* Sécurité : l'onglet ne devient jamais trop grand */
  height: 20px;
  border-radius: 8px 8px 0 0;
}

/* =========================================
   2. LES FEUILLES DE PAPIER
   ========================================= */
.folder-papers {
  position: absolute;
  bottom: 10px; left: 10%; right: 10%; top: -10px;
  z-index: 2;
}
.paper {
  position: absolute;
  bottom: 0;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 4px 4px 0 0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.paper-1 {
  top: 5px; left: 0; right: 10%;
  transform: rotate(-2deg);
  transform-origin: bottom left;
}
.paper-2 {
  top: 0; left: 10%; right: 0;
  transform: rotate(2deg);
  transform-origin: bottom right;
  padding: 8px;
  display: flex; flex-direction: column; gap: 4px;
}

/* Lignes de texte factices */
.paper-line { height: 4px; background: #f1f5f9; border-radius: 2px; }
.line-long { width: 80%; }
.line-medium { width: 60%; }
.line-short { width: 40%; }

/* =========================================
   3. LE RABAT AVANT
   ========================================= */
.folder-front {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 80px; 
  border-radius: 12px;
  z-index: 3;
  padding: 1rem 0.8rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.04); 
  transition: all 0.3s ease;
}

.folder-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; /* Ajoute "..." si le titre est trop long */
}
.folder-subtitle {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* =========================================
   PALETTE DE COULEURS PASTEL
   ========================================= */
.front-blue { background-color: #a1d9ff; }
.back-blue { background-color: #77cfff; }
.front-purple { background-color: #6af986; }
.back-purple { background-color: #22cd4d; }
.front-orange { background-color: #ffedd5; }
.back-orange { background-color: #fed7aa; }
.front-gray { background-color: #f1f5f9; }
.back-gray { background-color: #e2e8f0; }

/* =========================================
   RESPONSIVE DESIGN (Mobiles)
   ========================================= */
@media (max-width: 480px) {
  .folder-card { height: 95px; margin-top: 10px; }
  .folder-back { height: 85px; }
  .folder-front { 
    height: 65px; 
    padding: 0.8rem 0.6rem; 
  }
  .folder-title { font-size: 0.85rem; }
  .folder-subtitle { font-size: 0.7rem; }
  .folder-tab { top: -10px; height: 15px; }
}
</style>