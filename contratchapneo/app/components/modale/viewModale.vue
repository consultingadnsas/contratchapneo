<template>
  <div class="view-modale" @click.self="$emit('close')">
    <div class="modal-content">
      
      <!-- BOUTON FERMER -->
      <button class="close-btn" @click="$emit('close')" aria-label="Fermer">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- BLOC 1 : TITRE & DESCRIPTION (En haut sur mobile, à droite sur PC) -->
      <div class="info-header-section">
        <h2 class="contract-title">{{ contract?.title || 'Titre du contrat' }}</h2>
        <div class="contract-description">
          <p>{{ contract?.description || 'Aucune description détaillée fournie pour ce document.' }}</p>
        </div>
      </div>

      <!-- BLOC 2 : APERÇU DU DOCUMENT (Au centre sur mobile, à gauche sur PC) -->
      <div class="preview-section">
        <div class="page-a4">
          <p class="document-text">
            {{ contract?.document_preview || "L'aperçu de ce document n'est pas encore disponible." }}
          </p>
          <div class="fade-bottom"></div>
        </div>
      </div>

      <!-- BLOC 3 : FOOTER D'ACHAT (Verrouillé en bas partout) -->
      <div class="action-footer">
        <div class="price-container">
          <span class="price-amount">{{ formatPrice(contract?.prix) }}</span>
          <span class="price-currency">FCFA</span>
        </div>

        <button class="btn-buy" @click="handleFlyToCart($event)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="cart-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
          </svg>
          <span>Acheter</span>
        </button>
      </div>

    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

interface Contrat {
  id?: string;
  category: string;
  title: string;
  description: string;
  prix: string | number;
  document_preview?: string;
  [key: string]: any;
}

export default defineComponent({
  name: 'ViewModale',
  props: {
    contract: {
      type: Object as PropType<Contrat | null>,
      default: null
    }
  },
  emits: ['close', 'buy'],
  
  setup(props, { emit }) {
    
    const formatPrice = (price?: number | string) => {
      if (!price) return '0';
      return Number(price).toLocaleString('fr-FR');
    };

    const handleFlyToCart = (event: MouseEvent) => {
      const cartBubble = document.querySelector('.glass-bubble');
      
      if (!cartBubble) {
        emit('buy', props.contract?.id); 
        return;
      }

      const startX = event.clientX;
      const startY = event.clientY;

      const cartRect = cartBubble.getBoundingClientRect();
      const endX = cartRect.left + (cartRect.width / 2);
      const endY = cartRect.top + (cartRect.height / 2);

      const ghost = document.createElement('div');
      ghost.style.position = 'fixed';
      ghost.style.left = `${startX}px`;
      ghost.style.top = `${startY}px`;
      ghost.style.width = '20px';
      ghost.style.height = '20px';
      ghost.style.backgroundColor = '#156ca9';
      ghost.style.borderRadius = '50%';
      ghost.style.zIndex = '99999';
      ghost.style.pointerEvents = 'none'; 
      ghost.style.transform = 'translate(-50%, -50%)'; 
      ghost.style.boxShadow = '0 4px 12px rgba(21, 108, 169, 0.5)';
      
      document.body.appendChild(ghost);

      const animation = ghost.animate([
        { transform: 'translate(-50%, -50%) scale(1)', opacity: 1 },
        { transform: `translate(calc(-50% + ${endX - startX}px), calc(-50% + ${endY - startY}px)) scale(0.2)`, opacity: 0.5 }
      ], {
        duration: 600, 
        easing: 'cubic-bezier(0.25, 1, 0.5, 1)' 
      });

      animation.onfinish = () => {
        ghost.remove(); 
        emit('buy', props.contract?.id);
      };
    };

    return {
      formatPrice,
      handleFlyToCart
    };
  }
});
</script>

<style scoped>
/* ==========================================
   1. BASE : DESIGN MOBILE-FIRST (Centré & Compact)
========================================== */
.view-modale {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center; /* 👈 La modale est bien centrée sur l'écran */
  z-index: 9990;
  padding: 1rem; 
}

.modal-content {
  position: relative;
  width: 100%;
  max-width: 500px; /* 👈 Limite la largeur sur mobile pour ne pas être trop massif */
  height: 50vh; /* 👈 S'adapte au contenu */
  max-height: 100vh; /* 👈 Ne dépassera jamais 85% de l'écran */
  background: #ffffff;
  border-radius: 20px; /* 👈 Bords arrondis de tous les côtés */
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* BOUTON FERMER */
.close-btn {
  position: absolute;
  top: 0.8rem;
  right: 0.8rem;
  z-index: 50;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background: #f1f5f9;
  color: #1e293b;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.size-6 { width: 16px; height: 16px; }

/* EN-TÊTE (Titre et Description) */
.info-header-section {
  padding: 1.2rem 3rem 1rem 1.2rem; 
  flex-shrink: 0;
  border-bottom: 1px solid #f1f5f9;
}


.contract-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--primary-color);
  line-height: 1.2;
  margin: 0 0 0.4rem 0;
}

.contract-description p {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2; 
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* APERÇU DU DOCUMENT (Zone défilante ultra-compacte) */
.preview-section {
  height: 270px; /* 👈 CRUCIAL : Hauteur fixe petite pour libérer de la place */
  flex: none; /* Empêche le conteneur de grandir */
  background: #e2e8f0; 
  overflow-y: auto; /* 👈 Force le scroll du document */
  padding: 0.8rem; 
}

/* Scrollbar fine pour mobile */
.preview-section::-webkit-scrollbar { width: 4px; }
.preview-section::-webkit-scrollbar-thumb { background-color: #94a3b8; border-radius: 10px; }

.page-a4 {
  background: white;
  width: 100%;
  padding: 1rem; 
  border-radius: 4px; 
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: relative;
  min-height: 100%;
}

.document-text {
  white-space: pre-wrap;
  font-family: 'Times New Roman', Times, serif;
  font-size: 0.8rem; 
  line-height: 1.4;
  color: #334155;
  text-align: justify;
}

.fade-bottom {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 50px; 
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
  border-radius: 0 0 4px 4px;
}

/* FOOTER D'ACHAT (Verrouillé en bas) */
.action-footer {
  flex-shrink: 0;
  background: #ffffff;
  padding: 0.8rem 1.2rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.8rem;
}

.price-container {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.price-amount {
  font-size: 1.4rem;
  font-weight: 800;
  color: #1e293b;
}

.price-currency {
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
}

.btn-buy {
  flex: 1; 
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.4rem;
  background-color: #156ca9;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.8rem;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(21, 108, 169, 0.2);
}

.cart-icon { width: 18px; height: 18px; }

/* ==========================================
   2. DESKTOP : DESIGN ÉCRAN DIVISÉ (PC & TABLETTES LARGES)
========================================== */
@media (min-width: 900px) {
  
  .view-modale {
    padding: 2rem;
  }

  .modal-content {
    border-radius: 24px; 
    height: 85vh;
    max-height: none;
    max-width: 1100px;
    display: grid;
    grid-template-columns: 60% 40%;
    grid-template-rows: 1fr auto;
  }

  .close-btn {
    top: 1.5rem; right: 1.5rem;
    width: 40px; height: 40px;
  }
  .size-6 { width: 22px; height: 22px; }

  /* L'aperçu reprend toute sa hauteur à gauche sur PC */
  .preview-section {
    grid-column: 1 / 2;
    grid-row: 1 / 3;
    height: 100%; /* 👈 On annule les 200px du mobile */
    border-right: 1px solid #e2e8f0;
    padding: 3rem;
    background: #f8fafc;
  }

  .page-a4 {
    padding: 4rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    border: none;
    max-width: none;
    border-radius: 0;
  }

  .document-text { font-size: 1.05rem; line-height: 1.6; }
  .fade-bottom { height: 150px; }

  /* Infos et Achat à droite */
  .info-header-section {
    grid-column: 2 / 3;
    grid-row: 1 / 2;
    padding: 3.5rem 3rem 1rem 3rem;
    border-bottom: none;
    overflow-y: auto; 
  }

  .badge-category { font-size: 0.85rem; padding: 0.4rem 1rem; }
  .contract-title { font-size: 1.5rem; margin-bottom: 1rem; }
  .contract-description p { 
    font-size: 1.05rem; 
    line-height: 1.7; 
    -webkit-line-clamp: unset; 
  }

  .action-footer {
    grid-column: 2 / 3;
    grid-row: 2 / 3;
    padding: 2rem 3rem 3rem 3rem;
    flex-direction: column; 
    align-items: flex-start;
  }

  .price-container {
    flex-direction: row; 
    align-items: baseline;
    margin-bottom: 1.5rem;
    gap: 0.5rem;
  }

  .price-amount { font-size: 2.5rem; }
  .price-currency { font-size: 1.2rem; }

  .btn-buy {
    width: 100%;
    padding: 1.2rem;
    font-size: 1.1rem;
    border-radius: 14px;
  }

  .cart-icon { width: 24px; height: 24px; }
}
</style>