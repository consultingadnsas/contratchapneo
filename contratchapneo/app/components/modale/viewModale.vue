<template>
  <transition name="modal-fade">
    <div v-if="contract" class="details-overlay" @click.self="$emit('close')">
      <div class="details-modal glass-effect">
        
        <button class="close-btn" @click="$emit('close')" aria-label="Fermer">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>

        <div class="modal-layout">

          <div class="modal-visual">
            <div class="page-a4-wrapper">
              <div class="page-a4">
                <p class="document-text">
                  {{ contract?.document_preview || "L'aperçu de ce document n'est pas encore disponible." }}
                </p>
                <div class="fade-bottom"></div>
              </div>
            </div>
          </div>

          <div class="modal-info">
            
            <h2 class="modal-title">
              {{ contract?.title || 'Titre du contrat' }}
            </h2>

            <div class="scrollable-body">
              <p class="long-description muted-text">
                {{ contract?.description || 'Aucune description détaillée fournie pour ce document.' }}
              </p>

              <div class="price-tag">
                <span class="price-label">Prix du modèle</span>
                <span class="price-amount">{{ formatPrice(contract?.prix) }} FCFA</span>
              </div>
            </div>

            <div class="modal-actions">
              <button class="btn-buy" @click="handleFlyToCart($event)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="cart-icon">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                </svg>
                <span>Acheter maintenant</span>
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  </transition>
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
/* ── Overlay & Base Modal ── */
.details-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(15, 23, 42, 0.7);
    z-index: 9999;
    display: flex; justify-content: center; align-items: center;
    padding: 2rem;
    backdrop-filter: blur(8px);
}

.glass-effect {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
}

.details-modal {
    width: 100%;
    max-width: 1100px; /* Légèrement plus grand pour bien respirer */
    border-radius: 32px;
    position: relative;
    overflow: hidden;
    animation: modalSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    max-height: 90vh;
    display: flex;
    flex-direction: column;
}

@keyframes modalSlideIn {
    from { opacity: 0; transform: translateY(30px) scale(0.95); }
    to   { opacity: 1; transform: translateY(0)    scale(1);    }
}

/* ── Bouton fermer ── */
.close-btn {
    position: absolute; top: 1.5rem; right: 1.5rem;
    background: rgba(15, 23, 42, 0.05); border: none; color: #0f172a;
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 10; transition: background 0.2s;
}
.close-btn:hover { background: rgba(15, 23, 42, 0.1); }
.close-btn svg   { width: 18px; height: 18px; }

/* ── Layout 2 colonnes ── */
.modal-layout {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    min-height: 500px; /* Réduit pour s'adapter aux petits écrans */
    height: 85vh; /* Prend 85% de la hauteur de l'écran */
    flex: 1;
    overflow: hidden;
}

/* ── Colonne gauche (Aperçu Document) ── */
.modal-visual {
    background: linear-gradient(160deg, #0f172a 0%, #1e3a5f 100%);
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    align-items: center; /* 👈 NOUVEAU : Centre la page horizontalement */
    justify-content: center; /* 👈 NOUVEAU : Centre la page verticalement */
    overflow: hidden; 
}

.page-a4-wrapper {
    flex-grow: 1;
    width: 100%;
    max-width: 550px; /* 👈 NOUVEAU : Donne un effet "vraie feuille" centrée */
    margin: 0 auto;
    overflow-y: auto;
    border-radius: 8px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    background: #ffffff;
    position: relative;
}

/* Scrollbar fine pour la page A4 */
.page-a4-wrapper::-webkit-scrollbar { width: 6px; }
.page-a4-wrapper::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); }
.page-a4-wrapper::-webkit-scrollbar-thumb { background-color: #94a3b8; border-radius: 10px; }

.page-a4 {
    padding: 2.5rem 2.5rem 4rem 2.5rem; 
    min-height: 100%;
    position: relative;
}

.document-text {
    white-space: pre-wrap;
    font-family: 'Times New Roman', Times, serif;
    font-size: 0.95rem; 
    line-height: 1.6;
    color: #334155;
    text-align: justify;
    margin: 0;
}

.fade-bottom {
    position: sticky;
    bottom: 0; left: 0; right: 0;
    height: 60px; 
    background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
    pointer-events: none;
}

/* ── Colonne droite (Infos) ── */
.modal-info {
    padding: 2.5rem; /* 👈 NOUVEAU : Padding réduit pour gagner de la place */
    background: #ffffff;
    display: flex; flex-direction: column;
    height: 100%; overflow: hidden;
}

.modal-title {
    font-size: 1.6rem; font-weight: 800; color: #0f172a;
    margin: 0 0 1rem; line-height: 1.2;
    flex-shrink: 0;
    padding-right: 2rem; /* Évite de cogner le bouton fermer */
}

/* Zone scrollable (Astuce min-height: 0 ajoutée) */
.scrollable-body {
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 1rem;
    margin-bottom: 1.5rem;
    width: 100%;
    min-height: 0; /* 👈 TRÈS IMPORTANT : Permet à la zone de rétrécir et ne pas pousser le bouton */
}

.scrollable-body::-webkit-scrollbar       { width: 6px; }
.scrollable-body::-webkit-scrollbar-track { background: #f8fafc; border-radius: 10px; }
.scrollable-body::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.scrollable-body::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.long-description { 
    font-size: 0.95rem; 
    line-height: 1.6; 
    color: #64748b; 
    margin-bottom: 1.5rem; 
}

/* Bloc prix */
.price-tag {
    width: 100%; padding: 1rem 1.2rem; border-radius: 12px;
    display: flex; flex-direction: column; align-items: center; gap: 0.2rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    margin-bottom: 1rem;
}
.price-label  { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #64748b; }
.price-amount { font-size: 1.8rem; font-weight: 800; color: #156ca9; }

/* Actions */
.modal-actions {
    display: flex; justify-content: center; gap: 1rem; width: 100%;
    flex-shrink: 0; /* Empêche le bouton de s'écraser */
    margin-top: auto;
    padding-bottom: 0.5rem;
}

.btn-buy {
    width: 100%;
    display: flex; justify-content: center; align-items: center; gap: 0.5rem;
    background-color: #156ca9; color: white;
    border: none; border-radius: 12px; padding: 1.1rem;
    font-size: 1.05rem; font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(21, 108, 169, 0.2);
    transition: transform 0.2s, background 0.2s;
}

.btn-buy:hover {
    background-color: #10507e;
    transform: translateY(-2px);
}

.cart-icon { width: 22px; height: 22px; }

/* Transition */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s; }
.modal-fade-enter-from,   .modal-fade-leave-to     { opacity: 0; }

/* ── Mobile ── */
@media (max-width: 768px) {
    .details-modal {
        max-height: 95vh;
        display: block;
        overflow-y: auto;
    }
    .modal-layout {
        grid-template-columns: 1fr;
        min-height: auto;
        height: auto;
        display: block;
    }
    .modal-visual { 
        padding: 1.5rem; 
        height: 350px; 
    }
    .page-a4-wrapper { max-width: none; }
    .page-a4 { padding: 1.5rem 1rem; }
    
    .modal-info   { padding: 1.5rem; height: auto; overflow: visible; }
    .scrollable-body { overflow-y: visible; padding-right: 0; margin-bottom: 0; }
    .modal-title  { font-size: 1.4rem; margin-bottom: 1rem; }
    
    .modal-actions { margin-top: 1rem; padding-bottom: 0; }
    .details-overlay { padding: 0.75rem; }
}
</style>